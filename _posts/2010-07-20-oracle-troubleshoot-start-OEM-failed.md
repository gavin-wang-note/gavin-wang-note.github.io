---
layout:     post
title:      "Oracle案例--OEM启动失败"
subtitle:   "Oracle troubleshoot--start OEM failed"
date:       2010-07-20
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 概述

当前的彩信网关，一般在安装指南中并不安装oem，所以启动OEM必定会失败。对于OEM启动失败的情况下，又不知如何去解决，建议直接重新安装一次OEM.

# emca命令使用说明

```
/opt/oracle/product/11g/bin/emca [operation] [mode] [dbType] [flags] [parameters]

-h | --h | -help | --help: prints this help message 
-version: prints the version

-config dbcontrol db [-repos (create | recreate)] [-cluster] [-silent] [-backup] [parameters]: configure Database Control for a database
-config centralAgent (db | asm) [-cluster] [-silent] [parameters]: configure central agent management
-config all db [-repos (create | recreate)] [-cluster] [-silent] [-backup] [parameters]: configure both Database Control and central agent management

-deconfig dbcontrol db [-repos drop] [-cluster] [-silent] [parameters]: de-configure Database Control
-deconfig centralAgent (db | asm) [-cluster] [ -silent] [parameters]: de-configure central agent management
-deconfig all db [-repos drop] [-cluster] [-silent] [parameters]: de-configure both Database Control and central agent management

-addInst (db | asm) [-silent] [parameters]: configure EM for a new RAC instance
-deleteInst (db | asm) [-silent] [parameters]: de-configure EM for a specified RAC instance

-reconfig ports [-cluster] [parameters]: explicitly reassign Database Control ports
-reconfig dbcontrol -cluster [-silent] [parameters]: reconfigures RAC Database Control deployment

-displayConfig dbcontrol -cluster [-silent] [parameters]: displays information about the RAC Database Control configuration

-migrate -from dbcontrol -to centralAgent  [-repos drop] [-cluster] [-silent] [parameters]: migrates EM configuration from Database Control to central agent

-upgrade (db | asm | db_asm) [-cluster] [-silent] [parameters]: upgrades an earlier version of the EM configuration to the current version

-restore (db | asm | db_asm) [-cluster] [-silent] [parameters]: restores the current version of the EM configuration to an earlier version

Parameters and Options:
[parameters]: [ -respFile fileName ] [ -paramName paramValue ]* 
db: perform configuration operation for a database (including databases that use ASM)
asm: perform configuration operation for an ASM-only instance
db_asm: perform upgrade/restore operation for a database and an ASM instance
-repos create: create a new Database Control repository
-repos drop: drop the current Database Control repository
-repos recreate: drop the current Database Control repository and recreate a new one
-cluster: perform configuration operation for a RAC database
-silent: perform configuration operation without prompting for parameters
-backup: configure automatic backup for a database

Parameters for single instance databases
        ORACLE_HOSTNAME: Local hostname
        SID: Database SID
        PORT: Listener port number
        ORACLE_HOME: Database ORACLE_HOME
        HOST_USER: Host username for automatic backup
        HOST_USER_PWD: Host user password for automatic backup
        BACKUP_SCHEDULE: Automatic backup schedule (HH:MM)
        EMAIL_ADDRESS: Email address for notifications
        MAIL_SERVER_NAME: Outgoing Mail (SMTP) server for notifications
        ASM_OH: ASM ORACLE_HOME
        ASM_SID: ASM SID
        ASM_PORT: ASM port
        ASM_USER_ROLE: ASM user role
        ASM_USER_NAME: ASM username
        ASM_USER_PWD: ASM user password
        SRC_OH: ORACLE_HOME for the database to be upgraded
        DBSNMP_PWD: Password for DBSNMP user
        SYSMAN_PWD: Password for SYSMAN user
        SYS_PWD: Password for SYS user
        DBCONTROL_HTTP_PORT: Database Control HTTP port
        AGENT_PORT: EM agent port
        RMI_PORT: RMI port for Database Control
        JMS_PORT: JMS port for Database Control
        EM_SWLIB_STAGE_LOC:  Software library location
        PORTS_FILE: Path to a static file specifying the ports to use (Default value : ${ORACLE_HOME}/install/staticports.ini).

Additional Parameters for cluster databases
        CLUSTER_NAME: Cluster name
        DB_UNIQUE_NAME: Database unique name
        SERVICE_NAME: Service name
        EM_NODE: Database Control node name
        EM_SID_LIST: Agent SID list [comma separated]
oracle@mmsg:~> emca -config dacontrol mmsgdb -repos recreate
/opt/oracle/product/11g/bin/emca [operation] [mode] [dbType] [flags] [parameters]

-h | --h | -help | --help: prints this help message 
-version: prints the version

-config dbcontrol db [-repos (create | recreate)] [-cluster] [-silent] [-backup] [parameters]: configure Database Control for a database
-config centralAgent (db | asm) [-cluster] [-silent] [parameters]: configure central agent management
-config all db [-repos (create | recreate)] [-cluster] [-silent] [-backup] [parameters]: configure both Database Control and central agent management

-deconfig dbcontrol db [-repos drop] [-cluster] [-silent] [parameters]: de-configure Database Control
-deconfig centralAgent (db | asm) [-cluster] [ -silent] [parameters]: de-configure central agent management
-deconfig all db [-repos drop] [-cluster] [-silent] [parameters]: de-configure both Database Control and central agent management

-addInst (db | asm) [-silent] [parameters]: configure EM for a new RAC instance
-deleteInst (db | asm) [-silent] [parameters]: de-configure EM for a specified RAC instance

-reconfig ports [-cluster] [parameters]: explicitly reassign Database Control ports
-reconfig dbcontrol -cluster [-silent] [parameters]: reconfigures RAC Database Control deployment

-displayConfig dbcontrol -cluster [-silent] [parameters]: displays information about the RAC Database Control configuration

-migrate -from dbcontrol -to centralAgent  [-repos drop] [-cluster] [-silent] [parameters]: migrates EM configuration from Database Control to central agent

-upgrade (db | asm | db_asm) [-cluster] [-silent] [parameters]: upgrades an earlier version of the EM configuration to the current version

-restore (db | asm | db_asm) [-cluster] [-silent] [parameters]: restores the current version of the EM configuration to an earlier version

Parameters and Options:
[parameters]: [ -respFile fileName ] [ -paramName paramValue ]* 
db: perform configuration operation for a database (including databases that use ASM)
asm: perform configuration operation for an ASM-only instance
db_asm: perform upgrade/restore operation for a database and an ASM instance
-repos create: create a new Database Control repository
-repos drop: drop the current Database Control repository
-repos recreate: drop the current Database Control repository and recreate a new one
-cluster: perform configuration operation for a RAC database
-silent: perform configuration operation without prompting for parameters
-backup: configure automatic backup for a database

Parameters for single instance databases
        ORACLE_HOSTNAME: Local hostname
        SID: Database SID
        PORT: Listener port number
        ORACLE_HOME: Database ORACLE_HOME
        HOST_USER: Host username for automatic backup
        HOST_USER_PWD: Host user password for automatic backup
        BACKUP_SCHEDULE: Automatic backup schedule (HH:MM)
        EMAIL_ADDRESS: Email address for notifications
        MAIL_SERVER_NAME: Outgoing Mail (SMTP) server for notifications
        ASM_OH: ASM ORACLE_HOME
        ASM_SID: ASM SID
        ASM_PORT: ASM port
        ASM_USER_ROLE: ASM user role
        ASM_USER_NAME: ASM username
        ASM_USER_PWD: ASM user password
        SRC_OH: ORACLE_HOME for the database to be upgraded
        DBSNMP_PWD: Password for DBSNMP user
        SYSMAN_PWD: Password for SYSMAN user
        SYS_PWD: Password for SYS user
        DBCONTROL_HTTP_PORT: Database Control HTTP port
        AGENT_PORT: EM agent port
        RMI_PORT: RMI port for Database Control
        JMS_PORT: JMS port for Database Control
        EM_SWLIB_STAGE_LOC:  Software library location
        PORTS_FILE: Path to a static file specifying the ports to use (Default value : ${ORACLE_HOME}/install/staticports.ini).

Additional Parameters for cluster databases
        CLUSTER_NAME: Cluster name
        DB_UNIQUE_NAME: Database unique name
        SERVICE_NAME: Service name
        EM_NODE: Database Control node name
        EM_SID_LIST: Agent SID list [comma separated]
```

# 重新创建OEM 

```
oracle@mmsg:~> emca -config dbcontrol db -repos recreate

STARTED EMCA at Jul 20, 2010 2:46:53 PM
EM Configuration Assistant, Version 11.1.0.7.0 Production
Copyright (c) 2003, 2005, Oracle.  All rights reserved.

Enter the following information:
Database SID: mmsgdb
Listener port number: 1521
Password for SYS user:  
Password for SYSMAN user: 
Email address for notifications (optional):   #这个是可选的
Outgoing Mail (SMTP) server for notifications (optional):  #这个是可选的
-----------------------------------------------------------------

You have specified the following settings

Database ORACLE_HOME ................ /opt/oracle/product/11g

Local hostname ................ mmsg
Listener port number ................ 1521
Database SID ................ mmsgdb
Email address for notifications ............... 
Outgoing Mail (SMTP) server for notifications ............... 

-----------------------------------------------------------------
Do you wish to continue? [yes(Y)/no(N)]: yes
Jul 20, 2010 2:48:24 PM oracle.sysman.emcp.EMConfig perform
INFO: This operation is being logged at /opt/oracle/cfgtoollogs/emca/mmsgdb/emca_2010_07_20_14_46_53.log.
Jul 20, 2010 2:48:25 PM oracle.sysman.emcp.EMReposConfig invoke
INFO: Dropping the EM repository (this may take a while) ...
Jul 20, 2010 2:50:18 PM oracle.sysman.emcp.EMReposConfig invoke
INFO: Repository successfully dropped
Jul 20, 2010 2:50:18 PM oracle.sysman.emcp.EMReposConfig createRepository
INFO: Creating the EM repository (this may take a while) ...
Jul 20, 2010 2:54:51 PM oracle.sysman.emcp.EMReposConfig invoke
INFO: Repository successfully created
Jul 20, 2010 2:54:54 PM oracle.sysman.emcp.EMReposConfig uploadConfigDataToRepository
INFO: Uploading configuration data to EM repository (this may take a while) ...
Jul 20, 2010 2:55:36 PM oracle.sysman.emcp.EMReposConfig invoke
INFO: Uploaded configuration data successfully
Jul 20, 2010 2:55:38 PM oracle.sysman.emcp.util.DBControlUtil configureSoftwareLib
INFO: Software library configured successfully.
Jul 20, 2010 2:55:38 PM oracle.sysman.emcp.EMDBPostConfig configureSoftwareLibrary
INFO: Deploying Provisioning archives ...
Jul 20, 2010 2:55:45 PM oracle.sysman.emcp.EMDBPostConfig configureSoftwareLibrary
INFO: Provisioning archives deployed successfully.
Jul 20, 2010 2:55:45 PM oracle.sysman.emcp.util.DBControlUtil secureDBConsole
INFO: Securing Database Control (this may take a while) ...
Jul 20, 2010 2:55:56 PM oracle.sysman.emcp.util.DBControlUtil secureDBConsole
INFO: Database Control secured successfully.
Jul 20, 2010 2:55:56 PM oracle.sysman.emcp.util.DBControlUtil startOMS
INFO: Starting Database Control (this may take a while) ...
Jul 20, 2010 2:56:16 PM oracle.sysman.emcp.EMDBPostConfig performConfiguration
INFO: Database Control started successfully
Jul 20, 2010 2:56:16 PM oracle.sysman.emcp.EMDBPostConfig performConfiguration
INFO: >>>>>>>>>>> The Database Control URL is https://mmsg:1158/em <<<<<<<<<<<
Jul 20, 2010 2:56:19 PM oracle.sysman.emcp.EMDBPostConfig invoke
WARNING: 
************************  WARNING  ************************

Management Repository has been placed in secure mode wherein Enterprise Manager data will be encrypted.  The encryption key has been placed in the file: /opt/oracle/product/11g/mmsg_mmsgdb/sysman/config/emkey.ora.   Please ensure this file is backed up as the encrypted data will become unusable if this file is lost. 

***********************************************************
Enterprise Manager configuration completed successfully
FINISHED EMCA at Jul 20, 2010 2:56:19 PM
oracle@mmsg:~>
```

# 登录OEM

创建OEM成功后，登陆OEM，默认端口1158,登录方式是：```https://hostip:1158/em/ ```，成功登录后，如下图所示：

<img class="shadow" src="/img/in-post/oracle-login-oem.png" width="400">

