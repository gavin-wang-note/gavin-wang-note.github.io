---
layout:     post
title:      "nose进度条中展示执行用例数与总数"
subtitle:   "nose progress bar"
date:       2019-11-20
author:     "Gavin"
catalog:    true
tags:
    - nose
    - Automation
    - Progress bar
---

# 概述

在使用nose 插件时，发现这个插件只能显示进度（nose-progressive），并不知道当前执行多少个用例，执行到哪个了，如下图所示：

<img class="shadow" src="/img/in-post/before_progress_bar.png" width="1200">



# 期待效果

这里源码有个问题，同时使用高亮（nose的  colorama  和  walkingnine-colorunit）和进度，会导致高亮和进度在用例执行结果信息输出时，两部分信息展示混杂在一起，已经修改源码解决，安装后无需做任何调整。

  由于只能看到一个进度条，无法知道当前要执行多少个用例，以及执行到了第几个用例，再次修改之。在进度条前面，显示已执行用例数（包含当前正在执行的用例）与总共要执行的用例数，效果如下图所示：

于是对源码（nose-progressive-master/noseprogressive/bar.py）做了如下调整：

    def update(self, test_path, number):
        """Draw an updated progress bar.
    
        At the moment, the graph takes a fixed width, and the test identifier
        takes the rest of the row, truncated from the left to fit.
    
        test_path -- the selector of the test being run
        number -- how many tests have been run so far, including this one
    
        """
        # TODO: Play nicely with absurdly narrow terminals. (OS X's won't even
        # go small enough to hurt us.)
    
        # Figure out graph:
        GRAPH_WIDTH = 14
        # min() is in case we somehow get the total test count wrong. It's tricky.
        num_filled = int(round(min(1.0, float(number) / self.max) * GRAPH_WIDTH))
        graph = ''.join([self._fill_cap(' ' * num_filled),
                         self._empty_cap(self._empty_char * (GRAPH_WIDTH - num_filled))])
    
        # Figure out the test identifier portion:
        # Avoid causing progress bar wraps due to more test cases when 
        # show number of runned/total test cases, modify it by wangyunzeng 2019-01-30
        # cols_for_path = self.cols - GRAPH_WIDTH - 2  # 2 spaces between path & graph
        cols_for_path = self.cols - GRAPH_WIDTH - 13  # 13 spaces between path & graph
        if len(test_path) > cols_for_path:
            test_path = test_path[len(test_path) - cols_for_path:]
        else:
            test_path += ' ' * (cols_for_path - len(test_path))
    
        # Put them together, and let simmer:
        # Show number of runned/total test cases, modify it by wangyunzeng 2019-01-30
        # self.last = self._term.bold(test_path) + '  ' + graph
        self.last = self._term.bold(test_path) + '  ' + str(number) + '/' + str(self.max) + '  ' + graph
        with self._at_last_line():
            self.stream.write(self.last)
        self.stream.flush()


再次执行，效果图如下：

<img class="shadow" src="/img/in-post/after_progress_bar.png" width="1200">



是不是清爽很多了~



