---
title: matplotlib绘图,为避免中文乱码而出现字体告警
date: 2027-11-27 23:00:00
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 解决使用matplotlib绘图时为了避免中文乱码而出现的字体告警问题 
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

自动化项目，`conftest.py`里有根据`feature mark`属性绘制饼图（使用`matplotlib`），为了防止饼图上中文出现乱码，使用了支持中文的字体，但是在保存成图片时会有一个告警，信息参考如下：

```shell
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 27979 (\N{CJK UNIFIED IDEOGRAPH-6D4B}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 35797 (\N{CJK UNIFIED IDEOGRAPH-8BD5}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 29992 (\N{CJK UNIFIED IDEOGRAPH-7528}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 20363 (\N{CJK UNIFIED IDEOGRAPH-4F8B}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 20998 (\N{CJK UNIFIED IDEOGRAPH-5206}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 24067 (\N{CJK UNIFIED IDEOGRAPH-5E03}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 21151 (\N{CJK UNIFIED IDEOGRAPH-529F}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
/home/gavin/tools/automation/conftest.py:651: UserWarning: Glyph 33021 (\N{CJK UNIFIED IDEOGRAPH-80FD}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format="webp")  # 保存为webp格式
```


知道是字体的问题，这个问题一直没有去解决，今天又碰见了，决心解决它。



# 解决方案

## 方案1：安装字体并使用它

查阅了一些资料，需要安装字体，比如：

```shell
# 安装文泉驿字体
fonts-wqy-microhei

# 或者安装文泉驿正黑字体
fonts-wqy-zenhei
```

但是这些字体，在`github[https://github.com/anthonyfok/fonts-wqy-microhei]` 上只有`Debian`系的，没有`RedHat`系的，也使用了`yum`尝试安装，并没有搜索到相关包，只能放弃。


## 方案2： 抑制matplotlib告警

```python
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
```

此方法没有效果，因为我有在`conftest.py`文件的开头，设定了`matplotlib`的日志级别：`logging.getLogger('matplotlib').setLevel(logging.INFO)`，除非将日志级别设置为`logging.ERROR`，否则还是会有告警出现，放弃此思路。


## 方案3：使用系统自带的字体

先查看了系统自带了哪些字体：

```shell
>>> import matplotlib
>>> import matplotlib.pyplot as plt
>>> print(set([f.name for f in matplotlib.font_manager.fontManager.ttflist if 'Hei' in f.name]))
set()
>>>
>>> print(set([f.name for f in matplotlib.font_manager.fontManager.ttflist if 'CJK' in f.name]))
{'Noto Sans CJK JP', 'Noto Serif CJK JP'}
>>>
```

既然系统有自带，那就改一下代码思路，无需写死使用的字体（旧版代码如下）：

```python
def generate_cycle_chart(case_counts, feature_counts):    # pylint: disable=W0621
    """绘制饼图的主函数"""
    # 设置中文字体为黑体，防止中文显示乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置负号正常显示
    plt.rcParams['axes.unicode_minus'] = False

    # 定义颜色
    colors1 = plt.cm.Paired(range(len(case_counts)))  # pylint: disable=W0621
    colors2 = plt.cm.Paired(range(len(feature_counts)))  # pylint: disable=E1101

    # 创建图形和子图
    _, axs = plt.subplots(1, 2, figsize=(24, 12), subplot_kw=dict(aspect="equal"))  # pylint: disable=R1735

    # 绘制两个甜甜圈图
    plot_donut_chart(axs[0], case_counts, colors1, "测试用例分布")
    plot_donut_chart(axs[1], feature_counts, colors2, "功能用例分布")

    # 保存 image
    img_name = os.path.join(get_report_path(), "testcase_distribution.webp")
    plt.savefig(img_name, format="webp")  # 保存为webp格式
```

改为获取系统自带字体，并按照优先级使用，优化后的代码如下：

```python
def generate_cycle_chart(case_counts, feature_counts):    # pylint: disable=W0621
    """绘制饼图的主函数"""
    # 设置中文字体，防止中文显示乱码
    try:
        import matplotlib.font_manager as fm

        # 字体优先级列表
        font_priority_list = [
            'SimHei',           # 黑体 (Windows)
            'Microsoft YaHei',  # 微软雅黑 (Windows)
            'Noto Sans CJK JP', # 你系统中已有的字体
            'Noto Sans CJK SC', # 思源黑体
            'WenQuanYi Micro Hei', # 文泉驿微米黑 (Linux)
            'WenQuanYi Zen Hei',   # 文泉驿正黑 (Linux)
            'DejaVu Sans',      # 系统默认
            'Arial Unicode MS'  # macOS
        ]

        # 获取系统所有可用字体
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        print(f"系统可用字体: {available_fonts[:10]}...")  # 只打印前10个
        
        # 按优先级选择第一个可用的字体
        selected_font = None
        for font_name in font_priority_list:
            if font_name in available_fonts:
                selected_font = font_name
                print(f"选择字体: {selected_font}")
                break

        if selected_font:
            plt.rcParams['font.sans-serif'] = [selected_font, 'DejaVu Sans']
        else:
            # 如果没有找到优先级字体，使用系统第一个支持中文的字体
            cjk_fonts = [f.name for f in fm.fontManager.ttflist if any(x in f.name for x in ['CJK', 'Chinese', 'Hei', 'YaHei'])]
            if cjk_fonts:
                plt.rcParams['font.sans-serif'] = [cjk_fonts[0], 'DejaVu Sans']
                print(f"使用CJK字体: {cjk_fonts[0]}")
            else:
                print("警告: 未找到合适的中文字体，使用默认字体")

        plt.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        print(f"字体设置失败: {e}")
        # 回退到默认设置
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

    # 定义颜色
    colors1 = plt.cm.Paired(range(len(case_counts)))  # pylint: disable=W0621
    colors2 = plt.cm.Paired(range(len(feature_counts)))  # pylint: disable=E1101

    # 创建图形和子图
    _, axs = plt.subplots(1, 2, figsize=(24, 12), subplot_kw=dict(aspect="equal"))  # pylint: disable=R1735

    # 绘制两个甜甜圈图
    plot_donut_chart(axs[0], case_counts, colors1, "测试用例分布")
    plot_donut_chart(axs[1], feature_counts, colors2, "功能用例分布")

    # 保存 image
    img_name = os.path.join(get_report_path(), "testcase_distribution.webp")

    # 抑制保存时的警告
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            plt.savefig(img_name, format="webp", bbox_inches='tight', dpi=100)
        except Exception as save_error:
            print(f"保存图片失败: {save_error}")
            # 尝试其他格式
            try:
                plt.savefig(img_name.replace('.webp', '.png'), bbox_inches='tight', dpi=100)
                print("已保存为PNG格式")
            except:
                print("无法保存图片")

    plt.close()  # 关闭图形，释放内存
```

# 小结

使用了方案3，既解决了生成饼图告警问题，又增加了容错性，一举多得。


