

---
description: '使用官方PHP SDK通过基于属性的发现和多种传输选项构建Model Context Protocol服务器的最佳实践'
applyTo: '**/*.php'
---

# PHP MCP服务器开发最佳实践

本指南提供了使用由The PHP Foundation维护的官方PHP SDK构建Model Context Protocol (MCP)服务器的最佳实践。

## 安装与设置

### 通过Composer安装

```bash
composer require mcp/sdk
```

### 项目结构

组织您的PHP MCP服务器项目：

```
my-mcp-server/
├── composer.json
├── src/
│   ├── Tools/
│   │   ├── Calculator.php
│   │   └── FileManager.php
│   ├── Resources/
│   │   ├── ConfigProvider.php
│   │   └── DataProvider.php
│   ├── Prompts/
│   │   └── PromptGenerator.php
│   └── Server.php
├── server.php           # 服务器入口
└── tests/
    └── ToolsTest.php
```

### Composer配置

```json
{
    "name": "your-org/mcp-server",
    "description": "MCP服务器用于...",
    "type": "project",
    "require": {
        "php": "^8.2",
        "mcp/sdk": "^0.1"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

## 服务器实现

### 基于属性的发现服务器

创建您的服务器入口：

```php
#!/usr/bin/env php
<?php

declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

use Mcp\Server;
use Mcp\Server\Transport\StdioTransport;

$server = Server::builder()
    ->setServerInfo('My MCP Server', '1.0.0')
    ->setDiscovery(__DIR__, ['.'])
    ->build();

$transport = new StdioTransport();

$server->run($transport);
```

### 带缓存的服务器

使用PSR-16缓存以提高性能：

```php
use Symfony\Component\Cache\Adapter\FilesystemAdapter;
use Symfony\Component\Cache\Psr16Cache;

$cache = new Psr16Cache(new FilesystemAdapter('mcp-discovery'));

$server = Server::builder()
    ->setServerInfo('My MCP Server', '1.0.0')
    ->setDiscovery(
        basePath: __DIR__,
        scanDirs: ['.', 'src'],
        excludeDirs: ['vendor', 'tests'],
        cache: $cache
    )
    ->build();
```

### 手动注册

程序化注册功能：

```php
use App\Tools\Calculator;
use App\Resources\Config;

$server = Server::builder()
    ->setServerInfo('My MCP Server', '1.0.0')
    ->addTool([Calculator::class, 'add'], 'add')
    ->addTool([Calculator::class, 'multiply'], 'multiply')
    ->addResource([Config::class, 'getSettings'], 'config://app/settings')
    ->build();
```

## 工具开发

### 带属性的简单工具

```php
<?php

namespace App\Tools;

use Mcp\Capability\Attribute\McpTool;

class Calculator
{
    /**
     * 将两个数字相加。
     * 
     * @param int $a 第一个数字
     * @param int $b 第二个数字
     * @return int 两个数字的和
     */
    #[McpTool]
    public function add(int $a, int $b): int
    {
        return $a + $b;
    }
}
```

### 带自定义名称的工具

```php
use Mcp\Capability\Attribute\McpTool;

class FileManager
{
    /**
     * 从文件系统读取文件内容。
     */
    #[McpTool(name: 'read_file')]
    public function readFileContent(string $path): string
    {
        if (!file_exists($path)) {
            throw new \InvalidArgumentException("文件未找到: {$path}");
        }
        
        return file_get_contents($path);
    }
}
```

### 带验证和模式的工具

```php
use Mcp\Capability\Attribute\{McpTool, Schema};

class UserManager
{
    #[McpTool(name: 'create_user')]
    public function createUser(
        #[Schema(format: 'email')]
        string $email,
        
        #[Schema(minimum: 18, maximum: 120)]
        int $age,
        
        #[Schema(
            pattern: '^[A-Z][a-z]+$',
            description: '首字母大写的姓名'
        )]
        string $firstName
    ): array
    {
        return [
            'id' => uniqid(),
            'email' => $email,
            'age' => $age,
            'firstName' => $firstName
        ];
    }
}
```

### 带复杂返回类型的工具

```php
use Mcp\Schema\Content\{TextContent, ImageContent};

class ReportGenerator
{
    #[McpTool]
    public function generateReport(string $type): array
    {
        return [
            new TextContent('报告已生成:'),
            TextContent::code($this->generateCode($type), 'php'),
            new TextContent('摘要: 所有检查通过。')
        ];
    }
    
    #[McpTool]
    public function getChart(string $chartType): ImageContent
    {
        $imageData = $this->generateChartImage($chartType);
        
        return new ImageContent(
            data: base64_encode($imageData),
            mimeType: 'image/png'
        );
    }
}
```

### 带匹配表达式的工具

```php
#[McpTool(name: 'calculate')]
public function performCalculation(float $a, float $b, string $operation): float
{
    return match($operation) {
        'add' => $a + $b,
        'subtract' => $a - $b,
        'multiply' => $a * $b,
        'divide' => $b != 0 ? $a / $b : 
            throw new \InvalidArgumentException('除以零'),
        default => throw new \InvalidArgumentException('无效的操作')
    };
}
```

## 资源实现

### 静态资源

```php
<?php

namespace App\Resources;

use Mcp\Capability\Attribute\McpResource;

class ConfigProvider
{
    /**
     * 提供当前应用程序的配置。
     */
    #[McpResource(
        uri: 'config://app/settings',
        name: 'app_settings',
        mimeType: 'application/json'
    )]
    public function getSettings(): array
    {
        return [
            'version' => '1.0.0',
            'debug' => false,
            'features' => ['auth', 'logging']
        ];
    }
}
```

### 带变量的资源模板

```php
use Mcp\Capability\Attribute\McpResourceTemplate;

class UserProvider
{
    /**
     * 通过ID和部分检索用户资料信息。
     */
    #[McpResourceTemplate(
        uriTemplate: 'user://{userId}/profile/{section}',
        name: 'user_profile',
        description: '按部分获取用户资料数据',
        mimeType: 'application/json'
    )]
    public function getUserProfile(string $userId, string $section): array
    {
        // 变量顺序必须与URI模板顺序一致
        return $this->users[$userId][$section] ?? 
            throw new \InvalidArgumentException("未找到资料部分");
    }
}
```

### 带文件内容的资源

```php
use Mcp\Schema\Content\{TextResourceContents, BlobResourceContents};

class FileProvider
{
    #[McpResource(uri: 'file://readme.txt', mimeType: 'text/plain')]
    public function getReadme(): TextResourceContents
    {
        return new TextResourceContents(
            uri: 'file://readme.txt',
            mimeType: 'text/plain',
            text: file_get_contents(__DIR__ . '/README.txt')
        );
    }
    
    #[McpResource(uri: 'file://image.png', mimeType: 'image/png')]
    public function getImage(): BlobResourceContents
    {
        $imageData = file_get_contents(__DIR__ . '/image.png');
        
        return new BlobResourceContents(
            uri: 'file://image.png',
            mimeType: 'image/png',
            blob: base64_encode($imageData)
        );
    }
}
```

## 提示实现

### 基本提示

```php
<?php

namespace App\Prompts;

use Mcp\Capability\Attribute\McpPrompt;

class PromptGenerator
{
    /**
     * 生成代码审查请求提示。
     */
    #[McpPrompt(name: 'code_review')]
    public function reviewCode(string $language, string $code, string $focus = 'general'): array
    {
        return [
            ['role' => 'assistant', 'content' => '你是一位专业的代码审查员。'],
            ['role' => 'user', 'content' => "请审查这段{$language}代码，重点关注{$focus}:\n\n```{$language}\n{$code}\n```"]
        ];
    }
}
```

### 带混合内容的提示

```php
use Mcp\Schema\Content\{TextContent, ImageContent};
use Mcp\Schema\PromptMessage;
use Mcp\Schema\Enum\Role;

#[McpPrompt]
public function analyzeImage(string $imageUrl, string $question): array
{
    $imageData = file_get_contents($imageUrl);
    
    return [
        new PromptMessage(Role::Assistant, [
            new TextContent('你是一位图像分析专家。')
        ]),
        new PromptMessage(Role::User, [
            new TextContent($question),
            new ImageContent(
                data: base64_encode($imageData),
                mimeType: 'image/jpeg'
            )
        ])
    ];
}
```

## 完成提供者

### 值列表完成提供者

```php
use Mcp\Capability\Attribute\{McpPrompt, CompletionProvider};

#[McpPrompt]
public function generateContent(
    #[CompletionProvider(values: ['blog', 'article', 'tutorial', 'guide'])]
    string $contentType,
    
    #[CompletionProvider(values: ['beginner', 'intermediate', 'advanced'])]
    string $difficulty
): array
{
    return [
        ['role' => 'user', 'content' => "创建一个{$difficulty}级别的{$contentType}"]
    ];
}
```

### 枚举完成提供者

```php
enum Priority: string
{
    case LOW = 'low';
    case MEDIUM = 'medium';
    case HIGH = 'high';
}

enum Status
{
    case DRAFT;
    case PUBLISHED;
    case ARCHIVED;
}

#[McpResourceTemplate(uriTemplate: 'tasks/{taskId}')]
public function getTask(
    string $taskId,
    
    #[CompletionProvider(enum: Priority::class)]
    string $priority,
    
    #[CompletionProvider(enum: Status::class)]
    string $status
): array
{
    return $this->tasks[$taskId] ?? [];
}
```

### 自定义完成提供者

```php
use Mcp\Server\Session\InMemorySessionStore;

$server = Server::builder()
    ->setServerInfo('My Server', '1.0.0')
    ->setSession(new InMemorySessionStore(3600))
    ->build();
```

## 传输选项

### 标准输入/输出传输

用于命令行集成（默认）：

```php
use Mcp\Server\Transport\StdioTransport;

$transport = new StdioTransport();
$server->run($transport);
```

### HTTP传输

用于基于网络的集成：

```php
use Mcp\Server\Transport\StreamableHttpTransport;
use Nyholm\Psr7\Factory\Psr17Factory;

$psr17Factory = new Psr17Factory();

$request = $psr17Factory->createServerRequestFromGlobals();

$transport = new StreamableHttpTransport(
    $request,
    $psr17Factory,  // 响应工厂
    $psr17Factory   // 流工厂
);

$response = $server->run($transport);

// 在您的网络框架中发送响应
foreach ($response->getHeaders() as $name => $values) {
    foreach ($values as $value) {
        header("$name: $value", false);
    }
}

http_response_code($response->getStatusCode());
echo $response->getBody();
```

## 会话管理

### 内存会话（默认）

```php
$server = Server::builder()
    ->setServerInfo('My Server', '1.0.0')
    ->setSession(ttl: 7200) // 2小时
    ->build();
```

### 基于文件的会话

```php
use Mcp\Server\Session\FileSessionStore;

$server = Server::builder()
    ->setServerInfo('My Server', '1.0.0')
    ->setSession(new FileSessionStore(__DIR__ . '/sessions'))
    ->build();
```

### 自定义会话存储

```php
use Mcp\Server\Session\InMemorySessionStore;

$server = Server::builder()
    ->setServerInfo('My Server', '1.0.0')
    ->setSession(new InMemorySessionStore(3600))
    ->build();
```

## 错误处理

### 工具中的异常处理

```php
#[McpTool]
public function divideNumbers(float $a, float $b): float
{
    if ($b === 0.0) {
        throw new \InvalidArgumentException('不允许除以零');
    }
    
    return $a / $b;
}

#[McpTool]
public function processFile(string $filename): string
{
    if (!file_exists($filename)) {
        throw new \InvalidArgumentException("文件未找到: {$filename}");
    }
    
    if (!is_readable($filename)) {
        throw new \RuntimeException("文件不可读: {$filename}");
    }
    
    return file_get_contents($filename);
}
```

### 自定义错误响应

SDK会自动将异常转换为MCP客户端可理解的JSON-RPC错误响应。

## 测试

### PHPUnit工具测试

```php
<?php

namespace Tests;

use PHPUnit\Framework\TestCase;
use App\Tools\Calculator;

class CalculatorTest extends TestCase
{
    private Calculator $calculator;
    
    protected function setUp(): void
    {
        $this->calculator = new Calculator();
    }
    
    public function testAdd(): void
    {
        $result = $this->calculator->add(5, 3);
        $this->assertSame(8, $result);
    }
    
    public function testDivideByZero(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('除以零');

        $this->calculator->divide(10, 0);
    }
}
```

### 测试服务器发现

```php
public function testServerDiscoversTools(): void
{
    $server = Server::builder()
        ->setServerInfo('Test Server', '1.0.0')
        ->setDiscovery(__DIR__ . '/../src', ['.'])
        ->build();
    
    $capabilities = $server->getCapabilities();
    
    $this->assertArrayHasKey('tools', $capabilities);
    $this->assertNotEmpty($capabilities['tools']);
}
```

## 性能最佳实践

### 使用发现缓存

在生产环境中始终使用缓存：

```php
use Symfony\Component\Cache\Adapter\RedisAdapter;
use Symfony\Component\Cache\Psr16Cache;

$redis = new \Redis();
$redis->connect('127.0.0.1', 6379);

$cache = new Psr16Cache(new RedisAdapter($redis));

$server = Server::builder()
    ->setServerInfo('My Server', '1.0.0')
    ->setDiscovery(
        basePath: __DIR__,
        scanDirs: ['src'],
        excludeDirs: ['vendor', 'tests', 'var', 'cache'],
        cache: $cache
    )
    ->build();
```

### 优化扫描目录

仅扫描必要的目录：

```php
$server = Server::builder()
    ->setDiscovery(
        basePath: __DIR__,
        scanDirs: ['src/Tools', 'src/Resources'],  // 具体目录
        excludeDirs: ['vendor', 'tests', 'var', 'cache']
    )
    ->build();
```

### 使用OPcache

在生产环境中启用OPcache以提升PHP性能：

```ini
; php.ini
opcache.enable=1
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=10000
opcache.validate_timestamps=0
```

## 框架集成

### Laravel集成

```php
// app/Console/Commands/McpServer.php
namespace App\Console\Commands;

use Illuminate\Console\Command;
use Mcp\Server;
use Mcp\Server\Transport\StdioTransport;

class McpServer extends Command
{
    protected $signature = 'mcp:serve';
    protected $description = '启动MCP服务器';
    
    public function handle()
    {
        $server = Server::builder()
            ->setServerInfo('Laravel MCP Server', '1.0.0')
            ->setDiscovery(app_path(), ['Tools', 'Resources'])
            ->build();
        
        $transport = new StdioTransport();
        $server->run($transport);
    }
}
```

### Symfony集成

```php
// 使用symfony/mcp-bundle进行原生集成
composer require symfony/mcp-bundle
```

## 部署

### Docker部署

```dockerfile
FROM php:8.2-cli

# 安装扩展
RUN docker-php-ext-install pdo pdo_mysql

# 安装Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 设置工作目录
WORKDIR /app

# 复制应用程序
COPY . /app

# 安装依赖
RUN composer install --no-dev --optimize-autoloader

# 使服务器可执行
RUN chmod +x /app/server.php

CMD ["php", "/app/server.php"]
```

### systemd服务

```ini
[Unit]
Description=MCP PHP服务器
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/mcp-server
ExecStart=/usr/bin/php /var/www/mcp-server/server.php
Restart=always

[Install]
WantedBy=multi-user.target
```

## MCP客户端配置

### Claude桌面配置

```json
{
  "mcpServers": {
    "php-server": {
      "command": "php",
      "args": ["/absolute/path/to/server.php"]
    }
  }
}
```

### MCP检查器测试

```bash
npx @modelcontextprotocol/inspector php /path/to/server.php
```

## 其他资源

- [官方PHP SDK仓库](https://github.com/modelcontextprotocol/php-sdk)
- [MCP元素文档](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md)
- [服务器构建器文档](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
- [传输文档](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
- [示例](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md)
- [MCP规范](https://spec.modelcontextprotocol.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)