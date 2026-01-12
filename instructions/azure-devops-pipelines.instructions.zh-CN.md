

---
description: 'Azure DevOps Pipeline YAML 文件的最佳实践'
applyTo: '**/azure-pipelines.yml, **/azure-pipelines*.yml, **/*.pipeline.yml'
---

# Azure DevOps Pipeline YAML 最佳实践

## 通用指南

- 使用一致的 YAML 语法并正确缩进（2 个空格）
- 始终为流水线、阶段、任务和步骤提供有意义的名称和显示名称
- 实现完善的错误处理和条件执行
- 使用变量和参数使流水线可重用且易于维护
- 遵循最小权限原则管理服务连接和权限
- 包含全面的日志记录和诊断信息以便排查问题

## 流水线结构

- 使用阶段组织复杂流水线以实现更好的可视化和控制
- 使用任务分组相关步骤并启用并行执行
- 在阶段和任务之间实现适当的依赖关系
- 使用模板来复用流水线组件
- 保持流水线文件专注且模块化 - 将大型流水线拆分为多个文件

## 构建最佳实践

- 使用特定的代理池版本和 VM 镜像以确保一致性
- 缓存依赖项（npm、NuGet、Maven 等）以提高构建性能
- 实现适当的构件管理，使用有意义的名称和保留策略
- 使用构建变量来管理版本号和构建元数据
- 包含代码质量门（代码检查、测试、安全扫描）
- 确保构建可重现且与环境无关

## 测试集成

- 在构建过程中运行单元测试
- 以标准格式（JUnit、VSTest 等）发布测试结果
- 包含代码覆盖率报告和质量门
- 在适当的阶段实现集成和端到端测试
- 在可用时使用测试影响分析以优化测试执行
- 在测试失败时快速失败以提供及时反馈

## 安全考虑

- 使用 Azure Key Vault 管理敏感配置和机密信息
- 实现适当的机密管理，使用变量组
- 使用具有最小必要权限的服务连接
- 启用安全扫描（依赖项漏洞、静态分析）
- 为生产部署实现审批门
- 在可能的情况下使用托管标识而非服务主体

## 部署策略

- 实现适当的环境提升（开发 → 预发布 → 生产）
- 使用具有适当环境目标的部署任务
- 在适当的情况下实现蓝绿部署或金丝雀部署策略
- 包含回滚机制和健康检查
- 使用基础设施即代码（ARM、Bicep、Terraform）实现一致的部署
- 为每个环境实现适当的配置管理

## 变量和参数管理

- 使用变量组在流水线之间共享配置
- 实现运行时参数以支持灵活的流水线执行
- 使用基于分支或环境的条件变量
- 加密敏感变量并标记为机密
- 记录变量用途和预期值
- 使用变量模板处理复杂的变量逻辑

## 性能优化

- 在适当的情况下使用并行任务和矩阵策略
- 实现依赖项和构建输出的适当缓存策略
- 在不需要完整历史记录时使用浅层克隆进行 Git 操作
- 通过多阶段构建和分层缓存优化 Docker 镜像构建
- 监控流水线性能并优化瓶颈
- 高效使用流水线资源触发器

## 监控和可观测性

- 在流水线中包含全面的日志记录
- 使用 Azure 监视器和应用洞察力进行部署跟踪
- 实现适当的故障通知和成功通知策略
- 包含部署健康检查和自动回滚触发
- 使用流水线分析识别改进机会
- 记录流水线行为和故障排查步骤

## 模板和可重用性

- 为常见模式创建流水线模板
- 使用 extends 模板实现完整的流水线继承
- 实现步骤模板以复用任务序列
- 使用变量模板处理复杂的变量逻辑
- 适当版本化模板以确保稳定性
- 记录模板参数和使用示例

## 分支和触发策略

- 为不同分支类型实现适当的触发器
- 使用路径过滤器仅在相关文件更改时触发构建
- 为主分支（main/master）配置适当的 CI/CD 触发器
- 使用拉取请求触发器进行代码验证
- 为维护任务实现计划触发器
- 考虑在多仓库场景中使用资源触发器

## 示例结构

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*
      - README.md

variables:
  - group: shared-variables
  - name: buildConfiguration
    value: 'Release'

stages:
  - stage: Build
    displayName: '构建与测试'
    jobs:
      - job: Build
        displayName: '构建应用程序'
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: UseDotNet@2
            displayName: '使用 .NET SDK'
            inputs:
              version: '8.x'
          
          - task: DotNetCoreCLI@2
            displayName: '恢复依赖项'
            inputs:
              command: 'restore'
              projects: '**/*.csproj'
          
          - task: DotNetCoreCLI@2
            displayName: '构建应用程序'
            inputs:
              command: 'build'
              projects: '**/*.csproj'
              arguments: '--configuration $(buildConfiguration) --no-restore'

  - stage: Deploy
    displayName: '部署到预发布环境'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployToStaging
        displayName: '部署到预发布环境'
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  displayName: '下载构件'
                  artifact: drop
                - task: AzureWebApp@1
                  displayName: '部署到 Azure Web 应用'
                  inputs:
                    azureSubscription: 'staging-service-connection'
                    appType: 'webApp'
                    appName: 'myapp-staging'
                    package: '$(Pipeline.Workspace)/drop/**/*.zip'
```

## 常见反模式要避免

- 在 YAML 文件中直接硬编码敏感值
- 使用过于宽泛的触发器导致不必要的构建
- 在单个阶段中混合构建和部署逻辑
- 未实现适当的错误处理和清理机制
- 使用未计划升级的过时任务版本
- 创建难以维护的单体流水线
- 未使用适当的命名约定以提高清晰度
- 忽视流水线安全最佳实践