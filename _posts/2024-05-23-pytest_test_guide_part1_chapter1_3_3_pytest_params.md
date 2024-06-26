---
title: 《pytest测试指南》-- 章节1-3 pytest参数详解PART3
date: 2024-05-23 20:39:15
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-3 pytest参数详解PART3
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

[续上文](https://gavin-wang-note.github.io/2024/05/22/pytest_test_guide_part1_chapter1_3_2_pytest_params/)

## 3.2.4 pytest-warnings 相关参数


### 3.2.4.1 参数 -W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS

`pytest` 中的 `-W PYTHONWARNINGS` 或 `--pythonwarnings=PYTHONWARNINGS` 选项允许你指定如何处理 Python 的警告。这些选项的使用与 Python 标准库中的 `warnings` 模块的行为类似。你可以通过这个 `pytest` 选项来控制警告的显示，比如忽略某些类型的警告，或者将它们转换成错误。

**使用方法：**

`PYTHONWARNINGS` 是一个逗号分隔的字符串，用来定义如何处理特定的警告。它可以包括几个动作（action）:

- `ignore`：忽略某些警告。
- `error`：将某些警告转化为错误。
- `always`：总是打印出某些警告，忽略其他警告过滤器。
- `default`：打印每个警告的第一次出现。
- `module`：打印每个模块里警告的第一次出现。
- `once`：只打印警告的第一次出现。

这些动作可以被用来过滤特定的警告类型。例如：

```shell
pytest -W ignore::UserWarning
```

这个命令将会忽略所有的 `UserWarning` 类型警告。

如果你想把某个特定警告转换成错误，可以使用：

```shell
pytest -W error::RuntimeWarning
```

这样做会将所有 `RuntimeWarning` 类型警告当作错误来处理。

你还可以组合这些过滤器，例如：

```shell
pytest -W ignore::UserWarning -W error::RuntimeWarning
```

这将忽略 `UserWarning` 警告，并把 `RuntimeWarning` 警告当作错误。

**请注意**：

该选项影响测试的执行，因为它可以导致原本只会发出警告的情况变为引发测试错误的情况。因此，通过适当地配置这个选项，可以帮助开发者在持续集成流程中提前识别潜在的问题，并促使他们修正可能的不佳的编程实践或即将弃用的功能的使用。




### 3.2.4.2 参数  --maxfail=num

`pytest` 的 `--maxfail=num` 选项允许你设置在达到一定数量的失败测试用例后立即停止测试会话。参数 `num` 代表最大失败测试用例的数量。这是一个非常实用的功能，可以让你在大型测试套件中，当遇到多个失败测试时快速地得到反馈，而不需要等待整个测试套件运行完毕。

**使用方法：**

当你想要运行 `pytest` 测试，并在失败数达到某个值时停止测试，可以使用如下方式：

```shell
pytest --maxfail=2
```

这个例子中，`--maxfail=2` 表明一旦有2个测试失败，`pytest` 将停止执行剩下的测试。

这对于快速识别和解决常见的问题特别有用。例如，在开发新功能时，可能会引入一些导致多个测试失败的问题。使用 `--maxfail` 选项可以帮助你快速发现和定位这些问题，节省时间。

此外，该选项也常用于持续集成（CI）环境中。在CI中，如果很早就知道测试会失败，没有必要继续运行剩下的测试。这样可以早点释放CI资源，供其他开发者使用。

**请注意：**

`--maxfail` 后面的数字必须是一个正整数，表示最大失败数。如果设置为 `0` 或者不提供该选项，那么 `pytest` 将会运行所有的测试用例，无论有多少失败。



### 3.2.4.3 参数 --strict-config

`pytest` 的 `--strict-config` 选项是一个在测试过程中用于强化配置文件检查的选项。开启该选项后，在处理 `pytest` 配置文件（诸如 `pytest.ini`, `tox.ini`, `pyproject.toml`, `setup.cfg` 等）时，`pytest` 将会更加严格地进行检查。如果存在任何不被识别的设置项，`pytest` 将会抛出错误并终止测试过程。

这个选项在确保测试配置的准确性方面非常有用，避免了可能由于配置文件中的拼写错误或其他不一致导致的微妙 bugs。

**使用方法：**

当你想要运行 `pytest` 并确保配置文件中没有任何无法识别的配置项时，可以在命令行中包含该选项：

```shell
pytest --strict-config
```

如果你的配置文件中所有的配置项都是 `pytest` 可以识别的，测试将会像往常一样运行。但如果存在任何 `pytest` 不认识的配置项名，测试将会终止，并给出错误消息，指出不被识别的配置项。

这提高了配置文件的标准，帮助、确保开发者不会意外地添加无效的配置，从而避免后期难以发现的错误。当你维护一个大型项目或在团队中合作时，使用 `--strict-config` 能够帮助维持配置文件的质量和一致性。




### 3.2.4.4 参数 --strict-markers

`pytest` 的 `--strict-markers` 选项用于确保测试中使用的所有标记（markers）都经过预定义。这意味着如果你的测试用例使用了未经注册的标记，开启 `--strict-markers` 选项后，`pytest` 将会抛出错误并终止测试。

在 `pytest` 中，标记可以用来给测试用例添加元数据，例如 `@pytest.mark.slow` 可以标记运行缓慢的测试。但是，有时候开发者可能会错误地使用未定义的标记，这可能会导致混淆和错误的测试行为。

**使用方法：**

当你想要运行 `pytest` 并确保所有使用的标记都已预定义时，可以在命令行中添加这个选项：

```shell
pytest --strict-markers
```

现在，如果你运行 `pytest` 并且其中一个测试用例使用了像 `@pytest.mark.someundefinedmarker` 这样的未注册标记，测试会因为错误而停止，并提示有关该未定义标记的信息。

这个选项在确保标记的正确使用以及避免拼写错误时非常有用。尤其是在团队协作和大项目中，由于有多人参与编写测试，使用 `--strict-markers` 选项可以帮助维持清晰的标记使用协议。

要预定义一个标记，你可以在 `pytest` 配置文件中的 `[pytest]` 部分添加 `markers` 选项，并列出你想要使用的标记。例如，在 `pytest.ini` 文件中预定义 `slow` 和 `serial` 标记：

```ini
[pytest]
markers =
  slow: mark tests as slow to run
  serial: mark tests that should be run serially
```

使用 `--strict-markers` 有助于避免测试运行时由于打字错误或忘记预定义标记而潜在引入的问题。




### 3.2.4.5 参数 --strict

在较早版本的 `pytest` 中，`--strict` 选项用于确保测试不会使用任何未注册的标记（markers）。若使用了未注册的标记，`pytest` 会抛出错误并终止测试。这有助于防止拼写错误和遗漏在配置文件中注册标记。

然而，随着 `pytest` 的发展，这个选项已经被废弃掉，功能等价于 ` --strict-markers`。




### 3.2.4.6 参数 -c FILE, --config-file=FILE

`pytest` 命令行工具提供 `-c FILE` 或 `--config-file=FILE` 参数，允许你指定自定义的配置文件（如 `pytest.ini`、`tox.ini` 或 `setup.cfg`）来运行测试，而不是使用项目目录中的默认配置文件。

这个选项非常有用，特别是当你在不同的环境中运行测试或需要对测试执行不同的配置时。比如，开发和生产环境可能需要不同的配置，或者你可能想要对一组特定的测试用例使用特定的配置。

**使用方法：**

```shell
pytest -c custom_pytest.ini
```

或者：

```shell
pytest --config-file=custom_pytest.ini
```

这里 `custom_pytest.ini` 是你自定义的配置文件的文件名。

在这个自定义的配置文件中，你可以设置与默认 `pytest.ini` 文件相同的 `pytest` 配置选项，包括但不限于：

- `markers`：预定义的测试标记。
- `testpaths`：指定测试搜索的路径。
- `addopts`：提供额外命令行参数。
- `filterwarnings`：自定义警告过滤规则。

**请注意：**

指定 `-c` 或 `--config-file` 选项后，仅该指定的配置文件会被加载，`pytest` 不会自动加载项目中的其他配置文件，所以确保指定的文件包含了运行测试所需的所有配置信息。

使用 `-c` 指定自定义配置文件的功能为测试提供了更大的灵活性，它允许开发者在不同场景下调整测试设置，而无需更改项目中的主配置文件。




### 3.2.4.7 参数 --continue-on-collection-errors

在 `pytest` 中，`--continue-on-collection-errors` 选项允许测试执行在遇到收集阶段的错误时继续运行，而不是如默认行为那样立即停止。收集阶段是 `pytest` 总体测试执行流程中的第一步，其任务是找到所有应该执行的测试用例。

通常，如果在收集测试用例时发生错误（比如因为一个测试文件的代码有语法错误），`pytest` 会停止所有操作并立即返回错误。这可能不利于一些情况，特别是当你想要查看所有存在问题的测试收集项，而不是在首个问题出现时就停止。

使用 `--continue-on-collection-errors` 选项的命令行示例如下：

```shell
pytest --continue-on-collection-errors
```

当你使用这个选项时，即使在收集阶段出现了错误，`pytest` 也会继续收集下一个测试用例并尝试执行那些能够成功收集到的测试用例。在所有测试都尝试运行之后，`pytest` 仍然会将结果标记为失败，并且在输出中提供收集错误的详细信息。

这个选项对于调试和快速识别项目中所有存在的潜在集合问题特别有用。这确保了开发者在一次测试执行中就能发现全部问题，而不是修复一个再来一次只为了发现另一个问题。然而，在持续集成（CI）环境中，如果你希望在任何收集错误出现时立即停止构建过程，则不应该使用此选项。



### 3.2.4.8 参数 --rootdir=ROOTDIR

`pytest` 命令行工具提供了 `--rootdir=ROOTDIR` 参数，该参数允许你显式指定项目的根目录，而不是让 `pytest` 自动尝试发现它。项目的根目录是 `pytest` 用来查找和存储所有相关配置文件（如 `pytest.ini`、`tox.ini` 、`pyproject.toml`、`tox.ini`或 `setup.cfg`）以及测试文件和目录的位置。

默认情况下，`pytest` 会自动从当前工作目录开始，向上递归搜索包含 `pytest.ini`、`pyproject.toml`、`tox.ini`、`setup.cfg` 或 `setup.py` 等文件的文件夹，将第一个符合条件的文件夹视为项目根目录。但是，在某些复杂的项目结构中，自动检测可能不准确，或者你可能希望将测试结果限制在特定子目录下。在这些场景中，可以使用 `--rootdir` 参数来手动设置根目录。

**使用方法：**

```shell
pytest --rootdir=/path/to/rootdir
```

其中 `/path/to/rootdir` 应该被替换为你希望作为 `pytest` 根目录的路径。

通过设置根目录，你能够控制以下方面：

* **测试发现**：`pytest` 只会在指定的根目录下查找测试用例。
* **配置文件应用**：仅使用位于指定根目录中的配置文件。
* **测试相关路径**：所有文件、目录和包都相对于指定的根目录解析。

这个选项对于控制在特定环境下的 `pytest` 行为特别有帮助，或者当你要在一个较大项目中针对特定部分运行测试时。使用 `--rootdir` 可以确保 `pytest` 的运行环境与预期的一致，避免因自动探测的不准确而可能导致的问题。



## 3.2.5 collection 相关参数


### 3.2.5.1 参数 --collect-only, --co

`pytest` 的 `--collect-only`（简写为 `--co`）选项是用于收集所有可用测试而不执行它们（俗称dry run）。在某些情况下，你可能只想查看有哪些测试用例可以被运行，而不想实际执行它们。这可以帮助你了解测试范围，调试收集阶段的问题，或者为更具体的测试运行做准备。

执行带有 `--collect-only` 选项的 `pytest` 命令，`pytest` 会进入收集模式，列出所有找到的测试用例，但不实际运行它们。

**使用方法：**

```shell
pytest --collect-only
# 或者使用简写方式
pytest -co
```

以下是使用这个选项可能出现的一些场景：

* **预览测试用例**：当你有数百甚至数千个测试用例时，你可以使用此选项快速查看这些用例，而无需等待所有测试运行完成。
* **测试结构更改**：在重构测试代码结构或添加新测试时，此选项可以帮助你验证是否所有预期的测试都被 `pytest` 正确识别了。
* **集成到开发流程**：在持续集成/持续部署 (CI/CD) 流程中，你可以使用此选项快速检查测试集合，然后根据需要决定是否进行下一步行动。

还有一种情况就是，你想确认某些用 `-k` 选项指定的测试将正确匹配和收集，这时使用 `--collect-only` 和 `-k` 结合可以帮助确认这一点：

```shell
pytest -co -k "some_keyword"
```

使用这个命令，`pytest` 仅会列出那些匹配特定关键字的测试用例，而不会运行它们。

在执行了 `--collect-only` 之后，`pytest` 会显示它找到的所有测试用例，通常包括测试文件的路径、测试类的名字（如果有的话）以及测试函数的名字。这些信息将以一种结构化且易于阅读的格式输出到控制台。




### 3.2.5.2 参数 --pyargs

`pytest` 的 `--pyargs` 选项允许用户使用 Python 模块导入路径来指定要测试的包，而不是文件系统路径。这意味着实际上你可以在安装了包的任何地方运行测试，而不需要知道它在文件系统中的位置。

通常，`pytest` 测试是根据文件系统中的位置来运行的，但是如果你想要测试一个已经安装到你的 Python 环境中（例如通过 `pip install`）的包，`--pyargs` 选项会非常有用。

**使用方法：**

```shell
pytest --pyargs my_package
```

在这个例子中，`my_package` 需要被替换为你想要测试的安装包的名称。`pytest` 会从你的 Python 环境中导入该包，并运行该包中所有的测试。这种方式跟运行本地开发代码的测试是分开的，适合用于测试已经被打包和安装的包。

使用 `--pyargs` 的一些常见用例包括：

* **测试本地未开发的包**：如果你工作在一个大型项目上，并只是想要运行安装的版本的测试，不想运行开发中的代码测试。

* **在复杂的环境中运行测试**：如果你在一个复杂的环境中，例如在一个大型的应用中运行 `pytest`，并且不一定知道所有相关包的文件系统位置。

* **持续集成 (CI) 流程**：当构建和测试过程在隔离环境中执行时，可能需要测试已被打包和安装的库版本。

`--pyargs` 选项也可以与其他 `pytest` 选项结合使用，如 `-k` 来运行匹配某个特定模式的测试，或是 `-m` 来运行带有特定标记的测试。

不过，当使用 `--pyargs` 时，重要的是确保所指定的包在当前的 Python 环境中是可导入的，即它已经被安装。如果 `pytest` 不能导入指定的包，它将抛出一个错误。




### 3.2.5.3 参数 --ignore=path

在使用 `pytest` 进行测试时，有时你可能需要从测试过程中排除掉某些特定的文件或目录。这是 `--ignore=path` 选项的用途，它可以指示 `pytest` 忽略给定路径的文件或目录。

当你在 `pytest` 中使用 `--ignore` 参数时，示例如下：

```shell
pytest --ignore=some_directory
```

此命令将指导 `pytest` 忽略名为 `some_directory` 的目录中的所有文件，这意味着该目录下的任何测试都不会被收集或执行。

你也可以使用文件路径作为参数：

```shell
pytest --ignore=some_directory/test_file.py
```

在这个例子中，`pytest` 将会忽略 `some_directory/test_file.py` 文件，即使它包含可执行的测试。

`--ignore` 参数的通用用法：

* **将特定目录排除在测试之外**：当你有一些测试目录并不想在特定情况下运行时，比如示例代码或者是正在进行的实验性代码或者是`.git/.svn`之类的commit记录信息目录。

* **单个文件排除**：如果你想要忽略特定的文件，就像前面示例中的那样，指定具体文件路径。

* **多个忽略路径**：可以通过在命令行上添加多个 `--ignore` 选项来指定多个忽略路径。

```shell
pytest --ignore=some_directory --ignore=other_directory
```

* **与其他选项配对**：可以将 `--ignore` 与其他 `pytest` 命令行选项（如 `-k` 或 `-m`）一起使用来定制测试的运行方式。

**请注意：**

使用 `--ignore` 可能需要精确的路径信息，如果有多个同名目录或文件，你应确保提供正确的路径以避免测试错过。

最后，当你需要忽略多个目录或文件时，也可以在 `pytest.ini`、`tox.ini` 或 `pyproject.toml` 文件中使用 `norecursedirs` 和 `testpaths` 配置选项来实现更灵活的配置。



### 3.2.5.4 参数 --ignore-glob=path

`pytest` 的 `--ignore-glob` 选项用于排除匹配特定全局模式（glob pattern）的文件和目录。相对于 `--ignore` 选项，`--ignore-glob` 提供了通配符匹配的能力，让你可以更灵活地定义哪些文件和目录应该被忽略。

**示例**：

```shell
pytest --ignore-glob='*temporary*'
```

在这个例子中，任何包含单词 "temporary" 的文件和目录都将被忽略。假设你有几个临时测试文件，它们的文件名中都含有 "temporary"，这个选项就允许你一次性排除它们，而不是挨个指定。

`--ignore-glob` 语法规则遵循传统的shell glob模式匹配，支持如下模式：

- `*` 匹配任意数量的任意字符（包括零个字符）。
- `?` 匹配任意单个字符。
- `[seq]` 匹配 `seq` 中任意字符（字符类）。
- `[!seq]` 匹配不在 `seq` 中的任意字符（否定字符类）。

举几个例子：

- 忽略所有 `.tmp` 后缀的文件：

```shell
pytest --ignore-glob='*.tmp'
```

- 忽略所有以 `temp_` 开头的目录：

```shell
pytest --ignore-glob='temp_*'
```

- 忽略所有一级目录下以 `.temp` 结尾的 python 文件：

```shell
pytest --ignore-glob='*/test_*.temp.py'
```

`--ignore-glob` 选项可以与 `--ignore` 选项一起使用，也可以单独使用，并且可以多次使用 `--ignore-glob` 以应用多个glob模式。

**请注意：**

`--ignore-glob` 对大小写敏感或不敏感的行为取决于操作系统。大多数UNIX和Linux系统是大小写敏感的，而 Windows 系统通常不是。

类似 `--ignore` 选项，`--ignore-glob` 也可以与 `pytest` 的其他选项配合使用，可以在配置文件中为 `pytest` 定义默认的忽略模式，使排除规则更加灵活和强大。



### 3.2.5.5 参数 --deselect=nodeid_prefix

`pytest` 的 `--deselect` 选项使得可以在命令行中指定要排除的特定测试。这可以用来从已选定的测试中进一步排除特定的测试函数或方法，无需修改代码或测试文件。

`nodeid`是 `pytest` 用来唯一标识测试项的一个字符串，它通常由文件路径、类名（对于测试类的测试方法）和测试函数或方法名组成。

**示例**：

```shell
pytest --deselect=test_module.py::TestClass::test_method
```

在这个例子中，即使 `test_module.py` 文件中的 `TestClass` 类的 `test_method` 方法符合测试收集的标准，它也会被明确地从测试运行中排除掉。

`--deselect` 选项的常见用法包括：

* **单个测试排除**：当你想要忽略单个的测试，可以直接使用它的`nodeid`进行排除。
* **多个测试排除**：你可以通过在命令行上多次使用 `--deselect` 选项来指定多个要排除的测试。

```shell
pytest --deselect=test_module.py::TestClass::test_method1 --deselect=test_module.py::test_function
```

* **参数化测试的部分实例排除**：如果你的测试函数使用了参数化（`pytest.mark.parametrize`），你可以只排除特定参数的实例。

```shell
pytest --deselect=test_module.py::test_function[parameter1]
```

`nodeid_prefix` 参数需要精确到能够标识特定测试的程度。`--deselect` 可以成为临时快速调整测试套件的工具，而不去修改测试代码或使用跳过（skip）装饰器。

**请注意：**

`--deselect` 选项通常是在与其他命令行选项结合使用的情况下最有效，比如与 `-k` 或者 `-m` 结合，先选择一个较大范围的测试集，然后再使用 `--deselect` 排除掉不需要运行的个别测试。




### 3.2.5.6 参数  --confcutdir=dir

`pytest` 的 `--confcutdir` 选项用来指定 "配置裁切目录" (configuration cutting directory) 的路径。这个参数影响 `pytest` 查找 `pytest.ini`、`tox.ini` 和 `setup.cfg` 等配置文件的行为。当 `pytest` 在执行测试的过程中向上递归搜索配置文件时，一旦到达这个指定的目录则停止搜索。

这个设置可能很有用，特别是在处理嵌套项目或包含多个子项目的代码库时，它可以帮助区分子项目的测试配置。

**示例**：

假设你有以下项目结构：

```shell
/home/project/
├── pytest.ini
├── setup.py
└── src/
    └── tests/
        ├── sub_project/
        │   ├── test_sub.py
        │   └── pytest.ini
        └── test_main.py
```

如果你想运行 `sub_project` 中的测试，但只想使用它自己的 `pytest.ini` 配置文件，你可以这样做：

```shell
pytest src/tests/sub_project --confcutdir=src/tests/sub_project
```

在这个例子中，即使 `/home/project/` 也有一个 `pytest.ini` 文件，使用 `--confcutdir` 参数指定 `src/tests/sub_project` 作为裁切目录之后，更高级别的 `pytest.ini` 将会被忽略，`pytest` 只会使用 `src/tests/sub_project` 下的配置文件。

这样，你就可以更精细地控制配置文件的搜索范围，确保测试行为的一致性。当希望忽略项目的基础或全局配置，而专注于子项目或特殊目录下的配置时，这个选项尤为有用。

不提供 `--confcutdir` 时，默认行为是从测试文件的当前目录开始向上搜索，直到根目录。设置 `--confcutdir` 使搜索过程在到达指定的目录时停止，不再向上递归。




### 3.2.5.7 参数 --noconftest

`pytest` 的 `--noconftest` 选项在执行测试时阻止自动加载 `conftest.py` 文件。`conftest.py` 文件允许用户定义和共享测试配置、测试夹具（fixtures）、钩子函数（hooks）等，而这些都可以跨多个测试文件使用。

当 `pytest` 执行测试时，默认情况下，它会在测试路径的所有相关目录中查找 `conftest.py` 文件，并自动加载它们。但有时，为了控制测试环境的复杂性，或者在特定的场景下，用户可能不想自动加载这些 `conftest.py` 文件。在这种情况下，可以使用 `--noconftest` 选项来运行 `pytest`。

使用 `--noconftest` 选项时，`pytest` 会忽视所有的 `conftest.py` 文件，这也就意味着任何在 `conftest.py` 中定义的夹具（fixtures）和钩子函数（hooks）都不会被加载，即使这些 `conftest.py` 放在测试收集路径中也一样。

**示例**：

```shell
pytest --noconftest tests/
```

在这个命令中，`pytest` 将运行位于 `tests` 目录下的所有测试，但它会忽略任何 `conftest.py` 文件。如果测试依赖于 `conftest.py` 中定义的配置或夹具，这些测试可能会失败，因为相应的设置和夹具不再可用。

**请注意：**

通常用户不会频繁地使用 `--noconftest` 选项，因为 `conftest.py` 文件是 `pytest` 强大灵活性的关键部分之一。该选项通常在调试过程中或当需要临时忽略某些夹具和配置时使用。

总体来说，`--noconftest` 选项可以帮助用户在某些情况下减少 `conftest.py` 文件带来的复杂性，但它同时也会减少 `pytest` 自定义和重用设置的能力。




### 3.2.5.8 参数 --keep-duplicates

`pytest` 的 `--keep-duplicates` 或 `--keepduplicates`选项在执行测试时允许目录级别用例多次执行，特别注意这里，需要指定目录而非具体的文件。

**使用方法：**

```shell
pytest --keep-duplicates path_a path_a
```



**示例：**

加入在`chapter1-3/duplicate`目录下有一个`test_duplicate.py`文件，内容如下：

```python
root@Gavin:~/code/chapter1-3# cd duplicate/
root@Gavin:~/code/chapter1-3/duplicate# cat test_duplicate.py 
#!/usr/bin/env python
# -*- encoding:UTF-8 -*-


def test_a():
    print('a1')


def test_b():
    print('b')


def test_a():
    print('a2')


def test_a():
    print('a3')
root@Gavin:~/code/chapter1-3/duplicate#
```

如果你想借助`pytest`默认行为执行函数`test_a` 三次，这是无法实现的， `--keep-duplicates` 参数并不作用于函数，作用于目录，实现重复路径下用例的多次执行。



当指定的重复路径为文件级别时，默认支持执行多次，如下，执行了两次（collected 4 items）：

```shell
root@Gavin:~/code/chapter1-3# pytest -s -v duplicate/test_duplicate.py duplicate/test_duplicate.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-3
collected 4 items
duplicate/test_duplicate.py::test_a a3
PASSED
duplicate/test_duplicate.py::test_b b
PASSED
duplicate/test_duplicate.py::test_a a3
PASSED
duplicate/test_duplicate.py::test_b b
PASSED

=============================== 4 passed in 0.01s =============================
root@Gavin:~/code/chapter1-3#
```



指定的重复路径为目录时，默认只会执行一次，如下，只执行了一次（（collected 2 items））：

```shell
root@Gavin:~/code/chapter1-3# pytest -s -v duplicate duplicate
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-3
collected 2 items
duplicate/test_duplicate.py::test_a a3
PASSED
duplicate/test_duplicate.py::test_b b
PASSED

=============================== 2 passed in 0.00s =============================
root@Gavin:~/code/chapter1-3#
```



当指定的路径为目录时，如果希望也执行多次，需要使用 --keep-duplicates参数，如下目录中的用例执行了2次：

```shell
root@Gavin:~/code/chapter1-3# pytest -s -v duplicate duplicate --keep-duplicates
============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-3
collected 4 items
duplicate/test_duplicate.py::test_a a3
PASSED
duplicate/test_duplicate.py::test_b b
PASSED
duplicate/test_duplicate.py::test_a a3
PASSED
duplicate/test_duplicate.py::test_b b
PASSED

============================== 4 passed in 0.01s =============================
root@Gavin:~/code/chapter1-3#
```



 `--keep-duplicates` 参数实用性不是很高，如果想多次执行某个后某些文件中的测试用例，需要传递多次目录到命令行（执行10遍需要传递10次目录），此方法略显笨拙，可以借助`pytest-count`插件，指定`--count=N`参数N值(N=10,表示执行10次)完成用例的多次执行。



### 3.2.5.9 参数 --collect-in-virtualenv

如果你借助`virtualenv`创建了独立的Python虚拟环境，将每个项目与其他项目独立开来，互不影响（比如解了依赖包版本冲突的问题），Python虚拟环境中存在测试用例，借助 `--collect-in-virtualenv` 的命令行选项，收集本地 `virtualenv` 目录中所有符合条件的测试文件、测试用例。

此参数用于不忽略 `virtualenv` 目录中测试用例，在有 `Python virtualenv` 开发环境下比较实用。



### 3.2.5.10 参数 --import-mode={prepend,append,importlib}

`pytest` 支持一个名为 `--import-mode` 的命令行选项，该选项用于控制如何导入测试模块。根据你选择的模式，`pytest` 在处理测试时会采用不同的方法来导入模块（默认使用`prepend`）。

这里是 `--import-mode` 选项支持的三种模式的详细解释：

* **prepend**:
  在这种模式下，`pytest` 会将测试所在的路径添加到 `sys.path` 列表的**开始处**。这意味着在搜索模块时，Python 解释器会首先检查测试文件所在的目录，这可能会覆盖同名模块的其他实例。即使存在同名的安装模块，Python 也会首先导入测试目录中的模块。

```shell
pytest --import-mode=prepend
```

* **append**:
  在这种模式下，`pytest` 会将测试所在的路径添加到 `sys.path` 列表的**末尾**。这意味着，测试运行时，只有在没有找到模块的情况下，才会去测试路径下查找和导入模块。这有助于避免与已安装在虚拟环境或系统路径中的同名模块发生冲突。

```shell
pytest --import-mode=append
```

* **importlib**:
  从 Python 3.1 开始引入的 `importlib` 机制，这是一种更加正规的导入机制，该模式不直接修改 `sys.path`。在 `importlib` 模式下，`pytest` 使用 `importlib.import_module` 函数来动态地导入测试模块。这种方式更接近于正常 Python 导入系统的工作方式，有助于避免某些可能由修改 `sys.path` 引起的问题。

```shell
pytest --import-mode=importlib
```

根据你的项目结构和需求，你可以选择最合适的导入模式来运行你的测试。例如，如果你想确保测试与模块的导入方式尽可能接近正常使用时的导入方式，你可能会选择 `importlib` 模式，而不是更改 `sys.path` 的 `prepend` 或 `append` 模式。




### 3.2.5.11 参数 --doctest-modules

`pytest` 是一个功能丰富的测试框架，它支持运行测试用例，包括 `doctest` 测试。

**`doctest`的作用：**

- 在python代码中寻找类似交互解释器里执行的命令，执行它们并且和这些命令的期望值进行比较。
- 用来验证`docstring`中的注释和代码实际的作用是一致的。
- 可以作为回归测试来验证代码能够正确执行。
- 可以用来编写模块的文档演示这些模块是如何处理输入得到输出的。

**`doctest`的要点：**

- 一般写在函数的`docstring`里面。
- 用`>>>`表示一个用例的开始，直到遇到空行或者下一个`>>>`。
- 使用`#doctest: +ELLIPSIS`（中文含义省略）来表示下面的省略号匹配任意内容。

`pytest` 的 `--doctest-modules` 选项是用来指示 `pytest` 收集并运行模块中的 `doctest` 测试的。`doctests` 是嵌入在 Python 文档字符串（`docstrings`）中的测试，常用于确保代码示例的正确性，并且可以作为简单的单元测试来使用。这些测试写在三引号`"""`之间，紧跟着函数、类或模块的描述。这种类型的测试很适合示例代码，因为它们可以同时作为文档和测试用例。

当你运行 `pytest` 并使用 `--doctest-modules` 选项时，`pytest` 将会：

* 扫描所有的 Python 模块文件（通常是 `.py` 扩展名的文件）。
* 在模块文件的文档字符串中查找 `doctest` 样式的交互式 Python 会话。
* 执行这些文档字符串中找到的命令，并验证命令的输出是否与文档字符串中的预期输出相匹配。

以下是如何在 `pytest` 中使用这个选项的示例：

```shell
pytest --doctest-modules
```

当使用这个选项时，`pytest` 会自动处理所有你的 Python 模块文件，无需额外的配置。

示例 `docstring` 中的 `doctest`：

```python
root@Gavin:~/code/chapter1-3# cat test_doctest.py 
#!/usr/bin/env python
# -*- coding:utf-8 -*-


def add(a, b):
    """
    Add two numbers together.

    >>> add(2, 3)
    5

    >>> add('hello', 'world')
    'helloworld'
    """
    return a + b
root@Gavin:~/code/chapter1-3#
```

在上面的例子中，函数 `add` 的文档字符串包含两个 `doctests`。第一个测试使用数字进行测试，第二个使用字符串。运行 `pytest` 时加上 `--doctest-modules` 选项，可以验证 `add` 函数对这两个例子的处理是正确的：

```shell
root@Gavin:~/code/chapter1-3# pytest -s -v --doctest-modules test_doctest.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-3
collected 1 item
test_doctest.py::test_doctest.add PASSED

=============================== 1 passed in 0.01s =============================
root@Gavin:~/code/chapter1-3#
```

如果将三引号`"""`之间的某个内容输出错位一下，比如修改成如下内容（只展示部分，将输出'5'前面增加几个空格）：

```
    Add two numbers together.

    >>> add(2, 3)
        5
```

此时加上 `--doctest-modules` 选项，执行效果如下：

```shell
root@Gavin:~/code/chapter1-3# pytest --doctest-modules test_doctest.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 1 item
test_doctest.py F                                                        [100%]

================================ FAILURES =====================================
__________________________ [doctest] test_doctest.add _________________________
006 
007     Add two numbers together.
008 
009     >>> add(2, 3)
Expected:
        5
Got:
    5

/root/code/chapter1-3/test_doctest.py:9: DocTestFailure
============================ short test summary info ==========================
FAILED test_doctest.py::test_doctest.add
============================ 1 failed in 0.01s ================================
root@Gavin:~/code/chapter1-3#
```



这个功能可以帮助你确保你的文档字符串中的示例始终是最新的，并且按照预期工作，作为一种快速检查或补充传统单元测试的方法。




### 3.2.5.12 参数 --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}

`pytest` 提供了一个名为 `--doctest-report` 的选项，用于控制当运行带有 `--doctest-modules` 选项的 `doctests` 时，测试失败的输出报告格式。此选项允许用户根据个人喜好选择不同的输出风格，这将会影响输出结果的可读性和信息量。

下面是 `--doctest-report` 选项支持的各种值的详细解释：

* **none**:
  这个选项会关闭所有的 `doctest` 报告输出；也就是说，即使 `doctest` 失败了，也不会打印任何差异信息。这可以用于只想知道测试是否通过，而不关心失败的详细信息的情况。

```shell
pytest --doctest-modules --doctest-report=none
```

* **cdiff**:
  使用这个选项，`pytest` 会显示 `doctest` 失败时的上下文差异（`contextual diff`），将旧值与新值并排显示。这种差异报告往往更加容易理解，因为它提供了一个明确的“更改前后”视图。

```shell
pytest --doctest-modules --doctest-report=cdiff
```

* **ndiff**:
  此选项启用 `ndiff` 格式报告，显示多行的正常差异(`diff`)。这是一个类似于 Unix `diff` 命令输出的详细字符级别的比较。

```shell
pytest --doctest-modules --doctest-report=ndiff
```

* **udiff**:
  使用 `udiff`（统一差异）格式输出差异。这提供了周围代码的一定量的上下文，这有助于理解差异发生在哪里以及模式是什么。这是代码评审和代码变更讨论中常用的格式。

```shell
pytest --doctest-modules --doctest-report=udiff
```

* **only_first_failure**:
  当使用此选项时，`pytest` 只会报告每个 `doctest` 指令块中的第一个失败。这对于只想快速看到引起失败的首个问题的情况很有帮助，减少了信息的过载。

```shell
pytest --doctest-modules --doctest-report=only_first_failure
```

根据你对反馈的需求，你可以选择最适合你的报告格式。如果你希望快速地看到失败的概要，`none` 或 `only_first_failure` 可能是有用的。如果你需要详细地了解为何测试失败，包括完整的差异信息，那么 `cdiff`、`ndiff` 或 `udiff` 可能更适合你。




### 3.2.5.13 参数 --doctest-glob=pat

文档测试是直接嵌入在Python文件（通常是`docstrings`中）的测试，它允许测试示例代码的正确性。

`--doctest-glob`参数让你指定一个模式（pattern），以此告诉`pytest`哪些文件应包括执行文档测试。默认情况下，`pytest` 只会在 `test*.txt` 文件中查找文档测试，以及在模块的`docstrings`中，但是有时你可能希望仅从匹配特定模式的文件中收集 `doctests`，可以通过发出以下命令来更改模式：

```shell
pytest --doctest-glob="*.rst"
```

例如，你可能有一组演示文件或示例脚本，并希望确保这些文件的文档字符串中的代码示例始终保持最新，如下。

```python
# content of test_example.txt

hello this is a doctest
>>> x = 3
>>> x
3
```

然后你就可以直接调用 `pytest` ：

```shell
root@Gavin:~/code/chapter1-3/Doctest# pytest 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3/Doctest
collected 1 item

test_example.txt .                                                        [100%]
============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-3/Doctest#
```

除了文本文件之外，还可以直接从类和函数的`docstrings`（包括测试模块）执行`doctest`：

```python
# content of test_mymodule.py
def test_something():
    """a doctest in a docstring
    >>> something()
    42
    """
    return 42
```

```shell
root@Gavin:~/code/chapter1-3/Doctest# pytest --doctest-modules
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3/Doctest
collected 2 items
test_mymodule.py .                                                       [ 50%]
test_example.txt .                                                       [100%]

============================== 2 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-3/Doctest# 
```

通过将这些更改放入`pytest.ini`文件，可以在项目中永久性地进行这些更改，如下所示：

```
# content of pytest.ini
[pytest]
addopts = --doctest-modules
```

`--doctest-glob=pat` 中`pat` 参数可以是任何 `shell` 兼容的文件匹配模式（大小写敏感），就像在 shell 中使用星号`*`来表示任何字符的序列，或问号`?`来表示任何单个字符。

这个选项非常有用，比如当你的项目中包含了有特定后缀的文档测试时，或者你只想运行匹配特定模式的文件中的 `doctests`。例如，以下是一些使用 `--doctest-glob` 选项的方式：

* `*.txt`：这会指示 `pytest` 搜索所有 `.txt` 扩展名的文件中的 `doctests`。

```shell
pytest --doctest-glob="*.txt"
```

* `*_example.py`：这会告诉 `pytest` 只在文件名以 `_mymodule.py` 结尾的 Python 文件中搜索 `doctests`。

```shell
pytest --doctest-glob="*_mymodule.py"
```

* `test_*.rst`：在这个例子中，`pytest` 会搜索所有以 `test_` 开头，并且扩展名为 `.rst` 的文件中的 `doctests`。

```shell
pytest --doctest-glob="test_*.rst"
```

如果只想执行指定目录下的文档测试，可以执行如下类似命令：

```shell
pytest --doctest-glob="test_*.rst" Doctest/
```

如果你想要同时测试多种模式的文件，可以多次使用`--doctest-glob`：

```bash
pytest --doctest-glob='*.md' --doctest-glob='*.rst'
```

这个命令会让`pytest`同时搜索`.md`和`.rst`文件进行文档测试。



使用`--doctest-glob`可以更加灵活地控制`pytest`在哪些文件上运行文档测试，从而能更好地适应各种项目布局和需求。要记住 `--doctest-glob` 选项可以多次使用来匹配不同的模式群组，每次使用可以指定一个模式。




### 3.2.5.14 参数 --doctest-ignore-import-errors

`pytest` 的 `--doctest-ignore-import-errors` 选项是用来指定在执行 `doctests` 时是否应该忽略模块的导入错误。当你运行 `doctests`，即使用 `--doctest-modules` 标志时，`pytest` 会尝试导入每个测试模块中的文档字符串中包含的代码。如果模块导入失败，通常 `pytest` 会报告一个错误。

启用 `--doctest-ignore-import-errors` 选项会告诉 `pytest` 在遇到导入错误时继续运行其余测试，而不是停止并报告错误。这可能在以下场景中有用：

- 当项目中有些模块因为特定原因（比如系统依赖或配置问题）在当前环境中无法导入时。
- 当你希望在一个大型项目中迅速运行所有有效的 `doctests`，而不关心那些因为环境问题而可能失败的测试。
- 当你正在处理连锁导入问题时，且不希望单个问题阻碍整个测试流程。

例如，如果你想运行 `doctests` 但忽略由于导入错误导致的失败，你可以使用以下命令：

```shell
pytest --doctest-modules --doctest-ignore-import-errors
```

**请注意：**

忽略导入错误可能会掩盖潜在的问题，因为这可能意味着测试不是在完全正确的环境中执行的。因此，在定位问题或确保环境配置正确之前，经常使用 `--doctest-ignore-import-errors` 选项可能不是最佳实践。通常推荐在开发和持续集成过程中解决所有导入错误，以确保测试的准确性和代码的完整性。



### 3.2.5.15 参数 --doctest-continue-on-failure

`pytest` 的`--doctest-continue-on-failure` 用于在执行 `doctest` 时修改测试行为的选项。通常，当一个 `doctest` 失败时，`pytest` 会停止运行当前文档字符串中余下的测试。这个默认行为意味着如果文档字符串中有多个独立的 `doctest` 示例，其中一个失败了，接下来的示例将不会被执行或验证。

启用 `--doctest-continue-on-failure` 选项后，即使一个 `doctest` 示例失败，`pytest` 也会继续运行同一个文档字符串中的剩余示例。这使得开发人员可以更好地了解文档字符串中有多少独立测试是有问题的，甚至在修复每个测试之前都能获得全部的失败示例的反馈。

使用示例：

```shell
pytest --doctest-modules --doctest-continue-on-failure
```

这个命令将会运行项目中所有模块的 `doctests`，并且即使某个示例失败，它也会继续运行模块中其它的 `doctest`。

这个选项对于诊断和修复文档中嵌入代码示例的问题尤其有用，因为你可以一次性看到所有失败的测试，而不必每次修复一个就重新运行一遍 `pytest`。

相比之下，如果没有 `--doctest-continue-on-failure` 选项，你可能会在修复了一个示例后才发现另一个示例也失败了，这可能导致更迭的修复过程更加冗长。

**请注意：**

即使 `--doctest-continue-on-failure` 选项允许继续执行测试，但是最终的测试结果反映了所有失败的测试，所以在全部修复之前，测试套件不会标记为成功。



## 3.2.6 test session debugging and configuration 相关参数


### 3.2.6.1 参数 --basetemp=dir

`pytest` 的 `--basetemp=dir` 选项是用来指定测试运行时的基本临时目录。在执行测试时，`pytest` 可能会创建临时文件和目录来存放测试相关的数据或文件。使用 `--basetemp` 选项，你可以控制这些临时文件应该被创建在哪个目录下。

例如，如果你想要所有临时测试数据存放在 `/tmp/pytest` 目录下，在运行 `pytest` 时加上以下选项：

```shell
pytest --basetemp=/tmp/pytest
```

当你指定 `--basetemp` 后，`pytest` 将会在你指定的目录中创建一个新的临时目录，这个目录的名称通常以 `pytest-` 开头，后面跟随一些随机生成的字符，以此保证每次测试运行都有一个独立的临时空间。在测试结束后，`pytest` 通常会自动清理它创建的临时目录，除非你另有配置。

这个选项有几个实际的用途：

- **隔离测试数据**：确保测试使用的临时文件不会与系统的其他部分冲突，并可以在一个已知的位置找到这些数据（便于调试或后续分析）。
- **特定的存储要求**：当系统的默认临时存储位置（如 `/tmp`）不适用于测试时（可能因为空间限制、权限问题或性能原因），你可以指定一个更合适的位置。

如果你在运行 `pytest` 命令时使用了 `--basetemp` 参数，但并没有看见相关的临时目录，可能有以下几个原因：

* **命令使用上的错误**：首先确保你已经正确使用了 `--basetemp` 参数，并指定了一个路径。比如：

```
pytest --basetemp=/path/to/tempdir
```

* **路径权限问题**：确认你有权限在指定的路径创建目录和文件。

* **测试用例没有创建文件**：如果运行的测试没有生成临时文件，那么即使你使用了 `--basetemp`，也可能不会看到临时目录，因为没有任何内容需要写入。

* **测试完成后目录被删除**：`pytest` 通常在测试结束后会清理测试期间创建的临时文件和目录，如果你在测试完成后立即查看，可能会发现临时目录已经不存在了。

* **非期望的路径**：如果提供的基本临时目录路径与预期不符，可能是由于路径中存在输入错误，或者是测试在运行时更改了路径。

* **输出重定向的问题**：如果你在命令中使用了输出重定向，可能会影响你对临时目录是否存在的监测。

示例：

```python
root@Gavin:~/code/chapter1-3# cat test_tmp_path.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

CONTENT = "Test content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0
root@Gavin:~/code/chapter1-3# 
```

执行如下命令：

```shell
pytest -s -v --basetemp=/tmp/pytest chapter1-3/test_tmp_path.py
```

在`/tmp`目录下产生了一个名为`pytest`目录，结构参考如下：

```
root@Gavin:/tmp/pytest# tree -a
.
├── test_create_file0
│   └── sub
│       └── hello.txt
└── test_create_filecurrent -> /tmp/pytest/test_create_file0

4 directories, 1 file
root@Gavin:/tmp/pytest# cat test_create_file0/sub/hello.txt 
Test contentroot@Gavin:/tmp/pytest# 
root@Gavin:/tmp/pytest# 
```

每次执行都会覆盖上一次的执行结果，如果想保留新近多个临时目录，请参考本书`[pytest] ini-options 相关参数`章节中`参数 tmp_path_retention_count (string)`处内容。

**请注意：**

应确保指定的目录在测试之前存在且可写（应在测试用例中显式地创建一些临时文件）。此外，在使用 `--basetemp` 指定临时目录时，也应谨慎考虑存储空间和权限，以保证测试的顺利进行。




### 3.2.6.2 参数 -V, --version

`pytest -V` 和 `pytest --version` 是 `pytest` 命令行接口中的两个选项，它们用于显示 `pytest` 的版本信息。二者效果相同，只是 `-V` 是 `--version` 的缩写形式。当你在终端或命令提示符中运行其中任何一个命令时，`pytest` 会输出当前安装的版本号。

这是一个用于检查你当前安装的 `pytest` 版本的快捷方式。这对于调试、确认环境配置或检查是否需要更新 `pytest` 版本等场景十分有用。知道确切的版本号可以帮助你查阅对应的文档，了解特定功能的支持情况或者解决可能出现的版本兼容性问题。

用法如下：

```shell
pytest -V
```

或者

```shell
pytest --version
```

执行这个命令后，你会看到类似于以下内容的输出：

```
pytest 7.4.0
```

这表明当前安装的 `pytest` 版本是 7.4.0。上述输出会因你的具体安装版本而异。

这个功能在排除问题时尤其方便，如果你在一个多人协作的项目中工作，它也可以帮助确认团队成员是否都在使用相同的 `pytest` 版本，以避免因版本差异导致的不一致问题。




### 3.2.6.3 参数 -h, --help

`pytest -h` 和 `pytest --help` 是 `pytest` 测试框架中的帮助选项，它们用来显示命令行上可用的选项和参数的简短帮助信息。这些选项不执行测试，而仅仅提供 `pytest`的使用帮助说明。这对于想要快速了解 `pytest` 提供的各种命令行选项和特性的用户很有帮助。使用 `-h` 或 `--help` 是相同的，提供相同的输出。

使用方法：

```shell
pytest -h
```

或者

```shell
pytest --help
```

执行以上任一命令，你将看到类似下面的输出内容：

```shell
usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         Only run tests which match the given substring expression. An
                        expression is a Python evaluatable expression where all names are
                        substring-matched against test names and their parent classes. 
                        Example: -k 'test_method or test_other' matches all test 
                        functions and classes whose name contains 'test_method' or 
                        'test_other', while -k 'not test_method' matches those that don't
                        contain 'test_method' in their names. -k 'not test_method
                        and not test_other' will eliminate the matches. Additionally 
                        keywords are matched to classes and functions containing extra 
                        names in their 'extra_keyword_matches' set, as well as functions
                        which have names assigned directly to them. The matching is 
                        case-insensitive.

  ... (additional help text for other options)
```

输出信息基本包括：

- `pytest` 的基本用法
- 如何选择和运行特定的测试
- 所有可用的命令行选项和它们的简短描述
- 针对复杂选项的详细用法说明

当你需要查找 `pytest` 命令的一些用途，或者当你记不清某个特定选项的详细语法时，`pytest -h` 或 `pytest --help` 都是非常便捷的记忆工具和参考资源。




### 3.2.6.4 参数 -p name

`pytest` 的`-p name` 是一个 `pytest` 命令行选项，其中 `-p` 是插件`plugin`的缩写，`name` 指的是你想要启用或禁用的插件的名称。该选项允许用户在命令行上控制 `pytest` 插件的行为。

具体来说，`-p` 选项有两种用途：

* **启用插件**: 如果你想在运行测试时显式启用某个插件，你可以使用 `-p` 选项加上插件的名称。这可能是在你的 `pytest` 配置文件中没有列出该插件，但你希望仅为当前的测试运行启用它的情况。
* **禁用插件**: 如果你想禁用某个特定的插件，可以在 `name` 前加上 `no:` 前缀。这在你想忽略某个默认加载的插件或者是为了排除与其他插件的冲突时很有用。

举一个实例，假设你有一个名为 `my_plugin` 的插件，你希望在运行 `pytest` 时启用它：

```shell
pytest -p my_plugin
```

如果你想要禁用 `my_plugin` 插件，你应该这样做：

```shell
pytest -p no:my_plugin
```

使用 `-p` 选项是一种临时修改 `pytest` 插件行为的快捷方式，无需修改项目的配置文件。这对于测试和调试插件功能非常有用，当然也适用于根据具体情况临时调整插件的加载。



### 3.2.6.5 参数 --trace-config

`pytest`的 `--trace-config` 是一个命令行选项，它告诉 `pytest` 在启动时输出配置、插件加载和其他诊断信息。这个选项通常用于调试 `pytest` 本身的行为，尤其是当涉及到复杂的配置或插件互操作性问题时。

当你运行带有 `--trace-config` 选项的 `pytest` 时，它将显示以下类型的信息：

- `pytest` 如何解析 `pytest.ini` 或 `tox.ini` 文件中的配置设置。
- 哪些插件被加载，包括内置插件和第三方插件。
- 插件加载的顺序。
- 任何与配置和插件相关的警告或错误。

例如，如果你运行：

```shell
pytest --trace-config
```

你可能会看到类似以下内容的输出：

```shell
root@Gavin:~/code# pytest -s -v chapter1-3/ --trace-config
PLUGIN registered: <_pytest.config.PytestPluginManager object at 0x7f824cb3a5d0>
PLUGIN registered: <_pytest.config.Config object at 0x7f824c06cfd0>
PLUGIN registered: <module '_pytest.mark' from '/usr/lib/python3/dist-packages/_pytest/mark/__init__.py'>
PLUGIN registered: <module '_pytest.main' from '/usr/lib/python3/dist-packages/_pytest/main.py'>
PLUGIN registered: <module '_pytest.runner' from '/usr/lib/python3/dist-packages/_pytest/runner.py'>
PLUGIN registered: <module '_pytest.fixtures' from '/usr/lib/python3/dist-packages/_pytest/fixtures.py'>
...
...
```

通过这种方式，`--trace-config` 为开发人员提供了关于 `pytest` 如何启动和加载其组件的深入见解，这是追踪复杂问题的有力工具。然而，对于日常使用并非必要，主要面向那些需要深入了解 `pytest` 工作原理的开发者。




### 3.2.6.6 参数 --debug=[DEBUG_FILE_NAME]

`pytest` 的`--debug=[DEBUG_FILE_NAME]` 是一个 `pytest` 命令行选项，用于记录 `pytest` 会话期间的详细调试信息并将其保存到一个文件中。这对于诊断复杂的问题或深入理解 `pytest` 的内部工作非常有帮助。

在这个选项中，`[DEBUG_FILE_NAME]` 是一个可选的参数。如果提供了文件名，`pytest` 会将调试日志保存到这个具体文件中。如果没有指定文件名，`pytest` 默认会创建一个名为 `pytestdebug.log` 的文件来保存调试信息。

当你使用此选项时，`pytest` 将会记录以下类型的信息：

- 测试的执行流程
- 插件的加载和使用情况
- 钩子函数（hook functions）的调用情况
- 异常和错误的详细追踪
- 以及其他可能对调试过程有帮助的信息

例如，要启动调试模式并将日志写入 `my_debug.log` 文件，你可以运行：

```shell
pytest --debug=my_debug.log
```

运行完成后，`my_debug.log` 文件将包含`pytest`会话的调试日志，其中可能包含关于测试执行、插件处理、配置读取等方面的细节信息。

通常，这个选项不会在日常的测试运行中使用，主要用于`pytest`插件开发、贡献者或当出现难以追踪的问题时。开发者可以通过分析调试日志来寻找和解决问题。




### 3.2.6.7 参数 -o OVERRIDE_INI, --override-ini=OVERRIDE_INI

`pytest`的 `-o OVERRIDE_INI, --override-ini=OVERRIDE_INI` 是一个用于在命令行上临时覆盖 `pytest` 配置文件中的设置的选项。这允许你在不更改 `pytest.ini`、`tox.ini` 或 `setup.cfg` 文件的情况下动态变更 `pytest` 的行为。

当运行 `pytest` 命令时，你可以使用 `-o` 或者 `--override-ini` 选项后跟一个或多个键值对，来覆盖默认的配置值。

例如，如果你想要覆盖 `addopts` 参数来在运行测试时改变默认的命令行选项，你可以这样做：

```sh
pytest -o addopts="-v -x" tests/
```

或者你想要改变报告详细程度：

```sh
pytest -o console_output_style="classic" tests/
```

这个选项非常有用，特别是在自动化脚本或者连续集成（CI）流程中，你可能希望基于特定的条件临时调整测试的行为。

**请注意：**

使用这个选项，即使相同的配置在文件中已经设置，该行为也会被命令行所覆盖，这些覆盖只会影响当前的测试运行，不会永久更改任何文件。




### 3.2.6.8 参数 --assert=MODE

`pytest` 提供了一个命令行选项 `--assert=MODE` 允许你控制断言（assert）语句的处理方式。`MODE` 可以是下面几个值之一：

* `plain`：这是最简单的断言模式，对断言使用标准的 `assert` 语句。如果断言失败，将会引发一个 `AssertionError` 异常，但不会提供对失败原因额外的上下文信息。
* `rewrite`：这是 `pytest` 的默认模式，它会使用一个特殊的断言重写机制。这个模式提供更多关于断言失败原因的详细信息。例如，它会显示断言表达式中每个变量的值。断言重写是通过在导入时实时转换字节码来实现的，这意味着在命令行或配置文件中启用该模式会自动处理所有测试模块中的断言。

通常，你不需要手动指定 `--assert` 选项，因为默认的 `rewrite` 模式对于大多数用户来说都是可以接受和有用的。然而，如果你遇到与断言相关的问题，或者如果你出于某种原因需要使用标准 Python 断言而不是 `pytest` 提供的增强断言机制，你可以通过更改这个选项来实现。

使用 `plain` 模式，可以这样启动 `pytest`：

```shell
pytest --assert=plain
```

这样将会关闭断言的重写功能，使用标准的 Python `assert` 语句。

而如果要确保使用 `pytest` 的断言重写功能，可以这样：

```shell
pytest --assert=rewrite
```

**请注意：**

使用断言重写功能有时可以暴露那些由于 Python 标准断言机制的局限性可能被遗漏的错误。这是因为 `pytest` 的断言重写功能会给出更多的断言失败上下文信息，帮助你快速了解为什么测试失败。




### 3.2.6.9 参数 --setup-only 

`pytest`的 `--setup-only` 是一个命令行选项，用于在不实际运行测试函数的情况下，只执行测试前的 `setup` 部分。这包括执行任何 `setup_method`、`setup_function`、`setup_class` 和 `pytest` 钩子（hook），如 `pytest_fixture_setup`。

这个选项通常用来帮助调试和验证 `setup` 代码是否按预期执行，特别是当你在设置复杂的测试环境或使用复杂的 `fixture` 时。使用这个选项可以让你确认 `setup` 逻辑本身没有问题，而不需要运行完整的测试或等待可能很长的测试执行时间。

命令行使用 `--setup-only` 选项的示例：

```shell
pytest --setup-only tests/
```

这将会处理指定目录（在这个例子中是 `tests/`）下的所有测试用例，但只执行 `setup` 代码，并不实际运行测试函数体中的代码。对于每个测试，`pytest` 将输出 `setup` 的相关步骤。

与其类似的还有一个 `--setup-show` 选项，它会在运行测试的同时显示 `setup` 和 `teardown` 的相应步骤。这对于分析测试执行流程很有帮助，但与 `--setup-only` 不同，它会完全运行测试。



### 3.2.6.10 参数 --setup-show

`pytest`的 `--setup-show` 是一个命令行选项，使用这个选项可以在运行测试的同时显示每个测试用例的 `setup` 和 `teardown` 阶段的信息。你可以通过这个选项来调试或查看你的 `fixture` 函数何时被调用，以及它们的执行过程。

该选项通常用于细化、了解测试的设置过程，尤其是当测试集涉及多个复杂的 `fixture` 时，或者当你需要加深理解 `pytest` 如何设置和清除测试环境时。它也可以帮助你查看 `fixture` 的作用域（function，class，module，session）及其相对于测试函数的激活顺序。

当你使用 `--setup-show` 参数运行 `pytest` 时，每个测试的 `setup` 和 `teardown` 阶段的详细信息都将被输出到控制台。这包括哪些 `fixture` 被用于哪个测试函数，以及相应的 `setup` 和 `teardown` 动作。

如下是如何使用 `--setup-show` 选项的一个示例：

```shell
pytest --setup-show tests/
```

这将会运行 `tests/` 目录下的所有测试，并在控制台上显示它们的 `setup` 和 `teardown` 信息。输出结果可能包括 `fixture` 的实例化，以及测试函数的调用和测试后的清理过程。

此外，除了直观地观察测试环境的准备和清理外，`--setup-show` 还可以帮助确定测试失败可能与哪个特定的 `setup` 或 `teardown` 步骤相关。这对于调试和修复测试中发现的问题非常有用。




### 3.2.6.11 参数 --setup-plan

`pytest`的` --setup-plan` 是 `pytest` 测试框架的一个命令行选项。这个选项允许用户查看测试的 `setup` 和 `teardown` 阶段计划，但不实际执行测试。它是一个比 `--setup-show` 更轻量级的版本，因为它不会实际运行测试或任何 `setup/teardown` 代码，而是只显示将要进行的操作。

在使用这个选项时，`pytest` 将解析测试文件，并输出一个执行计划，其中包括：

- 哪些 `fixture` 会在哪些测试函数之前被调用。
- Fixture 的作用域（例如：function, class, module, session）。
- 测试函数将会如何调用。
- 所有的 `setup` 和 `teardown` 动作。

例如，如果要查看 `tests/` 目录下所有测试的 `setup` 和 `teardown` 计划，可以按以下方式使用：

```shell
pytest --setup-plan tests/
```

使用 `--setup-plan` 选项的输出会告诉你：

* 测试集合的组成（例如，哪些测试函数包含在内）。
* 对于每个测试函数或类，`pytest` 将如何执行它们的前期准备工作。
* 各项 `setup/teardown` 操作。

一个简短的示例来说明`--setup-plan`如何使用：

```python
# content of test_setup_plan_example.py
import pytest

@pytest.fixture(scope="function")
def sample_fixture():
    print("\nSetting up fixture")
    yield
    print("Tearing down fixture")

def test_one(sample_fixture):
    assert True

def test_two(sample_fixture):
    assert True
```

如上代码执行`pytest --setup-plan chapter1-3/test_setup_plan_example.py`有类似以下的输出，它说明了每个测试函数的前置和后置步骤：

```shell
root@Gavin:~/code# pytest --setup-plan chapter1-3/test_setup_plan_example.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: metadata-3.0.0
collected 2 items
chapter1-3/test_setup_plan_example.py 
        SETUP    F sample_fixture
        chapter1-3/test_setup_plan_example.py::test_one (fixtures used: sample_fixture)
        TEARDOWN F sample_fixture
        SETUP    F sample_fixture
        chapter1-3/test_setup_plan_example.py::test_two (fixtures used: sample_fixture)
        TEARDOWN F sample_fixture

============================= no tests ran in 0.00s ===========================
root@Gavin:~/code# 
```

在上面的输出中，`SETUP`和`TEARDOWN`关键字表明了前置和后置的动作。`F`表示这个fixture的作用域是函数级别（每个测试函数调用前后都会执行），接着是fixture的名称（这里是`sample_fixture`）和测试函数的名称及其使用的fixtures。

由于 `--setup-plan` 仅显示将要执行的操作，而不实际执行它们，因此它对于快速理解测试的准备工作非常有用，尤其是在有大量复杂 `fixture` 或 `多层setup` 过程的大型测试套件中。这可以帮助测试开发者和维护者预见到执行测试时会发生哪些调用和清理操作，进而优化测试流程或进行调试。



## 3.2.7 logging 相关参数


### 3.2.7.1 参数 --log-level=LEVEL

`pytest` 提供了丰富的日志功能，通过使用命令行选项 `--log-level=LEVEL` 来配置日志级别。这允许你设置测试运行期间日志消息的详细程度。`LEVEL` 表示你希望看到的日志等级。Python 标准日志模块（logging）定义的6种日志级别包括（括号为级别对应的数值）：`NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)`。

当你在运行 `pytest` 命令时指定 `--log-level` 选项，你可以控制输出到控制台的日志信息的级别（或级别对应的数值）。例如：

```shell
pytest --log-level=INFO
```

在以上命令中，所有 `INFO` 级别以上的日志消息（包括 `WARNING`, `ERROR`, `CRITICAL`）都将被显示在控制台上。`DEBUG` 级别的消息将不会被显示，因为它们低于 `INFO` 级别。

Python日志级别如下：

- `DEBUG`: 最详细的日志级别，用于小范围的问题定位。
- `INFO`: 用于常规信息的输出，如程序运行状态。
- `WARNING`: 用于表示可能的问题，但不会阻止程序的运行。
- `ERROR`: 用于记录错误事件，此时程序可能无法正确执行某些功能。
- `CRITICAL`: 用于记录极其严重的问题，这种情况可能导致程序崩溃。

`pytest` 的日志功能和配置可以非常灵活，可以通过添加更多参数如 `--log-format` 和 `--log-date-format` 来定制日志消息的格式以及日期的显示格式，还可以通过配置文件 `pytest.ini` 或 `pyproject.toml` 来定义默认的日志级别和格式等。

使用合适的日志级别可以帮助你更有效地调试测试，并且关注于特定的问题，特别是在面对复杂或者出错难以追踪的测试代码时。




### 3.2.7.2 参数 --log-format=LOG_FORMAT

`pytest` 的 `--log-format=LOG_FORMAT` 是 `pytest` 测试框架中用于自定义日志输出格式的命令行选项。当你在使用 `pytest` 进行测试时，可以利用这个选项来改变日志信息显示的格式。

`LOG_FORMAT` 是一个字符串，用于确定记录的每条日志信息应当如何显示。你可以在这个字符串中使用一系列的预定义变量（如时间、记录级别、消息内容等）来定义自己的格式。

默认的日志格式通常是这样的：

```shell
%(levelname)s %(message)s
```

这里的 `%(levelname)s` 表示日志级别（例如 `INFO`、`DEBUG`），而 `%(message)s` 则代表日志消息本身。

如果你希望每条日志都显示时间戳、日志级别、文件名、函数名和行号，可以使用类似下面的格式字符串：

```shell
pytest --log-format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s"
```

在这个例子中，变量的意义如下：

- `%(asctime)s`: 日志事件的时间，比如 '2023-12-13 22:39:35,896' （年-月-日 时:分:秒,毫秒）的格式。可以通过 `--log-date-format` 进一步定制时间格式。
- `%(levelname)s`: 文本形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）。
- `%(filename)s`: 输出日志记录所在的源文件名。
- `%(funcName)s`: 日志记录点所在的函数名。
- `%(lineno)d`: 日志记录点的行号。
- `%(message)s`: 日志记录的消息文本。

使用 `--log-format` 自定义日志格式可以帮助开发者更清晰地了解日志背景信息，特别是在大型项目或复杂测试中，显示额外的上下文信息可以大大提高调试的效率。




### 3.2.7.3 参数 --log-date-format=LOG_DATE_FORMAT

在 `pytest` 中，`--log-date-format=LOG_DATE_FORMAT` 选项允许你自定义日志记录中时间戳的输出格式。该时间戳通常位于日志条目的开始位置，表示记录日志时的日期和时间。

`LOG_DATE_FORMAT` 使用与 Python 的 `datetime.strftime()` 方法相同的格式化字符串。你可以在这个字符串中使用一系列格式化代码来指定你希望在日志中看到的准确日期和时间格式。

一些常见的时间格式化代码包括：

- `%Y`: 年份，表示为完整的四位数（例如：2023）。
- `%m`: 月份，表示为两位数（01 到 12）。
- `%d`: 月中的第几天，表示为两位数（01 到 31）。
- `%H`: 小时（24小时制），表示为两位数（00 到 23）。
- `%M`: 分钟，表示为两位数（00 到 59）。
- `%S`: 秒数，表示为两位数（00 到 59）。

例如，如果你想在日志记录中包含小时、分钟和秒，你可以使用以下命令：

```shell
pytest --log-date-format="%H:%M:%S"
```

这将产生类似 "23:12:56" 的时间戳。

另一个例子，如果希望时间戳包含年月日和详细的时分秒，你可以使用以下命令：

```shell
pytest --log-date-format="%Y-%m-%d %H:%M:%S"
```

这将产生类似 "2023-12-13 23:15:06" 的时间戳。

使用 `--log-date-format` 选项能够在分析日志时提供更精确的时间信息，特别是当你需要对事件发生的时间序列进行详细审查时。这可以帮助开发人员和测试人员快速定位问题发生的时间点，并与其他系统或日志条目进行对比。



### 3.2.7.4 参数 --log-cli-level=LOG_CLI_LEVEL

`pytest` 的`--log-cli-level=LOG_CLI_LEVEL` 是 `pytest` 测试框架的一个命令行选项，它允许你为控制台日志输出设置特定的日志级别。`LOG_CLI_LEVEL` 是你希望 `pytest` 将日志记录信息输出到控制台的最低级别。

日志级别按照紧急程度从低到高排列如下：

- `DEBUG`: 用于详细的诊断信息。
- `INFO`: 用于确认程序按预期运行。
- `WARNING`: 某些未预期的事件发生，软件还是正常运行，但这可能会在将来导致问题。
- `ERROR`: 由于某些更严重的问题，软件已经不能执行某些功能了。
- `CRITICAL`: 严重错误，表明程序可能无法继续运行。

这个选项的一般用途是在运行测试时，能够直接在控制台上看到日志，而不需要查看日志文件。这对于调试或者实时监控测试进度非常有用。

举例来说，如果你想要在控制台上显示所有的 `WARNING` 级别及以上的日志消息，你可以这样运行 `pytest`：

```shell
pytest --log-cli-level=WARNING
```

这意味着所有 `WARNING`、`ERROR` 和 `CRITICAL` 级别的日志消息将会显示在控制台上，而 `DEBUG` 和 `INFO` 级别的消息不会显示。

如果你想看到所有级别的日志消息，也可以这样设置：

```shell
pytest --log-cli-level=DEBUG
```

在这种情况下，所有级别的日志消息都会在控制台输出。

这个选项在调试复杂的测试场景或者实时跟踪测试执行过程中特别有用，因为它允许开发者和测试者根据需要进行适当级别的日志输出调整。




### 3.2.7.5 参数 --log-cli-format=LOG_CLI_FORMAT

`pytest` 的`--log-cli-format=LOG_CLI_FORMAT` 是用来自定义 `pytest` 在控制台中输出日志格式的命令行选项。通过这个选项，你可以控制日志消息的布局，从而满足你对日志输出格式的具体需求。

在 `LOG_CLI_FORMAT` 中，你可以包含一系列的占位符变量，这些变量在输出时会被日志记录的具体信息替换。以下是一些常用的占位符和它们的含义：

- `%(asctime)s`: 输出日志记录的时间。
- `%(levelname)s`: 输出日志记录的等级（如 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`）。
- `%(message)s`: 输出日志消息本身。
- `%(filename)`: 输出源文件的名称。
- `%(funcName)`: 输出日志消息所在的函数名称。
- `%(lineno)`: 输出日志消息发出的代码行号。

例如，如果你希望自定义的日志格式包含时间戳、日志级别和消息本身，你可以在命令行中使用如下格式：

```shell
pytest --log-cli-format="%(asctime)s %(levelname)s: %(message)s" --log-cli-level=INFO
```

假设你还希望包含产生日志消息的源代码文件和行号，格式可以是：

```shell
pytest --log-cli-format="%(asctime)s %(levelname)s [%(filename):%(lineno)]: %(message)s" --log-cli-level=INFO
```

这么做之后，每当 `pytest` 输出日志到控制台时，它就会遵循指定的格式。这对于需要特定格式来进行日志分析或需要与其他日志系统集成的情况非常有用。

该选项特别有助于调试测试代码，因为你可以轻松调整显示给定测试中需要关注的特定信息。此外，当你正在开发测试或在持续集成环境中运行测试时，格式化的日志输出也能提供清晰的视觉线索，帮助快速定位问题。




### 3.2.7.6 参数 --log-cli-date-format=LOG_CLI_DATE_FORMAT

`pytest` 的`--log-cli-date-format=LOG_CLI_DATE_FORMAT` 是 `pytest` 测试框架的命令行选项之一，用于指定控制台日志时间戳的格式。这对于任何需要定制日志时间输出格式的情况很有帮助，特别是在生成的日志需要按特定格式进行解析或查看时。

在 `LOG_CLI_DATE_FORMAT` 中，你可以使用 `datetime` 模块中的格式代码来定义时间的显示方式。这些格式化代码允许你设置具体的日期和时间显示格式，比如年、月、日、小时、分钟和秒。

举例来说，如果你想要在控制台日志中只显示小时和分钟，则可以设置为：

```shell
pytest --log-cli-date-format="%H:%M"
```

这会导致日志消息中的时间戳仅显示小时和分钟，例如“21:51”。

如果你想要一个更详细的时间戳，包括年、月、日、小时、分钟和秒，则可以设置为：

```shell
pytest --log-cli-date-format="%Y-%m-%d %H:%M:%S"
```

这会导致日志消息中的时间戳显示为“2023-12-14 21:55:30”这样的格式。

这是 `datetime` 中常用的一些格式代码示例：

- `%Y`: 四位数的年份，例如 “2023”。
- `%m`: 月份（01至12）。
- `%d`: 一个月中的第几天（01至31）。
- `%H`: 24小时制的小时（00至23）。
- `%M`: 分钟（00至59）。
- `%S`: 秒（00至59）。

通过约定的格式代码，你可以按照需求制定几乎任何想要的日期时间格式。使用这个命令行选项可以帮助提高日志信息的可读性或确保它们与外部系统兼容。




### 3.2.7.7 参数 --log-file=LOG_FILE

`pytest` 的 `--log-file=LOG_FILE` 是一个命令行选项，它指示 `pytest` 将日志输出到一个文件中，而不是标准的输出（控制台）。使用这个选项，你可以指定日志文件的路径和文件名，保存测试运行的日志记录供后续分析或查阅时使用。

在这个命令中 `LOG_FILE` 占位符应该被替换为实际的文件名或文件路径。例如：

```shell
pytest --log-file=pytest_autotest.log
```

上面的命令会创建（如果还不存在的话）或重写（如果已经存在）一个名为 `pytest_autotest.log` 的文件，并且会把所有的日志输出都写入这个文件。

你也可以包含文件路径，以便指定日志文件应该被保存到哪里：

```shell
pytest --log-file=logs/pytest_autotest.log
```

如果你同时使用了 `--log-file` 和日志级别选项（比如 `--log-file-level`），你可以进一步控制记录到文件的日志详细程度。以下命令会将日志级别设置为 `INFO`，这意味着所有 `INFO` 级别及以上的日志消息（`WARNING`, `ERROR`, `CRITICAL`）将会被写到指定的日志文件中：

```shell
pytest --log-file=pytest_autotest.log --log-file-level=INFO
```

这个功能可以与其他有关日志的命令行选项一起使用，如 `--log-cli-level`（用于控制命令行的日志级别），`--log-file-format`（用于控制写入日志文件的格式），以及 `--log-file-date-format`（用于控制写入日志文件的日期格式）等。

**请注意：**

如果你在没有相应权限的目录里指定日志文件，或者如果磁盘空间不足，`pytest` 可能无法创建或写入日志文件，这将导致错误，请确保你有权限在指定的目录中创建文件。



### 3.2.7.8 参数 --log-file-level=LOG_FILE_LEVEL

`pytest` 的 `--log-file-level=LOG_FILE_LEVEL`是`pytest`命令行的一个选项，它允许你指定日志文件的日志记录级别。测试过程中会产生很多日志消息，它们分为不同的级别，如：DEBUG, INFO, WARNING, ERROR, 和 CRITICAL。通过设置`LOG_FILE_LEVEL`，你可以筛选出只有某个级别或者更高级别的日志消息会被记录到日志文件中。

`LOG_FILE_LEVEL`是一个占位符，你应该用某个具体的日志级别来替换它，如下面这些：

- `DEBUG`: 提供详细的信息，通常只在诊断问题时有用。
- `INFO`: 确认程序按预期运行。
- `WARNING`: 表示有一些意外情况，或者在近期需要注意的问题。
- `ERROR`: 表示有更严重的问题，程序的某些功能没有正常执行。
- `CRITICAL`: 表示非常严重的问题，程序无法执行。

例如，如果你只希望将错误级别及以上的消息记录到日志文件中，可以使用以下命令：

```shell
pytest --log-file-level=ERROR
```

这会记录所有的`ERROR`级别和`CRITICAL`级别的日志消息到日志文件中，而忽略`WARNING`、`INFO`和`DEBUG`级别的消息。

需要注意的是，`--log-file-level`选项通常与`--log-file`选项一起使用，用来指定输出日志的文件。如果没有同时指定`--log-file`，那么`--log-file-level`将不会产生任何影响，因为不会有日志文件来记录日志。像这样使用：

```shell
pytest --log-file=logs/pytest_autotest.log --log-file-level=ERROR
```

上述命令不仅设置了日志文件的位置和名称（`pytest_autotest.log`），还指定了日志文件中所记录消息的最低日志级别（`ERROR`）。这意味着只有`ERROR`级别和`CRITICAL`级别的消息会被写入到`pytest_autotest.log`中。



### 3.2.7.9 参数 --log-file-format=LOG_FILE_FORMAT

`pytest` 的 `--log-file-format=LOG_FILE_FORMAT` 是一个命令行选项，它允许你为`pytest`生成的日志文件自定义消息格式。通过这个选项，你可以控制日志消息的结构和内容，以便于后续分析或者仅仅是为了便于阅读。

`LOG_FILE_FORMAT` 是一个占位符，你需要将其替换为实际的格式字符串。格式字符串可以使用各种预定义的变量，像时间戳、日志级别、消息本身等。以下是一些常用的格式变量：

- `%(asctime)s` - 日志事件发生的时间
- `%(levelname)s` - 日志消息的级别（例如：DEBUG, INFO, WARNING, ERROR, CRITICAL）
- `%(message)s` - 日志消息字符串
- `%(filename)s` - 产生日志消息的源文件名
- `%(lineno)d` - 日志消息产生的代码行号

你可以自由地组合这些变量来构建自己需要的日志格式。比如：

```shell
pytest --log-file=pytest_autotest.log --log-file-format="%(asctime)s - %(levelname)s - %(message)s"
```

上述命令中，日志文件将包含时间戳、日志级别和日志消息这三个元素。生成的日志文件中的每条消息都会按照这个格式来记录。

完整的日志消息格式可能看起来像这样：

```shell
2023-12-14 23:10:00,000 - INFO - This is an information message
2023-12-14 23:10:01,234 - WARNING - This is a warning message
2023-12-14 23:10:02,345 - ERROR - This is an error message
```

这个格式化功能不仅可以让你选择性地包含对你有用的信息，还可以帮助你调整日志消息的顺序或者匹配监控系统或日志分析工具的需要。




### 3.2.7.10 参数 --log-file-date-format=LOG_FILE_DATE_FORMAT

`pytest`的 `--log-file-date-format=LOG_FILE_DATE_FORMAT` 允许用户自定义日志文件中的时间戳格式。当你设置了自定义的日志消息格式，并且在其中包含了时间戳时（通常使用 `%(asctime)s` 变量），你可以用这个选项指定日期和时间应该如何显示。

`LOG_FILE_DATE_FORMAT` 是一个占位符，你需要将它替换为一个具体的日期时间格式字符串。这个字符串应该符合Python的`datetime.strftime()`方法能够理解的格式。

日期时间格式字符串可以包含以下占位符：

- `%Y`: 四位数年份（例如：2023）
- `%m`: 月份（01至12）
- `%d`: 月份中的日子（01至31）
- `%H`: 小时（24小时制，00至23）
- `%M`: 分钟（00至59）
- `%S`: 秒（00至59）

例如，如果你希望设置一个年-月-日 时:分:秒的格式，可以使用以下的命令：

```shell
pytest --log-file=test_log.txt --log-file-format="%(asctime)s - %(levelname)s - %(message)s" --log-file-date-format="%Y-%m-%d %H:%M:%S"
```

使用上述命令时，日志文件 `test_log.txt` 中的时间戳将按照指定的日期时间格式显示。为了解释清楚，日志文件中的条目可能如下所示：

```shell
2023-12-14 23:30:59 - INFO - This is an information message
2023-12-14 23:31:00 - WARNING - This is a warning message
2023-12-14 23:31:01 - ERROR - This is an error message
```

这个选项对于想要根据个人偏好或特定需求（如与其他日志系统兼容）来配置日志文件非常有用。你可以根据需要选择合适的日期和时间格式，以便你的日志文件更加易于阅读和分析。




### 3.2.7.11 参数 --log-auto-indent=LOG_AUTO_INDENT

`pytest`的 `--log-auto-indent=LOG_AUTO_INDENT` 用于配置日志输出时的自动缩进功能，此设置有助于提高日志的可读性，尤其是在处理嵌套的日志消息时。

`LOG_AUTO_INDENT` 参数可以设置为以下几种类型的值：

* `on` 或 `true`: 启用自动缩进。这会使得每个缩进级别的日志消息相对于上一级别自动缩进一些额外的空格。
* `off` 或 `false`: 禁用自动缩进。所有的日志消息都将从新行的开始处打印出，不会有额外的缩进。
* 一个正整数: 指定缩进的具体空格数。这样，每增加一个缩进级别，日志消息将向右额外缩进指定数目的空格。

例如，使用命令行启用自动缩进功能，你可以这样设置：

```shell
pytest --log-auto-indent=on
```

或者，你可以指定每个缩进级别4个空格：

```shell
pytest --log-auto-indent=4
```

当启用该功能时，如果你的测试日志有递归或者层次结构的信息，比如测试套件内嵌套的测试函数，启用自动缩进将使得日志文件更容易被人理解，层次关系也更加清晰。




### 3.2.7.12 参数 --log-disable=LOGGER_DISABLE

`pytest` 的`--log-disable=LOGGER_DISABLE` 参数用于在运行 `pytest` 时临时禁用特定的日志记录器（logger）。本质上，这个选项可以用来控制哪些日志记录器的输出不应该显示在 `pytest` 的日志输出中。`LOGGER_DISABLE` 占位符应替换为你想要禁用的日志记录器的名称。

在大型软件项目中，日志输出可能来自多个地方，如不同的模块或者第三方库。有时候，你可能想要关闭某个特定日志记录器的日志显示，这可以通过 `--log-disable` 选项来实现。

例如，假设你有一个名为 `mysql.database` 的日志记录器，打印与数据库操作相关的日志，但在运行测试的时候你不想看到这部分的日志输出，你可以在 `pytest` 命令中这样指定：

```shell
pytest --log-disable=mysql.database
```

这条命令会禁止 `mysql.database` 日志记录器的所有日志输出。如果你想要同时禁止多个日志记录器，可以多次使用这个命令行选项。

需要指出的是，这个命令行选项对日志记录器的禁用是临时的，只影响当前的`pytest` 测试会话。一旦测试会话结束，日志记录器的状态会恢复到测试运行前的状态。

在使用这个选项时，应确保提供的日志器名称与代码中用于创建和使用日志记录器的名称一致。如果名称不匹配，`pytest` 将无法正确禁用相应的日志输出。



## 3.2.8 [pytest] ini-options 相关参数

这里涉及`pytest.ini|tox.ini|setup.cfg|pyproject.toml`几个文件，此处只介绍参数使用方法，对于几种配置文件的介绍，请参考本书《pytest配置文件》章节内容。


### 3.2.8.1 参数 markers (linelist)

在`pytest`中，标记（markers）是关键特性之一，它允许用户通过自定义的标记来分类测试。这种分类可以用于指定运行哪些测试，或者是在测试用例上附加额外的信息。

`pytest.ini`是`pytest`用来读取项目级别配置的文件。在`pytest.ini`文件中，可以使用`markers`部分来声明项目中将使用的标记。这样做的好处是可以避免在没有事先声明的情况下使用标记，从而引发警告信息。

以下是`pytest.ini`文件的一个例子，其中包含了一个`markers`部分（linelist【行列表】标识这些标记定义是列表格式，每行一个标记），参考如下：

```ini
# pytest.ini
[pytest]
markers =
    slow: mark tests as slow to run.
    smoke: smoke tests cover the main functionality of the program.
    serial: mark tests that should be run serially and not in parallel.
```

在上面的例子中，定义了三个标记：

- `slow`: 这个标记用来标识运行时间较长的测试，或执行缓慢的测试。
- `smoke`: 这个标记用来标识冒烟测试，通常是用来快速检查程序主要功能是否正常的测试。
- `serial`: 这个标记用来标识那些应该顺序执行而不是并行执行的测试。这可能是由于这些测试不能并行运行（例如，它们可能共享某些状态，或者它们可能与特定的资源交互，这个资源不能同时由多个测试访问）。

在测试代码中，可以使用`@pytest.mark.NAME`装饰器来应用一个标记，如：

```python
root@Gavin:~/code/chapter1-3# cat test_mark.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import time
import pytest


@pytest.mark.slow
def test_slow_example():
    time.sleep(30)
    pass  # long running test code
root@Gavin:~/code/chapter1-3
```

随着标记的声明，你现在可以使用`pytest -m NAME`来运行所有带有特定标记的测试，例如，要运行所有标记为慢运行的测试，可以运行：

```shell
pytest -m slow
```

声明标记不仅有助于抑制在没有定义的情况下使用标记的警告，而且也是向新开发人员说明项目中使用了哪些标记的一种方式。这创建了一个自文档化的测试套件，有助于理解特定测试的意图和分类。



### 3.2.8.2 参数 empty_parameter_set_mark (string)

在`pytest`的配置文件`pytest.ini`中，`empty_parameter_set_mark`是一个配置选项，它允许你指定当参数化测试(`@pytest.mark.parametrize`)没有参数值时如何处理。在默认情况下，如果参数化的数据集为空，`pytest`将不会运行该测试并抛出一个警告，因为没有提供任何用于测试的参数集。

通常，参数化测试预期至少应具有一组参数以供测试使用。然而，在某些情况下，参数集可能基于某些条件动态生成，其中一些条件可能导致没有参数集。在这种情况下，使用`empty_parameter_set_mark`可以控制`pytest`对这种情况的处理。

例如，你可以在`pytest.ini`文件中这样设置：

```ini
# pytest.ini
[pytest]
empty_parameter_set_mark = skip
```

这个配置将指示`pytest`跳过那些参数集为空的测试，而不是抛出警告。当配置为`skip`时，如果遇到参数化装饰器没有提供任何参数的情况，`pytest`将自动跳过相关的测试函数。

`empty_parameter_set_mark`选项可以设置为以下值之一：

- `skip`: 跳过没有参数的测试。
- `xfail`: 将没有参数的测试标为预期失败（expected fail）。
- `fail`: 强制失败，如果一个测试的参数集为空，则测试将立即失败。

当然，你也可以省略这个选项。如果不在配置文件中显式设置`empty_parameter_set_mark`，`pytest`会采用默认行为，即在没有提供参数集的情况下发出警告。

在选择如何配置这个选项时，请考虑你的测试策略和特定的用例，以便选择最适合你项目的处理方式。



### 3.2.8.3 参数 norecursedirs (args)

在`pytest`中，`norecursedirs`是`pytest.ini`文件里的一个配置项，用来指定那些不应被`pytest`递归搜索测试文件的目录。当`pytest`启动时，它会查找并收集测试可运行的文件，但有时你可能不希望`pytest`查看某些特定目录，例如，这些目录可能包含环境文件、备份、非测试代码等。

`norecursedirs`配置项的参数是一系列使用空格分隔的目录名（相对于项目根目录的路径）。`pytest`将忽略列表清单中的目录，不会在其中寻找测试代码。

这是`pytest.ini`中如何设置`norecursedirs`的例子：

```ini
# pytest.ini
[pytest]
norecursedirs = .git .tox .env _build tmp*
```

在上面的例子中：

- `.git`：通常是Git版本控制系统的隐藏文件夹，包含版本控制信息，你不希望`pytest`在这里搜索测试代码。
- `.tox`：典型的`tox`虚拟环境文件夹，通常包含虚拟环境设置的测试副本，无需由`pytest`进行测试搜索。
- `.env`：可能是虚拟环境的文件夹或包含环境变量的文件。
- `_build`：构建目录，可能是持续集成或文档生成时使用的目录。
- `tmp*`：这是一个通配符模式，`pytest`将忽略所有以`tmp`开头的目录。

当`pytest`运行时，它默认递归项目的所有目录来寻找测试文件，但如果在`norecursedirs`中指定了目录，`pytest`则会跳过这些目录。这可以提高测试收集的速度并避免不必要的搜索。




### 3.2.8.4 参数 testpaths (args)

在 `pytest` 中，`testpaths` 是 `pytest.ini` 配置文件中的一个选项，它用来指定 `pytest` 在测试收集阶段应当搜索测试用例的路径。当你用 `pytest` 运行测试时，它会在项目的目录结构中寻找测试文件，默认情况下会搜索整个项目。不过，如果你只想让 `pytest` 搜索特定的目录来收集测试，你就可以使用 `testpaths` 来限制搜索范围。

`testpaths` 配置项的参数是一系列目录名，这些目录名以空格分隔并且相对于项目的根目录。指定 `testpaths` 后，`pytest` 只会在这些目录中搜索测试文件。

以下是 `pytest.ini` 配置文件中 `testpaths` 选项的一个例子：

```ini
# pytest.ini
[pytest]
testpaths = prepare src
```

在此例中，`testpaths` 配置告诉 `pytest` 只在项目根目录下的 `prepare` 文件夹和 `src` 文件夹内搜索测试用例。这意味着任何不在这两个目录下的 Python 文件不会被当作测试文件来执行。

如果你的项目结构非常复杂，或者测试文件分散在不同的目录中，`testpaths` 可以帮助你准确地指向测试代码所在的位置。这样，你可以减少测试收集阶段的时间，并确保只有真正的测试代码被执行。这一选项对大型项目或包含多个子项目的仓库尤其有用，因为它允许你精确控制测试运行的范围。




### 3.2.8.5 参数 filterwarnings (linelist)

在 `pytest` 配置文件 `pytest.ini` 中，`filterwarnings` 选项允许你控制警告信息的显示。Python 的警告系统是一个内建的机制，用以告知开发者某些情况需要注意，但并非错误。然而，在运行测试时，某些警告可能会分散你的注意力，或者你可能想要专门处理某些类型的警告。

`filterwarnings` 选项接受一个“行列表”（linelist），每行都定义了一个警告过滤规则。这些规则使用与 Python `warnings` 模块相同的语法。

每个过滤规则的结构通常是：

```
action:message:category:module:lineno
```

其中：

- `action` 是要对符合以下规则的警告执行的行为，比如 `ignore`、`error`、`always`、`default`、`module` 或 `once`。
- `message` 是警告消息的正则表达式。如果留空，则表示对所有消息进行操作。
- `category` 是警告的类别，例如 `DeprecationWarning`、`UserWarning` 等。如果留空，则表示对所有警告类别应用这个操作。
- `module` 是生成警告的模块的正则表达式。如果留空，规则将适用于任何模块。
- `lineno` 是引发警告的代码行号，可以为一个数字或留空以适用于所有行。

在 `pytest.ini` 中使用 `filterwarnings` 选项的示例：

```ini
# pytest.ini
[pytest]
filterwarnings =
    error
    ignore::UserWarning
    ignore:functional.*:DeprecationWarning
    always::DeprecationWarning:module_of_interest
```

在上面的例子中，规则如下：

- `error`：把所有警告都转换为错误。
- `ignore::UserWarning`：忽视所有 `UserWarning` 类别的警告。
- `ignore:functional.*:DeprecationWarning`：忽视模块名匹配正则表达式 `functional.*` 的所有 `DeprecationWarning` 类别警告。
- `always::DeprecationWarning:module_of_interest`：始终显示 `module_of_interest` 模块中发出的 `DeprecationWarning` 类别的警告。

这样，你可以通过 `pytest.ini` 文件中的 `filterwarnings` 选项来自定义你的测试环境，无需修改代码即可控制或重定向警告输出。




### 3.2.8.6 参数 usefixtures (args)

在 `pytest` 中，`usefixtures` 是一个配置选项，它可以在 `pytest.ini` 文件中使用，来指定一个或多个 `fixture`（测试前置条件/测试夹具），这些 `fixture` 将被自动应用到所有测试用例中。使用 `usefixtures` 选项能够确保特定的 `setup` 代码在每个测试用例之前自动运行，而无需在每个测试函数中显式地请求它们。

这个设置对于需要在多个测试用例中应用相同前置条件的情况非常有用。`usefixtures` 选项可以减少重复代码，并确保一致的测试环境。

这是如何在 `pytest.ini` 文件中设置 `usefixtures` 选项的一个例子：

```ini
# pytest.ini
[pytest]
usefixtures = fixture1 fixture2
```

在上述配置中，`fixture1` 和 `fixture2` 是定义在测试代码中的 `fixture` 函数的名称。当设置了 `usefixtures` 后，`pytest` 会在执行每个测试用例之前自动调用这些 `fixture`。

请注意，虽然使用 `usefixtures` 选项便于全局应用 `fixture`，但它也可能引起混淆，特别是在大型的测试代码库中，因为在查看单个测试用例的代码时，可能不清楚是什么在背后自动应用了这些 `fixture`。因此，明确在测试函数或类中使用装饰器 `@pytest.mark.usefixtures(...)` 来声明使用的 `fixture` 可能更清晰易懂。

下面是如何在单个测试函数或测试类中应用相同的 `usefixtures`：

```python
root@Gavin:~/code/chapter1-3# cat test_use_fixtures.py 
#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pytest


@pytest.fixture()
def fixture1():
    """  This is a fixture1 example  """
    print("I'm fixture1")
    yield
    print("End of fixture1")


@pytest.fixture()
def fixture2():
    """  This is a fixture2 example  """
    print("I'm fixture2")
    pass


@pytest.mark.usefixtures("fixture1", "fixture2")
def test_example():
    print("Function of test_example")

@pytest.mark.usefixtures("fixture1", "fixture2")
class TestClass:
    def test_method1(self):
        print("Class method test case")
root@Gavin:~/code/chapter1-3#
```

需要注意的是，当在 `pytest.ini` 中全局使用 `usefixtures` 时，它适用于所有的测试，而使用装饰器的方式则提供了更细粒度的控制。



### 3.2.8.7 参数 python_files (args)

在 `pytest.ini` 配置文件中，`python_files` 参数指定了哪些文件被视为测试文件。`pytest` 会自动发现具有特定模式名的测试文件，并在其中寻找测试用例。默认情况下， `pytest` 会认为名称命名方式为 `test_*.py` 或 `*_test.py` 的文件为测试文件。

但是，有时你可能想要修改这个默认行为，以包含其他模式的文件。此时，你可以在 `pytest.ini` 文件中使用 `python_files` 参数来设置文件发现的模式。

以下是一个如何在 `pytest.ini` 中设置 `python_files` 参数的示例：

```ini
# pytest.ini
[pytest]
python_files = test_*.py *_test.py example_*.py
```

在上述配置中，`python_files` 参数被设置为一个空格分隔的列表，其中包含三个模式：

- `test_*.py`: 匹配任何以 `test_` 开头，以 `.py` 结尾的文件。
- `*_test.py`: 匹配任何以 `_test.py` 结尾的文件。
- `example_*.py`: 匹配任何以 `example_` 开头，以 `.py` 结尾的文件。

这意味着除了默认的测试文件命名模式之外，`pytest` 还会将任何文件名匹配 `example_*.py` 模式的文件当做测试文件，从而增加了测试文件的灵活性。

要使用这项配置，请确保你的 `pytest.ini` 文件位于项目根目录或测试目录中，这样 `pytest` 运行时才能正确地加载和应用配置。如果你有特定的测试目录结构或命名约定，调整 `python_files` 参数会非常有用。



### 3.2.8.8 参数 python_classes (args)

在`pytest`中，`python_classes`参数用于指定测试类的名称模式。默认情况下，`pytest`会收集以`Test`开头的类中的测试方法。

有时候，你可能想要自定义这个行为，以适应你的项目中的命名约定。使用`python_classes`配置选项，你可以告诉`pytest`哪些类应该被考虑为包含测试的类。

以下是如何在`pytest.ini`中设置`python_classes`参数的一个例子：

```ini
# pytest.ini
[pytest]
python_classes = *Suite Test*
```

在这个配置中：

- `*Suite`: 选取以`Suite`结尾的所有类。
- `Test*`: 选取以`Test`开头的所有类。

配置选项`python_classes`接受一个空格分隔的字符串列表，列表中的每个字符串用作类名称的匹配模式。只有与这些模式之一匹配的类中的测试方法才会被收集和执行。

这种配置方式增加了命名测试类的灵活性，并允许开发者根据自己的项目或团队的命名习惯来组织测试代码。

**请注意：**

`python_classes`配置选项的作用域是全局的；一旦在`pytest.ini`中设置了该选项，它将适用于整个项目的测试收集。因此，请在调整此设置时仔细权衡，以确保它不会意外排除应该被运行的测试。




### 3.2.8.9 参数 python_functions (args)

在`pytest`框架中，`python_functions` 配置选项用于定义哪些函数应被认为是测试函数。`pytest`默认会识别以 `test` 开头的函数为测试用例。

如果你希望自定义识别测试函数的命名模式，可以在 `pytest.ini` 文件中使用 `python_functions` 参数。下面是一个 `pytest.ini` 文件中 `python_functions` 参数的配置示例：

```ini
# pytest.ini
[pytest]
python_functions = test_* check_*
```

在这个例子中：

- `test_*`: 表示任何以 `test_` 开头的函数都是测试函数。
- `check_*`: 表示任何以 `check_` 开头的函数也被视作测试函数。

配置项 `python_functions` 接受一个空格分隔的字符串列表，列表中每个字符串都是一个匹配模式，用于识别测试函数。当 `pytest` 运行时，它会根据这些模式来收集测试用例。

这样的配置使得你可以非常灵活地定义自己的测试函数命名规范，以适应不同的项目或个人习惯。

**请注意：**

`pytest.ini` 应该位于项目的根目录中，以便`pytest`可以在启动时自动检测和应用这些配置。更改 `python_functions` 设定后，会影响整个项目中测试用例的识别行为，所以请确保新的模式不会排除任何应当执行的测试。




### 3.2.8.10 参数 disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool)

`pytest.ini` 中的 `disable_test_id_escaping_and_forfeit_all_rights_to_community_support` 是一个非常特别和较少使用的配置选项。顾名思义，这个设置有两个作用：

* 它禁用了 `pytest` 中用于测试ID的特殊字符转义。
* 正如它字面上的警告，使用这个选项可能会让你放弃在社区寻求支持的权利。

通常情况下，`pytest` 会自动转义测试ID中的某些特殊字符。测试ID是由 `pytest` 创建的，用于唯一标识测试用例的字符串。由于某些字符在命令行或其他上下文中可能有特殊意义，`pytest` 默认会对这些字符进行转义。

在极少数情况下，用户可能不希望 `pytest` 进行这种转义。例如，如果用户有非常具体的测试ID命名需求，且确信转义操作会影响到他们工作流程的某些部分，可以使用此选项禁止这种行为。

下面是 `pytest.ini` 文件中设置此选项的例子：

```ini
# pytest.ini
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true
```

这里，如果设置为 `true`，这个选项就会禁用测试ID的转义。

但是，如此直白的选项名字暗示了使用这个选项的潜在后果。`pytest`开发者在提供这一功能的同时表态说，如果你决定使用这个高级且不常规的特性，那么你可能就不能再依靠官方社区支持。也就是说，如果关闭了这个转义功能引起了其他问题，社区可能不会提供帮助。

因此，除非你非常清楚自己在做什么，并且能够自行解决可能出现的任何问题，否则最好不要更改这个配置选项。




### 3.2.8.11 参数 console_output_style (string)

`pytest.ini` 文件中的 `console_output_style` 配置选项允许用户自定义 `pytest` 的控制台输出样式。`pytest `提供了不同的输出样式，这可以帮助开发者以最适合他们的方式查看测试结果。

这个选项通常有以下几个可用的值：

* `classic`：这是最传统的输出样式，提供了基本的，行为行的输出，每个测试结果都简洁地列在一行上。
* `progress`：进度样式输出提供了一个进度条，显示了测试进程的概况。在进度条下方，它会输出失败的测试以供调试。
* `count`：计数样式只会显示测试的总数和到目前为止完成的测试数。
* `progress-even-when-capture-no`：此参数在`pytest 7.3.0 (2023-04-08)`引入，我们知道`--capture=no`会提升性能，启用此选项后，强制使用进度输出，即使捕获被禁用（`--capture=no`）。这在大型测试套件中非常有用，因为捕获(`--capture=yes`)可能会对性能产生重大影响。

下面是如何在 `pytest.ini` 文件中设置 `console_output_style` 选项的例子：

```ini
# pytest.ini
[pytest]
console_output_style = progress
```

在这个例子中，`console_output_style` 被设置为 `progress`，这意味着在运行测试时，`pytest` 将会以进度样式显示输出。

选择哪种样式取决于你的个人喜好或者团队的规定。一些开发者可能喜欢更多的视觉反馈，而另一些可能喜欢更简洁的输出。`console_output_style` 选项使得 `pytest` 能够更灵活地适应不同用户的需求。

**请注意：**

这个设置可能不会改变所有输出的详细程度，例如详细的错误报告。还有可能在未来的 `pytest` 版本中引入新的样式选项，所以建议查阅最新的 `pytest` 文档以获取当前支持的样式列表。




### 3.2.8.12 参数 xfail_strict (bool)

`pytest.ini` 文件中的 `xfail_strict` 配置选项是与 `pytest` 中的 "expected failures" (标记为 `xfail`) 测试相关的设置。该选项控制着标有 `xfail` 装饰器的测试用例的行为。在默认情况下，即 `xfail_strict` 为 `false` 时，如果一个标记为 `xfail` 的测试意外地通过了（即，并没有如预期失败），`pytest` 会将这个测试用例标记为 `XPASS`（意外通过），但不会把它视为测试失败。然而，如果开发者希望强制所有标记为 `xfail` 的测试严格按照预期来执行，即如果这些测试用例通过了就应该被视为一个错误，则可以将 `xfail_strict` 设置为 `true`。

当 `xfail_strict` 被设为 `true` 时，任何标记为 `xfail` 并且通过的测试都会在测试摘要中被报告为失败（`FAILED`），因为它们并没有表现出期望中的失败行为。

在 `pytest.ini` 文件中设置 `xfail_strict` 选项的格式如下：

```ini
# pytest.ini
[pytest]
xfail_strict = true
```

使用这个选项有助于确保测试结果与预期的一致，并可能揭露一些意料之外的问题，例如可能原本被认为是错误的代码实际上已被修复。这个选项通常用于强化测试流程，确保所有失败的测试都得到适当的关注和处理。

再次提醒，务必谨慎使用 `xfail_strict`，因为它可以改变测试套件的失败/成功逻辑。只有当你确实需要所有预期失败的测试严格执行失败时，才应该启用这个选项。



### 3.2.8.13 参数 tmp_path_retention_count (string)

`pytest.ini` 文件中的 `tmp_path_retention_count` 配置选项是与 `pytest` 中的临时文件和目录管理相关的。`pytest` 提供了一个功能，允许在测试过程中创建临时文件和目录。这些临时文件夹通常是在 `pytest` 测试会话结束时自动删除的，可确保不会留下任何垃圾数据。然而，有时候开发者可能希望保留这些临时文件夹，以便对失败的测试进行后续分析。`tmp_path_retention_count` 选项就是用来设置要保留的最近几个临时目录的数量。

更具体来说，此选项允许你指定一个数字，表示当你再次运行测试时，将保留多少个最新的临时目录。旧的临时目录将根据这个数字被删除，以确保不会占用太多的磁盘空间。

例如，在 `pytest.ini` 文件中可以这样设置 `tmp_path_retention_count` 选项：

```ini
# pytest.ini
[pytest]
tmp_path_retention_count = 3
```

在这个例子中，`pytest` 将保留最新的3个临时目录，其它旧的临时目录在新的测试运行开始时将被删除。

依然以文件`chapter1-3/test_tmp_path.py`为示例，执行如下命令：`pytest -s -v chapter1-3/test_tmp_path.py`，则会在测试输出中看到类似下面的路径：

```shell
/tmp/pytest-of-<username>/pytest-<session-id>/test_create_file0/
```

这个路径里：

- `pytest-of-`表示临时目录属于哪个用户。
- `pytest-`表示当前会话的ID，它在每次调用`pytest`时是唯一的，默认从0逐渐递增+1。
- `test_create_file0`表示这是第一个`test_create_file`函数的临时目录。

比如：

```shell
/tmp/pytest-of-root/pytest-0/test_create_file0  # 第一次执行
/tmp/pytest-of-root/pytest-1/test_create_file0  # 第二次执行
/tmp/pytest-of-root/pytest-2/test_create_file0  # 第三次执行
```

执行了三次，产生了三个临时目录，当第四次执行的时候，`pytest-0`被删除，`pytest-3`产生，以此类推。




### 3.2.8.14 参数 tmp_path_retention_policy (string) 

根据测试结果，由参数`tmp_path_retention_policy`控制 `tmp_path` 固件创建的目录是否保留。

这个选项通常有以下几个可用的值：

* all：保留所有测试的目录，无论结果如何（默认：all）。
* failed： 只为结果为错误或失败的测试保留目录。
* none：每次测试结束后，无论结果如何，都会删除目录。

在 `pytest.ini` 文件中设置 `tmp_path_retention_policy ` 选项的格式如下：

```shell
[pytest]
tmp_path_retention_policy = "failed"
```

合理使用这个选项有助于简化临时目录中测试结果，提升效率。




### 3.2.8.15 参数 enable_assertion_pass_hook (bool)

`pytest_assertion_pass` 是`pytest` 的一个可选钩子（`hook`），你可以在自定义的`pytest`插件中实现这个`hook`功能。当断言通过时，`pytest`会调用这个`hook`。这个功能对于跟踪断言成功的情况特别有用，例如在测试覆盖率分析、断言统计或教学环境中。

默认情况下，这个`hook`是不启用的，因为大多数用户并不需要断言通过的回调，并且启用该`hook`会增加额外的性能开销。如果需要使用，在 `pytest.ini` 文件中设置 `tmp_path_retention_policy ` 明确启用它，选项的格式如下：

```
[pytest]
enable_assertion_pass_hook = true
```

`pytest_assertion_pass`提供了以下参数供实现时使用：

- `item`: 正在执行的测试项对象，你可以使用这个对象获取当前测试的信息，比如它的名称、位置等。
- `lineno`: 是一个整数，表明通过的断言在测试函数中的行号。
- `orig`: 是断言原始的表达式字符串。
- `expl`: 是一个解释字符串，通常是`pytest`转换断言失败后提供的详细输出。

下面是`pytest_assertion_pass`钩子的使用示例（使用断言传递`hook`来计数所有断言）：

```python
# content of conftest.py

assertion_count = 0

def pytest_assertion_pass(item, lineno, orig, expl):
    global assertion_count
    assertion_count += 1


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print(f'\n{assertion_count} assertions tested.')
```

**实现步骤**：

1. 在`conftest.py`中定义`pytest_assertion_pass`函数。
2. 启用`enable_assertion_pass_hook`配置。
3. 运行`pytest`时，每当一个断言通过，`pytest_assertion_pass`函数将被调用。

输出结果示例参考如下(`12 assertions tested.`)：

```shell
____________________________________ test_fail ________________________________

    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

chapter1-3/test_verbosity.py:12: AssertionError

 assertions tested.
========================== short test summary info ==========================
FAILED chapter1-3/test_example.py::test_assert_failed - assert False
FAILED chapter1-3/test_example.py::test_assert_example - assert (5 + 10) == 20
FAILED chapter1-3/test_example.py::test_divide - ZeroDivisionError: division by zero
FAILED chapter1-3/test_example.py::test_output_example - assert 0
FAILED chapter1-3/test_example.py::test_another_example - ValueError: An error occurred.
FAILED chapter1-3/test_parameter_r.py::test_fail - assert 0 == 1
FAILED chapter1-3/test_time1.py::test_day_of_week - assert 3 == 1
FAILED chapter1-3/test_tmp_path.py::test_create_file - assert 0
FAILED chapter1-3/test_verbosity.py::test_fail - assert 1 == 2
== 9 failed, 23 passed, 2 skipped, 3 xfailed, 1 xpassed, 2 warnings in 37.14s ==
root@Gavin:~/code#
```

**请注意**：这个功能在编写解释性的测试或者学习如何编写以及调试测试时很有帮助，但是由于性能的考虑，不建议在常规的测试套件中启用这一`hook`。

如果你是在一个项目中看到这个选项，那么可以寻求该项目的其他成员或文档以了解其确切的用途。




### 3.2.8.16 参数 junit_suite_name (string)

在介绍之前，温馨提醒：

在本章节的`Reporting 相关参数`处有提及两个参数`--junit-xml`  和 `--junit-prefix`， 在使用生成`JUnitXML`报告时，请结合这两个参数使用。

言归正传，`junit_suite_name` 是 `pytest` 的一个配置选项，用于配置生成的 `JUnitXML` 报告中的 `testsuite` 名称。`JUnitXML` 格式被许多持续集成系统（如 Jenkins）识别，因此，该选项对于集成测试结果到这些系统中非常有用。

当你在使用 `pytest` 运行测试并希望生成 `JUnitXML` 格式的测试报告时，可以使用 `--junitxml` 命令行参数。`junit_suite_name` 选项允许你自定义该报告中的 `testsuite` 标签的 `name` 属性。

在 `pytest.ini` 文件中，这个选项的使用可能如下所示：

```ini
[pytest]
junit_suite_name = my_test_suite
```

在上述配置中，`my_test_suite` 将用作测试套件的名字。它会出现在生成的 `JUnitXML` 报告的 `<testsuite>` 标签中的 `name` 属性。如果没有设置这个选项，`pytest` 将使用默认的命名约定，通常是文件路径和参数组合。

举个例子，假设你的测试套件产生的 `JUnitXML` 报告可能包含如下内容：

```xml
<testsuite errors="0" failures="1" name="my_test_suite" skipped="0" tests="10" time="0.123">
    ...
</testsuite>
```

**请注意：**

在这里 `<testsuite>` 标签的 `name` 属性被设置为了 "my_test_suite"，这对于在 CI 系统中区分不同的测试套件来说很有帮助。




### 3.2.8.17 参数 junit_logging (string)

`pytest.ini` 中的 `junit_logging` 选项是用于控制 `pytest` 在生成的 `JUnitXML` 报告中记录日志的详细程度。这个选项接受一些字符串值，指定如何处理测试过程中捕获的日志信息。

在使用 `pytest` 运行测试，并希望生成一个 `JUnitXML` 格式的测试报告时，可以通过 `--junitxml` 命令行参数来指定输出文件。`junit_logging` 选项可以进一步定义这个报告中包含的日志信息的详细程度。

配置值包括：`no|log|system-out|system-err|out-err|all`

- `no`: 默认行为，即不在报告中包含任何额外的日志信息。
- `log`：在报告中仅包含`logging`模块捕获的日志输出。
- `system-out`: 在报告中记录标准输出（`stdout`）内容。
- `system-err`: 在报告中记录标准错误（`stderr`）内容。
- `out-err`：在报告中同时记录包含标准输出(`stdout`)和标准错误(`stderr`)的输出。
- `all`：在报告中包含所有可能的输出（包括`system-out`，`system-err` 和  `log`）。

例如，在 `pytest.ini` 文件中配置 `junit_logging` 选项可能如下：

```ini
[pytest]
junit_logging = system-out
```

上述配置会将所有日志信息归档在每个用例的 `<system-out>` 部分。这意味着在 `JUnitXML` 报告文件中，每个 `<testcase>` 元素可以有一个 `<system-out>` 子元素，包含从该测试用例中捕获的日志输出。这有助于调试失败的测试用例，因为你可以直接在XML报告中查看日志输出。

在生成的 `JUnitXML` 报告文件中，具有日志信息的 `testcase` 元素可能看起来像这样：

```xml
<testcase classname="tests.test_module" name="test_function" time="0.005">
    <system-out><![CDATA[这里是日志输出内容部分]]></system-out>
</testcase>
```

XML 中的 `CDATA` 部分用于确保日志文本不会被错误解释为 XML 标记。



### 3.2.8.18 参数  junit_log_passing_tests (bool)

`junit_log_passing_tests` 是 `pytest.ini` 文件中的一个配置选项，它控制是否应该记录通过的测试用例的日志输出到生成的 `JUnitXML` 报告中。这是一个布尔值设置，可以设置为 `true` 或 `false`。

当你使用 `pytest` 运行测试并通过 `--junitxml` 命令行参数生成 `JUnitXML` 格式的测试报告时，你可能想要记录各个测试（无论是通过还是失败）的日志输出。默认情况下，`pytest` 只记录失败的测试用例的日志输出。如果你希望即使是通过的测试用例，它们的日志输出也被记录在报告中，你可以设置 `junit_log_passing_tests` 选项为 `true`。

在 `pytest.ini` 文件中，`junit_log_passing_tests` 选项的定义如下：

```ini
[pytest]
junit_log_passing_tests = true
```

将此选项设置为 `true` 意味着在 `JUnitXML` 报告的 `<testcase>` 元素中，会包含所有测试用例的日志信息，不管它们是通过了还是失败了。例如，即使一个测试用例通过了，它的日志内容也将包涵在 `<system-out>` 或 `<system-err>` 标签中（取决于 `junit_logging` 设置）。

反之，如果设置为 `false` 或不设置该选项（默认行为），则只有失败的测试用例的日志输出会被记录在 `JUnitXML` 报告文件中。

这项设置对于调试和在持续集成中获取测试信息都很有用，特别是当你希望保留所有测试用例的完整记录时。




### 3.2.8.19 参数 junit_duration_report (string)

`junit_duration_report` 是 `pytest.ini` 配置文件中的一个选项，用于控制在 `JUnitXML` 报告文件中，测试时长信息的记录方式。`junit_duration_report` 选项接受一个字符串值，用于指定如何报告测试持续时间。

以下是 `junit_duration_report` 配置值：

- `call`: 仅报告测试调用阶段（测试函数执行）的持续时间。
- `total`: 报告整个测试阶段（包括测试的设置和拆卸）的总持续时间。

在 `pytest.ini` 文件中配置 `junit_duration_report` 选项的示例如下：

```ini
[pytest]
junit_duration_report = call
```

如果你配置了 `call`，那么在生成的 `JUnitXML` 报告中，每个 `<testcase>` 元素的 `time` 属性将仅反映执行测试本身所花费的时间，不包括设置和拆卸阶段的时间。而如果你设置为 `total`，`time` 属性将包括测试的设置、执行和拆卸阶段的总时长。

例如，如果 `junit_duration_report` 设置为 `call`，对于成功的测试用例，在 `JUnitXML` 报告文件中的 `<testcase>` 元素可能看起来像这样：

```xml
<testcase classname="tests.test_module" name="test_function" time="0.001"/>
```




### 3.2.8.20 参数 junit_family (string)

`junit_family` 是 `pytest.ini` 文件中的一个配置选项，该选项指定生成的 `JUnitXML` 报告的格式版本。不同的持续集成系统要求的 `JUnitXML` 格式可能会有细微差别， `junit_family` 使得 `pytest` 能够生成与这些系统兼容的报告。

以下是 `junit_family` 配置值：

- `xunit1`: 这是一个传统的格式，与 `JUnit 3.x` 系列兼容，也兼容那些期望旧版本格式的工具。
- `xunit2`: 这是更现代的格式，与 `JUnit 4.x/5.x` 系列兼容，提供更丰富的细节信息和特性，并且通常是推荐的选项。
- `xunit_1_0`, `xunit_1_1`, `xunit_1_2`: 在不同的 `pytest` 版本中，这些值代表了介于上述两个主要格式之间的其他变种，它们可能包含或排除一些详细信息。

在 `pytest.ini` 文件中配置 `junit_family` 选项的示例：

```ini
[pytest]
junit_family = xunit2
```

如果你设置为 `xunit2`，生成的 `JUnitXML` 报告将使用 `JUnit 4.x/5.x` 格式，例如：

```xml
<testsuite timestamp="yyyyMMddTHHmmss" name="pytest" tests="N" errors="E" failures="F" skipped="S">
    <testcase classname="test_module" name="test_function" time="0.001">
        ...
    </testcase>
    ...
</testsuite>
```

选择正确的 `junit_family` 值对于确保报告文件被你的 CI 系统正确解析很重要。例如，如果你使用 `Jenkins`，你需要确认你的 Jenkins 插件对哪种格式的 XML 报告支持最好。




### 3.2.8.21 参数 doctest_optionflags (args)

`doctest_optionflags` 是 `pytest.ini` 文件中的一个配置选项，它允许你指定在运行 `doctest`（即那些嵌入在文档字符串中的可执行示例）时应用哪些选项标志。这些标志来自 Python 标准库中的 `doctest` 模块，并且可以控制如何运行和评估文档测试。

在 `pytest` 里使用 `doctest_optionflags` 你可以设定如下几个参数：

- `ELLIPSIS`: 当你在文档测试的输出中使用 `...` 时，允许你省略一些输出，不需要输出完全匹配。
- `IGNORE_EXCEPTION_DETAIL`: 这允许你忽略异常的具体细节，如使用不同版本的 Python 在异常消息中打印不同文本。
- `NORMALIZE_WHITESPACE`: 忽略输出中的空白差异，包括行尾空格和行间的空格数量差异。
- `ALLOW_UNICODE`: 允许在输出中使用 `unicode` 字符，即使 `doctest` 源中没有使用 `unicode` 字符。
- `ALLOW_BYTES`: 允许在输出中使用 bytes 字符。

这些是 `doctest` 模块中定义的一些常用选项标志。

在 `pytest.ini` 文件中配置 `doctest_optionflags` 选项的示例：

```ini
[pytest]
doctest_optionflags = ELLIPSIS NORMALIZE_WHITESPACE
```

这样配置之后，运行 `pytest` 的文档测试时将会自动应用 `ELLIPSIS` 和 `NORMALIZE_WHITESPACE` 这两个选项标志。

**请注意：**参数值应该是通过空格分隔的标志列表，无需添加逗号或其他分隔符。如上面的示例所示，多个标志应该简单地并排书写。

使用 `doctest_optionflags` 能让你的文档测试更加灵活和健壮，尤其是当你的测试需要在不同环境或 Python 版本中执行时。这对于确保文档测试的一致性非常有帮助。同时，这也可以提高测试的可读性，因为你可以使用省略号等标志来避免不必要的输出验证。



### 3.2.8.22 参数 doctest_encoding (string)

`doctest_encoding` 是 `pytest.ini` 文件中的一个配置选项，它用来指定在运行 `doctest` —— 也就是嵌入在 Python 文档字符串（`docstring`）中的测试 —— 时，应当使用的文件编码。这项设置特别有用，当你的文档字符串中含有非 ASCII 字符并且你想要确保 `doctest` 能够正确地读取和执行这些测试时。

通常，Python 文件默认使用 `UTF-8` 编码，但是在某些情况下，可能需要指定不同的编码方式，例如，当你的代码文件是用另一种编码方式保存的时候。

在 `pytest.ini` 文件中配置 `doctest_encoding` 的典型方式是：

```ini
[pytest]
doctest_encoding = utf-8
```

示例中使用了 `utf-8` 编码，这是目前最常见的字符编码。如果你有特别的编码需求，比如使用 `latin1`, `utf-16` 或其他编码标准，可以相应地修改这个配置项。

如果不在 `pytest.ini` 中指定 `doctest_encoding` 或将其留空，`pytest` 通常会默认使用 `UTF-8` 编码。

**请注意：**

对于 Python 代码，建议始终使用 `UTF-8` 编码，除非有特定的理由不这样做。这样做有助于确保代码在不同的环境和地区之间具有一致性和良好的兼容性。

在配置 `doctest_encoding` 时，需要确保你所指定的编码方式与你的 Python 文件中的实际编码一致，以防止读取时发生解码错误。此外，你应该只在确实需要时更改此设置，大多数情况下使用默认的 `UTF-8` 编码就足够了。



### 3.2.8.23 参数 cache_dir (string)

`cache_dir` 是 `pytest.ini` 文件中的一个配置选项，它允许你指定 `pytest` 缓存数据（如测试结果和插件数据）的目录。`pytest` 使用这个缓存目录来存储和重用会话间的数据，提高测试效率。这个目录通常是`.pytest_cache`，默认位于项目的根目录中。

在 `pytest.ini` 文件中设置 `cache_dir` 选项的例子如下：

```ini
[pytest]
cache_dir = .custom_cache
```

上面的配置会将 `pytest` 的缓存目录设置为项目根目录下的 `.custom_cache` 文件夹。

关于 `cache_dir` 的几点说明：

* 如果你不设置 `cache_dir`，`pytest` 默认会使用 `.pytest_cache` 目录。
* 你可以设置为相对路径（相对于 `pytest.ini` 文件所在的目录），或者绝对路径。
* 如果你在版本控制系统（如 Git）中，可能会想要将 `pytest` 的缓存目录添加到 `.gitignore` 文件中，以避免将这些缓存数据提交到代码仓库中。
* 当你运行 `pytest` 时，如果指定的缓存目录不存在，`pytest` 将会自动创建它。
* 当使用持续集成服务时，有时设置特定的缓存目录是很有用的，这样可以在不同的测试运行之间共享缓存数据，减少不必要的重复计算。

总的来说，`cache_dir` 配置项对于控制 `pytest` 如何和在哪里缓存数据是很有帮助的，但对大多数项目来说，默认的缓存设置已经足够好了。只有当你想要自定义或在多个环境中保持缓存数据的一致性时，才需要改变它。




### 3.2.8.24 参数 log_level (string)

`log_level` 是 `pytest.ini` 文件中的一个配置选项，用于指定在 `pytest` 执行测试时记录的日志级别。设置日志级别可以帮助控制测试运行期间输出的日志数量，将重要信息区分出来，便于开发者诊断问题。

日志级别通常有以下几种：

- `CRITICAL` - 严重错误，表明程序的功能受到影响。
- `ERROR` - 发生错误，可能影响程序的某个部分的功能。
- `WARNING` - 发生非致命性问题，是一个警告提示。
- `INFO` - 确认事情按预期工作，提供通常的系统状态信息。
- `DEBUG` - 详细信息，通常只在诊断问题时有用。
- `NOTSET` - 不设置日志级别，默认情况下将打印所有级别的日志信息。

在 `pytest.ini` 文件中设置 `log_level` 的示例：

```ini
[pytest]
log_level = INFO
```

以上的配置将会设置测试运行时的日志级别为 `INFO`，这意味着将会输出 `INFO`, `WARNING`, `ERROR`, 和 `CRITICAL` 级别的日志信息，而 `DEBUG` 级别的信息则不会被输出。

如果你不在 `pytest.ini` 中设置 `log_level`，或者将其设置为 `NOTSET`，则所有级别的日志信息都会被输出，并且会依赖于 Python 的日志系统的默认配置。

适当配置 `log_level` 对于保持测试输出的可读性和寻找bug时的日志管理十分有帮助。在调试期间可能会使用 `DEBUG` 级别来获得尽可能多的信息，而在常规的测试或生产环境中可能会使用 `WARNING` 或 `INFO` 级别以减少日志的干扰。




### 3.2.8.25 参数 log_format (string)

`log_format` 是 `pytest.ini` 文件中的一个配置选项，它定义了 `pytest` 在运行测试时记录日志时使用的格式。通过指定日志消息的结构，可以让日志输出更加清晰和有用。这个格式字符串可以包含各种变量，用来表示日志记录中的不同组成部分，比如时间、记录级别、消息内容等。

下面是常见的日志格式变量：

- `%(asctime)s`：记录事件发生的日期和时间。
- `%(levelname)s`：日志记录的级别（如 DEBUG、INFO、WARNING、ERROR、CRITICAL）。
- `%(name)s`：日志记录器的名称。
- `%(filename)s`：源代码文件名。
- `%(funcName)s`：日志记录所在的函数名。
- `%(lineno)d`：日志记录所在的源代码行号。
- `%(message)s`：日志消息内容本身。

在 `pytest.ini` 文件中设置 `log_format` 的示例：

```ini
[pytest]
log_format = %(asctime)s - %(levelname)s - %(message)s
```

此配置定义了一种日志格式，其中包含了事件发生的时间、日志级别和日志消息本身。当测试用例运行时，这将是你看到的日志消息的格式。

如果在 `pytest.ini` 文件中没有设置 `log_format` 选项，`pytest` 将使用 Python `logging` 模块的默认格式设置。

自定义日志格式对于开发者来说非常有用，因为它使得日志消息可以根据个人偏好或团队的日志策略进行调整，以提高日志的可读性和实用性。在调试测试用例或是审核测试运行日志时，合理配置的日志格式能够极大地帮助开发者快速定位和理解问题。




### 3.2.8.26 参数 log_date_format (string)

在 `pytest.ini` 文件中，`log_date_format` 用来定义在日志格式中包含时间（通常通过 `%(asctime)s` 标记）时，日期和时间应该如何显示。使用这个配置，你可以自定义时间的格式，以匹配你的需求或者是预定的日志格式标准。

`log_date_format` 遵循 Python 的 `datetime.strftime()` 方法所使用的格式化字符串。这意味着你可以使用特定的格式化代码来表示日期和时间的各个部分。

下面是一些常用的格式化代码：

- `%Y`：四位数的年份。
- `%m`：两位数的月份。
- `%d`：两位数的日期。
- `%H`：两位数的小时（24小时制）。
- `%M`：两位数的分钟。
- `%S`：两位数的秒。

举个例子，如果你想要设置日期格式为 `年-月-日 时:分:秒`，那么你的 `log_date_format` 应该看起来像这样：

```ini
[pytest]
log_date_format = %Y-%m-%d %H:%M:%S
```

这将使所有的时间戳都以例如 `2023-12-15 23:00:00` 的格式展示。

在没有设置 `log_date_format` 的情况下，默认值通常是 `%Y-%m-%d %H:%M:%S`，即显示完整的日期和时间。自定义 `log_date_format` 可以让日志中的时间戳更符合你对日志记录的具体要求，使日志消息更易于阅读和分析。



### 3.2.8.27 参数 log_cli (bool)

`pytest.ini` 配置文件中的 `log_cli` 选项是一个布尔值，用于控制 `pytest` 是否应该直接在命令行界面（CLI，即打屏）上输出日志。当这个选项被设置为 `true` （或者是 `1`），`pytest` 会在测试运行时实时显示日志消息到控制台。这对于开发者来说特别有用，因为它允许实时跟踪和监视测试执行期间发生的日志事件。

默认情况下，`log_cli` 通常是关闭的，这意味着即便你的测试代码中有日志记录调用，这些日志不会出现在命令行输出中。如果启用了 `log_cli`，你可以通过 `log_cli_level` 和 `log_cli_format` 进一步控制日志的详细程度和格式。

例如，设置 `pytest.ini` 文件以启用命令行日志输出可能看起来像这样：

```ini
[pytest]
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

这里：

- `log_cli = true` 将 CLI 日志记录启用。
- `log_cli_level = INFO` 设置了最低日志级别为 INFO。
- `log_cli_format` 定义了日志消息的格式，这里包括时间戳、日志级别以及日志信息本身。
- `log_cli_date_format` 设置了日志中使用的时间格式。

这样配置后，你就会在 `pytest` 运行测试时看到实时的日志输出，根据上面的配置，它将包括时间戳、日志级别和消息内容等信息。通过在测试过程中查看这些详细的日志输出，可以帮助你更快地诊断和解决问题。



### 3.2.8.28 参数 log_cli_level (string)

在 `pytest.ini` 配置文件中，`log_cli_level` 选项用于设置命令行接口（CLI）日志的最低级别。这个字符串选项确定了在命令行上实时输出的日志消息的最低严重性级别。它适用于当你设置了 `log_cli = true` 以启用实时日志输出到控制台时。

下面是一些可以设置的日志级别，按照严重程度由低到高排序：

- `DEBUG`: 最详细的日志级别，包括大量的信息，通常用于开发和调试过程中。
- `INFO`: 用于常规的信息性消息，这些消息描述程序的一般运行状态。
- `WARNING`: 用于提示一些意外情况，或即将发生的问题（例如 '即将废弃的特性' 警告）。
- `ERROR`: 反映出较严重的问题，影响程序的部分功能。
- `CRITICAL`: 用于极为严重的问题，可能导致应用程序的崩溃。

设置 `log_cli_level` 的目的是为了过滤掉那些低于你指定级别的日志消息，只显示级别相等或更高的。这样做可以减少命令行中显示的日志数量，让你聚焦于更重要的信息。

例如，如果你只想看到 `WARNING` 及以上级别的日志消息，你可以这样设置你的 `pytest.ini` 文件：

```ini
[pytest]
log_cli = true
log_cli_level = WARNING
```

在上面的例子中，只有 `WARNING`、`ERROR` 和 `CRITICAL` 级别的日志消息会显示到控制台上。所有 `INFO` 和 `DEBUG` 级别的日志都不会显示出来。




### 3.2.8.29 参数 log_cli_format (string)

在 `pytest.ini` 配置文件内，`log_cli_format` 选项允许你自定义命令行界面（CLI）中显示的日志输出格式。这个字符串选项指定了在启用了命令行日志（使用 `log_cli = true`）时，日志消息应该如何显示。

`log_cli_format` 支持使用一系列预定义的变量，这些变量将会在日志消息被实际输出时替换成相应的值。这种格式化方式类似于 Python 的标准日志库（`logging` 模块）使用的格式。

以下是一些常见的预定义格式变量：

- `%(levelname)s`: 日志级别的文本表示（例如 'INFO', 'ERROR'）。
- `%(asctime)s`: 创建日志记录的时间。可以通过 `log_cli_date_format` 进一步定义时间的显示格式。
- `%(message)s`: 日志消息的实际文本。
- `%(filename)s`: 输出日志消息的源文件名称。
- `%(lineno)d`: 输出日志消息的源代码行号。
- `%(name)s`: 日志记录器的名称。
- `%(threadName)s`: 进行日志记录的线程名称。

你可以按照自己的偏好组合这些变量，定义出符合需求的日志输出格式。例如，你可能想要一个包含时间戳、日志级别和消息本身的格式：

```ini
[pytest]
log_cli = true
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
```

使用上面的配置后，输出的日志可能看起来像这样：

```shell
2023-12-16 12:50:00 [INFO] Test started
2023-12-16 12:50:01 [WARNING] This is a warning message
2023-12-16 12:50:02 [ERROR] This is an error message
```

`log_cli_format` 的灵活性允许你调整日志输出以便更好地理解你的测试过程中发生了什么。通过在每个日志消息前加上时间戳，可以帮助你识别测试中的性能瓶颈或问题产生的时间顺序。使用日志级别可以让你更快地过滤和发现错误。其他信息，如源文件名和代码行号，可以帮助你在出现问题时快速定位错误来源。




### 3.2.8.30 参数 log_cli_date_format (string)

在 `pytest.ini` 配置文件中，`log_cli_date_format` 选项用于自定义命令行接口（CLI）日志的时间戳格式。当你在 `pytest` 中启用实时日志功能 (`log_cli = true`) 并且指定了一个日志格式 (`log_cli_format`) 包含时间信息（通过 `%(asctime)s` 变量）时，`log_cli_date_format` 提供了一种方法来控制这些时间戳的外观。

`log_cli_date_format` 的值应该是一个字符串，符合 Python `datetime` 模块中 `strftime` 方法的参数。通过这种方式，你可以对时间的显示格式进行高度自定义。

以下是一些常用的时间格式化代码，你可以用来设置 `log_cli_date_format`：

- `%Y`: 四位数的年份表示（例如，2023）
- `%m`: 月份（01到12）
- `%d`: 月中的一天（01到31）
- `%H`: 24小时制的小时数（00到23）
- `%M`: 分钟数（00到59）
- `%S`: 秒数（00到59）

例如，如果你希望时间戳以 "年-月-日 时:分:秒" 的形式显示，你可以在 `pytest.ini` 文件中这样设置：

```ini
[pytest]
log_cli = true
log_cli_format = %(asctime)s %(levelname)s %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

这样，假如有一条日志消息在2023年12月17日下午13时10分0秒被记录，使用上述的配置，它的输出格式可能会是这样：

```
2023-12-17 13:10:00 INFO Test is starting
```

通过自定义 `log_cli_date_format`，你可以确保日志消息的时间戳格式能够满足你的具体需求，无论是为了更好的可读性、遵循特定的日志标准，或者与其他系统集成时保持一致性。




### 3.2.8.31 参数 log_file (string)

在 `pytest.ini` 配置文件中，`log_file` 选项指定了一个文件的路径，`pytest` 将会将日志输出记录到这个文件中。这允许开发者和测试工程师保存有关测试执行的日志信息，以便于日后进行问题诊断和性能分析。

`log_file` 的值应当是一个字符串，代表了日志文件将要保存的路径。给定的路径可以是相对的也可以是绝对的。如果指定的文件已经存在，`pytest` 会在每次测试会话开始时截断该文件（覆盖写）。

如果你想要在运行测试时自动记录所有日志到文件中，你可以在 `pytest.ini` 文件中添加如下配置：

```ini
[pytest]
log_file = logs/pytest_autotest.log
```

这里的 `logs/pytest_autotest.log` 是一个例子，表示日志将被写入项目目录下的 `logs` 文件夹中的 `pytest_autotest.log` 文件。（请先确保该 `logs` 文件夹存在或者`pytest`有相应的创建文件夹的权限。）

与日志文件相关的其他配置选项也可以在 `pytest.ini` 中设置，例如：

- `log_file_level`: 设置写入日志文件的日志级别（例如 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`）。
- `log_file_format`: 自定义写入日志文件中的日志消息格式。
- `log_file_date_format`: 自定义日志文件中时间戳的格式。

当配置了 `log_file` 选项，`pytest` 会在每次运行时自动将日志输出到这个文件，这让追踪和保留测试历史变得更加便捷。这些日志可以被用来分析测试失败的原因，或者作为持续集成和部署过程中记录的一部分。




### 3.2.8.32 参数 log_file_level (string)

`pytest.ini` 配置文件中的 `log_file_level` 选项用来设置将日志输出到指定文件时的日志级别。日志级别决定了哪些级别的日志信息（如调试、信息、警告、错误、严重错误等）将被包含在日志文件中。

`log_file_level` 的可能值与Python内置日志系统（logging module）的可用日志级别一致，包括以下选项：

- `NOTSET`
- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

当设置了 `log_file_level`，只有该级别或更高级别的日志消息会被写入到日志文件中。例如，如果设置为 `INFO`，则 `DEBUG` 级别的日志将不会被记录到文件中，而 `INFO`、`WARNING`、`ERROR` 和 `CRITICAL` 级别的则会。

举例来说，若要在 `pytest.ini` 中设置将错误级别以上的日志写入到日志文件，可以这样配置：

```ini
[pytest]
log_file = test.log
log_file_level = ERROR
```

这样配置之后，在执行测试时，只有 `ERROR` 和 `CRITICAL` 级别的日志会被写入到 `test.log` 文件中。这可以帮助开发人员过滤掉不太关注的低级别日志信息，专注于潜在的错误和关键问题。

**请注意：**如果未明确设置 `log_file_level`，则会使用默认的日志级别，该级别通常是 `WARNING`，这意味着会记录 `WARNING`、`ERROR` 和 `CRITICAL` 级别的日志信息到文件中。



### 3.2.8.33 参数 log_file_format (string)

在 `pytest.ini` 配置文件中，`log_file_format` 设置用于自定义记录到日志文件中的日志消息的格式。该设置决定了每条日志信息应该如何展示，包括它们的结构、包含哪些字段以及这些字段的顺序。

`log_file_format` 的值是一个格式化字符串，其中可以包含一系列预定义的格式化变量，这些变量代表了不同的日志记录信息。Python 内置的日志模块（logging module）提供了以下几种常用的变量：

- `%(levelname)s`：日志级别的文本形式（例如 "DEBUG", "INFO"）。
- `%(asctime)s`：日志事件发生的时间。
- `%(message)s`：日志消息体。
- `%(filename)s`：产生日志的源文件名称。
- `%(funcName)s`：产生日志的函数名称。
- `%(lineno)d`：产生日志的代码行号。

你可以组合这些变量来创建任何你需要的日志格式。例如，下面是一个典型的 `log_file_format` 配置：

```ini
[pytest]
log_file = test.log
log_file_format = %(asctime)s - %(levelname)s - %(message)s
```

在上述配置中:

- `%(asctime)s` 包含了日志消息的时间戳。
- `%(levelname)s` 表明了消息的日志级别。
- `%(message)s` 是日志消息的文本。

这样设置后，日志文件中的每一行都将遵循“时间戳 - 日志级别 - 消息内容”的格式。例如，日志文件中的一行可能看起来像这样：

```
2023-12-17 13:40:00,000 - ERROR - An error occurred during the test
```

如果未设置 `log_file_format`，`pytest` 将使用其默认的日志格式。

此外，你还可以通过 `log_date_format` 配置日志时间戳的格式。例如：

```ini
[pytest]
log_file = test.log
log_file_format = %(asctime)s - %(levelname)s - %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

在这个例子中，时间戳将按照 `"YYYY-MM-DD HH:MM:SS"` 的格式来记录。如果你需要不同的格式，可以根据 [Python datetime 模块](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)的 `strftime()` 和 `strptime()` 函数的行为来自定义时间戳的格式。




### 3.2.8.34 参数 log_file_date_format (string)

在 `pytest.ini` 配置文件中，`log_file_date_format` 选项用于定义当使用日志记录功能写入日志到文件时，时间戳的格式。这个设置指定了日志中包含的时间信息部分应该如何显示。

时间戳格式通常根据 [Python datetime 模块](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) 提供的 `strftime()` 和 `strptime()` 函数可识别的格式化字符串来定义。

`log_file_date_format` 的值是一个字符串，用于描述时间戳的显示格式。下面是一些常见的组件以及它们的含义：

- `%Y`：四位数年份，例如 `2021`
- `%m`：两位数月份，从 `01` 到 `12`
- `%d`：两位数的日，从 `01` 到 `31`
- `%H`：两位数的小时，从 `00` 到 `23`
- `%M`：两位数的分钟，从 `00` 到 `59`
- `%S`：两位数的秒，从 `00` 到 `59`

例如，要设置为24小时格式，带有年份、月份、日期、小时、分钟和秒的时间戳，你可以将配置写成这样：

```ini
[pytest]
log_file = test.log
log_file_format = %(asctime)s - %(levelname)s - %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
```

有了这样的配置，日志文件中的记录可能会包含如下格式的时间戳：

```
2023-12-17 15:39:21 - ERROR - An error occurred during the test
```

如果 `log_file_date_format` 没有在 `pytest.ini` 中被设置，那么默认的时间戳格式将会被使用，这个默认格式通常是年月日时分秒（包含毫秒）。

添加 `log_file_date_format` 到你的配置中，可以帮助你精确地知道每条日志消息是在什么时候生成的，这在调试时尤其有用。




### 3.2.8.35 参数 log_auto_indent (string)

`log_auto_indent` 是在 `pytest.ini` 配置文件（或其他`pytest`配置文件，如 `tox.ini` 或 `pyproject.toml` 中指定的 `pytest` 配置段）中用于设置日志输出自动缩进功能的选项。

当 `log_auto_indent` 选项被设置时，它会影响多行日志消息的格式。多行日志消息中，除了第一行外，后续的行将根据这个设置进行缩进，使得日志文件更易于阅读。

`log_auto_indent` 有以下几种值：

- `true` 或 `on`：开启自动缩进。所有的多行日志消息都会自动缩进，缩进量与第一行中日志前缀的长度相匹配。
- `false` 或 `off`：关闭自动缩进。日志消息的所有行都会从行的开始处写起，不做任何缩进。
- 数字（例如 `4`）：开启自动缩进，并使用指定数量的空格作为缩进量。例如，如果设置为 `4`，那么多行日志消息的第二行及以后的每一行都将比第一行多缩进四个空格。

以下是一个 `pytest.ini` 的示例配置：

```ini
[pytest]
log_file = test.log
log_file_format = %(asctime)s - %(levelname)s - %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
log_auto_indent = true
```

在这个配置中，`log_auto_indent` 被设置为 `true`，这意味着在日志文件中，如果日志消息包含多行，除了第一行外的所有行都会自动进行缩进。

假设你在测试中有这样的一个多行日志消息：

```python
logger.info("This is a multi-line log message:\nSecond line of the message\nThird line of the message")
```

在 `log_auto_indent` 被设置为 `true` 时，日志文件中将显示为：

```shell
2023-12-17 16:20:00,000 - INFO - This is a multi-line log message:
                                Second line of the message
                                Third line of the message
```

注意每条日志消息后续的行都已经与第一行的开始对齐，这使得日志的阅读与分析更加方便清晰。




### 3.2.8.36 参数 pythonpath (paths)

在 `pytest.ini` 配置文件中， `pythonpath` 配置选项用于在测试时添加特定的路径到 `sys.path`（这实际上是Python用来查找模块的路径列表）， `pytest` 读取的配置文件中（如 `pytest.ini`、`tox.ini` 或 `pyproject.toml`）使用钩子（hook）来添加路径到 `sys.path`。

如果要在 `pytest`中添加额外的路径，你一般有以下几种方式：

 `pytest.ini` 的示例配置：

```
pythonpath = /path/to/your/module
```

除此之外，还可以通过如下方式设置以期达到`pythonpath`的效果，如下：

* 使用 `conftest.py` 文件

在你的测试目录中创建一个 `conftest.py` 文件，并在其中添加代码以加载所需的路径：

```python
# conftest.py
import sys
sys.path.append('/path/to/your/module')
```

* 设置 `PYTHONPATH` 环境变量

在命令行中，你可以在运行 `pytest` 前设置 `PYTHONPATH` 环境变量：

```shell
export PYTHONPATH=/path/to/your/module:$PYTHONPATH
```

这在 Unix/Linux系统上有效，如果你使用的是Windows，则使用 `set` 命令：

```cmd
set PYTHONPATH=/path/to/your/module;%PYTHONPATH%
```

* 在 `pytest.ini` 或其他配置文件中定义 `addopts`

在配置文件中通过 `addopts` 为命令行增加参数以实现相同的目的，只要记住 `addopts` 的方式不会直接修改 `sys.path`，而是通过`pytest`的命令行参数（如 `-m` 来指定模块路径）来影响测试执行环境。

```ini
[pytest]
addopts = --pyargs /path/to/your/module
```




### 3.2.8.37 参数 faulthandler_timeout (string)

`faulthandler_timeout` 用于在启动 Python 的 `faulthandler` 模块，该模块在测试运行时出现死锁或长时间没有响应的情况下可以帮助捕获诸如 `segfaults`（段错误） 以及其他底层错误的跟踪信息。

当你在 `pytest.ini`, `tox.ini`，或 `pyproject.toml` 文件的相应方段中设置了 `faulthandler_timeout` 之后，`pytest` 会在每个测试用例开始时启动 `faulthandler`，并且如果测试用例运行的时间超过了设置的秒数，它将会打印一个堆栈跟踪信息到 `stderr`。这在调试测试用例死锁或运行时间异常长的情况时非常有用。

这个选项的值是一个字符串，代表超时秒数。

例如，在 `pytest.ini` 中设置 `faulthandler_timeout`：

```ini
[pytest]
faulthandler_timeout = 60
```

这个配置意味着，在每个测试用例执行时，如果 60 秒内没有完成，`faulthandler` 将会被触发，打印相关的堆栈跟踪信息到 `stderr`。

**请注意：**

`faulthandler_timeout` 只在 Python 3.3 以上版本生效，因为 `faulthandler` 模块是在这个版本新增的。同时，这个功能有时并不适用于所有的测试情况，因为它会增加一些额外的性能开销，并且可能会与 IDE 或其他工具的调试器相冲突。因此，在有需要时使用，不建议默认总是打开这个选项。



### 3.2.8.38 参数 addopts (args)

在 `pytest` 中，`addopts` 是一个配置选项，它允许你在命令行参数中提前设置和添加默认 `pytest` 参数。这意味着每次你运行 `pytest` 时，无需手动输入这些参数，`pytest` 会自动将 `addopts` 中的参数包含在执行中。

可以在很多配置文件中设置 `addopts`，比如 `pytest.ini`、`tox.ini` 或者 `pyproject.toml`。下面是 `pytest.ini` 文件中使用 `addopts` 的典型方式：

```ini
[pytest]
addopts = -ra -q
```

这里列出了两个参数作为例子：

- `-r`：后面跟着字符（如 `a`），用以增加测试报告的信息。字符 `a` 表示所有测试（不管是成功、失败等）都会在测试报告中显示额外信息。
- `-q`：代表静默模式，减少测试运行的输出信息显示。

`addopts` 可以接收多个参数，这些参数应该是在命令行上使用 `pytest` 时可以接受的参数。

这些参数可能包括：

- `-v`, `--verbose`：增加测试运行的详细信息输出。
- `-x`, `--exitfirst`：遇到第一个错误时立刻停止测试。
- `--durations=N`：显示测试的执行时间，N为显示的慢速测试数量。
- `--cov=PACKAGE`：运行 `pytest-cov` 插件来测量代码覆盖率。
- `-k EXPRESSION`：仅运行匹配表达式的测试。
- `--maxfail=NUM`：设置在 `NUM` 个失败后停止运行测试。

例如，如果你想设置 `pytest` 每次运行时都要产生代码覆盖率报告（需要安装第三方插件`pytest-cov`），并且以相对详细的方式展示，可以如下配置：

```ini
[pytest]
addopts = --cov=my_package --verbose
```

这样设置后，当你只执行 `pytest` 命令时，它将自动添加上面的选项，无需你手动输入它们。

使用 `addopts` 可以方便地共享测试行为设置，确保开发团队或CI/CD流水线中所有成员和环境运行测试时使用相同的参数。但是，也需要注意，`addopts` 中的配置可能被命令行参数所覆盖。如果你要在特定情形下更改行为，可以在命令行中指定不同的参数来临时覆盖 `addopts` 的设置。




### 3.2.8.39 参数 minversion (string)

`minversion` 是 `pytest` 中用于指定运行测试所需要的 `pytest` 的最小版本。这个选项被设置在 `pytest.ini`、`tox.ini` 或者 `pyproject.toml` 文件中，以确保 `pytest` 的某些特性或插件依赖特定的版本才能正常工作。

如果当前环境中的 `pytest` 版本低于 `minversion` 指定的版本， `pytest` 将报错并退出，提示用户必须升级 `pytest` 到一个更新的版本。

这是一个例子，演示如何在 `pytest.ini` 文件中设置 `minversion`：

```ini
[pytest]
minversion = 7.0
```

上面的配置指定了至少需要 `pytest` 的 7.0 版本。如果试图使用低于 7.0 版本的 `pytest` 运行测试，你会得到一个错误提示，告诉你需要升级 `pytest`。

使用 `minversion` 很有用，尤其是在你依赖于某个新版本才有的特性，或者你想要确保所有人使用同一版本的 `pytest`，避免因为版本差异出现不一致的测试结果。不过，这个选项也要谨慎使用，特别是作为库的作者时，设置太高的版本要求可能会无意中排除掉一些还未升级的用户。




### 3.2.8.40 参数 required_plugins (args)

`required_plugins` 是 `pytest` 配置文件中的用于指定运行测试集需要安装的插件。这个选项可被包含在 `pytest.ini`、`tox.ini` 或者 `pyproject.toml` 文件中。通过这个选项，你可以声明一组插件的依赖关系，以确保在开始运行 `pytest` 测试前，所有必须的插件都已经安装好。

如果没有安装列出的某个插件，则在运行 `pytest` 时会产生错误，并提醒用户需要先安装缺失的插件。

下面是一个如何在 `pytest.ini` 文件中使用 `required_plugins` 的范例：

```ini
[pytest]
required_plugins = pytest-cov>=4.0.0 pytest-xdist>=3.2.1
```

在上面的例子中，我们指定了两个插件 —— `pytest-cov` 和 `pytest-xdist` 作为运行测试集所需要的插件，并且分别提供了它们的最低版本要求。这意味着，开发者或者CI环境在运行测试之前，至少需要安装版本为4.0.0或以上的 `pytest-cov` 和版本为3.2.1或以上的 `pytest-xdist` 插件。

使用 `required_plugins` 也有助于保持一致性，特别是当你测试的某些方面依赖于特定插件的功能时。它确保了所有人在本地或者CI/CD环境中运行的测试环境都是完备的，减少了因环境配置不一致而造成的问题。

如果某个插件没有安装，`pytest` 会给出相应的错误消息，并可能建议使用 pip 安装所缺失的插件。如果所需的插件未能满足最小版号要求，`pytest` 也会提示版本不符合要求。所有这些都帮助维持了一个健壯的自动化测试环境。





## 3.2.9 Environment variables 相关参数


### 3.2.9.1 参数 PYTEST_ADDOPTS

`PYTEST_ADDOPTS` 是一个环境变量，用于在命令行调用 `pytest` 时，向 `pytest` 命令添加额外的命令行选项（不论这些选项在 `pytest.ini` 文件中是否已经被指定）。这对于临时添加、改变某些选项，或者将其加入到持续集成（CI）脚本中非常有用。

当你设置了 `PYTEST_ADDOPTS` 环境变量，`pytest` 将在运行时读取这些额外的命令行选项，并将它们应用到测试会话中。这样，你可以不用直接编辑测试脚本或配置文件，而是通过环境变量控制 `pytest` 的行为。

举个例子，假设你想要以详细模式运行测试，并开启一个特定的 `pytest` 插件功能，你可以这样设置环境变量：

```shell
export PYTEST_ADDOPTS="-v --some-plugin-option"
```

接下来，无论是在终端手动运行 `pytest`，还是在 CI 系统中，你都无需在命令行中明确写出这些选项，`pytest` 会自动从 `PYTEST_ADDOPTS` 环境变量中读取并使用它们。

另外一个使用场景是，你可以通过 `PYTEST_ADDOPTS` 来设置一些通用的选项，例如，指定测试运行时的 CPU 数量（使用 `pytest-xdist` 插件）：

```shell
export PYTEST_ADDOPTS="-nauto"
```

这个命令会告诉 `pytest` 自动检测 CPU 核心数量，并分配相应数量的工作线程来并行运行测试。

**请注意：**

通过 `PYTEST_ADDOPTS` 设置的选项会优先于在 `pytest.ini` 或其他配置文件中指定的选项。这意味着，环境变量中的设置可以覆盖配置文件中的设置。因此，当使用 `PYTEST_ADDOPTS` 时，要清楚其对系统中其他 `pytest` 配置的影响。




### 3.2.9.2 参数 PYTEST_PLUGINS

`PYTEST_PLUGINS` 是一个环境变量，它允许用户在不改变测试代码和不使用命令行选项的情况下，预先加载一组特定的`pytest`插件。这个环境变量可以用来确保在`pytest`开始收集测试项之前，必要的插件已经被加载。

设置 `PYTEST_PLUGINS` 可以在一个测试会话中声明一个或多个插件名称（以英文逗号分隔），`pytest`在启动时会自动加载这些插件。以下是如何使用该环境变量的示例：

```shell
export PYTEST_PLUGINS="pytest_cov,pytest_mock"
```

上述命令将预先加载 `pytest-cov` 和 `pytest-mock` 插件。请注意插件名称是以逗号分隔的，而且不包含空格和插件版本号。

`PYTEST_PLUGINS` 通常用于下面这些情况：

* 当你构建一个自定义的测试环境或框架，并且你想确保一组特定的插件总是被加载时，可以使用这个变量来强制加载这些插件。
* 当你使用持续集成（CI）系统并且需要预先指定插件，但不想修改配置文件或者测试代码时。
* 在作为私人或特殊用途的插件开发和测试时，你可能会设置这个环境变量以便能够在不发布插件的情况下快速对其进行测试。

**请注意：**

当你在代码中通过 `pytest_plugins` 变量（注意变量名和环境变量名的区别）显式导入了一个插件时，或者你在 `pytest.ini`，`tox.ini` 或 `pyproject.toml` 文件中列出了需要的插件时，`PYTEST_PLUGINS` 环境变量中列出的插件会与它们累加，同时被加载。

`PYTEST_PLUGINS` 设置在`pytest`测试会话开始时就被读取，并且不能在测试会话运行中更改。如果尝试动态更改这个环境变量并且希望它在同一个测试会话中生效，可能是无效的。因此，设置这个变量一般要在调用 `pytest` 命令之前完成。



### 3.2.9.3 参数 PYTEST_DISABLE_PLUGIN_AUTOLOAD

`PYTEST_DISABLE_PLUGIN_AUTOLOAD` 是一个环境变量，用于控制 `pytest` 是否自动加载插件。默认情况下，`pytest` 会自动加载安装在系统中且注册了的插件，这些插件可能是通过 `pip` 安装的，也可能是通过设置 `pytest_plugins` 变量在测试代码中直接引入的。当设定为1时，它会告诉 `pytest` 不要自动加载任何插件。这可能在调试测试或插件本身时非常有用，也可以帮助你确保测试的隔离性和一致性。

如果你希望在运行 `pytest` 时禁止自动加载插件，你可以在命令行中设置这个环境变量，如下所示：

在Linux或macOS系统上，你可以通过在命令行上运行以下命令来设置该环境变量：

```sh
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
```

在Windows系统上，可以用以下方式设置：

```shell
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
```

请注意，这只会影响当前的shell会话。一旦关闭终端或打开新的终端，环境变量将不再生效，除非再次设置。

如果你需要在一个特定的调用中临时设置这个变量，可以使用以下语法：

在Linux或macOS上：

```sh
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
```

在Windows PowerShell上：

```shell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"; pytest
```

这样就可以运行 `pytest` 而不自动加载插件。这通常是用于特定的测试环境，或者在你想要精确控制哪些插件被加载的情况下非常有用。举例来说，如果你正在开发一个新的`pytest`插件，或者想要复现一个不含第三方插件干扰的问题，那么可以使用 `PYTEST_DISABLE_PLUGIN_AUTOLOAD` 来保证在运行测试时，仅加载你明确指定的插件。

**请注意：**

即使设置了 `PYTEST_DISABLE_PLUGIN_AUTOLOAD`，你仍然可以通过命令行选项 `--plugins` 或通过在代码中声明 `pytest_plugins` 变量的方式来手动加载特定的插件。此外，通过 `PYTEST_ADDOPTS` 环境变量传递的命令行选项也仍然有效，它们可用于添加其他的命令行参数，这些参数并不受 `PYTEST_DISABLE_PLUGIN_AUTOLOAD` 环境变量的影响。




### 3.2.9.4 参数 PYTEST_DEBUG

`PYTEST_DEBUG` 是一个用于 `pytest` 的环境变量，它允许用户启用 `pytest` 的调试模式。当设置这个变量时，`pytest` 会提供额外的调试信息，这可能对于插件开发者、贡献者以及希望解决特定测试问题的用户而言是有帮助的。

当你设置 `PYTEST_DEBUG` 环境变量时，`pytest` 将记录更多的调试信息到一个文件中，默认是 `_pytest.debug.log`。这包括了 `pytest` 的内部日志，如插件的加载信息、配置和钩子函数(hook)的调用细节。

要启用 `pytest` 调试模式，你可以在运行测试之前在 Linux类系统的终端或 Windows 的命令提示符中设置环境变量：

在 Linux或 macOS 中：

```shell
export PYTEST_DEBUG=1
```

在 Windows 命令行中：

```cmd
set PYTEST_DEBUG=1
```

随后运行你的测试套件，`pytest` 将会在当前目录下生成包含调试信息的 `_pytest.debug.log` 文件。

这个调试日志非常详细，它包括了关于每一个测试项的收集和执行过程的信息，以及钩子(hook)调用和插件管理等方面的信息。这对于调试复杂的测试问题特别有用，比如当你遇到一个你怀疑与 `pytest` 的内部行为相关的问题时。

**请注意：**

`PYTEST_DEBUG` 并不是通常用于测试脚本或软件项目本身的错误的工具。对于这些目的，你可能会使用 Python 的标准调试工具，如 `pdb`。

总之，`PYTEST_DEBUG` 是一个非常专业的工具，主要用于当你需要深入了解 `pytest` 的内部机制时提供帮助。对于大多数`pytest`用户来说，他们可能不需要使用这个特性。在正常使用中，更推荐的调试方法包括使用 `pytest` 的诸如 `-v`（verbose）或 `-s`（disable all capturing）等内置命令行选项，以及利用 Python 的标准调试器。



# 3.3 本章小结

本章针对`pytest`框架中的参数设置进行了详细介绍，包括常用选项、命令选项、标记选项、调试选项、xdist选项等等。我们介绍了`pytest`参数的功能和使用方法，并通过实例演示了每个参数的具体应用。

通过使用pytest参数，我们可以轻松地控制pytest的测试执行过程，以便更好地满足我们的测试需求和定制需求。例如，我们可以选择是否打印测试用例的详细信息，是否运行多线程测试，是否跳过某些测试用例等。通过这些参数设置，我们可以使测试过程更高效、更准确、更全面。

尽管本文涵盖了pytest所有的参数及其使用方法，但pytest框架的使用和发展是不断变化和完善的，因此我们需要随着进一步的技术发展和需求变化，不断掌握最新的参数设置和使用方法。

总之，`pytest`参数是`pytest`测试框架中独特的功能和优势之一，通过本文的介绍和实例演示，你可以更好地掌握`pytest`的参数设置方法和技术，以便更好地编写测试用例、运行测试过程并从中获得更准确的测试结果，为测试过程提供更加灵活、准确和高效的服务。
