

描述: '使用 LangChain 与 Python 的说明'
适用范围: "**/*.py"

# LangChain Python 指南

这些说明指导 GitHub Copilot 为 LangChain 的 Python 应用生成代码和文档。重点在于 LangChain 特有的模式、API 和最佳实践。

## Runnable 接口（LangChain 特有）

LangChain 的 `Runnable` 接口是组合和执行链（chains）、聊天模型（chat models）、输出解析器（output parsers）、检索器（retrievers）以及 LangGraph 图表的基础。它提供了一种统一的 API 来调用、批量处理、流式处理、检查和组合组件。

**关键 LangChain 特有功能:**

- 所有主要的 LangChain 组件（聊天模型、输出解析器、检索器、图表）均实现 `Runnable` 接口。
- 支持同步（`invoke`、`batch`、`stream`）和异步（`ainvoke`、`abatch`、`astream`）执行。
- 批处理（`batch`、`batch_as_completed`）优化了并行 API 调用；通过 `RunnableConfig` 中的 `max_concurrency` 设置来控制并行度。
- 流式 API（`stream`、`astream`、`astream_events`）在输出生成时实时返回结果，这对响应式大语言模型（LLM）应用至关重要。
- 输入/输出类型是组件特定的（例如，聊天模型接受消息，检索器接受字符串，输出解析器接受模型输出）。
- 使用 `get_input_schema`、`get_output_schema` 及其 JSONSchema 变体来检查模式，用于验证和 OpenAPI 生成。
- 使用 `with_types` 覆盖复杂 LCEL 链中推断的输入/输出类型。
- 使用 LCEL 声明式组合 Runnables：`chain = prompt | chat_model | output_parser`。
- 在 Python 3.11+ 中自动传播 `RunnableConfig`（标签、元数据、回调、并发）；在 Python 3.9/3.10 的异步代码中需手动处理。
- 使用 `RunnableLambda`（简单转换）或 `RunnableGenerator`（流式转换）创建自定义 Runnables；避免直接子类化。
- 使用 `configurable_fields` 和 `configurable_alternatives` 配置运行时属性和替代方案，用于动态链和 LangServe 部署。

**LangChain 最佳实践:**

- 使用批处理进行大语言模型（LLM）或检索器的并行 API 调用；设置 `max_concurrency` 以避免速率限制。
- 对于聊天界面和长输出，优先使用流式 API。
- 在自定义链和部署端点中始终验证输入/输出模式。
- 在 `RunnableConfig` 中使用标签和元数据用于 LangSmith 的追踪和复杂链的调试。
- 对于自定义逻辑，使用 `RunnableLambda` 或 `RunnableGenerator` 包装函数，而不是直接子类化。
- 对于高级配置，通过 `configurable_fields` 和 `configurable_alternatives` 暴露字段和替代方案。

- 使用 LangChain 的聊天模型集成进行对话式 AI：

- 从 `langchain.chat_models` 或 `langchain_openai`（例如 `ChatOpenAI`）导入。
- 使用 `SystemMessage`、`HumanMessage`、`AIMessage` 组合消息。
- 对于工具调用，使用 `bind_tools(tools)` 方法。
- 对于结构化输出，使用 `with_structured_output(schema)`。

示例：
```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

chat = ChatOpenAI(model="gpt-4", temperature=0)
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain?")
]
response = chat.invoke(messages)
print(response.content)
```

- 将消息组合为 `SystemMessage`、`HumanMessage` 和可选的 `AIMessage` 对象列表。
- 对于 RAG（检索增强生成），将您的向量数据库与检索器结合，并与 LLM 链接（请参阅 LangChain 检索器和 RAGChain 文档）。
- 对于高级搜索，使用向量数据库特定选项：Pinecone 支持混合搜索和元数据过滤；Chroma 支持过滤和自定义距离度量。
- 始终在您的环境中验证向量数据库集成和 API 版本；LangChain 不同版本之间常见有破坏性变更。
- 示例（InMemoryVectorStore）:

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

embedding_model = OpenAIEmbeddings()
vector_store = InMemoryVectorStore(embedding=embedding_model)

documents = [Document(page_content="LangChain content", metadata={"source": "doc1"})]
vector_store.add_documents(documents=documents, ids=["doc1"])

results = vector_store.similarity_search("What is RAG?", k=2)
for doc in results:
    print(doc.page_content, doc.metadata)
```

- 对于生产环境，优先使用持久化向量数据库（Chroma、Pinecone、Qdrant、Weaviate），并根据提供商文档配置身份验证、扩展和备份。
- 参考: https://python.langchain.com/docs/integrations/vectorstores/

## 提示工程与治理

- 将标准提示存储在 `prompts/` 目录下，并从代码中通过文件名引用。
- 编写单元测试以断言所需占位符存在，并且渲染后的提示符合预期模式（长度、变量存在性）。
- 维护一个 CHANGELOG 记录影响行为的提示和模式变更。

## 聊天模型

LangChain 提供了一致的聊天模型接口，并支持监控、调试和优化功能。

### 集成

集成可以是：

1. 官方：由 LangChain 团队或提供商维护的 `langchain-<provider>` 包装集成。
2. 社区：贡献的集成（在 `langchain-community` 中）。

聊天模型通常遵循以 `Chat` 为前缀的命名规范（例如 `ChatOpenAI`、`ChatAnthropic`、`ChatOllama`）。不带 `Chat` 前缀（或带 `LLM` 后缀）的模型通常实现较旧的字符串输入/字符串输出接口，对于现代聊天流程不推荐使用。

### 接口

聊天模型实现 `BaseChatModel` 并支持 `Runnable` 接口：流式处理、异步、批处理等。许多操作接受和返回 LangChain 的 `messages`（如 `system`、`user`、`assistant` 角色）。详情请参阅 BaseChatModel API 参考文档。

关键方法包括：

- `invoke(messages, ...)` — 发送消息列表并接收响应。
- `stream(messages, ...)` — 在令牌到达时流式传输部分输出。
- `batch(inputs, ...)` — 批处理多个请求。
- `bind_tools(tools)` — 附加工具适配器以进行工具调用。
- `with_structured_output(schema)` — 请求结构化响应的辅助方法。

### 输入和输出

- LangChain 支持其自己的消息格式和 OpenAI 的消息格式；在您的代码库中保持一致选择。
- 消息包含 `role` 和 `content` 块；内容可以包含结构化或多媒体负载（如支持）。

### 标准参数

常见支持的参数（提供商依赖）：

- `model`: 模型标识符（例如 `gpt-4o`、`gpt-3.5-turbo`）。
- `temperature`: 随机性控制（0.0 确定性 — 1.0 创造性）。
- `timeout`: 取消前等待的秒数。
- `max_tokens`: 响应令牌限制。
- `stop`: 停止序列。
- `max_retries`: 网络/限制失败时的重试次数。
- `api_key`, `base_url`: 提供商认证和端点配置。
- `rate_limiter`: 可选的 BaseRateLimiter 用于间隔请求以避免提供商配额错误。

> 注意：并非所有提供商都实现了所有参数。请始终查阅提供商集成文档。

### 工具调用

聊天模型可以调用工具（API、数据库、系统适配器）。使用 LangChain 的工具调用 API 来：

- 通过严格的输入/输出类型注册工具。
- 观察并记录工具调用请求和结果。
- 在传递给模型或执行副作用之前验证工具输出。

请参阅 LangChain 文档中的工具调用指南以获取示例和安全模式。

### 结构化输出

使用 `with_structured_output` 或模式强制方法从模型请求 JSON 或类型化输出。结构化输出对于可靠提取和后续处理（解析器、数据库写入、分析）至关重要。

### 多模态

一些模型支持多模态输入（图像、音频）。请查阅提供商文档以了解支持的输入类型和限制。多模态输出较为罕见，应视为实验性功能并严格验证。

### 上下文窗口

模型具有有限的上下文窗口，以令牌数衡量。在设计对话流程时：

- 保持消息简洁，并优先考虑重要上下文。
- 当上下文超出窗口时，在模型外部修剪旧上下文（摘要或归档）。
- 使用检索器 + RAG 模式来呈现相关的长格式上下文，而不是将大文档粘贴到聊天中。

## 高级主题

### 速率限制

- 在初始化聊天模型时使用 `rate_limiter` 来间隔调用。
- 实现指数退避重试，并在被限制时考虑备用模型或降级模式。

### 缓存

- 对于对话的精确输入缓存通常效果不佳。考虑使用基于语义的缓存（基于嵌入）来处理重复的语义级查询。
- 语义缓存引入了对嵌入的依赖，不适用于所有场景。
- 仅在缓存能降低成本且满足正确性要求时（例如 FAQ 机器人）使用缓存。

## 最佳实践

- 为公共 API 使用类型提示和数据类。
- 在调用 LLM 或工具前验证输入。
- 从密钥管理器加载密钥；从不记录密钥或未脱敏的模型输出。
- 确定性测试：模拟 LLM 和嵌入调用。
- 缓存嵌入和频繁检索结果。
- 可观测性：记录请求 ID、模型名称、延迟和净化后的令牌计数。
- 对外部调用实现指数退避和幂等性。

## 安全与隐私

- 将模型输出视为不可信。在执行生成的代码或系统命令前进行净化。
- 验证任何用户提供的 URL 和输入以避免 SSRF 和注入攻击。
- 文档数据保留政策，并添加 API 以在请求时擦除用户数据。
- 限制存储的 PII（个人身份信息）并加密静态敏感字段。