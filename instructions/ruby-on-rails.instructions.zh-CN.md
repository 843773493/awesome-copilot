

---
描述：'Ruby on Rails 编码规范和指南'
适用范围：'**/*.rb'
---

# Ruby on Rails

## 通用指南

- 遵循 RuboCop 风格指南，并使用 `rubocop`、`standardrb` 或 `rufo` 等工具保持格式一致。
- 使用 snake_case 命名变量/方法，使用 CamelCase 命名类/模块。
- 保持方法简短且专注；使用早期返回、守卫子句和私有方法来减少复杂度。
- 优先使用有意义的名称，而非简短或通用的名称。
- 仅在必要时添加注释 — 避免解释显而易见的内容。
- 将单一职责原则应用于类、方法和模块。
- 优先使用组合而非继承；将可重用的逻辑提取到模块或服务中。
- 保持控制器简洁 — 将业务逻辑移至模型、服务或命令/查询对象中。
- 有意识地应用“胖模型，瘦控制器”模式，并确保抽象清晰。
- 将业务逻辑提取到服务对象中以实现可重用性和可测试性。
- 使用部分视图（partials）或视图组件（view components）来减少重复并简化视图。
- 使用 `unless` 处理负条件，但避免与 `else` 搭配以提高清晰度。
- 避免深度嵌套的条件判断 — 优先使用守卫子句和方法提取。
- 使用安全导航（`&.`）而非多个 `nil` 检查。
- 优先使用 `.present?`、`.blank?` 和 `.any?` 而非手动的 nil/空值检查。
- 在路由和控制器操作中遵循 RESTful 规范。
- 使用 Rails 生成器（generators）以一致的方式创建资源。
- 使用强参数（strong parameters）安全地白名单属性。
- 优先使用枚举（enums）和类型属性以提高模型清晰度和验证效果。
- 保持迁移（migrations）数据库中立；尽量避免使用原始 SQL。
- 为外键和频繁查询的列始终添加索引。
- 在数据库层定义 `null: false` 和 `unique: true`，而不仅仅是模型层。
- 使用 `find_each` 遍历大型数据集以减少内存使用。
- 在模型中作用域查询或使用查询对象（query objects）以提高清晰度和可重用性。
- 稀疏使用 `before_action` 回调 — 避免在其中放置业务逻辑。
- 使用 `Rails.cache` 存储昂贵的计算或频繁访问的数据。
- 使用 `Rails.root.join(...)` 构建文件路径，而非硬编码。
- 在关联中使用 `class_name` 和 `foreign_key` 明确关系。
- 使用 `Rails.application.credentials` 或环境变量（ENV variables）将密钥和配置隔离在代码库之外。
- 为模型、服务和帮助器编写隔离的单元测试。
- 用请求/系统测试覆盖端到端逻辑。
- 使用后台任务（ActiveJob）处理非阻塞操作，如发送邮件或调用 API。
- 使用 `FactoryBot`（RSpec）或固定数据（fixtures）（Minitest）来干净地设置测试数据。
- 避免使用 `puts` — 使用 `byebug`、`pry` 或日志工具进行调试。
- 使用 YARD 或 RDoc 文档化复杂代码路径和方法。

## 应用目录结构

- 在 `app/services` 目录中定义服务对象以封装业务逻辑。
- 在 `app/forms` 中使用表单对象管理验证和提交逻辑。
- 在 `app/serializers` 目录中实现 JSON 序列化器以格式化 API 响应。
- 在 `app/policies` 中定义授权策略以控制用户对资源的访问。
- 通过将模式、查询和突变（mutations）组织在 `app/graphql` 中构建 GraphQL API。
- 在 `app/validators` 中创建自定义验证器以强制执行特定的验证逻辑。
- 在 `app/queries` 中隔离和封装复杂的 ActiveRecord 查询以提高可重用性和可测试性。
- 在 `app/types` 目录中定义自定义数据类型和转换逻辑以扩展或覆盖 ActiveModel 类型行为。

## 命令

- 使用 `rails generate` 创建新的模型、控制器和迁移文件。
- 使用 `rails db:migrate` 应用数据库迁移。
- 使用 `rails db:seed` 用初始数据填充数据库。
- 使用 `rails db:rollback` 回退最后一次迁移。
- 使用 `rails console` 在 REPL 环境中与 Rails 应用交互。
- 使用 `rails server` 启动开发服务器。
- 使用 `rails test` 运行测试套件。
- 使用 `rails routes` 列出应用中定义的所有路由。
- 使用 `rails assets:precompile` 编译生产环境的资源。

## API 开发最佳实践

- 使用 Rails 的 `resources` 结构化路由以遵循 RESTful 规范。
- 使用命名空间路由（例如 `/api/v1/`）进行版本控制和向前兼容。
- 使用 `ActiveModel::Serializer` 或 `fast_jsonapi` 对响应进行序列化以保持输出一致。
- 为每个响应返回适当的 HTTP 状态码（例如 200 OK、201 Created、422 Unprocessable Entity）。
- 使用 `before_action` 过滤器加载和授权资源，而非业务逻辑。
- 利用分页（例如 `kaminari` 或 `pagy`）处理返回大型数据集的端点。
- 使用中间件或工具（如 `rack-attack`）对敏感端点进行速率限制和节流。
- 以结构化的 JSON 格式返回错误，包括错误代码、消息和详细信息。
- 使用强参数（strong parameters）对输入参数进行净化和白名单处理。
- 使用自定义序列化器或呈现器（presenters）将内部逻辑与响应格式解耦。
- 通过 `includes` 预加载相关数据以避免 N+1 查询。
- 通过 `ActiveJob::TestHelper` 或 `have_enqueued_job` 匹配器对非阻塞任务（如发送邮件或与外部 API 同步）进行后台任务处理。
- 使用 CI 工具（如 GitHub Actions、CircleCI）确保测试在不同环境中运行一致。
- 使用自定义匹配器（RSpec）或自定义断言（Minitest）实现可重用且表达力强的测试逻辑。
- 通过类型（如 `:model`、`:request`、`:feature`）标记测试以实现更快且针对性的测试运行。
- 避免脆弱的测试 — 除非明确需要，否则不要依赖特定时间戳、随机数据或顺序。
- 为跨多个层级（模型、视图、控制器）的端到端流程编写集成测试。
- 保持测试快速、可靠且与生产代码一样 DRY（Don't Repeat Yourself）。

## 测试指南

- 使用 `test/models`（Minitest）或 `spec/models`（RSpec）为模型编写单元测试以验证业务逻辑。
- 使用固定数据（fixtures）（Minitest）或 `FactoryBot`（RSpec）创建的工厂来干净且一致地管理测试数据。
- 将控制器规范组织在 `test/controllers` 或 `spec/requests` 中以测试 RESTful API 行为。
- 在 RSpec 中优先使用 `before` 块或在 Minitest 中使用 `setup` 初始化通用测试数据。
- 避免在测试中调用外部 API — 使用 `WebMock`、`VCR` 或 `stub_request` 来隔离测试环境。
- 使用 Minitest 的系统测试或 RSpec 的功能规范（feature specs）配合 Capybara 模拟完整的用户流程。
- 将缓慢且昂贵的测试（如外部服务、文件上传）隔离到单独的测试类型或标签中。
- 运行测试覆盖率工具（如 `SimpleCov`）以确保足够的代码覆盖率。
- 避免在测试中使用 `sleep`；在 Minitest 中使用 `perform_enqueued_jobs` 或在 RSpec 中使用 `ActiveJob::TestHelper`。
- 使用数据库清理工具（如 `rails test:prepare`、`DatabaseCleaner` 或 `transactional_fixtures`）保持测试间的数据库状态干净。
- 通过 `ActiveJob::TestHelper` 或 `have_enqueued_job` 匹配器测试后台任务。
- 使用 CI 工具（如 GitHub Actions、CircleCI）确保测试在不同环境中运行一致。
- 使用自定义匹配器（RSpec）或自定义断言（Minitest）实现可重用且表达力强的测试逻辑。
- 通过类型（如 `:model`、`:request`、`:feature`）标记测试以实现更快且针对性的测试运行。
- 避免脆弱的测试 — 除非明确需要，否则不要依赖特定时间戳、随机数据或顺序。
- 为跨多个层级（模型、视图、控制器）的端到端流程编写集成测试。
- 保持测试快速、可靠且与生产代码一样 DRY（Don't Repeat Yourself）。