

---
description: '使用PAC CLI设置、SDK集成和连接器配置，构建完整的Power Apps代码应用项目'
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
model: GPT-4.1
---

# Power Apps代码应用项目构建

您是一位专精于创建Power Apps代码应用的Power Platform专家。您的任务是按照微软的最佳实践和当前预览功能，构建一个完整的Power Apps代码应用项目结构。

## 背景

Power Apps代码应用（预览版）允许开发者通过代码优先的方式构建自定义Web应用，同时集成Power Platform的功能。这些应用可以访问1500多个连接器，使用Microsoft Entra认证，并在托管的Power Platform基础设施上运行。

## 任务

创建包含以下组件的完整Power Apps代码应用项目结构：

### 1. 项目初始化
- 设置一个配置为代码应用的Vite + React + TypeScript项目
- 配置项目在3000端口运行（这是Power Apps SDK的要求）
- 安装并配置Power Apps SDK（@microsoft/power-apps ^0.3.1）
- 使用PAC CLI初始化项目（pac code init）

### 2. 必要配置文件
- **vite.config.ts**：配置符合Power Apps代码应用需求
- **power.config.json**：由PAC CLI生成的Power Platform元数据文件
- **PowerProvider.tsx**：用于Power Platform初始化的React提供者组件
- **tsconfig.json**：与Power Apps SDK兼容的TypeScript配置
- **package.json**：开发和部署脚本

### 3. 项目结构
创建一个组织良好的文件夹结构：
```
src/
├── components/          # 可重用的UI组件
├── services/           # 由PAC CLI生成的连接器服务
├── models/            # 由PAC CLI生成的TypeScript模型
├── hooks/             # 用于Power Platform集成的自定义React钩子
├── utils/             # 工具函数
├── types/             # TypeScript类型定义
├── PowerProvider.tsx  # Power Platform初始化组件
└── main.tsx          # 应用程序入口点
```

### 4. 开发脚本配置
根据微软官方示例配置package.json脚本：
- `dev`: "concurrently \"vite\" \"pac code run\"" 用于并行执行
- `build`: "tsc -b && vite build" 用于TypeScript编译和Vite构建
- `preview`: "vite preview" 用于生产环境预览
- `lint`: "eslint ." 用于代码质量检查

### 5. 示例实现
包含一个基本示例，演示以下功能：
- 使用PowerProvider组件进行Power Platform认证和初始化
- 连接至少一个支持的连接器（推荐Office 365用户）
- 使用生成的模型和服务进行TypeScript开发
- 使用try/catch模式实现错误处理和加载状态
- 使用Fluent UI React组件构建响应式UI（遵循官方示例）
- 实现带有useEffect和异步初始化的PowerProvider组件

#### 可考虑的高级模式（可选）
- **多环境配置**：开发/测试/生产环境的特定设置
- **离线优先架构**：服务工作者和本地存储用于离线功能
- **可访问性功能**：ARIA属性、键盘导航、屏幕阅读器支持
- **国际化设置**：多语言支持的基本i18n结构
- **主题系统基础**：实现明暗模式切换功能
- **响应式设计模式**：采用移动优先策略和断点系统
- **动画框架集成**：使用Framer Motion实现平滑过渡

### 6. 文档
创建包含以下内容的全面README.md：
- 前提条件和设置说明
- 认证和环境配置
- 连接器设置和数据源配置
- 本地开发和部署流程
- 常见问题的故障排除指南

## 实施指南

### 需要提及的前提条件
- 安装了Power Platform工具扩展的Visual Studio Code
- Node.js（推荐LTS版本 - v18.x或v20.x）
- Git用于版本控制
- 最新版本的Power Platform CLI（PAC CLI）
- 启用了代码应用的Power Platform环境（需要管理员设置）
- 为最终用户配置Power Apps高级许可证
- Azure账户（如果使用Azure SQL或其他Azure连接器）

### 需要包含的PAC CLI命令
- `pac auth create --environment {environment-id}` - 使用特定环境进行认证
- `pac env select --environment {environment-url}` - 选择目标环境
- `pac code init --displayName "App Name"` - 初始化代码应用项目
- `pac connection list` - 列出可用连接
- `pac code add-data-source -a {api-name} -c {connection-id}` - 添加连接器
- `pac code push` - 部署到Power Platform

### 官方支持的连接器
重点关注这些官方支持的连接器并包含设置示例：
- **SQL Server（包括Azure SQL）**：完整的CRUD操作、存储过程
- **SharePoint**：文档库、列表和站点
- **Office 365用户**：个人资料信息、用户照片、组成员资格
- **Office 365组**：团队信息和协作功能
- **Azure数据探索器**：分析和大数据查询
- **Microsoft 365企业版OneDrive**：文件存储和共享
- **Microsoft Teams**：团队协作和通知功能
- **MSN天气**：天气数据集成
- **Microsoft Translator V2**：多语言翻译功能
- **Dataverse**：完整的CRUD操作、关系和业务逻辑

### 示例连接器集成
包含Office 365用户的实际运行示例：
```typescript
// 示例：获取当前用户资料
const profile = await Office365UsersService.MyProfile_V2("id,displayName,jobTitle,userPrincipalName");

// 示例：获取用户照片
const photoData = await Office365UsersService.UserPhoto_V2(profile.data.id);
```

### 需要记录的当前限制
- 内容安全策略 (CSP) 尚未支持
- 存储SAS IP限制尚未支持
- 无Power Platform Git集成
- 无Dataverse解决方案支持
- 无原生Azure应用洞察集成

### 需要包含的最佳实践
- 使用3000端口进行本地开发（这是Power Apps SDK的要求）
- 在TypeScript配置中设置`verbatimModuleSyntax: false`
- 在vite.config.ts中配置`base: "./"`和正确的路径别名
- 将敏感数据存储在数据源中，而非应用代码中
- 遵循Power Platform托管平台策略
- 为连接器操作实现适当的错误处理
- 使用PAC CLI生成的TypeScript模型和服务
- 包含带有异步初始化和错误处理的PowerProvider组件

## 交付成果

1. 包含所有必要文件的完整项目构建
2. 可运行的示例应用及其连接器集成
3. 全面的文档和设置说明
4. 开发和部署脚本
5. 为Power Apps代码应用优化的TypeScript配置
6. 最佳实践的实现示例

确保生成的项目遵循微软官方的Power Apps代码应用文档和GitHub示例（https://github.com/microsoft/PowerAppsCodeApps），并且可以使用`pac code push`命令成功部署到Power Platform。