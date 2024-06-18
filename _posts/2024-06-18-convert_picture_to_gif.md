---
title: 如何将图片或视频转转gif
date: 2024-06-18 17:12:37
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 图片转gif，视频转gif
categories:
    - [GIF]
tags:
    - GIF
---

# 前言



做了这么久的自动化开发，没有录制一些自动化设计与执行过程相关的视频，一直觉得这些视频比较大，不好放在`github blog`上，最近突然想到将视频转换为`gif`文件，这样内容会小一些。

虽然能够将视频上传到哔哩哔哩或者优酷之类的流媒体网站上（需要会员），提供链接到`github blog`文章中会更节省空间，到考虑到需要`VIP`，so...

鉴于此，本文介绍如何将一些图片转换成`gif`动图文件，以及将`mp4`视频转换成`gif`动图文件。

# 将图片转换为gif动图

常见的转换方式有：借助转换工具，或者代码转换。

这里介绍一下`Linux`下的几种转换方式，当然，也可以借助在线转换工具在线转换（往往有约束条件，免费的也是最贵的）。



## 使用ImageMagick

`ImageMagick`是一个强大的图像处理工具集，在大多数`Linux`发行版中都可用。

安装`ImageMagick`：`apt-get install imagemagick`（对于`Debian/Ubuntu`系统）或相应的包管理器命令。
转换图片到`GIF`：例如，如果你有一系列图片文件名为 `image1.png, image2.png`等，并想把它们合并成一个`GIF`：      


```shell
convert image*.png output.gif
```

或者如果需要设置延迟时间（每帧显示的时间），可以使用：

```shell
convert -delay 100 image*.png output.gif  # delay单位是十分之一秒
```



**说明:**

这里有个问题需要注意，如果使用`image*.png`，生成的`gif`文件内容具有随机性，即里面播放的各个静态`png`画面顺序可能不是自己想要的，比如说有`image1.png`，一直到`image9.png`，总共9张`png`图片，播放顺序预期是从`image1`到`image9`，但实际生成具有随机性，为了解决此问题，可以使用类似如下指令规避：

```shell
convert image1.png image2.png image3.png image4.png image5.png image6.png image7.png image8.png image19.png output.gif
```

即指定文件顺序。

如果文件命名具有一定的顺序规则，则借助`Linux`下的正则实现转换，如：

```shell
convert image[1-9].png output.gif
```



## 使用ffmpeg

`ffmpeg`也是一个功能丰富的多媒体框架，可以用来处理视频和图像。

安装`ffmpeg`:

`apt install ffmpeg` 

安装`ffmpeg`后，可以使用以下命令将图片序列转换成一个动态的`GIF`：

```shell
ffmpeg -i input.jpg -vf "fps=10" output.gif  # fps表示每秒播放的帧数
```



## 使用在线服务或GUI应用程序

如果不想安装任何软件包，也可以选择在线服务来完成这个任务。
    
## 使用Python脚本

使用`Python`中的`Pillow`库可以方便地进行图像处理操作。首先确保安装了`Pillow`库：`pip install Pillow`

示例代码片段如下：


```python    
import os

import PIL.Image as Image


def get_gif(pic_dir, nums, t=0.1):
  """
  param pic_dir: string, the picture dir
  param: nums: int, the numbers of the pictures
  param t: delapy times, unit is second
  """
  imgs = []
  for i in range(nums):
    pic_name = '{}/{}.png'.format(pic_dir, i+1)
    temp = Image.open(pic_name)
    imgs.append(temp)
  save_name = '{}/{}.gif'.format(pic_dir, os.path.split(pic_dir)[-1])
  imgs[0].save(save_name, save_all=True, append_images=imgs, duration=t)
  return save_name


if __name__ == '__main__':
  pic_dir = '/root/pngs'
  save_name = get_gif(pic_dir, 12, 0.25)
  print('制作完成。所属文件:{}'.format(save_name))
```



运行效果如下：



```shell
root@Service:~/pngs# python3 t.py 
制作完成。所属文件:/root/pngs/pngs.gif
root@Service:~/pngs# ll
total 121232
drwxr-xr-x  4 root root     4096 Jun 18 10:02 ./
drwx------ 24 root root     4096 Jun 18 10:02 ../
-rw-r--r--  1 root root   209303 Jun 17 14:43 10.png
-rw-r--r--  1 root root   676914 Jun 17 14:43 11.png
-rw-r--r--  1 root root   279929 Jun 17 14:43 12.png
-rw-r--r--  1 root root   204480 Jun 17 14:43 13.png
-rw-r--r--  1 root root   259175 Jun 17 14:43 1.png
-rw-r--r--  1 root root   205840 Jun 17 14:43 2.png
-rw-r--r--  1 root root   231139 Jun 17 14:43 3.png
-rw-r--r--  1 root root   433484 Jun 17 14:43 4.png
-rw-r--r--  1 root root   603103 Jun 17 14:43 5.png
-rw-r--r--  1 root root   546179 Jun 17 14:43 6.png
-rw-r--r--  1 root root   130152 Jun 17 14:43 7.png
-rw-r--r--  1 root root   201282 Jun 17 14:43 8.png
-rw-r--r--  1 root root   199003 Jun 17 14:43 9.png
-rw-r--r--  1 root root     7276 Jun 17 14:52 a.txt
drwxr-xr-x  2 root root     4096 Jun 17 16:02 good/
-rw-r--r--  1 root root  1031069 Jun 18 10:02 pngs.gif
drwxr-xr-x  2 root root     4096 Jun 17 15:32 source/
-rw-r--r--  1 root root  1181735 Jun 18 09:47 test.gif
-rw-r--r--  1 root root      670 Jun 18 10:02 t.py
-rw-r--r--  1 root root 23096859 Jun 17 16:17 Web1.gif
-rw-r--r--  1 root root 94581304 Jun 17 15:33 待编辑.mp4
root@Service:~/pngs# 
```





# mp4视频转gif

借助`ffmpeg`进行转换和压缩:

```shell
root@Service:~/pngs# ffmpeg -t 176 -ss 00:00:03 -i 待编辑.mp4  out.gif
ffmpeg version 6.0-6ubuntu1.1 Copyright (c) 2000-2023 the FFmpeg developers
  built with gcc 13 (Ubuntu 13.2.0-4ubuntu3)
  configuration: --prefix=/usr --extra-version=6ubuntu1.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libglslang --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librist --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --disable-sndio --enable-libjxl --enable-pocketsphinx --enable-librsvg --enable-libvpl --disable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-libplacebo --enable-librav1e --enable-shared
  libavutil      58.  2.100 / 58.  2.100
  libavcodec     60.  3.100 / 60.  3.100
  libavformat    60.  3.100 / 60.  3.100
  libavdevice    60.  1.100 / 60.  1.100
  libavfilter     9.  3.100 /  9.  3.100
  libswscale      7.  1.100 /  7.  1.100
  libswresample   4. 10.100 /  4. 10.100
  libpostproc    57.  1.100 / 57.  1.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '待编辑.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    title           : EV录屏5.1.6软件录制
    encoder         : Lavf58.33.100
    comment         : 本视频由湖南一唯信息科技开发的EV录屏软件录制, www.ieway.cn
  Duration: 00:12:47.90, start: 0.000000, bitrate: 985 kb/s
  Stream #0:0[0x1](und): Video: h264 (Constrained Baseline) (avc1 / 0x31637661), yuvj420p(pc, bt709/unknown/unknown, progressive), 1912x1032, 976 kb/s, 19.84 fps, 20 tbr, 10240 tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 5 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
      vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:0 -> #0:0 (h264 (native) -> gif (native))
Press [q] to stop, [?] for help
[swscaler @ 0x638b73408d40] deprecated pixel format used, make sure you did set range correctly
[swscaler @ 0x638b73408d40] [swscaler @ 0x638b73416dc0] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73408d40] [swscaler @ 0x638b73427480] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73408d40] [swscaler @ 0x638b73437b40] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73408d40] [swscaler @ 0x638b73448200] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73408d40] [swscaler @ 0x638b734588c0] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] deprecated pixel format used, make sure you did set range correctly
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73423d80] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73430d40] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7343dd00] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7344acc0] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73457c80] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] deprecated pixel format used, make sure you did set range correctly
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73423d80] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73430d40] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7343dd00] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7344acc0] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73457c80] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] deprecated pixel format used, make sure you did set range correctly
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73423d80] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73430d40] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7343dd00] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b7344acc0] No accelerated colorspace conversion found from yuv420p to bgr8.
[swscaler @ 0x638b73416dc0] [swscaler @ 0x638b73457c80] No accelerated colorspace conversion found from yuv420p to bgr8.
Output #0, gif, to 'out.gif':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    title           : EV录屏5.1.6软件录制
    comment         : 本视频由湖南一唯信息科技开发的EV录屏软件录制, www.ieway.cn
    encoder         : Lavf60.3.100
  Stream #0:0(und): Video: gif, bgr8(pc, gbr/unknown/unknown, progressive), 1912x1032, q=2-31, 200 kb/s, 20 fps, 100 tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
      encoder         : Lavc60.3.100 gif
frame= 3502 fps=188 q=-0.0 Lsize=   18123kB time=00:02:55.95 bitrate= 843.8kbits/s speed=9.47x    
video:18123kB audio:0kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000108%
root@Service:~/pngs#
```

**说明:**

* -t 要截取的视频时长
* -ss 开始时间
* -i 源视频文件
* 最后为输出文件名


生成的gif文件大小信息参考如下：

```shell
root@Service:~/pngs# ll
total 169480
drwxr-xr-x  3 root root     4096 Jun 17 16:01 ./
drwx------ 24 root root     4096 Jun 17 15:57 ../
-rw-r--r--  1 root root   209303 Jun 17 14:43 10.png
-rw-r--r--  1 root root   676914 Jun 17 14:43 11.png
-rw-r--r--  1 root root   279929 Jun 17 14:43 12.png
-rw-r--r--  1 root root   204480 Jun 17 14:43 13.png
-rw-r--r--  1 root root   259175 Jun 17 14:43 1.png
-rw-r--r--  1 root root   205840 Jun 17 14:43 2.png
-rw-r--r--  1 root root   231139 Jun 17 14:43 3.png
-rw-r--r--  1 root root   433484 Jun 17 14:43 4.png
-rw-r--r--  1 root root   603103 Jun 17 14:43 5.png
-rw-r--r--  1 root root   546179 Jun 17 14:43 6.png
-rw-r--r--  1 root root   130152 Jun 17 14:43 7.png
-rw-r--r--  1 root root   201282 Jun 17 14:43 8.png
-rw-r--r--  1 root root   199003 Jun 17 14:43 9.png
-rw-r--r--  1 root root  1751656 Jun 17 14:45 API.gif
-rw-r--r--  1 root root 24201866 Jun 17 16:01 APP.gif
-rw-r--r--  1 root root 18558255 Jun 17 15:35 out.gif
drwxr-xr-x  2 root root     4096 Jun 17 15:32 source/
-rw-r--r--  1 root root 24879179 Jun 17 15:58 Web1.gif
-rw-r--r--  1 root root  5328623 Jun 17 15:59 Web2.gif
-rw-r--r--  1 root root 94581304 Jun 17 15:33 待编辑.mp4
root@Service:~/pngs#
```

压缩一下看看效果：

需要先安装`gifsicle`:

`apt-get install gifsicle`

将之前的`gif`文件放入`good`目录，方便辨别，然后进行压缩，参考命令如下：

```shell
root@Service:~/pngs# #gifsicle -O3 input.gif -o output.gif
root@Service:~/pngs# gifsicle -O3 good/Web1.gif -o Web1.gif
gifsicle: warning: huge GIF, conserving memory (processing may take a while)
root@Service:~/pngs# gifsicle -O3 good/Web2.gif -o Web2.gif
gifsicle: warning: huge GIF, conserving memory (processing may take a while)
root@Service:~/pngs# 
```

**说明:**

* -O3 表示使用最大的优化级别。
* good/Web1.gif 是输入的 GIF 文件。
* -o Web1.gif 是输出的 GIF 文件。

或者使用：

`gifsicle --optimize=3 --lossy=80 -o output.gif input.gif`

在其中：

* --optimize=3 表示使用最大的优化级别，这有助于减小文件大小。
* --lossy=80 是一个损失性压缩的参数，值越大，压缩率越高。


使用这两种方式，压缩效果都甚微：

```shell
root@Service:~/pngs# ll
total 123776
drwxr-xr-x  4 root root     4096 Jun 17 16:05 ./
drwx------ 24 root root     4096 Jun 17 15:57 ../
-rw-r--r--  1 root root   209303 Jun 17 14:43 10.png
-rw-r--r--  1 root root   676914 Jun 17 14:43 11.png
-rw-r--r--  1 root root   279929 Jun 17 14:43 12.png
-rw-r--r--  1 root root   204480 Jun 17 14:43 13.png
-rw-r--r--  1 root root   259175 Jun 17 14:43 1.png
-rw-r--r--  1 root root   205840 Jun 17 14:43 2.png
-rw-r--r--  1 root root   231139 Jun 17 14:43 3.png
-rw-r--r--  1 root root   433484 Jun 17 14:43 4.png
-rw-r--r--  1 root root   603103 Jun 17 14:43 5.png
-rw-r--r--  1 root root   546179 Jun 17 14:43 6.png
-rw-r--r--  1 root root   130152 Jun 17 14:43 7.png
-rw-r--r--  1 root root   201282 Jun 17 14:43 8.png
-rw-r--r--  1 root root   199003 Jun 17 14:43 9.png
-rw-r--r--  1 root root     7276 Jun 17 14:52 a.txt
drwxr-xr-x  2 root root     4096 Jun 17 16:02 good/
drwxr-xr-x  2 root root     4096 Jun 17 15:32 source/
-rw-r--r--  1 root root 23071991 Jun 17 16:05 Web1.gif
-rw-r--r--  1 root root  4849543 Jun 17 16:05 Web2.gif
-rw-r--r--  1 root root 94581304 Jun 17 15:33 待编辑.mp4
root@Service:~/pngs# ls -l good/
total 72976
-rw-r--r-- 1 root root  1751656 Jun 17 14:45 API.gif
-rw-r--r-- 1 root root 24201866 Jun 17 16:01 APP.gif
-rw-r--r-- 1 root root 18558255 Jun 17 15:35 out.gif
-rw-r--r-- 1 root root 24879179 Jun 17 15:58 Web1.gif
-rw-r--r-- 1 root root  5328623 Jun 17 15:59 Web2.gif
root@Service:~/pngs#
```

使用第二种方式（指定--lossy）压缩，不仅耗时，而且压缩效果和第一种基本没差别（从文件大小上看，大小基本没压缩，画质差不多）。


