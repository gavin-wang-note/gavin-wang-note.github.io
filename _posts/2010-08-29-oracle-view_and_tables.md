---
layout:     post
title:      "Oracle SQL篇之常用视图与表汇总"
subtitle:   "Oracle SQL -- Views and tables of summary"
date:       2010-08-29
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# DBA_

```
DBA_2PC_NEIGHBORS                包含待处理事务进入连接和退出连接信息。
DBA_2PC_PENDING                 包含等待恢复的分布式事务的信息。
DBA_ALL_TABLES                 显示数据库中所有表（对象表和关系表）的描述。
DBA_ANALYZE_OBJECTS         列出分析对象。
DBA_ASSOCIATIONS                 列出用户定义的统计信息。
DBA_AUDIT_EXISTS                 列出由AUDIT NOT EXISTS(不存在审计)和AUDIT EXISTS（存在审
计）产生的审计跟踪条目。
DBA_AUDIT_OBJECT         包含系统中所有对象的审计跟踪记录。
DBA_AUDIT_SESSION         列出关于CONNECT（连接）和DISCONNECT（断开连接）的所有审讯跟踪记录。
DBA_AUDIT_STATEMENT 列出关于GRANT（授权）、REVOKE（取消）、AUDIT〔审计〕、NOAUDIT（不审计）和ALTER SYSTEM(改变系统)语句的审记跟踪记录。
DBA_AUDIT_TRAIL　        列出所有的审记跟踪条目。
DBA_BLOCKERS　        列出所有人等待一个会话持有的锁的所有会话，但并非它们自己在等待一个锁。
DBA_CATALOG         列出所有数据库表、视图、同义词和序列。
DBA_CLU_COLUMNS         列出表列到簇列的映射。
DBA_CLUSTER_HASH_EXPRESSIONS     列出所有簇的散列（hash）函数。
DBA_CLUSTERS         包含数据库中所有族的描述。
DBA_COL_COMMENS        列出所有表和视图列的注解。
DBA_COL_PRIVS        列出数据库中授予列的所有权限。
DBA_COLL_TYPES        显示数据库中所有命名的集合类型，如VARRAY（数组）、嵌套表、对象表，等等；
DBA_CONS_COLUMNS        包含在约束定义中的，可访问的列的信息
DBA_CONSTRAINTS        包含所有表上的约束定义。
DBA_CONTEXT        列出所有上下文名字空间的信息。
DBA_DATA_FILES        包含有关数据库文件的信息
DBA_DB_LINKS        列出数据库中的所有数据库链接。
DBA_DDL_LOCKS        列出数据库持有的所有DDL锁，及所有对一个DDL锁的未定请求。
DBA_DEPENDENCIES        列出对象之间的依赖性。在没有任何数据库链接时所创建的视图上的依赖性也是可用的。
DBA_DIM_ATTRIBUTES        代表维级和功能依赖的列之间的关系。维级列所在的表，必须与所依赖列所在的表相匹配。
DBA_DIM_CHILD_OF        代表在维中的一对维级之间的1：n的层次关系。
DBA_DIM_HIERARCHIES        代表一个维层次。
DBA_DIM_JOIN_KEY        代表两个维表之间的连接。这种连接通常在一个双亲维级列和一个子列之间指定。
DBA_DIM_LEVEL_KEY        代表一个维级的列。一个级中列的位置通过KEY_POSITION来指定。
DBA_DIM_LEVELS        代表一个维级。一个维级的所有列，必须来自于同一关系。
DBA_DIMENSIONS        代表维对象。
DBA_DIRECTORIES        提供数据库中所有目录对象的信息。
DBA_DML_LOCKS        列出数据库中持有的所有DML锁，和对一个DML锁的所有未决请求。
DBA_ERRORS         列出数据库中所有存储的对象的当前错误。
DBA_EXP_FILES        包含导出文件的描述。
DBA_EXP_OBJECTS        列出以增量方式导出的对象。
DBA_EXP_VERSION        包含最后导出会话的版本号。
DBA_EXTENTS        列出数据库中组成所有段的区。
DBA_FREE_SPACE        列出所有表空间中的空闲分区。
DBA_FREE_SPACE_COALESCED        包含表空间中合并空间的统计数据。
DBA_IND_COLUMNS        包含在所有表和簇中组成索引的列的描述。
DBA_IND_EXPRESSIONS        列出在所有表和簇中函数型索引的表达示。
DBA_IND_PARTITIONS        为每一个索引分区，描述分区级的分区信息、分区的存储参数和由ANALYZE决定的各种分区统计数据。
DBA_IND_SUBPARTITIONS                                为当前用户拥有的每一个索引子分区，描述分区级的分区信息、子分区的存储参数和由ANALYZE决定的各种分区统计数据。
DBA_INDEXES        包含数据库中所有索引的描述。
DBA_INDEXTYPE_OPERATORS                列出由索引类型支持的所有操作符。
DBA_INDEXTYPES        列出所有的索引类型。
DBA_JOBS        列出数据库中的所有作业。
DBA_JOBS_RUNNING        列出数据库中当前运行的所有作业。
DBA_LIBRARIES        列出数据库中所有的库。
DBA_LOB_PARTITIONS        显示包含在表中的用户可访问的LOB。
DBA_LOB_SUBPARTITIONS                 显示LOB数据子分区中的分区级属性。
DBA_LOBS         显示包含在所有表中的LOB.
DBA_LOCK_INTERNAL         包含每个被持有的锁或简易锁的一行信息，及锁或简易锁的每一个未决定请求的一行信息。
DBA_LOCKS         列出数据库中持有的所有锁或简易锁，及一个锁或简易锁的所有未决请求。
DBA_METHOD_PARAMS        包含数据库中类型的方法参数的描述。
DBA_METHOD_RESULTS        包含数据库中所有类型的方法结果的描述。
DBA_MVIEW_AGGREGATES                代表在聚集实例化视图的SELECT列表中出现的分组函数（聚集方法）。
DBA_MVIEW_ANALYSIS        代表潜在地支持查询重写，并有可用于应用程序分析的附加信息的实例化视图。这种视图包括任何引用远程表或者包括如SYSDATE或USER等非静态值的实例化视图。
DBA_MVIEW_DETAIL_RELATIONS                代表命名细节关系，这些关系或者在一个实例化视图的FROM列表中，或者直接通过FORM列表中的视图引用。在这个表中，没有表示实例化视图中的内嵌视图。
DBA_MVIEW_JOINS        在一个实例化视图的WHERE子句中，代表两个列之间的连接。
DBA_MVIEW_KEYS        代表命名细节关系，这些关系或者在一个实例化视图的FROM列表中，或者直接通过FORM列表中的视图引用。在这个表中，没有表示实例化视图中的内嵌视图。
DBA_NESTED_TABLES        显示包含在所有表中的嵌套表的描述。
DBA_OBJ_AUDIT_OPTS        列出一个用户所拥有的所有对象的审计选项。
DBA_OBJECT_SIZE         列出各类PL/SQL对象的、用字节数表示大小。
DBA_OBJECT_TABLES        显示数据库中所有对象表的描述。
DBA_OBJECTS         列出数据库中所有的对象。
DBA_OPANCILLARY         列出操作符连接的附加信息。
DBA_OPARGUMENTS        列出操作符连接的参数信息。
DBA_OPBINDINGS        列出操作符连接。
DBA_OPERATORS         列出操作符。
DBA_OUTLINE_HINTS         列出组成概要的提示集。
DBA_OUTLINES          列出有关概要的信息。
DBA_PART_COL_STATISTICS                 包含所有表分区的列统计数据和直方图信息。
DBA_PART_HISTOGRAMS        包含所有表分区上直方图的直方图数据（每个直方图的端点）。
DBA_PART_INDEXES        列出所有分区索引的对象级分区信息。
DBA_PART_KEY_COLUMNS        描述所有分区对象的分区关键字列。
DBA_PART_LOBS        描述分区LOB的表级信息，包括LOB数据分区的缺省属性。
DBA_PART_TABLES         列出所有分区表的对象级分区信息。
DBA_PARTIAL_DROP_TABS         描述部分删除的表。
DBA_PENDING_TRANSACTIONS         提供关于未完成事务（由于故障或协调器没有提交或回滚）的信息。
DBA_POLICIES         列出策略。
DBA_PRIV_AUDIT_OPTS         描述通过系统和由用户审计的当前系统权限。
DBA_PROFILES         显示所有启动文件及其限制
DBA_QUEUE_SCHEDULES        描述当前传播信息的方案。
DBA_QUEUE_TABLES        描述在数据库中建立的所有队列表中的队列的名称和类型。
DBA_QUEUE        描述数据库中每一个队列的操作特征。
DBA_RCHILD        列出任何刷新组中的所有子组。
DBA_REFRESH        列出所有刷新组。
DBA_REFRESH_CHILDREN        列出刷新组中所有对象。
DBA_REFS        描述数据库中所有表的对象类型列中的REF列和REF属性。
DBA_REGISTERED_SNAPSHOT_GROUPS        列出该场地的所有快照登记组。
DBA_REGISTERED_SNAPSHOT                                检索本地表的远程快照的信息。
DBA_REPCAT_REFRESH_TEMPLATES                与Advanced Replication(高级复制)一起使用。
DBA_REPCAT_TEMPLATES_PARMS                        与Advanced Replication(高级复制)一起使用。
DBA_REPCAT_TEMPLATES_SITES                        与Advanced Replication(高级复制)一起使用。
DBA_REPCAT_USER_AUTHORIZATIONS                与Advanced Replication(高级复制)一起使用。
DBA_REPCAT_USER_PARM_VALUES                与Advanced Replication(高级复制)一起使用。
DBA_REPCATLOG                                                与Advanced Replication(高级复制)一起使用。
DBA_REPCOLUMN                                                与Advanced Replication(高级复制)一起使用。
DBA_REPCOLUMN_GROUP                                        与Advanced Replication(高级复制)一起使用。
DBA_REPCONFLICT                                                与Advanced Replication(高级复制)一起使用。
DBA_REPDDL                                                与Advanced Replication(高级复制)一起使用。
DBA_REPGENERATED                                                与Advanced Replication(高级复制)一起使用。
DBA_REPGENOBJECTS                                                与Advanced Replication(高级复制)一起使用。
DBA_REPGROUP                                                与Advanced Replication(高级复制)一起使用。
DBA_REPGROUPED_COLUMN                                与Advanced Replication(高级复制)一起使用。
DBA_REPKEY_COLUMNS                                                与Advanced Replication(高级复制)一起使用。
DBA_REPOBJECT                                                与Advanced Replication(高级复制)一起使用。
DBA_REPPARAMETER_COLUMN                        与Advanced Replication(高级复制)一起使用。
DBA_REPPRIORITY                                                与Advanced Replication(高级复制)一起使用。
DBA_REPPRIORITY_GROUP                                与Advanced Replication(高级复制)一起使用。
DBA_REPPROP                                                与Advanced Replication(高级复制)一起使用。
DBA_REPPESOL_STATS_CONTROL                        与Advanced Replication(高级复制)一起使用。
DBA_REPRESOLUTION                                                与Advanced Replication(高级复制)一起使用。
DBA_REPRESOLUTION_METHOD                        与Advanced Replication(高级复制)一起使用。
DBA_REPSITES                                                与Advanced Replication(高级复制)一起使用。
DBA_RGROUP                                                列出所有刷新组。
DBA_ROLE_PRIIVS                                                     列出授予用户和角色的角色
DBA_ROLES                                                    列出数据库中存在的所有角色
DBA_ROLLBACK_SEGS                                                   包含回滚段的描述
DBA_RSRC_CONSUMER_GROUP_PRIVS           列出所有已授权的资源消费组、用户和角色。
DBA_RSRC_CONSUMER_GROUPS                    列出数据库中存在的所有资源消费组。
DBA_RSRC_MANAGER_SYSTEM_PRIVS           列出所有已授予属于资源管理员系统权限的用户
和角色。
DBA_RSRC_PLAN_DIRECTIVES                            列出数据库中存在的所有资源计划的指示。
DBA_RSRC_PLANS                                                     列出数据库中存在的所有资源计划。
DBA_RULESETS                                                     列出规则集信息。
DBA_SEGMENTS                                                     包含分配级所有数据库段的存储信息。
DBA_SEOUENCES                                                     包含数据库中所有序列的描述。
DBA_SNAPSHOT_LOG_FILTER_COLS    列出记录在快照日志上的所有过滤列（不包括PK列）
DBA_SNAPSHOT_LOGS                                    列出数据库中所有的快照日志。
DBA_SNAPSHOT_REFRESH_TIMES                   列出快照刷新次数。
DBA_SNAPSHOTS                                                    列出数据库中所有的快照。
DBA_SOURCE                                                   包含数据库中所有存储对象的来源。
DBA_STMT_AUDIT_OPTS                                   包含的信息为：描述通过系统并由用户审计的当前
系统审计选项。
DBA_SUBPART_COL_STATISTICS                   列出表子分区的列统计数据和直方图信息。
DBA_SUBPART_HISTOGRAMS           列出表子分区中直方图的实际数据（每个直方图的端点）。
DBA_SUBPART_KEY_COLUMNS   列出用Composite  Range(复合排列)或HASH方法进行分区
的表（和表上的本地索引）的子分区关键字列。
DBA_SYNONYMS                                   列出数据库中所有同义词
DBA_SYS_PRIVS                                   列出授予用户和角色的系统权限。
DBA_TAB_COL_STATISTICS                   包含在DBA_TAB_COLUMNS视图中的列统计数据和直方图信息。
DBA_ TAB_COLUMNS                                   包含所有表、视图和簇的描述列的信息。
DBA_TAB_COMMENTS                                  包含对数据库中所有表和视图的注解。
DBA_TAB_HISTOGRAMS                   列出所有表中列的直方图。
DBA_TAB_PARTITIONS                                  对每一个表分区，描述它的分区级分区信息、分区的存储参数，和由
ANALYZE                        决定的各种分区统计数据。
DBA_TAB_PRIVS                          列出数据库中所有授予对象的授权。
DBA_TAB_SUBPARTITIONS   对每一个表的子分区，描述它的名称、表的名称和它所属的分区，
以及它的存储属性。
DBA_TABLES                          包含数据库中所有关系表的描述。
DBA_TABLESPACES                          包含所有表空间的描述
DBA_TEMP_FILES                          包含数据库临时文件的信息。
DBA_TRIGGER_COLS                          列出所有触发器中列的用法。
DBA_TRIGGERS                          列出数据库中所有触发器。
DBA_TS_QUOTAS                          列出所有用户的表空间限额。
DBA_TYPE_ATTRS                           显示数据库中类型的属性。
DBA_TYPE_METHODS                          描述数据库中所有类型的方法。
DBA_TYPES                           显示数据库中所有的抽象数据类型。
DBA_UNUSED_COL_TABS          包含对所有具有未使用列的表的描述。
DBA_UPDATABLE_COLUMNS  包含对可在一个连接视图中，由数据库管理员更新的列的描述。
DBA_USERS                          列出数据库中所有用户的信息。
DBA_USTATS                           包含当前用户的信息。
DBA_VARRAYS                           列出用户可以访问的视图的文本。
DBA_VIEWS                            包含数据库中所有视图的文本。
DBA_WAITERS                           列出所有正在等待一个锁的会话，以及列出正在阻止它们获得该锁的会话。
```

# $(v$动态视图)

```
V$ACCESS           显示当前被锁定的数据库中的对象及正在访问它们的会话。
V$ACTIVE_INSTANCES  为当前安装的数据库中出现的所有实例建立从实例名到实例号码的
映射
V$AQ                  描述当前数据库中队列的统计量。
V$ARCHIVE           包含归档所需的重做日志文件中的信息。每一行提供了一个线程所需的信息。这些信息在V$LOG中也是可用的。Oracle建议你使用V$LOG.
V$ARCHIVE_DEST          描述当前实例的所有归档日志目的文件及它们的当前值、模式和状态。
V$ARCHIVED_LOG          显示控制文件中的归档日志信息，包括归档日志名。在联重做日志文件成功地归档或清除（如果日志被清除，名字列将为NULL）后，一条归档日志记录被插入。如果这个日志被归档两次，那么就将有两条具有相同THREAD#，SEQUENCE#，FIRST_CHANG#值的归档日志记录，但它们的名字不同。当一个归档日志从一个备份集或一个副本中被恢复时，一个归档日志记录也将被插入。
V$ARCHIVE_PROCESSES   为一个实例提供关于不同ARCH进程状态的信息。
V$BACKUP          显示所有联机数据文件的备份状态。
V$BACKUP_ASYNC_IO   从控制文件中显示备份集的信息。在这个备份集成功完成后，一个
备份集记录将被插入。
V$BACKUP_CORRUPTION    从控制文件中显示数据文件备份中有关损坏的信息。注意在控
制文件和归档日志备份文件中损坏是不能容忍的
V$BACKUP_DATAFILE   从控制文件中显示备份数据文件和备份控制文件的信息。
V$BACKUP_DEVICE                           显示关于支持备份设备的信息。如果一个设备类型不支持指名的设备，那么将为这个设备类型返回一个带有设备类型和NULL设备名的行。如果一个设备类型支持指名的设备，那么将为每一个这种类型的可用设备返回一行。特殊的设备类型DISK不会通过这个视图返回，因为它总是可用的 。
V$BACKUP_PIECE  从控制文件中显示备份块的信息。每一个备份集由一个更多个备份块组
成。
V$BACKUP_REDOLOG          从控制文件中显示关于备份集中归档日志的信息。注意联机的重做日
志文件不能够被直接备份。它们必须首先被存储到磁盘上然后再进行
备份。一个归档日志备份集能包含一个或多个归档日志。
V$BACKUP_SET           从控制文件中显示备份集的信息。在备份集成功完成后，一个备份集记录将被插入。
V$BACKUP_SYNC_IO    从控制文件中显示备份集的信息。在备份集成功完成后，一个备份
集记录将被插入。
V$BGPROCESS          描述后台进程。
V$BH          这是一个并行服务器视图。这个视图为系统全局区中的每一个缓冲区给出了状态和探查次数。
V$BUFFER_POOL          显示关于这个实例所有可用缓冲池的信息。这个“集合数”属于LRU简易锁集的数目。
V$BUFFER_POOL_STATISTICS  显示关于这个实例所有可用缓冲池的信息。这个“集合数”
属于LRU简易锁集的数目。
V$CACHE          这是一个并行服务器视图。这个视图包含当前实例的SGA中的每一个块的头部信息，这个实例是与一个特殊数据库对象相关联的。
V$CACHE_LOCK           这是一个并行服务器的视图。除了特殊平台锁管理器标识符不同外，
V$CACHE_LOCK        与V$CACHE非常相似。如果这个特殊平台锁管理器为监视当前正发生的PCM锁操作提供了工具，那么这些信息可能是有用的。
V$CIRCUIT          包含关于虚电路的信息，这个虚电路是用户通过调度程序和服务器到数据库的所有连接。
V$CLASS_PING          显示每一个块类中被探查块的数目。用这个视图可以比较不同类的块竞争。
V$COMPATIBILITY          显示数据库实例使用中的特征，可能阻止系统性能下降到先前的版本。这是这些信息的动态（SGA）版本，它不可能反映出所用过的另外一些实例的特征，并可能包含暂时的不兼容性（如UNDO段），不过这将在数据库完全的关闭掉后不复存在。
V$COMPATSEG          列出数据库使用中的永久性的特征，这些特征将会阻止数据库回到早期的版本中去。
V$CONTEXT          列出当前对话的设置属性。
V$CONTROLFILE           列出控制文件的名字。
V$CONTROLFILE_RECORD_SECTION  显示关于控制文件记录部分的信息。
V$COPY_CORRUPTION  显示关于控制文件中数据文件副本损坏的信息。
V$DATABASE          包含控制文件中数据库信息。
V$DATAFILE           包含控制文件中数据库文件的信息。
V$DATAFILE_COPY          显示控制文件中数据文件副本的信息。
V$DATAFILE_HEADER  显示数据文件头部的数据文件信息。
V$DBFILE          列出组成数据库中的所有数据文件。这个视图是为历史兼容性保留的，我们建议用V$DATAFILE来代替。
V$DBLINK          描述由发布对V$DBLINK查询的会话所打开的所有数据库链接（用
IN_TRANSACTION=YES链接）。这些数据库链接必须在关闭前被提交或滚回。
V$DB_OBJECT_CACHE  显示缓存在库高速缓存中的数据库对象。这些对象包括表、索引、簇、
同义词定义、PL/SQL过程和包及触发器。
V$DB_PIPES          显示当前数据库中的管道。
V$DELETED_OBJECT   显示控制文件中被删除归档日志、数据文件副本和备份块的信息。这
个视图的唯一目的是优化恢复目录的再同步操作。当一个归档日志、数据文件副本或备份块被删除时，相应的记录将被做上删除标志。
V$DISPATCHER          提供调度进程的信息。
V$ DISPATCHER_RATE  为调度进程提供速率统计量。
V$DLM_ALL_LOCKS          这是一个并行服务器视图。V$DLM_ALL_LOCKS列出当前所有锁的信息，这些是锁管理器已知的被阻塞或阻塞其他对象的锁信息。
V$DLM_CONVERT_LOCAL  显示本地锁转换操作所消耗的时间。
V$DLM_CONVERT_REMOTE  显示远程锁转换操作所消耗的时间。
V$DLM_LOCKS                 这是一个并行服务器视图。V$DLM_ALL_LOCKS 列出当前所有锁的信息，这些是锁管理器已知的被阻塞或阻塞其他对象的锁信息。
V$DLM_MISC          显示多种DLM统计量。
V$DLM_RESS          这是一个并行服务器的视图，它显示了当前锁管理器已知的全部资源的信息。
V$ENABLEDPRIVS           显示被授予的权限。这些权限可以在SYS.SYSTEM_PRIVILEGES_MAP这个表中找到。
V$ENQUEUE_LOCK           显示排队状态对象所拥有的全部锁。这个视图中的列等同于V$LOCK
中的列。更多的信息参见V$LOCK.
V$EVENT_NAME           包含等待事件的信息。
V$EXECUTION           显示并行执行中的信息。
V$FALSE_PING           这是一个并行服务器视图。这个视图显示可能得到探查失败的缓冲区，探查被同样锁保护的缓冲区10次以上，如像另一个探查10次以上的缓冲区。被鉴别为获得探查失败信息的缓冲区能够被重新映射到GC_FILES_TO_LOCKS 中以减少锁的冲突。
V$FAST_START_SERVERS                  提供关于执行并行事务恢复的所有从属恢复操作的信息。
V$FAST_START_TRANSACTIONS          包含关于Oracle 恢复中的事务进展信息。
V$FILE_PING           显示每一个数据文件被探查的块数目。反过来，这些信息能被用来决定对一个存在的数据文件访问方式，同时也可以决定从数据文件块到PCM锁的新的映射。
V$FILESTAT           包含文件关于读/写统计量的信息
V$FIXED_TABLE           显示数据库中所有动态性能表、视图和导出表。一些V$表（如
V$ROLLNAME）涉及到了真正的表，没有被列出来。
V$FIXED_VIEW_DEFINITION    包含所有固定视图的定义（以V$开头的视图）。应谨慎地使
用这个表。Oracle 总是想从版本到版本保持固定视图的行为，但是固定视图的定义能够在没有通知的情况下改变。用这些定义通过使用动态性能表中的索引列可以优化你的查询。
V$GLOBAL_BLOCKED_LOCKS  显示全局块锁。
V$GLOBAL_TRANSACTION            显示当前激活的全局事务的信息。
V$HS_AGENT           标识当前运行在一个给定的主机上的HS代理的集合，每一个代理进程用一行表示。
V$HS_SESSION          标识当前为一个Oracle 服务器打开的HS会话集。
V$INDEXED_FIXED_COLUMN   显示建立索引的动态性能表中的列（X$表），X$表能够在没
有通知的情况下改变。使用这个视图仅仅在写查询方面比固定视图（V$视图）的效率要高。
V$INSTANCE           显示当前实例的状态。这个V$INSTANCE 版本同早期的V$INSTANCE 版本不兼容。
V$INSTANCE_RECOVERY   用来监视执行用户指定恢复读次数的限制机制。
V$LATCH         为非双亲简易锁列出统计表，同时为双亲简易锁列出总计统计。就是说，每一个双亲简易锁的统计量包括它的每一个子简易锁的计算值。
V$LATCHHOLDER           包含当前简易锁持有者的信息。
V$LATCHNAME           包含关于显示在V$LATCH中的简易锁的解码简易锁名字的信息。
V$LATCHNAME        中的行与V$LATCH中的行有一一对应的关系。
V$LATCH_CHILDREN   包含关于子简易锁的统计量。这个视图包括V$LATCH中的所有列和
一个CHILD#列。注意如果子简易锁LATCH#列相匹配，那么它们将具有相同的双亲。
V$LATCH_MISSES         包含试图获得一个简易锁失败的统计量。
V$LATCH_PARENT           包含关于双亲简易锁的统计量。V$LATCH_PARENT中的列与V$LATCH中的列是相等的。
V$LIBRARYCACHE          包含关于高速缓存性能和活动的统计量。
V$LICENSE           包含关于许可证限制的信息。
V$LOADCSTAT           包含在一个直接装载执行过程中所编译的SQL*Loader统计量。这些统计量适用于整个的加载。既然装载数据和查询不能在同一时间进行，那么，任何对这个表的SELECT操作都将会导致”no  rows  retured”(没有行返回)
V$LOADTSTAT          包含在一个直接装载执行过程中所编译的SQL*Loader统计量。这些统计量适用于当前的表。既然装载数据和查询不能在同一时间进行，那么，任何对这个表的SELECT操作都将会导致”no  rows  retured”(没有行返回)
V$LOCK           列出当前ORACLE服务器所持有的锁和对一个锁或简易锁的未决请求。
V$LOCK_ACTIVITY    这是一个并行服务器视图。它显示当前实例的DLM锁操作活动，每
一行对应着锁操作的类型。
V$LOCK_ELEMENT           这是一个并行服务器视图。每一个被缓冲高速缓存使用的PCM锁在
V$LOCK_ELEMENT中都有一个条目。与一个锁元素相对应的PCM锁的名字是（‘BL’，indx,class）。
V$LOCKED_OBJECT                                   列出在这个系统中每一个事务所获得的全部锁。
V$LOCKS_WITH_COLLISIONS   这是一个并行服务器视图。用这个视图可以查找保护多重锁
缓冲区的锁，这些缓冲区的每一个至少被强制性的读或写达十次以上。那些正经历着探查失败的缓冲区，主要是由于被映射到同样的锁上。
V$LOG                   包含控制文件中的日志文件信息。
V$LOGFILE            包含重做日志文件的信息。
V$LOGHIST            包含控制文件中的日志历史信息。这个视图是为历史兼容性保留的。这里建议使用V$LOG_HISTORY来代替它。
V$LOGMNR_CONTENTS           包含日志历史信息。
V$LOGMNR_DICTIONARY   包含日志历史信息。
V$LOGMNR_LOGS                          包含日志信息。
V$LOGMNR_PARAMETERS   包含日志信息。
V$LOG_HISTORY                           包含控制文件中的日志历史信息。
V$MLS_PARAMETERS           这是一个ORACLE委托服务器（Trusted Oracle Server）视图，这个视图列出ORACLE指定委托服务器的初始化参数。更多的信息，可以在你的ORACLE委托文件中查到。
V$MTS           包含调节多线程的服务器的信息。
V$MYSTAT        包含当前会话的统计量。
V$NLS_PARAMETERS   包含当前NLS参数的值。
V$NLS_VALID_VALUES    列出NLS参数所有有效的信息。
V$OBJECT_DEPENDENCY   能够通过当前装戴在共享池中的包、过程或游标来决定依赖于那
一个对象。例如，与V$SESSIONV和$SQL一起，它能被用来决定在SQL语句中使用哪一个正在被用户执行的表。要知道更多的信息，请见V$SESSION和V$SQL
V$OBSOLETE_PARAMETER   列出陈旧的参数。只要有某一值为TRUE，你就应该检查为什
么。
V$OFFLINE_CURSOR    显示控制文件中数据文件的脱机信息。
V$OPEN_CURSOR                   列出每一个用户会话当前打开的和解析的游标。
V$OPTION            列出用ORACLE服务器安装的选项。
V$PARALLEL_DEGREE_LIMIT_MTH    显示所有有效的并行度限制资源分配的方法。
V$PARAMETER                   列出关于初始化参数的信息。
V$PING            这是一个并行服务器视图。除了只显示至少被探查一次的块有所不同外，V$PING视图与V$CACHE视图完全是一样的，这个视图包含当前实例的SGA中每一块的块首部信息，这个实例是与一个特定的数据库对象相关联的。
V$PQ_SESSTAT              列出并行查询会话的统计信息。注意：这个视图在未来的版本中将会成为过的 。
V$PQ_SLAVE            列出一个实例上每个活动并行执行服务器的统计量。注意：这个视图在未来的版本中将会过时而被一个新的称做V$PX_PROCESS的视图所代替。
V$PQ_SYSSTAT            列出并行查询的系统统计量。注意：这个视图在未来的版本中将会过时而被一个新的称做V$PX_PROCESS_SYSSTAT的视图所代替。
V$PQ_TQSTAT            包含并行执行操作上的统计量。这些统计量是在完成了查询后编辑的，并且仅在会话期保持。它显示在执行树的每一级阶段，通过每一个并行运行服务器处理的行数。这个视图能够帮助在一个查询执行中测定不平衡的问题。注意：这个视图在未来的版本中将称做V$PX_TQSTAT视图。
V$PROCESS            包含关于当前活动进程的信息。当LATCHWAIT列显示一个进程正等待什么样的简易锁时，LATCHSPIN列就显示一个进程正围绕什么样简易锁运行。在多处理器机器上，ORACLE进程在等待一个简易锁之前是围绕它运行的。
V$PROXY_ARCHIVEDLOG    包含归档日志备份文件的描述信息，这些备份文件带有一个称
为Proxy副本的新特征。每一个行代表一个归档日志的备份信息。
V$PROXY_DATAFILE                   包含数据文件和控制文件备份的描述信息，这个备份文件带了一个称
为Proxy副本的新特征。每一行代表一个数据库文件的备份信息。
V$PWFILE_USERS                    列出被授予SYSDBA和SYSOPER权限的用户，这些权限就象从
password文件中衍生而来一样。
V$PX_PROCESS            包含正运行并行操作的会话的信息。
V$PX_PROCESS_SYSSTAT   包含正运行并行操作的会话的信息。
V$PX_SESSION            包含正运行并行操作的会话的信息。
```

说明：

* 通过数据字典可查询更详细的视图数据

```
SQL> desc dictionary
 名称                                      是否为空? 类型
 ----------------------------------------- -------- ----------------------------
 TABLE_NAME                                         VARCHAR2(30)
 COMMENTS                                           VARCHAR2(4000)

SQL> select * from dictionary;
```
