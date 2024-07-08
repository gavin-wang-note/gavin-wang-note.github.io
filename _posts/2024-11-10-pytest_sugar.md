---
title: 测试用例进度显示插件pytest-sugar源码解读
date: 2024-11-10 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 测试用例进度显示插件pytest-sugar源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-sugar` 是一个用于美化 `pytest` 命令行输出的插件，它显示一个更好的进度条和有趣的提示信息。

使用此插件后（一旦安装，默认自动使用此插件），执行用例效果参考如下图所示：

<img class="shadow" src="/img/in-post/pytest-sugar_result.png" width="1200">

下文是关于 `pytest-sugar` 相关测试代码详细解析。


# 导入和插件定义

```python
import re
import pytest
from pytest_sugar import strip_colors

pytest_plugins = "pytester"
```

- **`re`**：导入正则表达式模块，用于在文本中搜索模式。
- **`pytest`**：导入 `pytest`，作为测试框架。
- **`strip_colors`**：从 `pytest_sugar` 中导入 `strip_colors` 函数，用于移除带颜色的输出。
- **`pytest_plugins = "pytester"`**：启用 `pytest` 内置的 `pytester` 插件，以便在测试中使用 `testdir fixture`。

# 获取测试报告中的计数

```python
def get_counts(stdout):
    output = strip_colors(stdout)

    def _get(x):
        m = re.search(r"\d %s" % x, output)
        if m:
            return m.group()[0]
        return "n/a"

    return {
        x: _get(x)
        for x in (
            "passed",
            "xpassed",
            "failed",
            "xfailed",
            "deselected",
            "error",
            "rerun",
            "skipped",
        )
    }
```

- **`get_counts(stdout)`**：这个函数从测试报告输出中获取所有测试的计数。
  - **`output = strip_colors(stdout)`**：移除输出中的颜色。
  - **`_get(x)`**：内部函数，使用正则表达式搜索测试计数。返回找到的第一个匹配项或 `'n/a'`。
  - **返回的字典**：包含所有测试状态及其对应的计数。

# 断言测试计数

```python
def assert_count(testdir, *args):
    """Assert that n passed, n failed, ... matches"""
    without_plugin = testdir.runpytest("-p", "no:sugar", *args).stdout.str()
    with_plugin = testdir.runpytest("--force-sugar", *args).stdout.str()

    count_without = get_counts(without_plugin)
    count_with = get_counts(with_plugin)

    assert count_without == count_with, (
        "When running test with and without plugin, "
        "the resulting output differs.\n\n"
        "Without plugin: %s\n"
        "With plugin: %s\n"
        % (
            ", ".join(f"{v} {k}" for k, v in count_without.items()),
            ", ".join(f"{v} {k}" for k, v in count_with.items()),
        )
    )
```

- **`assert_count(testdir, *args)`**：运行测试并断言结果在启用和禁用 `pytest-sugar` 插件时是否一致。
  - **`testdir.runpytest`**：运行 `pytest`。
  - **`get_counts()`**：获取测试状态计数。
  - **`assert count_without == count_with`**：断言结果一致。如果不一致，打印详细信息。

# 测试类TestTerminalReporter

以下是一个 `TestTerminalReporter` 测试类，包含多个测试方法，每个方法都有相应的注释解释。

```python
class TestTerminalReporter:
    def test_new_summary(self, testdir):
        # 创建一个简单的测试文件
        testdir.makepyfile(
            """
            import pytest

            def test_sample():
                assert False
            """
        )
        # 运行pytest并捕捉输出
        output = testdir.runpytest("--force-sugar").stdout.str()
        assert "test_new_summary.py:3 test_sample" in strip_colors(output)

    def test_old_summary(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            def test_sample():
                assert False
            """
        )
        output = testdir.runpytest("--force-sugar", "--old-summary").stdout.str()
        assert "test_old_summary.py:4: assert False" in strip_colors(output)

    def test_xfail_true(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xfail
            def test_sample():
                assert True
            """
        )
        assert_count(testdir)

    def test_xfail_false(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xfail
            def test_sample():
                assert False
            """
        )
        assert_count(testdir)

    def test_report_header(self, testdir):
        testdir.makeconftest(
            """
            def pytest_report_header(startdir):
                pass
            """
        )
        testdir.makepyfile(
            """
            def test():
                pass
            """
        )
        result = testdir.runpytest("--force-sugar")
        assert result.ret == 0, result.stderr.str()

    def test_xfail_strict_true(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xfail(strict=True)
            def test_sample():
                assert True
            """
        )
        assert_count(testdir)

    def test_xfail_strict_false(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xfail(strict=True)
            def test_sample():
                assert False
            """
        )
        assert_count(testdir)

    def test_xpass_true(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xpass
            def test_sample():
                assert True
            """
        )
        assert_count(testdir)

    def test_xpass_false(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xpass
            def test_sample():
                assert False
            """
        )
        assert_count(testdir)

    def test_flaky_test(self, testdir):
        pytest.importorskip("pytest_rerunfailures")
        testdir.makepyfile(
            """
            import pytest

            COUNT = 0

            @pytest.mark.flaky(reruns=10)
            def test_flaky_test():
                global COUNT
                COUNT += 1
                assert COUNT >= 7
            """
        )
        assert_count(testdir)

    def test_xpass_strict(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.xfail(strict=True)
            def test_xpass():
                assert True
            """
        )
        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            [
                "*test_xpass*",
                "*XPASS(strict)*",
                "*1 failed*",
            ]
        )

    def test_teardown_errors(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            @pytest.yield_fixture
            def fixt():
                yield
                raise Exception

            def test_foo(fixt):
                pass
            """
        )
        assert_count(testdir)

        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            ["*ERROR at teardown of test_foo*", "*1 passed*", "*1 error*"]
        )

    def test_skipping_tests(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            @pytest.mark.skipif(True, reason='This must be skipped.')
            def test_skip_this_if():
                assert True
            """
        )
        assert_count(testdir)

    def test_deselecting_tests(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            @pytest.mark.example
            def test_func():
                assert True

            def test_should_be():
                assert False
            """
        )
        assert_count(testdir)

    def test_item_count_after_pytest_collection_modifyitems(self, testdir):
        testdir.makeconftest(
            """
            import pytest

            @pytest.hookimpl(hookwrapper=True, tryfirst=True)
            def pytest_collection_modifyitems(config, items):
                yield
                items[:] = [x for x in items if x.name == 'test_one']
            """
        )
        testdir.makepyfile(
            """
            def test_one():
                print('test_one_passed')

            def test_ignored():
                assert 0
            """
        )
        result = testdir.runpytest("-s")
        result.stdout.fnmatch_lines(
            [
                "*test_one_passed*",
                "*100%*",
            ]
        )
        assert result.ret == 0

    def test_fail(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            def test_func():
                assert 0
            """
        )
        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            [
                "* test_func *",
                "    def test_func():",
                ">       assert 0",
                "E       assert 0",
            ]
        )
```

## test_fail_unicode_crashline

```python
    def test_fail_unicode_crashline(self, testdir):
        testdir.makepyfile(
            """
            # -*- coding: utf-8 -*-
            import pytest
            def test_func():
                assert b'hello' == b'Bj\\xc3\\xb6rk Gu\\xc3\\xb0mundsd'
            """
        )
        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            [
                "* test_func *",
                "    def test_func():",
                ">       assert * == *",
                "E       AssertionError: assert * == *",
            ]
        )
```
这个测试方法:
- 创建一个包含 `Unicode` 字符的测试文件，确保测试插件可以正确处理 `Unicode` 断言错误。
- 运行测试并检查输出是否包含预期的诊断信息。

## test_fail_in_fixture_and_test

```python
    def test_fail_in_fixture_and_test(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            def test_func():
                assert False

            def test_func2():
                assert False

            @pytest.fixture
            def failure():
                return 3/0

            def test_lol(failure):
                assert True
            """
        )
        assert_count(testdir)
        output = strip_colors(testdir.runpytest("--force-sugar").stdout.str())
        assert output.count("         -") == 2
```
这个测试方法:
- 创建一个含有多个故障测试和一个故障装置的测试文件。
- 使用 `assert_count` 检查测试结果。
- 移除颜色后检查输出中是否有两个破折号，用于标示错误位置。

## test_fail_fail

```python
    def test_fail_fail(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            def test_func():
                assert 0
            def test_func2():
                assert 0
            """
        )
        assert_count(testdir)
        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            [
                "* test_func *",
                "    def test_func():",
                ">       assert 0",
                "E       assert 0",
                "* test_func2 *",
                "    def test_func2():",
                ">       assert 0",
                "E       assert 0",
            ]
        )
```
这个测试方法:
- 创建两个都会失败的测试函数。
- 检查在启用和禁用 `pytest-sugar` 插件时，测试结果是否一致。
- 确认输出中显示的错误信息和断言失败。

## test_error_in_setup_then_pass

```python
    def test_error_in_setup_then_pass(self, testdir):
        testdir.makepyfile(
            """
            def setup_function(function):
                print ("setup func")
                if function is test_nada:
                    assert 0
            def test_nada():
                pass
            def test_zip():
                pass
            """
        )
        assert_count(testdir)
        result = testdir.runpytest("--force-sugar")

        result.stdout.fnmatch_lines(
            [
                "*ERROR at setup of test_nada*",
                "",
                "function = <function test_nada at *",
                "",
                "*setup_function(function):*",
                "*setup func*",
                "*if function is test_nada:*",
                "*assert 0*",
                "test_error_in_setup_then_pass.py:4: AssertionError",
                "*Captured stdout setup*",
                "*setup func*",
                "*1 passed*",
            ]
        )
        assert result.ret != 0
```
这个测试方法:
- 创建一个在 `setup` 阶段会失败的测试文件，确保 `pytest-sugar` 可以处理 `setup` 错误。
- 检查结果输出中的错误信息，包括 `setup` 函数和 `assert` 语句的位置。

## test_error_in_teardown_then_pass

```python
    def test_error_in_teardown_then_pass(self, testdir):
        testdir.makepyfile(
            """
            def teardown_function(function):
                print ("teardown func")
                if function is test_nada:
                    assert 0
            def test_nada():
                pass
            def test_zip():
                pass
            """
        )
        assert_count(testdir)
        result = testdir.runpytest("--force-sugar")

        result.stdout.fnmatch_lines(
            [
                "*ERROR at teardown of test_nada*",
                "",
                "function = <function test_nada at*",
                "",
                "*def teardown_function(function):*",
                "*teardown func*",
                "*if function is test_nada*",
                ">*assert 0*",
                "E*assert 0*",
                "test_error_in_teardown_then_pass.py:4: AssertionError",
                "*Captured stdout teardown*",
                "teardown func",
                "*2 passed*",
            ]
        )
        assert result.ret != 0
```
这个测试方法:
- 创建一个在 `teardown` 阶段会失败的测试文件，确保 `pytest-sugar` 可以处理 `teardown` 错误。
- 检查结果输出中的错误信息，包括 `teardown` 函数和 `assert` 语句的位置。

## test_collect_error

```python
    def test_collect_error(self, testdir):
        testdir.makepyfile("""raise ValueError(0)""")
        assert_count(testdir)
        result = testdir.runpytest("--force-sugar")
        result.stdout.fnmatch_lines(
            [
                "*ERROR collecting test_collect_error.py*",
                "test_collect_error.py:1: in <module>",
                "    raise ValueError(0)",
                "E   ValueError: 0",
            ]
        )
```
这个测试方法:
- 创建一个在导入时就会引发 `ValueError` 异常的测试文件。
- 检查 `pytest-sugar` 是否正确处理收集阶段的错误，并确保错误信息被正确打印。

## test_verbose

```python
    def test_verbose(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            def test_true():
                assert True

            def test_true2():
                assert True

            def test_false():
                assert False

            @pytest.mark.skip
            def test_skip():
                assert False

            @pytest.mark.xpass
            def test_xpass():
                assert True

            @pytest.mark.xfail
            def test_xfail():
                assert True
            """
        )
        assert_count(testdir, "--verbose")
```
这个测试方法:
- 创建一个包含多种不同状态的测试文件，通过 `--verbose` 选项运行 `pytest`，确保 `pytest-sugar` 可以处理详细输出。
- 检查测试结果在启用和禁用 `pytest-sugar` 时是否一致。

## test_verbose_has_double_colon

```python
    def test_verbose_has_double_colon(self, testdir):
        testdir.makepyfile(
            """
            def test_true():
                assert True
            """
        )
        output = testdir.runpytest("--force-sugar", "--verbose").stdout.str()
        assert "test_verbose_has_double_colon.py::test_true" in strip_colors(output)
```
这个测试方法:
- 创建一个简单的测试文件，并运行 `pytest`，确保在启用 `pytest-sugar` 的情况下能够正确处理和显示带双冒号的测试名称。

## test_xdist

```python
    def test_xdist(self, testdir):
        pytest.importorskip("xdist")
        testdir.makepyfile(
            """
            def test_nada():
                pass
            def test_zip():
                pass
            """
        )
        result = testdir.runpytest("--force-sugar", "-n2")

        assert result.ret == 0, result.stderr.str()
```
这个测试方法:
- 检查 `pytest-sugar` 和 `pytest-xdist` 插件的兼容性。
- 创建简单的测试文件，通过 `-n2` 选项并行运行测试，确保测试在并行环境中正常运行。

## test_xdist_verbose

```python
    def test_xdist_verbose(self, testdir):
        pytest.importorskip("xdist")
        testdir.makepyfile(
            """
            def test_nada():
                pass
            def test_zip():
                pass
            """
        )
        result = testdir.runpytest("--force-sugar", "-n2", "-v")

        assert result.ret == 0, result.stderr.str()
```
这个测试方法:
- 对前一个测试方法稍作修改，启用详细输出以确保详细信息在并行环境中被正确显示。

## test_doctest

```python
    def test_doctest(self, testdir):
        """Test doctest-modules"""
        testdir.makepyfile(
            """
            class ToTest():
                @property
                def doctest(self):
                    \"\"\"
                        >>> Invalid doctest
                    \"\"\"
            """
        )
        result = testdir.runpytest("--force-sugar", "--doctest-modules")
        assert result.ret == 1, result.stderr.str()
```
这个测试方法:
- 创建包含无效 `doctest` 的测试文件，确保 `pytest-sugar` 能够处理 `doctest` 模块并显示相关的错误信息。
- 运行测试并断言返回码为 1（表示测试失败）。


## test_doctest_lineno

```python
    def test_doctest_lineno(self, testdir):
        """Test location reported for doctest-modules"""
        testdir.makepyfile(
            """
            def foobar():
                '''
                >>> foobar()
                '''
                raise NotImplementedError
            """
        )
        result = testdir.runpytest("--force-sugar", "--doctest-modules")
        assert result.ret == 1, result.stderr.str()
        result.stdout.fnmatch_lines(
            [
                "UNEXPECTED EXCEPTION: NotImplementedError()",
                "*test_doctest_lineno.py:3: UnexpectedException",
                "Results*:",
                "*-*test_doctest_lineno.py*:3*",
            ]
        )
```
这个测试方法:
- 创建一个包含无效 `doctest` 的测试文件，并在测试中引发 `NotImplementedError` 异常。
- 运行测试并断言返回码为 1。
- 检查输出中是否正确显示了错误位置，包括文件名和行号。

# 操作步骤及验证

这些测试方法主要是为了确保 `pytest-sugar` 能够正确处理各种测试状态和错误，并在输出中提供有益的信息。以下是如何操作和确保 `pytest-sugar` 正常工作的操作步骤及验证方法：

1. **环境要求**：
   - 安装 `pytest`。
   - 安装 `pytest-sugar`。
   - 如果需要并发测试，安装 `pytest-xdist`。
   - 如果需要测试重试功能，安装 `pytest-rerunfailures`。

2. **运行测试**：
   - 将 `test_example.py` 文件保存为 `parent.py` 和 `child.py`。
   - 在终端中运行以下命令执行测试：
     ```shell
     pytest test_example.py
     ```

3. **检查输出**：
   - 确认输出中没有报错，所有测试用例都正确执行。
   - 检查是否显示了进度条和其他美化的输出。

# 总结

`pytest-sugar` 通过提供更好的输出格式和进度条等功能，帮助开发者在运行测试时更容易理解测试进度和结果。然而，在丰富的功能之后，确保插件与 `pytest` 和其他插件的兼容性至关重要。这份测试代码通过广泛的测试用例来验证 `pytest-sugar` 的功能和健壮性。

这些测试验证了 `pytest-sugar` 在以下方面的行为：
- 不同测试通过、失败、跳过和预期失败（`xfail`）的情况处理。
- 测试结果的总结及输出格式验证。
- 插件与 `pytest-xdist` 并行化插件的兼容性。
- 处理 `doctest` 并显示具体行号错误位置。
