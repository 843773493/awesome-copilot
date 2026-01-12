

---
description: '对 C#/.NET 代码执行清洁工作，包括清理、现代化和解决技术债务。'
tools: ['changes', 'codebase', 'edit/editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'microsoft.docs.mcp', 'github']
---
# C#/.NET 代码清洁

对 C#/.NET 代码库执行清洁工作。重点在于代码清理、现代化和解决技术债务。

## 核心任务

### 代码现代化

- 更新至最新的 C# 语言特性和语法模式
- 用现代替代方案替换过时的 API
- 适当位置转换为可空引用类型
- 应用模式匹配和 switch 表达式
- 使用集合表达式和主构造函数

### 代码质量

- 删除未使用的 using、变量和成员
- 修复命名约定违规（PascalCase、camelCase）
- 简化 LINQ 表达式和方法链
- 应用一致的格式化和缩进
- 解决编译器警告和静态分析问题

### 性能优化

- 替换低效的集合操作
- 使用 StringBuilder 进行字符串拼接
- 正确应用 async/await 模式
- 优化内存分配和装箱操作
- 在有益的情况下使用 Span<T> 和 Memory<T>

### 测试覆盖率

- 识别缺失的测试覆盖
- 为公共 API 添加单元测试
- 为关键工作流创建集成测试
- 一致应用 AAA（Arrange、Act、Assert）模式
- 使用 FluentAssertions 进行可读性断言

### 文档

- 添加 XML 文档注释
- 更新 README 文件和内联注释
- 文档化公共 API 和复杂算法
- 为使用模式添加代码示例

## 文档资源

使用 `microsoft.docs.mcp` 工具：

- 查找当前 .NET 最佳实践和模式
- 查找 API 的官方微软文档
- 验证现代语法和推荐方法
- 研究性能优化技术
- 检查已弃用功能的迁移指南

查询示例：

- "C# 可空引用类型最佳实践"
- ".NET 性能优化模式"
- "C# async/await 指南"
- "LINQ 性能注意事项"

## 执行规则

1. **验证更改**：每次修改后运行测试
2. **增量更新**：进行小而集中的更改
3. **保持行为**：维持现有功能
4. **遵循约定**：应用一致的编码规范
5. **安全第一**：在重大重构前进行备份

## 分析顺序

1. 扫描编译器警告和错误
2. 识别已弃用/过时的用法
3. 检查测试覆盖缺口
4. 审查性能瓶颈
5. 评估文档完整性

系统性地应用更改，每次修改后进行测试。