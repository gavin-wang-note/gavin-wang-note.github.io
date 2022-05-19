---
layout:     post
title:      "获取ceph PG 分布"
subtitle:   "Get ceph PG allocate"
date:       2022-05-19
author:     "Gavin"
catalog:    true
tags:
    - ceph
---



# 概述



# 第一版


```
#!/bin/bash

ceph_version=`ceph -v | awk '\{\{print \$3\}\}'`

if [[ ${ceph_version} =~ '10.' ]]; then
    pg_stat="pg_stat"
    up="up"
elif [[ ${ceph_version} =~ '12.' ]]; then
    pg_stat="PG_STAT"
    up="UP"
fi

ceph pg dump | egrep -v "^[0-9]*  " | awk '
/^'$pg_stat'/ { col=1; while($col!="'"$up"'") {col++}; col++ }
/^[0-9a-f]+.[0-9a-f]+/ { match($0,/^[0-9a-f]+/); pool=substr($0, RSTART, RLENGTH); poollist[pool]=0;
up=$col; i=0; RSTART=0; RLENGTH=0; delete osds; while(match(up,/[0-9]+/)>0) { osds[++i]=substr(up,RSTART,RLENGTH); up = substr(up, RSTART+RLENGTH) }
for(i in osds) {array[osds[i],pool]++; osdlist[osds[i]];}
}
END {
printf("\n");
printf("pool :\t"); for (i in poollist) printf("%s\t",i); printf("| SUM \n");
for (i in poollist) printf("--------"); printf("-------------\n");
for (i in osdlist) { printf("osd.%i\t", i); sum=0;
for (j in poollist) { printf("%i\t", array[i,j]); sum+=array[i,j]; poollist[j]+=array[i,j] }; printf("| %i\n",sum) }
for (i in poollist) printf("--------"); printf("--------------\n");
printf("SUM :\t"); for (i in poollist) printf("%s\t",poollist[i]); printf("|\n");
}'
```

结果展示如下：

<img class="shadow" src="/img/in-post/pg_allocate_v1.png" width="1200">


# 第二版

```
#!/bin/bash

ceph_version=`ceph -v | awk '\{\{print \$3\}\}'`

if [[ ${ceph_version} =~ '10.' ]]; then
    pg_stat="pg_stat"
    up="up"
elif [[ ${ceph_version} =~ '12.' ]]; then
    pg_stat="PG_STAT"
    up="UP"
fi

ceph pg dump | awk '
 /^'$pg_stat'/ { col=1; while($col!="UP") {col++}; col++ }
 /^[0-9a-f]+\.[0-9a-f]+/ { match($0,/^[0-9a-f]+/); pool=substr($0, RSTART, RLENGTH); poollist[pool]=0;
 up=$col; i=0; RSTART=0; RLENGTH=0; delete osds; while(match(up,/[0-9]+/)>0) { osds[++i]=substr(up,RSTART,RLENGTH); up = substr(up, RSTART+RLENGTH) }
 for(i in osds) {array[osds[i],pool]++; osdlist[osds[i]];}
}
END {
 printf("\n");
 slen=asorti(poollist,newpoollist);
 printf("pool :\t");for (i=1;i<=slen;i++) {printf("%s\t", newpoollist[i])}; printf("| SUM \n");
 for (i in poollist) printf("--------"); printf("----------------\n");
 slen1=asorti(osdlist,newosdlist)
 delete poollist;
 for (j=1;j<=slen;j++) {maxpoolosd[j]=0};
 for (j=1;j<=slen;j++) {for (i=1;i<=slen1;i++){if (array[newosdlist[i],newpoollist[j]] >0  ){minpoolosd[j]=array[newosdlist[i],newpoollist[j]] ;break } }}; 
 for (i=1;i<=slen1;i++) { printf("osd.%i\t", newosdlist[i]); sum=0; 
 for (j=1;j<=slen;j++)  { printf("%i\t", array[newosdlist[i],newpoollist[j]]); sum+=array[newosdlist[i],newpoollist[j]]; poollist[j]+=array[newosdlist[i],newpoollist[j]];if(array[newosdlist[i],newpoollist[j]] != 0){poolhasid[j]+=1 };if(array[newosdlist[i],newpoollist[j]]>maxpoolosd[j]){maxpoolosd[j]=array[newosdlist[i],newpoollist[j]];maxosdid[j]=newosdlist[i]};if(array[newosdlist[i],newpoollist[j]] != 0){if(array[newosdlist[i],newpoollist[j]]<=minpoolosd[j]){minpoolosd[j]=array[newosdlist[i],newpoollist[j]];minosdid[j]=newosdlist[i]}}}; printf("| %i\n",sum)} for (i in poollist) printf("--------"); printf("----------------\n");
 slen2=asorti(poollist,newpoollist);
 printf("SUM :\t"); for (i=1;i<=slen;i++) printf("%s\t",poollist[i]); printf("|\n");
 printf("Osd :\t"); for (i=1;i<=slen;i++) printf("%s\t",poolhasid[i]); printf("|\n");
 printf("AVE :\t"); for (i=1;i<=slen;i++) printf("%.2f\t",poollist[i]/poolhasid[i]); printf("|\n");
 printf("Max :\t"); for (i=1;i<=slen;i++) printf("%s\t",maxpoolosd[i]); printf("|\n");
 printf("Osdid :\t"); for (i=1;i<=slen;i++) printf("osd.%s\t",maxosdid[i]); printf("|\n");
 printf("per:\t"); for (i=1;i<=slen;i++) printf("%.1f%\t",100*(maxpoolosd[i]-poollist[i]/poolhasid[i])/(poollist[i]/poolhasid[i])); printf("|\n");
 for (i=1;i<=slen2;i++) printf("--------");printf("----------------\n");
 printf("min :\t"); for (i=1;i<=slen;i++) printf("%s\t",minpoolosd[i]); printf("|\n");
 printf("osdid :\t"); for (i=1;i<=slen;i++) printf("osd.%s\t",minosdid[i]); printf("|\n");
 printf("per:\t"); for (i=1;i<=slen;i++) printf("%.1f%\t",100*(minpoolosd[i]-poollist[i]/poolhasid[i])/(poollist[i]/poolhasid[i])); printf("|\n");
}'
```

结果显示如下图：

<img class="shadow" src="/img/in-post/PG_ALLOCATE_V2.png" width="1200">



# 语法的解释


```/^pg_stat/ { col=1; while($col!="up") {col++}; col++ } ```

这个是匹配pg dump 的输出结果里面pg_stat那个字段，开始计数为1，不是up值就将col的值加1，这个匹配到的就是我们经常看到的[1,10]这个值最后的col++是将col值+1,因为字段里面有up,up_primary,我们需要的是up_primary


```/?[1]+.[0-9a-f]+/ { match($0,/?[2]+/); pool=substr($0, RSTART, RLENGTH); poollist[pool]=0;```

这个是匹配前面的 1.17a pg号 ，使用自带的match函数 做字符串的过滤统计匹配.号前面的存储池ID， 并得到 RSTART, RLENGTH 值，这个是取到前面的存储池ID，使用substr 函数，就可以得到pool的值了，poollist[pool]=0，是将数组的值置为0


```up=$col; i=0; RSTART=0; RLENGTH=0; delete osds; while(match(up,/[0-9]+/)>0) { osds[++i]=substr(up,RSTART,RLENGTH); up = substr(up, RSTART+RLENGTH) }```

先将变量置0，然后将osd编号一个个输入到osds[i]的数组当中去


```for(i in osds) {array[osds[i],pool]++; osdlist[osds[i]];}```

将osds数组中的值输入到数组当中去，并且记录成osdlist，和数组array[osd[i],pool]


```
printf("\n");
printf("pool :\t"); for (i in poollist) printf("%s\t",i); printf("| SUM \n");
```

打印osd pool的编号


```for (i in poollist) printf("--------"); printf("----------------\n");```

根据osd pool的长度打印----


```for (i in osdlist) { printf("osd.%i\t", i); sum=0;```

打印osd的编号



```for (j in poollist) { printf("%i\t", array[i,j]); sum+=array[i,j]; poollist[j]+=array[i,j] }; printf("| %i\n",sum) }```
打印对应的osd的pg数目，并做求和的统计


```
for (i in poollist) printf("--------"); printf("----------------\n");
printf("SUM :\t"); for (i in poollist) printf("%s\t",poollist[i]); printf("|\n");
```

打印新的poollist里面的求和的值,修改版本里面用到的函数

```slen1=asorti(osdlist,newosdlist)```

这个是将数组里面的下标进行排序，这里是对osd和poollist的编号进行排序 slen1是拿到数组的长度，使用for进行遍历输出

