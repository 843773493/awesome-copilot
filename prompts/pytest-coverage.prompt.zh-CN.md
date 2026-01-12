

---
agent: agent
description: '使用 pytest 运行测试并生成覆盖率报告，发现未被覆盖的代码行，并将覆盖率提升至 100%。'
---

测试的目标是覆盖所有代码行。

生成覆盖率报告的方法如下：

pytest --cov --cov-report=annotate:cov_annotate

如果你要检查特定模块的覆盖率，可以这样指定：

pytest --cov=your_module_name --cov-report=annotate:cov_annotate

你也可以指定运行特定的测试，例如：

pytest tests/test_your_module.py --cov=your_module_name --cov-report=annotate:cov_annotate

打开 cov_annotate 目录以查看注释的源代码。
每个源文件对应一个文件。如果某个文件的源代码覆盖率是 100%，则表示所有代码行都被测试覆盖，因此无需打开该文件。

对于每个覆盖率低于 100% 的文件，请在 cov_annotate 中找到对应的文件并审查该文件。

如果某行以!（感叹号）开头，则表示该行未被测试覆盖。
为这些未被覆盖的行添加测试用例。

持续运行测试并改进覆盖率，直到所有代码行都被覆盖。