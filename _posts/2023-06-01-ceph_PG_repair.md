---
layout:     post
title:      "ceph PG 修复"
subtitle:   "ceph PG repair"
date:       2023-06-01
author:     "Gavin"
catalog:    true
tags:
    - ceph
    - python
---



# 概述

3月份的时候，江苏电力这个客户发生PG状态异常(纯粹是友情支持，发生问题的环境非我司ceph集群，而是ceph 开源集群)，需要进行手工修复。

应客户要求，临时写了个修复脚本，供客户设置定时任务，定期自动修复。

考虑到一些PG状态是无法修复的，做了一些保护；以及修复失败的保护。

# 实践


## inconsistent_pg_repair.py

脚本内容如下：

```
import os
import sys
import gzip
import json
import time
import errno
import select
import atexit
import socket
import logging
import commands
import traceback
import logging.handlers

from threading import Event
from fcntl import flock, LOCK_EX, LOCK_NB
from signal import signal, SIGTERM, SIGKILL, SIGUSR1


class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', kill_timeout=90):
        """
        Constructor.

        @param  pidfile:    path of the pid file
        @type   pidfile:    string
        @param  stdin:      path of the stdin
        @type   stdin:      string
        @param  stdout:     path of the stdout
        @type   stdout:     string
        @param  stderr:     path of the stderr
        @type   stderr:     string
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.lock_fd = -1
        self._kill_timeout = kill_timeout
        self._daemon_stopped = Event()
        self.first_loop = True

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+b', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        """
        Delete the pid file.
        """
        os.remove(self.pidfile)

    def lock_or_exit(self):
        try:
            self.lock_fd = os.open(self.pidfile, 
                                   os.O_CREAT|os.O_TRUNC|os.O_WRONLY|os.O_EXCL,
                                   0o666)
        except OSError as e:
            if e.errno == errno.EEXIST:
                self.lock_fd = os.open(self.pidfile,os.O_WRONLY)
            else:
                sys.stderr.write(
                    u"Can not create pidfile : {} error {} \n".format(
                        self.pidfile, str(e)
                    )
                )
                sys.exit(1)

        try:
            # flock can be  inherited by child process, even exec()
            flock(self.lock_fd, LOCK_EX | LOCK_NB)
        except IOError as e:
            if e.errno == errno.EAGAIN:
                sys.stderr.write(
                    u"pidfile {} is locked, Daemon already running?\n".format(
                        self.pidfile
                    )
                )
                sys.exit(0)
            else:
                sys.stderr.write(
                    u"failed to lock the pid file {} , error {}".format(
                        self.pidfile, str(e)
                    )
                )
                sys.exit(1)

    def start(self):
        """
        Start the daemon
        """

        self.lock_or_exit()

        # Start the daemon
        self.prepare_start()
        self.daemonize()
        signal(SIGTERM, self.handle_term)
        signal(SIGUSR1, self.handle_siguser1)
        daemon_name = self.__class__.__name__
        try:
            logger.info('Daemon {} start'.format(daemon_name))
            self.run()
            logger.info('Daemon {} stopped'.format(daemon_name))
        except Exception:
            logger.exception('Daemon {} terminates unexpectedly'.format(daemon_name))

    def get_pid(self):
        # Get the pid from the pidfile
        try:
            pid_str = (open(self.pidfile).read().strip())
            if len(pid_str):
                pid = int(pid_str)
            else:
                pid = None
        except IOError:
            pid = None
        return pid

    def stop(self):
        """
        Stop the daemon
        """
        pid = self.get_pid()

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            waiting_killed = 0
            while 1:
                if waiting_killed == 0:
                    os.kill(pid, SIGTERM)
                elif waiting_killed < self._kill_timeout:
                    os.kill(pid, 0)
                else:
                    # Use kill pg to force kill all subprocess
                    os.killpg(os.getpgid(pid), SIGKILL)
                time.sleep(1)
                waiting_killed = waiting_killed + 1
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def prepare_start(self):
        """
        You should override this method when you subclass Daemon. It will be called before the process has been
        daemonized by start() or restart().
        """

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

    def terminate(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by stop() or restart().
        """
    
    def user_signal_1(self):
        """
        You may override this method when you subclass Daemon.
        The default method toogle to change the loglevel from between debug and info
        """

        new_level = logging.INFO if EZLog.getLevel() == logging.DEBUG else logging.DEBUG
        EZLog.setLevel(new_level)
        logger.info('Daemon {} log level is chaged to {}'.format(
            self.__class__.__name__,
            'debug ' if new_level == logging.DEBUG else 'info'))

    def is_daemon_running(self, wait=0):
        # do not wait for first loop
        if self.first_loop and wait > 0:
            wait = 0
            self.first_loop = False
        return not self._daemon_stopped.wait(wait)

    def handle_term(self, sig, frm):
        logger.info('Got signal: {}'.format(sig))
        if self.is_daemon_running():
            self._daemon_stopped.set()
            self.terminate()

    def handle_siguser1(self, sig, frm):
        logger.info('Got signal: {}'.format(sig))
        self.user_signal_1()


class BtLogger():

    def __init__(self, log_name, log_file_name, log_level=logging.DEBUG, max_bytes=5*1024*1024, backup_count=5):

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)-8s[line:%(lineno)-4s] [%(levelname)-5s] %(message)s')

        self.h_rotating_file = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=max_bytes, backupCount=backup_count)
        self.h_rotating_file.setFormatter(formatter)
        self.h_rotating_file.rotator = self._rotator
        self.h_rotating_file.namer = self._namer
        self.h_stream = logging.StreamHandler(sys.stdout)
        self.h_stream.setFormatter(formatter)

        self.h_rotating_file.setLevel(log_level)
        self.h_stream.setLevel(logging.INFO)
        self.logger.addHandler(self.h_rotating_file)
        self.logger.addHandler(self.h_stream)

    def _namer(self, name):
        return name + ".gz"

    def _rotator(self, source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            with gzip.open(dest, "wb") as gf:
                gf.write(data)
        os.remove(source)

    def get_logger(self):
        return self.logger


sleep_time = 1 * 60 * 1
logger = BtLogger(__name__, "/var/log/inconsistent_pg_repair.log", log_level=logging.DEBUG).get_logger()


class RepairDaemon(Daemon):
    """ Repari inconsistent PG in daemon  """

    @staticmethod
    def pg_not_health():
        unhealth_pg = ["scrubbing", "nearfull", "incomplete", "full", "backfill",
                       "degraded", "remapped", "stale", "recovering"]
        pg_stat = commands.getoutput('ceph pg stat').strip()
        for each_unhealth_pg in unhealth_pg:
            if each_unhealth_pg in pg_stat:
                logger.error("[ERROR]  Find unhealth PG : (%s), do nothing, exit!!!", each_unhealth_pg)
                sys.exit(2)

    @staticmethod
    def get_inconsistent_pg():
        inconsistent_pg = []
        res = commands.getoutput("/usr/bin/ceph --connect-timeout=10 health detail | "
                                 "grep inconsistent | grep acting").strip()

        if res:
            if 'failed_repair' in res:
                logger.error("[ERROR]  Find 'failed_repair' PG, do nothing, exit!!!")
                sys.exit(2)

            for each_element in res.split('\n'):
                inconsistent_pg.append(each_element.strip().split()[1])

            # Remove duplicate and None element
            inconsistent_pg = {}.fromkeys(inconsistent_pg).keys()
            inconsistent_pg = filter(None, inconsistent_pg)
            logger.debug("Find inconsistent PG : (%s)", inconsistent_pg)
            return inconsistent_pg
        else:
            logger.debug("Not find inconsistent PG.")
            return inconsistent_pg

    def auto_repair(self, pg_name):
        """
        Run 'ceph pg reapir pg_name', try to repair PG
        :param pg_name, string, a PG id
        """
        repair_cmd = "ceph pg repair {}".format(pg_name)
        logger.info("Starts to repair PG : (%s), command : (%s)", pg_name, repair_cmd)
        repair_res = commands.getoutput(repair_cmd)

        health_res = commands.getoutput('/usr/bin/ceph --connect-timeout=10 -s').strip()
        if 'failed_repair' in health_res:
            logger.error("[ERROR]  Repair PG :(%s) failed, please pay more attention!!!!!")
            sys.exit(1)
        else:
            logger.info("Repair PG : (%s) result : (%s), now sleep (%s)", pg_name, repair_res, sleep_time)
            time.sleep(sleep_time) 

    def list_inconsistent_obj_repair(self):
        """
        List inconsistent object for each inconsistent PG before, then repair
        """
        self.pg_not_health()

        inconsistent_pg = self.get_inconsistent_pg()
        if len(inconsistent_pg) > 3:
            logger.warn("[WARN]  Found more than 3 abnormal PGs, suggest to repair manually, exits!!!")
            sys.exit(3)

        if len(inconsistent_pg):
            for each_pg in inconsistent_pg:
                list_cmd = "rados list-inconsistent-obj {} --format=json-pretty".format(each_pg)
                list_res = commands.getoutput(list_cmd)
                logger.debug("rados list-inconsistent-obj %s : (%s)", each_pg, list_res)
                if list_res and len(json.loads(list_res)['inconsistents']):
                    logging.warn("Find inconsistent PG : (%), now reapir "
                                 "(%s)",json.loads(list_res)['inconsistents'], each_pg)
                    self.auto_repair(each_pg)
                else:
                    logging.warn("PG in inconsistent, but list inconsistent object is None, skip to repair!!!")
        else:
            logger.info("Not find inconsistent PG, skip.")

    def run(self):
        logger.info("Repair inconsistent PG Daemon starts run")

        while self.is_daemon_running(wait=30):
            try:
                self.list_inconsistent_obj_repair()
            except Exception:
                logger.error("ezsnapsched exception: {}".format(traceback.format_exc()))


if __name__ == '__main__':
    daemon = RepairDaemon('/var/run/bt-repair.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

```

