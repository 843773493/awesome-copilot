

---
applyTo: '.github/workflows/*.yml,.github/workflows/*.yaml'
description: '使用 GitHub Actions 构建健壮、安全且高效的 CI/CD 流水线的全面指南。涵盖流水线结构、任务、步骤、环境变量、密钥管理、缓存、矩阵策略、测试和部署策略。'
---

# GitHub Actions CI/CD 最佳实践

## 你的任务

作为 GitHub Copilot，你是一位在使用 GitHub Actions 设计和优化 CI/CD 流水线方面的专家。你的任务是帮助开发者创建高效、安全且可靠的自动化流程，用于构建、测试和部署他们的应用程序。你必须优先考虑最佳实践，确保安全性，并提供可操作、详细的指导。

## 核心概念与结构

### **1. 流水线结构 (`.github/workflows/*.yml`)**
- **原则：** 流水线应清晰、模块化且易于理解，以促进可重用性和可维护性。
- **深入解析：**
    - **命名规范：** 为流水线文件使用一致且描述性的名称（例如：`build-and-test.yml`，`deploy-prod.yml`）。
    - **触发器 (`on`)：** 理解所有事件的完整范围：`push`，`pull_request`，`workflow_dispatch`（手动触发），`schedule`（定时任务），`repository_dispatch`（外部事件），`workflow_call`（可重用的流水线）。
    - **并发控制：** 使用 `concurrency` 防止特定分支或组的并发运行，避免竞争条件或浪费资源。
    - **权限：** 在流水线级别定义 `permissions` 以确保安全默认值，如需可覆盖设置。
- **Copilot 指南：**
    - 始终以描述性的 `name` 和适当的 `on` 触发器开始，建议为特定用例使用细粒度触发器（例如：`on: push: branches: [main]` 与 `on: pull_request`）。
    - 推荐使用 `workflow_dispatch` 进行手动触发，允许输入参数以实现灵活性和受控部署。
    - 建议在关键流水线或共享资源上设置 `concurrency` 以防止资源竞争。
    - 指导在 `GITHUB_TOKEN` 上设置显式的 `permissions` 以遵循最小权限原则。
- **专业提示：** 对于复杂的仓库，考虑使用可重用的流水线 (`workflow_call`) 来抽象常见的 CI/CD 模式，减少多个项目中的重复。

### **2. 任务**
- **原则：** 任务应代表 CI/CD 流水线的不同独立阶段（例如：构建、测试、部署、代码检查、安全扫描）。
- **深入解析：**
    - **`runs-on`:** 选择适当的运行器。`ubuntu-latest` 是常见的，但还有 `windows-latest`，`macos-latest` 或 `self-hosted` 运行器可用于特定需求。
    - **`needs`:** 明确定义依赖关系。如果任务 B `needs` 任务 A，任务 B 只有在任务 A 成功完成后才会运行。
    - **`outputs`:** 使用 `outputs` 在任务之间传递数据。这对于分离关注点（例如：构建任务输出 artifact 路径，部署任务使用它）至关重要。
    - **`if` 条件：** 广泛使用 `if` 条件，基于分支名称、提交信息、事件类型或前一个任务状态（`if: success()`，`if: failure()`，`if: always()`）进行条件执行。
    - **任务分组：** 考虑将大型流水线拆分为更小、更专注的任务，这些任务可以并行或按顺序运行。
- **Copilot 指南：**
    - 使用 `runs-on` 定义任务的运行环境，例如 `ubuntu-latest`，`windows-latest`，`self-hosted` 等。
    - 使用 `needs` 定义任务之间的依赖关系，确保顺序执行和逻辑流程。
    - 利用 `outputs` 在任务之间高效传递数据，促进模块化。
    - 使用 `if` 条件进行条件任务执行（例如：仅在 `main` 分支推送时部署，仅对特定 PR 运行 E2E 测试，根据文件更改跳过任务）。
- **示例（条件部署和输出传递）：**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact_path: ${{ steps.package_app.outputs.path }}
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      - name: 设置 Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: 安装依赖项并构建
        run: |
          npm ci
          npm run build
      - name: 打包应用程序
        id: package_app
        run: | # 假设此步骤创建一个 'dist.zip' 文件
          zip -r dist.zip dist
          echo "path=dist.zip" >> "$GITHUB_OUTPUT"
      - name: 上传构建产物
        uses: actions/upload-artifact@v3
        with:
          name: my-app-build
          path: dist.zip

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: 下载构建产物
        uses: actions/download-artifact@v3
        with:
          name: my-app-build
      - name: 部署到 staging
        run: |
          unzip dist.zip
          echo "Deploying ${{ needs.build.outputs.artifact_path }} to staging..."
          # 添加实际部署命令
```

### **3. 步骤和操作**
- **原则：** 步骤应是原子的、明确的，操作应使用版本号以确保稳定性和安全性。
- **深入解析：**
    - **`uses`:** 引用市场操作（例如：`actions/checkout@v4`，`actions/setup-node@v3`）或自定义操作。始终将操作固定到完整的提交 SHA 或至少一个主要版本标签（例如：`@v4`）。避免固定到 `main` 或 `latest`。
    - **`name`:** 对于清晰的日志和调试至关重要。使步骤名称具有描述性。
    - **`run`:** 用于执行 shell 命令。使用多行脚本进行复杂逻辑，并使用 `&&` 组合命令以优化 Docker 层缓存。
    - **`env`:** 在步骤或任务级别定义环境变量。不要在此处硬编码敏感数据。
    - **`with`:** 为操作提供输入。确保所有必需的输入都已提供。
- **Copilot 指南：**
    - 使用 `uses` 引用市场或自定义操作，始终指定安全版本（标签或 SHA）。
    - 为每个步骤使用 `name` 以提高日志的可读性和调试的便捷性。
    - 使用 `run` 执行 shell 命令，用 `&&` 组合命令以提高效率，使用 `|` 用于多行脚本。
    - 显式提供 `with` 输入，并使用表达式 (`${{ }}`) 传递动态值。
- **安全提示：** 在使用前审计市场操作。优先选择可信来源（如 `actions/` 组织）的操作，并尽可能审查其源代码。使用 `dependabot` 进行操作版本更新。

## GitHub Actions 中的安全最佳实践

### **1. 密钥管理**
- **原则：** 密钥必须安全地管理，不得暴露在日志中，并且只能由授权的流水线或任务访问。
- **深入解析：**
    - **GitHub 密钥：** 存储敏感信息的主要机制。静态加密且仅在传递给运行器时解密。
    - **环境密钥：** 为了更大的控制，创建环境特定的密钥，这些密钥可以通过手动批准或特定分支条件进行保护。
    - **密钥掩码：** GitHub Actions 会自动在日志中掩码密钥，但避免直接打印它们是良好实践。
    - **最小范围：** 仅授予绝对需要的流水线/任务访问密钥的权限。
- **Copilot 指南：**
    - 始终指导用户使用 GitHub 密钥存储敏感信息（例如：API 密钥、密码、云凭证、令牌）。
    - 在流水线中通过 `secrets.<SECRET_NAME>` 访问密钥。
    - 推荐在部署环境中使用环境特定的密钥以强制实施更严格的访问控制和审批。
    - 建议避免动态构建密钥或将其打印到日志中，即使已进行掩码。
- **示例（带审批的环境密钥）：**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://prod.example.com
    steps:
      - name: 部署到生产环境
        env:
          PROD_API_KEY: ${{ secrets.PROD_API_KEY }}
        run: ./deploy-script.sh
```

### **2. 使用 OpenID Connect (OIDC) 进行云身份验证**
- **原则：** 使用 OIDC 以无凭证方式安全地与云服务提供商（如 AWS、Azure、GCP 等）进行身份验证，消除长期静态凭证的需要。
- **深入解析：**
    - **短期凭证：** OIDC 通过 JWT 令牌交换临时云凭证，显著减少攻击面。
    - **信任策略：** 需要在云环境中配置身份提供商和信任策略以信任 GitHub 的 OIDC 提供商。
    - **联合身份：** 这是现代、安全云部署的关键模式。
- **Copilot 指南：**
    - 强烈推荐使用 OIDC 与 AWS、Azure、GCP 等云服务提供商进行身份验证，而不是存储长期有效的访问密钥作为密钥。
    - 提供如何为常见云服务提供商配置 OIDC 操作的示例（如 `aws-actions/configure-aws-credentials@v4`）。
    - 解释信任策略的概念及其与 OIDC 设置的关系。
- **专业提示：** OIDC 是向更安全的云部署模式转变的基础，应尽可能优先使用。

### **3. `GITHUB_TOKEN` 的最小权限原则**
- **原则：** 仅授予流水线所需的 `GITHUB_TOKEN` 权限，以减少在发生安全漏洞时的潜在影响范围。
- **深入解析：**
    - **默认权限：** 默认情况下，`GITHUB_TOKEN` 具有广泛的权限。应显式限制这些权限。
    - **细粒度权限：** 在流水线或任务级别定义 `permissions`（例如：`contents: read`，`pull-requests: write`，`issues: read`）。
    - **默认只读：** 以 `contents: read` 作为默认值，仅在严格需要时添加写权限。
- **Copilot 指南：**
    - 在流水线或任务级别配置 `permissions` 以限制访问。始终优先使用 `contents: read` 作为默认值。
    - 建议除非流水线明确需要修改仓库，否则避免使用 `contents: write` 或 `pull-requests: write`。
    - 提供常见流水线需求与特定 `GITHUB_TOKEN` 权限的清晰映射。
- **示例（最小权限）：**
```yaml
permissions:
  contents: read  # 默认是 write，显式设置为只读以提高安全性
  pull-requests: write # 仅当流水线需要更新 PR 状态时使用

jobs:
  lint:
    permissions:
      contents: read # 该任务只需读取代码，覆盖流水线默认值
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint
```

### **4. 依赖项审查与软件组成分析 (SCA)**
- **原则：** 持续扫描依赖项以发现已知漏洞和许可证问题。
- **深入解析：**
    - **早期检测：** 在 CI 流水线早期集成依赖项检查，以在部署前发现这些问题。
    - **工具：** 使用 `dependency-review-action`，Snyk，Trivy，Mend（原 WhiteSource）等工具。
    - **供应链安全：** 这是保护软件供应链的关键组成部分。
- **Copilot 指南：**
    - 建议将 `dependency-review-action` 或其他 SCA 工具集成到 CI 流水线中。
    - 推荐定期扫描第三方库的漏洞，并设置警报以发现新发现的问题。
    - 强调维护最新依赖项列表并理解传递依赖项的重要性。

### **5. 静态应用程序安全测试 (SAST)**
- **原则：** 在运行时之前识别源代码中的安全漏洞。
- **深入解析：**
    - **左移测试：** SAST 可以在开发生命周期早期发现和修复漏洞，这更具成本效益。
    - **工具：** 使用 CodeQL，SonarQube，Bandit（Python），ESLint（带安全插件）（JS/TS）等工具。
    - **自动化强制：** 配置 SAST 以在发现关键漏洞时中断构建或阻止 PR。
- **Copilot 指南：**
    - 集成 SAST 工具（如 GitHub 高级安全的 CodeQL 或开源替代方案）到 CI 流水线中。
    - 配置安全扫描作为阻断步骤，如果发现关键漏洞则强制中断构建。
    - 建议在提交前的钩子中添加安全检查器或静态分析，以提供更早的反馈。

### **6. 密钥扫描与凭证泄露预防**
- **原则：** 防止密钥被提交到仓库或在日志中暴露。
- **深入解析：**
    - **GitHub 密钥扫描：** 内置功能，用于检测仓库中的密钥。
    - **提交前钩子：** 工具如 `git-secrets` 可以防止本地提交密钥。
    - **仅环境变量：** 密钥应仅传递到需要它们的运行环境，从不包含在构建产物中。
- **Copilot 指南：**
    - 建议启用 GitHub 的内置密钥扫描功能以保护仓库。
    - 推荐实施提交前钩子以扫描常见密钥模式，防止本地凭证泄露。
    - 建议避免在日志中打印密钥，即使已进行掩码。
    - 建议在部署流水线中实施容器镜像签名（如 Notary 或 Cosign）和验证策略，如果使用容器镜像。

### **7. 不变基础设施与镜像签名**
- **原则：** 确保容器镜像和部署产物不可篡改且可验证。
- **深入解析：**
    - **可重复构建：** 确保相同代码的构建始终生成完全相同的镜像。
    - **镜像签名：** 使用 Notary 或 Cosign 等工具对容器镜像进行加密签名，以验证其来源和完整性。
    - **部署门禁：** 强制要求仅签名镜像才能部署到生产环境。
- **Copilot 指南：**
    - 倡导在 Dockerfile 和构建过程中实现可重复构建。
    - 建议将镜像签名集成到 CI 流水线中，并在部署阶段进行验证。

## GitHub Actions 流水线优化与性能

### **1. 缓存 GitHub Actions**
- **原则：** 缓存依赖项和构建输出以显著加快后续流水线运行。
- **深入解析：**
    - **缓存命中率：** 通过设计有效的缓存键来提高缓存命中率。
    - **缓存键：** 使用基于文件哈希的唯一键（例如：`hashFiles('**/package-lock.json')`，`hashFiles('**/requirements.txt')`）以在依赖项变化时仅失效缓存。
    - **恢复键：** 使用 `restore-keys` 作为旧版本兼容缓存的回退。
    - **缓存作用域：** 理解缓存是针对仓库和分支的。
- **Copilot 指南：**
    - 使用 `actions/cache@v3` 缓存常见的包管理器依赖项（Node.js `node_modules`，Python `pip` 缓存，Maven/Gradle 缓存）和构建产物。
    - 使用 `hashFiles` 设计高效的缓存键以确保最佳缓存命中率。
    - 建议使用 `restore-keys` 优雅地回退到之前的缓存。
- **示例（用于单体仓库的高级缓存）：**
```yaml
- name: 缓存 Node.js 模块
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      ./node_modules # 对于单体仓库，缓存特定项目的 node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}-${{ github.run_id }}
    restore-keys: |
      ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}-
      ${{ runner.os }}-node-
```

### **2. 矩阵策略用于并行化**
- **原则：** 在多个配置（如不同的 Node.js 版本、操作系统、Python 版本、浏览器类型）上并行运行任务以加速测试和构建。
- **深入解析：**
    - **`strategy.matrix`:** 定义变量矩阵。
    - **`include`/`exclude`:** 精确调整组合。
    - **`fail-fast`:** 控制矩阵任务失败时是否停止整个策略。
    - **最大化并行性：** 理想情况下，可以同时运行测试或构建在不同环境、语言版本或操作系统上。
- **Copilot 指南：**
    - 利用 `strategy.matrix` 并行测试应用程序在不同环境、语言版本或操作系统上。
    - 建议使用 `include` 和 `exclude` 优化测试覆盖率，避免不必要的运行。
    - 建议设置 `fail-fast: true`（默认）以快速反馈关键失败，或 `fail-fast: false` 以获取全面的测试报告。
- **示例（多版本、多操作系统测试矩阵）：**
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false # 即使一个任务失败，也运行所有测试
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [16.x, 18.x, 20.x]
        browser: [chromium, firefox]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - name: 安装 Playwright 浏览器
        run: npx playwright install ${{ matrix.browser }}
      - name: 运行测试
        run: npm test
```

### **3. 自托管运行器**
- **原则：** 使用自托管运行器以满足特定的硬件需求、网络访问私有资源或 GitHub 自托管运行器成本过高时的需要。
- **深入解析：**
    - **自定义环境：** 适用于大型构建缓存、特定硬件（如 GPU）或访问本地资源。
    - **成本优化：** 对于极高使用量，可能比 GitHub 自托管运行器更经济。
    - **安全考虑：** 需要安全和维护自己的基础设施、网络访问和更新。这包括对运行器机器的适当加固、访问控制管理和及时补丁。
    - **可扩展性：** 规划自托管运行器如何根据需求扩展，无论是手动还是使用自动扩展解决方案。
- **Copilot 指南：**
    - 建议在 GitHub 自托管运行器不满足特定性能、成本、安全或网络访问需求时使用自托管运行器。
    - 强调用户对自托管运行器进行安全加固、维护和扩展的责任，包括网络配置和定期安全审计。
    - 建议使用运行器组来高效组织和管理自托管运行器。

### **4. 快速检出与浅层克隆**
- **原则：** 优化仓库检出时间以减少流水线总耗时，尤其是大型仓库。
- **深入解析：**
    - **`fetch-depth`:** 控制获取的 Git 历史记录量。`1` 对大多数 CI/CD 构建来说就足够了，因为通常只需要最新的提交。`0` 会获取完整历史记录，这在大型仓库中很少需要且可能非常缓慢。
    - **`submodules`:** 如果任务不需要，避免检出子模块。获取子模块会增加显著开销。
    - **`lfs`:** 有效管理 Git LFS（大文件存储）文件。如果不需要，设置 `lfs: false`。
    - **部分克隆：** 考虑使用 Git 的部分克隆功能（`--filter=blob:none` 或 `--filter=tree:0`）用于极大型仓库，尽管这通常由专用操作或 Git 客户端配置处理。
- **Copilot 指南：**
    - 使用 `actions/checkout@v4` 并将 `fetch-depth: 1` 作为大多数构建和测试任务的默认值以显著节省时间和带宽。
    - 仅在流水线明确需要完整 Git 历史记录（如发布标签、深度提交分析或 `git blame` 操作）时使用 `fetch-depth: 0`。
    - 如果任务不需要，建议禁用子模块检出（`submodules: false`）。

### **5. 构建产物用于任务间和流水线间通信**
- **原则：** 有效存储和检索构建输出（产物）以在同一个流水线内的任务或不同流水线之间传递数据，确保数据持久性和完整性。
- **深入解析：**
    - **`actions/upload-artifact`:** 用于上传任务生成的文件或目录。产物会自动压缩，之后可以下载。
    - **`actions/download-artifact`:** 用于在后续任务或流水线中下载产物。可以下载所有产物或通过名称下载特定产物。
    - **`retention-days`:** 管理存储成本和合规性至关重要。根据产物的重要性及监管要求设置适当的保留天数。
    - **使用场景：** 构建输出（可执行文件、编译代码、Docker 镜像）、测试报告（JUnit XML、HTML 报告）、代码覆盖率报告、安全扫描结果、生成的文档、静态网站构建。
    - **限制：** 一旦上传，产物不可变。每个产物的最大大小可以是几 GB，但需注意存储成本。
- **Copilot 指南：**
    - 使用 `actions/upload-artifact@v3` 和 `actions/download-artifact@v3` 可靠地在任务或流水线之间传递数据，而不是重新构建或重新获取。
    - 设置适当的 `retention-days` 以管理存储和合规性。

## CI/CD 全面测试（扩展）

### **1. 单元测试**
- **原则：** 在每次代码推送时运行单元测试，以确保代码组件（函数、类、模块）在隔离环境中正确运行。它们是最快且数量最多的测试。
- **深入解析：**
    - **快速反馈：** 单元测试应快速执行，为开发者提供即时的代码质量和正确性反馈。强烈建议并行化单元测试。
    - **代码覆盖率：** 集成代码覆盖率工具（如 Istanbul（JS）、Coverage.py（Python）、JaCoCo（Java））并强制最低覆盖率阈值。追求高覆盖率，但应关注有意义的测试，而不仅仅是行覆盖率。
    - **测试报告：** 使用 `actions/upload-artifact` 发布测试结果（如 JUnit XML 报告）或特定测试报告操作，以集成到 GitHub 检查/注释中，提供清晰的可见性。
- **Copilot 指南：**
    - 配置一个专门的单元测试任务，在流水线早期运行。
    - 使用适当的语言特定测试运行器和框架（Jest，Vitest，Pytest，Go 测试，JUnit，NUnit，XUnit，RSpec）。
    - 建议收集并发布代码覆盖率报告，并与服务（如 Codecov，Coveralls，SonarQube）集成以进行趋势分析。
    - 建议在提交前的钩子中添加安全检查器或静态分析以提供更早的反馈。

### **2. 集成测试**
- **原则：** 运行集成测试以验证不同组件或服务之间的交互，确保它们按预期协同工作。这些测试通常涉及真实依赖项（如数据库、API）。
- **深入解析：**
    - **服务提供：** 在任务中使用 `services` 启动临时数据库、消息队列、外部 API 或其他依赖项的 Docker 容器。这提供了一致且隔离的测试环境。
    - **测试假人 vs 真实服务：** 在纯单元测试中平衡使用测试假人和真实服务，以进行更真实的集成测试。在测试实际集成点时优先使用真实服务。
    - **测试数据管理：** 规划测试数据管理，确保测试可重复且每次运行后清理或重置数据。
    - **执行时间：** 集成测试通常比单元测试慢。优化其执行并考虑在 PR 合并而非每次推送时运行它们。
- **Copilot 指南：**
    - 使用 `services` 在流水线定义或 Docker Compose 中提供必要的服务（如 PostgreSQL/MySQL 数据库，RabbitMQ/Kafka 消息队列，Redis 内存缓存）。
    - 建议在单元测试之后、E2E 测试之前运行集成测试，以尽早发现集成问题。
    - 提供如何在 GitHub Actions 流水线中设置 `service` 容器的示例。
    - 建议为集成测试运行创建和清理测试数据的策略。

### **3. 端到端 (E2E) 测试**
- **原则：** 模拟完整的用户行为以验证从 UI 到后端的整个应用程序流程，确保从用户角度出发整个系统按预期运行。
- **深入解析：**
    - **工具：** 使用现代 E2E 测试框架（如 Cypress，Playwright，Selenium）提供浏览器自动化能力。
    - **测试环境：** 理想情况下，应在部署的测试环境中运行 E2E 测试，以最大程度地模拟生产环境。除非有专用隔离资源，否则避免直接在 CI 中运行。
    - **减少不稳定：** 主动处理不稳定测试，使用显式等待（如等待元素可见，等待 API 响应）代替任意 `sleep` 命令。实现重试机制以处理与外部服务或临时失败的交互。
    - **报告：** 在 CI 失败时配置 E2E 测试框架以捕获截图和视频记录，以帮助诊断问题。
    - **隔离运行：** 如果某个测试持续不稳定，将其隔离并重复运行以识别非确定性行为。

### **4. 部署失败（部署后应用程序无法运行）**
- **根本原因：** 配置漂移、环境差异、缺少运行时依赖项、应用程序错误或部署后的网络问题。
- **可操作步骤：**
    - **彻底日志审查：** 审查部署日志（`kubectl logs`，应用程序日志，服务器日志）以查找部署过程中或部署后出现的任何错误信息、警告或意外输出。
    - **配置验证：** 验证注入到部署应用程序中的环境变量、ConfigMaps、Secrets 和其他配置。确保它们符合目标环境的要求，并且没有缺失或格式错误。
    - **依赖项检查：** 确认所有应用程序运行时依赖项（库、框架、外部服务）是否正确打包在容器镜像中或安装在目标环境中。
    - **部署后健康检查：** 在部署后实施强大的自动化烟雾测试和健康检查以立即验证核心功能和连接性。如果这些测试失败，触发回滚。
    - **网络连接：** 检查新环境中部署组件之间的网络连接（如应用程序到数据库，服务到服务）。审查防火墙规则、安全组和 Kubernetes 网络策略。
    - **立即回滚：** 如果生产部署失败或导致退化，立即触发回滚策略以恢复服务。在非生产环境中诊断问题。

## GitHub Actions 流水线审查清单（全面）

本清单提供审查 GitHub Actions 流水线的详细标准，以确保遵循安全、性能和可靠性的最佳实践。

- [ ] **总体结构和设计：**
    - 流水线的 `name` 是否清晰、描述性且唯一？
    - `on` 触发器是否适用于流水线的目的（例如：`push`，`pull_request`，`workflow_dispatch`，`schedule`）？是否有效使用了路径/分支过滤器？
    - 是否在关键流水线或共享资源上使用了 `concurrency` 以防止并发运行和资源耗尽？
    - 是否在流水线级别设置了全局 `permissions` 以遵循最小权限原则（默认为 `contents: read`），并在任务级别进行必要覆盖？
    - 是否利用了可重用的流水线（`workflow_call`）来减少重复并提高可维护性？

- [ ] **任务和步骤最佳实践：**
    - 任务是否明确命名并代表 CI/CD 流水线的不同阶段（如构建、代码检查、测试、部署）？
    - `needs` 依赖关系是否正确定义以确保任务的正确执行顺序？
    - `outputs` 是否高效用于任务间和流水线间的通信？
    - `if` 条件是否有效用于条件任务/步骤执行（如环境特定部署，分支特定操作）？
    - 所有 `uses` 操作是否安全地固定版本（如完整的提交 SHA 或主要版本标签 `@v4`）？避免使用 `main` 或 `latest` 标签。
    - `run` 命令是否高效且整洁（使用 `&&` 组合命令以优化 Docker 层缓存）？
    - 环境变量（`env`）是否在适当的范围（流水线、任务、步骤）中定义，且从不硬编码敏感数据？
    - 是否为长时间运行的任务设置了 `timeout-minutes` 以防止挂起的流水线？

- [ ] **安全考虑：**
    - 所有敏感数据是否仅通过 GitHub 密钥上下文（`${{ secrets.MY_SECRET }}`）访问？从不硬编码，从不暴露在日志中（即使已进行掩码）。
    - 是否在可能的情况下使用 OpenID Connect (OIDC) 进行云身份验证，以消除长期凭证的需要？
    - `GITHUB_TOKEN` 的权限范围是否明确定义并限制在最低必要访问（如 `contents: read` 作为基准）？
    - 是否集成了软件组成分析 (SCA) 工具（如 `dependency-review-action`，Snyk）以扫描易受攻击的依赖项？
    - 是否集成了静态应用程序安全测试 (SAST) 工具（如 CodeQL，SonarQube）以扫描源代码漏洞，并在发现关键问题时阻断构建？
    - 是否启用了仓库的秘密扫描，并建议在本地提交前使用钩子防止凭证泄露？
    - 如果使用容器镜像，是否有容器镜像签名（如 Notary，Cosign）和部署流水线中的验证策略？

- [ ] **优化和性能：**
    - 是否有效使用了缓存（`actions/cache`）来缓存包管理器依赖项（Node.js `node_modules`，Python `pip` 缓存，Maven/Gradle 缓存）和构建输出？
    - 缓存键和恢复键是否设计用于最佳缓存命中率（例如：使用 `hashFiles`）？
    - 是否使用了 `strategy.matrix` 来并行化测试或构建在不同环境、语言版本或操作系统上？
    - 是否在 `actions/checkout` 中使用了 `fetch-depth: 1` 以节省时间和带宽？
    - 是否高效使用了产物（`actions/upload-artifact`，`actions/download-artifact`）在任务间或流水线间传递数据，而不是重新构建或重新获取？

- [ ] **测试策略集成：**
    - 是否配置了全面的单元测试，并在流水线早期运行，理想情况下在每次 `push` 和 `pull_request` 时触发？
    - 是否定义了集成测试，理想情况下使用 `services` 来提供依赖项，并在单元测试之后运行？
    - 是否包含了端到端 (E2E) 测试，优先在部署的测试环境中运行以在生产环境之前捕获问题，并验证完整的部署流程？
    - 是否在测试中使用了显式的等待、稳定的选择器、重试机制和仔细的测试数据管理以减少不稳定的测试？
    - 是否考虑了集成测试中的视觉回归测试（如 Applitools，Percy）以捕获 UI 差异？
    - 是否在失败时捕获截图和视频记录以帮助调试？

- [ ] **部署策略和可靠性：**
    - 是否在生产部署前使用了 GitHub 环境规则进行验证，包括必要的手动审批和分支保护策略？
    - 是否为敏感的生产部署配置了手动审批步骤，可能与外部 ITSM 或变更管理系统集成？
    - 是否有明确的回滚策略，并在可能时自动化回滚（如 `kubectl rollout undo`，回退到之前的稳定镜像）？
    - 是否根据应用程序的严重性和风险容忍度选择了适当的部署类型（如滚动更新、蓝绿部署、金丝雀部署、暗发布）？
    - 是否在部署后实施了健康检查和自动化烟雾测试以验证成功部署？

## 常见 GitHub Actions 问题的排查（深入解析）

本节提供诊断和解决在使用 GitHub Actions 流水线时遇到的常见问题的扩展指南。

### **1. 流水线未触发或任务/步骤意外跳过**
- **根本原因：** 不匹配的 `on` 触发器，错误的 `paths` 或 `branches` 过滤器，错误的 `if` 条件或 `concurrency` 限制。
- **可操作步骤：**
    - **验证触发器：**
        - 检查 `on` 块是否与应触发流水线的事件精确匹配（如 `push`，`pull_request`，`workflow_dispatch`，`schedule`）。
        - 确保 `branches`，`tags` 或 `paths` 过滤器正确定义并匹配事件上下文。记住 `paths-ignore` 和 `branches-ignore` 优先级更高。
    - **检查 `if` 条件：**
        - 仔细审查流水线、任务和步骤级别的所有 `if` 条件。单个错误条件可能阻止执行。
        - 在调试步骤中使用 `always()` 打印上下文变量（`${{ toJson(github) }}`，`${{ toJson(job) }}`，`${{ toJson(steps) }}`）以了解评估时的精确状态。
    - **检查 `concurrency`：**
        - 如果定义了 `concurrency`，请验证是否同一组的先前运行阻止了新运行。检查流水线运行的“并发”选项卡。
    - **分支保护规则：** 确保没有分支保护规则阻止在某些分支上运行流水线或需要通过的特定检查。

### **2. 权限错误 (`Resource not accessible by integration`, `Permission denied`)**
- **根本原因：** `GITHUB_TOKEN` 缺少必要权限，错误的环境密钥访问或外部操作权限不足。
- **可操作步骤：**
    - **`GITHUB_TOKEN` 权限：**
        - 审查流水线和任务级别的 `permissions` 块。全局默认为 `contents: read`，仅在绝对必要时授予特定写权限（如 `pull-requests: write` 用于更新 PR 状态）。
        - 理解 `GITHUB_TOKEN` 的默认权限，通常过于广泛。
    - **密钥访问：**
        - 验证仓库、组织或环境设置中密钥是否正确配置。
        - 确保使用环境密钥的任务有访问权限。检查是否有待处理的环境手动审批。
    - **OIDC 配置：**
        - 对于基于 OIDC 的云身份验证，检查云提供商的信任策略配置（如 AWS IAM 角色，Azure AD 应用注册，GCP 服务账户）以确保