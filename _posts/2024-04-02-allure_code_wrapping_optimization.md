---
layout:     post
title:      "Allure报告常见封装代码优化"
subtitle:   "Allure报告常见封装代码优化"
date:       2024-04-02 22:03:29
img: "/img/pytest/allure2.jpg"
author:     "Gavin Wang"
catalog:    true
summary: Allure报告常见封装之代码优化
categories:
    - [Automation]
    - [Allure]
tags:
    - Automation
    - Allure
---

# 概述

本文介绍Allure常见报告的封装，诸如allure的操作步骤、allure附件的上传。
有一份代码，尝试优化它，使之更pythonnic。


# 代码

文件AllureReportTools.py，封装了关于生成Allure报告的常见功能，内容如下所示：

```python
import allure

from typing import Any
from pathlib import Path

from json import dumps as json_dumps
from allure_commons.types import AttachmentType


def get_file_property(filepath: str) -> tuple[str, str, str]:
    """
    获取文件属性

    :param filepath:
    :return:
    """
    file = Path(filepath)
    filename = file.name
    file_root_name = file.stem
    filetype = file.suffix[1:]
    return filename, file_root_name, filetype


def allure_step(step: str, var: str | dict) -> None:
    """
    allure 操作步骤

    :param step: 操作步骤
    :param var: 操作步骤中的变量
    :return:
    """
    with allure.step(step):
        allure.attach(
            body=json_dumps(var, ensure_ascii=False, indent=2) if isinstance(var, dict) else var,
            name='JSON Serialize',
            attachment_type=AttachmentType.JSON,
        )


def allure_attach(
    body: Any = None, name: str | None = None, attachment_type: str = 'JSON', extension: Any = None
) -> None:
    """
    allure 报告上传附件

    :param body: 显示的内容
    :param name: 附件名称
    :param attachment_type: 文件类型，默认 JSON
    :param extension:
    :return:
    """
    allure.attach(
        body=body,
        name=name,
        attachment_type=getattr(AttachmentType, attachment_type.upper(), None),
        extension=extension,
    )


def allure_attach_file(filepath: str, name: str | None = None, extension: Any = None) -> None:
    """
    allure 报告上传附件

    :param filepath: 文件路径
    :param name:
    :param extension:
    :return:
    """
    file_property = get_file_property(filepath)
    filename = file_property[0]
    filetype = file_property[2]
    if filetype == 'txt':
        filetype = 'TEXT'
    elif filetype == 'uri':
        filetype = 'URI_LIST'
    allure.attach.file(
        source=filepath,
        name=name or filename,
        attachment_type=getattr(AttachmentType, filetype.upper(), None),
        extension=extension,
    )
```


# 优化

## 代码优化点

* 使用Python的类型注释来提升代码可读性。
* 使用pathlib库简化文件操作，避免手动字符串拼接路径。
* 更合理的函数和变量命名，提升代码可读性。
* 使用枚举值，避免硬编码文件类型。
* 精简allure_attach和allure_attach_file方法，提高其可用性。

## 优化后代码示例

```python
import allure
import json

from typing import Any
from pathlib import Path
from allure_commons.types import AttachmentType


def get_file_properties(filepath: Path) -> tuple[str, str, str]:
    """
    Obtain properties of the file.
    """
    return filepath.name, filepath.stem, filepath.suffix.lstrip('.')


def serialize_var(var: Any) -> str:
    """
    Serialize variable to a formatted string.
    """
    return json.dumps(var, ensure_ascii=False, indent=2) if isinstance(var, dict) else str(var)


@allure.step('{step}')
def report_step(step: str, var: Any) -> None:
    """
    Record an action step in Allure with its variable.
    """
    allure.attach.body(
        body=serialize_var(var),
        name='json_serialize',
        attachment_type=AttachmentType.JSON,
    )


def attach_to_report(body: Any, name: str = 'attachment', attachment_type: AttachmentType = AttachmentType.JSON) -> None:
    """
    Attach a content to Allure report.
    """
    allure.attach(
        body=body,
        name=name,
        attachment_type=attachment_type
    )


def attach_file_to_report(filepath: Path, name: str | None = None) -> None:
    """
    Attach a file to Allure report.
    """
    name = name or filepath.name
    _, _, file_type = get_file_properties(filepath)
    attach_type = AttachmentType.TEXT if file_type == 'txt' else getattr(AttachmentType, file_type.upper(), AttachmentType.JSON)

    allure.attach.file(
        source=str(filepath),
        name=name,
        attachment_type=attach_type
    )
```

在此代码中，每个函数都精确地完成一个单一任务，符合函数编程的原则。
代码的可读性和可用性有所提高，附加的命名约定和类型注释有助于未来代码的维护和理解。
总之，更pythonnic。
