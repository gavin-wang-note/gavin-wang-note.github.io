---
layout:     post
title:      "python中fileno是什么"
date:       2024-07-01
author:     "Gavin Wang"
img:        "/medias/featureimages/66.jpg"
catalog:    true
summary:    在Python中，sys.stdin.fileno()&sys.stderr.fileno()到底是啥
categories:
    - [python]
tags:
    - python
---


# 概述

今天看`pytest`源码（`root@Gavin:~/pytest-main/src/_pytest# vim faulthandler.py`），引发了此文的编写。

```python
def get_stderr_fileno() -> int:
    try:
        fileno = sys.stderr.fileno()
        # The Twisted Logger will return an invalid file descriptor since it is not backed
        # by an FD. So, let's also forward this to the same code path as with pytest-xdist.
        if fileno == -1:
            raise AttributeError()
        return fileno
    except (AttributeError, ValueError):
        # pytest-xdist monkeypatches sys.stderr with an object that is not an actual file.
        # https://docs.python.org/3/library/faulthandler.html#issue-with-file-descriptors
        # This is potentially dangerous, but the best we can do.
        return sys.__stderr__.fileno()
```

那么，在`python`中，`sys.stderr.fileno()`到底是个啥？

# 打开面纱

我在自己环境中运行了一下：

```shell
root@Gavin:~# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.stdin.fileno()
0
>>> exit()
root@Gavin:~# cd -
/root/pytest-main/src/_pytest
root@Gavin:~/pytest-main/src/_pytest# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.stderr.fileno()
2
>>> exit()
root@Gavin:~/pytest-main/src/_pytest# 
```

运行结果分别是0和2，所以它们是标准流和文件描述符。

# 标准流和文件描述符

在`Unix`和`Linux`系统上，标准输入、标准输出和标准错误分别对应于以下文件描述符：

* 标准输入（`stdin`）：文件描述符为 0
  - 用于从用户获取输入数据。例如：`sys.stdin.fileno()` 返回 0。
* 标准输出（`stdout`）：文件描述符为 1
  - 用于输出常规数据。例如：`sys.stdout.fileno()` 返回 1。
* 标准错误（`stderr`）：文件描述符为 2
  - 用于输出错误消息和诊断信息。例如：`sys.stderr.fileno()` 返回 2。

文件描述符是一个低级概念，它是一个整数，代表一个打开的文件。每个打开的文件都有一个唯一的文件描述符。

在`Unix`和类似`Unix`的操作系统中，文件描述符是由内核分配的。当你打开一个文件、套接字或其他输入/输出资源时，内核会返回一个整数值作为文件描述符，用于标识这个资源。文件描述符是操作系统管理文件、套接字和其他资源的核心机制。

在`Python`中，文件对象（如 `sys.stdin、sys.stdout` 和 `sys.stderr`）都有一个方法 `fileno()`，可以返回它们对应的文件描述符，分别对应0,1,2。


# 文件描述符的使用

文件描述符在许多系统级编程任务中非常有用，例如：

## 重定向标准流

可以重定向标准输入、标准输出和标准错误到文件或其他设备中。


```python
import sys
import os

# 打开一个文件用于写入
f = open('output.txt', 'w')

# 备份原始标准输出文件描述符
original_stdout_fd = os.dup(sys.stdout.fileno())

# 替换标准输出文件描述符为文件的文件描述符
os.dup2(f.fileno(), sys.stdout.fileno())

# 测试输出
print("这个输出会被写入到output.txt文件中。")

# 恢复标准输出到最早的输出
os.dup2(original_stdout_fd, sys.stdout.fileno())

# 关闭文件
f.close()

# 验证恢复标准输出
print("这个输出会被显示到控制台。")
```

## 跨进程通信

文件描述符可以用于在进程间通信，比如通过 `Unix` 域套接字或管道来传递文件描述符。

1. **父进程**创建文件并写入数据，然后通过 `Unix` 域套接字发送文件描述符给子进程。

2. **子进程**接收文件描述符并读取文件内容。



`parent.py`

```python
import os
import socket
import array
import sys

def send_fd(sock, fd):
    """发送文件描述符到 socket"""
    fds = array.array("i", [fd])
    sock.sendmsg([b'x'], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)])

if __name__ == '__main__':
    # 创建 Unix 域套接字对
    parent_sock, child_sock = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)

    # 创建一个文件 example.txt 并写入一些数据
    with open('example.txt', 'w') as f:
        f.write("hello from parent process")

    # 使用 fork 创建子进程
    pid = os.fork()

    if pid > 0:
        # 父进程
        child_sock.close()  # 关闭子进程的套接字
        try:
            with open('example.txt', 'r') as f:
                send_fd(parent_sock, f.fileno())  # 传递文件描述符
            parent_sock.sendall(b"File descriptor sent!")
        except Exception as e:
            print("An error occurred:", e)
        finally:
            parent_sock.close()
            os.waitpid(pid, 0)  # 等待子进程结束
            print("Parent process done.")
    else:
        # 子进程
        parent_sock.close()  # 关闭父进程的套接字
        try:
            # 接收文件描述符
            msg, ancdata, flags, addr = child_sock.recvmsg(1, socket.CMSG_LEN(array.array("i", [0]).itemsize))
            for cmsg_level, cmsg_type, cmsg_data in ancdata:
                if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                    fd = array.array("i", cmsg_data)[0]

            if fd < 0:
                print("Received invalid file descriptor")
            else:
                print(f"Received file descriptor {fd}")
                with os.fdopen(fd, 'r') as f:
                    print("Child process received data:", f.read())
        except Exception as e:
            print("An error occurred:", e)
        finally:
            child_sock.close()
```



* 函数 `send_fd(sock, fd)`：
  - 将文件描述符转换为字节格式并通过 `Unix` 域套接字发送。
* 在主程序部分：
  - 创建一个 Unix 域套接字对 (`socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)`)，返回两个套接字：一个用于父进程，一个用于子进程。
  - 写入数据到文件 `example.txt` 中。
  - 使用 `os.fork()` 创建子进程。
  - 在父进程中，关闭子进程的套接字，并调用 `send_fd` 发送文件描述符。
  - 在子进程中，关闭父进程的套接字，并接收文件描述符，然后使用 `os.fdopen(fd, 'r')` 打开接收到的文件描述符并读取数据。



`child.py`

```python
import os
import socket
import array
import sys

def recv_fd(pipe_in):
    """从管道接收文件描述符"""
    msg, ancdata, flags, addr = pipe_in.recvmsg(1, socket.CMSG_LEN(array.array("i", [0]).itemsize))
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            return array.array("i", cmsg_data)[0]

if __name__ == '__main__':
    pipe_in_fd = int(sys.argv[1])  # 从命令行参数获取管道的读端文件描述符
    pipe_in = socket.fromfd(pipe_in_fd, socket.AF_UNIX, socket.SOCK_STREAM)

    # 接收文件描述符
    fd = recv_fd(pipe_in)
    pipe_in.close()

    # 确保文件描述符有效性
    if fd < 0:
        print("Received invalid file descriptor")
    else:
        print(f"Received file descriptor {fd}")

    # 使用接收的文件描述符读取文件内容
    with os.fdopen(fd, 'r') as f:
        print("Child process received data:", f.read())
```



**子进程 `child.py`**：

- 关闭父进程的套接字。
- 通过 `recvmsg` 接收文件描述符来确保进程间文件描述符正确传递。
- 使用 `os.fdopen(fd, 'r')` 打开接收到的文件描述符并读取数据



运行效果：



```shell
root@Gavin:~/test# python3 parent.py 
Received file descriptor 3
Child process received data: hello from parent process
Parent process done.
root@Gavin:~/test# cat example.txt 
hello from parent processroot@Gavin:~/test#
```



## 低级文件操作

可以通过文件描述符进行低级读写操作，提供更多的灵活性和性能优化选择。


```python
import os

# 打开一个文件
fd = os.open('example.txt', os.O_RDWR | os.O_CREAT)

# 写入数据
os.write(fd, b'Hello, World!')

# 读取数据
os.lseek(fd, 0, os.SEEK_SET)
print(os.read(fd, 12))  # b'Hello, World!'

# 关闭文件
os.close(fd)
```



# 小结

文件描述符是一个底层概念，用于标识和管理系统中的打开文件或输入/输出流。

它们是整数，由内核分配和管理。 

在`Python`中，文件对象如 `sys.stdin`、`sys.stdout` 和 `sys.stderr` 都可以通过 `fileno()` 方法获得对应的文件描述符。

这些描述符在系统编程中非常有用，可以用于重定向、跨进程通信和低级文件操作。


