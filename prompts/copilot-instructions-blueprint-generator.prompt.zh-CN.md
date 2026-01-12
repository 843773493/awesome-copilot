

---
description: '一种与技术无关的蓝图生成器，用于创建全面的 copilot-instructions.md 文件，指导 GitHub Copilot 生成符合项目标准、架构模式和确切技术版本的代码。该生成器通过分析现有代码库模式并避免假设来实现这一目标。'
agent: 'agent'
---

# GitHub Copilot 指令蓝图生成器

## 配置变量
${PROJECT_TYPE="Auto-detect|.NET|Java|JavaScript|TypeScript|React|Angular|Python|Multiple|Other"} <!-- 主要技术 -->
${ARCHITECTURE_STYLE="Layered|Microservices|Monolithic|Domain-Driven|Event-Driven|Serverless|Mixed"} <!-- 架构方法 -->
${CODE_QUALITY_FOCUS="Maintainability|Performance|Security|Accessibility|Testability|All"} <!-- 质量优先级 -->
${DOCUMENTATION_LEVEL="Minimal|Standard|Comprehensive"} <!-- 文档要求 -->
${TESTING_REQUIREMENTS="Unit|Integration|E2E|TDD|BDD|All"} <!-- 测试方法 -->
${VERSIONING="Semantic|CalVer|Custom"} <!-- 版本控制方法 -->

## 生成的提示

"生成一个全面的 copilot-instructions.md 文件，该文件将指导 GitHub Copilot 生成符合我们项目标准、架构和技术版本的代码。所有指令必须严格基于代码库中的实际代码模式，避免任何假设。请遵循以下方法：

### 1. 核心指令结构

```markdown
# GitHub Copilot 指令

## 优先级指南

在为该仓库生成代码时：

1. **版本兼容性**：始终检测并尊重项目中使用的语言、框架和库的确切版本
2. **上下文文件**：优先考虑 .github/copilot 目录中定义的模式和标准
3. **代码库模式**：当上下文文件未提供具体指导时，扫描代码库以识别已建立的模式
4. **架构一致性**：保持我们的 ${ARCHITECTURE_STYLE} 架构风格和已建立的边界
5. **代码质量**：在所有生成的代码中优先考虑 ${CODE_QUALITY_FOCUS == "All" ? "可维护性、性能、安全性、可访问性和可测试性" : CODE_QUALITY_FOCUS}

## 技术版本检测

在生成代码之前，扫描代码库以识别：

1. **语言版本**：检测项目中使用的编程语言的确切版本
   - 检查项目文件、配置文件和包管理器
   - 查找语言特定的版本指示符（例如 .NET 项目中的 <LangVersion>）
   - 绝不使用超出检测到的版本的语言特性

2. **框架版本**：识别所有框架的确切版本
   - 检查 package.json、.csproj、pom.xml、requirements.txt 等文件
   - 在生成代码时尊重版本约束
   - 绝不建议使用检测到的框架版本中不可用的功能

3. **库版本**：记录关键库和依赖项的确切版本
   - 生成与这些特定版本兼容的代码
   - 绝不使用检测到版本中不可用的 API 或功能

## 上下文文件

优先考虑 .github/copilot 目录中的以下文件（如果存在）：

- **architecture.md**：系统架构指南
- **tech-stack.md**：技术版本和框架细节
- **coding-standards.md**：代码风格和格式标准
- **folder-structure.md**：项目组织指南
- **exemplars.md**：需遵循的示例代码模式

## 代码库扫描指令

当上下文文件未提供具体指导时：

1. 识别与正在修改或创建的文件相似的文件
2. 分析以下模式：
   - 命名约定
   - 代码组织
   - 错误处理
   - 日志方法
   - 文档风格
   - 测试模式
   
3. 遵循代码库中最一致的模式
4. 当存在冲突模式时，优先采用较新文件或测试覆盖率更高的文件中的模式
5. 绝不引入代码库中未发现的模式

## 代码质量标准

${CODE_QUALITY_FOCUS.includes("Maintainability") || CODE_QUALITY_FOCUS == "All" ? `### 可维护性
- 编写具有清晰命名的自文档化代码
- 遵循代码库中显而易见的命名和组织约定
- 严格遵循已建立的模式以确保一致性
- 保持函数专注于单一职责
- 限制函数复杂度和长度以匹配现有模式` : ""}

${CODE_QUALITY_FOCUS.includes("Performance") || CODE_QUALITY_FOCUS == "All" ? `### 性能
- 遵循代码库中已有的内存和资源管理模式
- 匹配代码库中处理计算密集型操作的现有模式
- 遵循代码库中已建立的异步操作模式
- 与现有模式一致地应用缓存
- 根据代码库中显而易见的模式进行优化` : ""}

${CODE_QUALITY_FOCUS.includes("Security") || CODE_QUALITY_FOCUS == "All" ? `### 安全性
- 遵循代码库中已有的输入验证模式
- 应用代码库中使用的相同清理技术
- 使用与现有模式匹配的参数化查询
- 遵循代码库中已建立的身份验证和授权模式
- 根据现有模式处理敏感数据` : ""}

${CODE_QUALITY_FOCUS.includes("Accessibility") || CODE_QUALITY_FOCUS == "All" ? `### 可访问性
- 遵循代码库中已有的可访问性模式
- 与现有组件匹配 ARIA 属性使用方式
- 保持与现有代码一致的键盘导航支持
- 遵循代码库中已建立的颜色和对比度模式
- 应用与代码库一致的文本替代模式` : ""}

${CODE_QUALITY_FOCUS.includes("Testability") || CODE_QUALITY_FOCUS == "All" ? `### 可测试性
- 遵循代码库中已建立的可测试代码模式
- 与代码库中使用的相同测试类和方法命名约定匹配
- 使用代码库中相同的断言模式
- 应用代码库中相同的模拟方法
- 与现有测试中一致的测试隔离模式` : ""}

## 文档要求

${DOCUMENTATION_LEVEL == "Minimal" ? 
`- 匹配现有代码中发现的注释级别和风格
- 根据代码库中观察到的模式进行文档编写
- 遵循现有代码中对非显而易见行为的文档编写模式
- 使用与现有代码相同的参数描述格式` : ""}

${DOCUMENTATION_LEVEL == "Standard" ? 
`- 遵循代码库中发现的精确文档格式
- 匹配现有注释的 XML/JSDoc 风格和完整性
- 以相同风格文档参数、返回值和异常
- 遵循现有代码中对使用示例的编写模式
- 匹配现有代码中的类级文档风格和内容` : ""}

${DOCUMENTATION_LEVEL == "Comprehensive" ? 
`- 遵循代码库中最详细的文档编写模式
- 匹配文档最完整的代码的风格和完整性
- 严格按照最全面文档的文件进行文档编写
- 遵循现有代码中对文档链接的编写模式
- 匹配代码库中对设计决策解释的详细程度` : ""}

## 测试方法

${TESTING_REQUIREMENTS.includes("Unit") || TESTING_REQUIREMENTS == "All" ? 
`### 单元测试
- 匹配现有单元测试的精确结构和风格
- 遵循现有代码中看到的测试类和方法命名约定
- 使用现有测试中相同的断言模式
- 应用现有代码中相同的模拟方法
- 遵循现有代码中一致的测试隔离模式` : ""}

${TESTING_REQUIREMENTS.includes("Integration") || TESTING_REQUIREMENTS == "All" ? 
`### 集成测试
- 遵循代码库中相同的集成测试模式
- 匹配现有代码中测试数据设置和清理的模式
- 使用代码库中相同的组件交互测试方法
- 遵循现有代码中验证系统行为的模式` : ""}

${TESTING_REQUIREMENTS.includes("E2E") || TESTING_REQUIREMENTS == "All" ? 
`### 端到端测试
- 匹配现有 E2E 测试的结构和模式
- 遵循代码库中已建立的 UI 测试模式
- 应用现有代码中相同的用户旅程验证方法` : ""}

${TESTING_REQUIREMENTS.includes("TDD") || TESTING_REQUIREMENTS == "All" ? 
`### 测试驱动开发
- 遵循代码库中显而易见的 TDD 模式
- 匹配现有代码中看到的测试用例进展
- 在测试通过后应用相同的重构模式` : ""}

${TESTING_REQUIREMENTS.includes("BDD") || TESTING_REQUIREMENTS == "All" ? 
`### 行为驱动开发
- 匹配现有测试中的 Given-When-Then 结构
- 遵循现有代码中相同的行为描述模式
- 在测试用例中应用相同的业务重点级别` : ""}

## 技术特定指南

${PROJECT_TYPE == ".NET" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### .NET 指南
- 检测并严格遵循当前使用的特定 .NET 版本
- 仅使用与检测到的版本兼容的 C# 语言特性
- 严格按照代码库中出现的 LINQ 使用模式进行操作
- 匹配现有代码中的异步/等待使用模式
- 应用现有组件中使用的相同依赖注入方法
- 使用现有代码中相同的集合类型和模式` : ""}

${PROJECT_TYPE == "Java" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### Java 指南
- 检测并遵循当前使用的特定 Java 版本
- 严格按照代码库中的设计模式进行操作
- 匹配现有代码中的异常处理模式
- 使用代码库中相同的集合类型和方法
- 应用现有代码中明显的依赖注入模式` : ""}

${PROJECT_TYPE == "JavaScript" || PROJECT_TYPE == "TypeScript" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### JavaScript/TypeScript 指南
- 检测并遵循当前使用的特定 ECMAScript/TypeScript 版本
- 严格按照代码库中的模块导入/导出模式进行操作
- 匹配现有代码中的 TypeScript 类型定义
- 使用现有代码中相同的异步模式（Promise、async/await）
- 遵循相似文件中的错误处理模式` : ""}

${PROJECT_TYPE == "React" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### React 指南
- 检测并遵循当前使用的特定 React 版本
- 匹配现有组件的组件结构模式
- 严格按照代码库中的 Hook 和生命周期模式进行操作
- 应用现有组件中使用的相同状态管理方法
- 匹配现有代码中的属性类型和验证模式` : ""}

${PROJECT_TYPE == "Angular" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### Angular 指南
- 检测并遵循当前使用的特定 Angular 版本
- 严格按照代码库中的组件和模块模式进行操作
- 与现有代码中精确匹配装饰器的使用方式
- 应用代码库中相同的 RxJS 模式
- 遵循现有代码中组件通信的模式` : ""}

${PROJECT_TYPE == "Python" || PROJECT_TYPE == "Auto-detect" || PROJECT_TYPE == "Multiple" ? `### Python 指南
- 检测并遵循当前使用的特定 Python 版本
- 严格按照现有模块中的导入组织方式操作
- 如果代码库中使用了类型提示，请匹配其模式
- 应用现有代码中相同的错误处理模式
- 遵循现有代码中的模块组织模式` : ""}

## 版本控制指南

${VERSIONING == "Semantic" ? 
`- 遵循代码库中应用的语义化版本控制模式
- 匹配现有代码中对重大变更的文档记录
- 以相同方式处理弃用通知` : ""}

${VERSIONING == "CalVer" ? 
`- 遵循代码库中应用的日历版本控制模式
- 匹配现有代码中对变更的文档记录
- 以相同方式突出显示重大变更` : ""}

${VERSIONING == "Custom" ? 
`- 匹配代码库中观察到的确切版本控制模式
- 遵循现有文档中使用的相同变更日志格式
- 应用项目中使用的相同标签约定` : ""}

## 通用最佳实践

- 严格按照现有代码中的命名约定进行命名
- 匹配相似文件中的代码组织模式
- 与现有模式一致地应用错误处理
- 与代码库中一致的测试方法进行操作
- 匹配现有代码中的日志模式
- 使用与代码库中一致的配置方法

## 项目特定指导

- 在生成任何代码之前，彻底扫描代码库
- 严格尊重现有架构边界
- 匹配周围代码的风格和模式
- 当有疑问时，优先考虑现有代码的一致性，而不是外部最佳实践或较新的语言特性
"