# 错误处理模式

在您的 Copilot SDK 应用程序中优雅地处理错误。

> **可运行示例：** [recipe/error-handling.ts](recipe/error-handling.ts)
>
> ```bash
> cd recipe && npm install
> npx tsx error-handling.ts
> # 或: npm run error-handling
> ```

## 示例场景

您需要处理各种错误情况，例如连接失败、超时和无效响应。

## 基础 try-catch

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();

try {
    await client.start();
    const session = await client.createSession({ model: "gpt-5" });

    const response = await session.sendAndWait({ prompt: "Hello!" });
    console.log(response?.data.content);

    await session.destroy();
} catch (error) {
    console.error("错误：", error.message);
} finally {
    await client.stop();
}
```

## 处理特定错误类型

```typescript
try {
    await client.start();
} catch (error) {
    if (error.message.includes("ENOENT")) {
        console.error("未找到 Copilot CLI。请先安装它。");
    } else if (error.message.includes("ECONNREFUSED")) {
        console.error("无法连接到 Copilot CLI 服务器。");
    } else {
        console.error("意外错误：", error.message);
    }
}
```

## 超时处理

```typescript
const session = await client.createSession({ model: "gpt-5" });

try {
    // sendAndWait 带超时（毫秒）
    const response = await session.sendAndWait(
        { prompt: "复杂问题..." },
        30000 // 30秒超时
    );

    if (response) {
        console.log(response.data.content);
    } else {
        console.log("未收到响应");
    }
} catch (error) {
    if (error.message.includes("timeout")) {
        console.error("请求超时");
    }
}
```

## 中止请求

```typescript
const session = await client.createSession({ model: "gpt-5" });

// 启动请求
session.send({ prompt: "写一个很长的故事..." });

// 在满足某些条件后中止请求
setTimeout(async () => {
    await session.abort();
    console.log("请求已中止");
}, 5000);
```

## 优雅关闭

```typescript
process.on("SIGINT", async () => {
    console.log("正在关闭...");

    const errors = await client.stop();
    if (errors.length > 0) {
        console.error("清理错误：", errors);
    }

    process.exit(0);
});
```

## 强制停止

```typescript
// 如果 stop() 耗时过长，可强制停止
const stopPromise = client.stop();
const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error("超时")), 5000));

try {
    await Promise.race([stopPromise, timeout]);
} catch {
    console.log("正在强制停止...");
    await client.forceStop();
}
```

## 最佳实践

1. **始终进行清理**：使用 try-finally 确保调用 `client.stop()`
2. **处理连接错误**：CLI 可能未安装或未运行
3. **设置适当的超时**：长时间运行的请求应设置超时
4. **记录错误日志**：捕获错误详情以便调试
