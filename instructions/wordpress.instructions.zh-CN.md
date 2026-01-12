

---
applyTo: 'wp-content/plugins/**,wp-content/themes/**,**/*.php,**/*.inc,**/*.js,**/*.jsx,**/*.ts,**/*.tsx,**/*.css,**/*.scss,**/*.json'
description: 'WordPress 插件和主题的编码、安全性和测试规则'
---

# WordPress 开发 — Copilot 指南

**目标：** 生成安全、高性能、可测试且符合官方 WordPress 实践规范的代码。优先使用钩子（hooks）、小函数、依赖注入（合理时）以及清晰的职责分离。

## 1) 核心原则
- **绝不要修改 WordPress 核心代码。** 通过 **动作（actions）** 和 **过滤器（filters）** 进行扩展。
- 对于插件，始终包含插件头信息并在入口 PHP 文件中防止直接执行。
- 使用唯一的前缀或 PHP 命名空间以避免全局命名冲突。
- 加载资源（assets）；**不要在 PHP 模板中内联原始 `<script>`/`<style>`**。
- 将用户可见的字符串设为可翻译，并加载正确的文本域（text domain）。

### 最小化插件头信息与执行保护
```php
<?php
defined('ABSPATH') || exit;
/**
 * 插件名称: 精彩功能
 * 描述: 示例插件骨架。
 * 版本: 0.1.0
 * 作者: 示例
 * 许可证: GPL-2.0-or-later
 * 文本域: awesome-feature
 * 域路径: /languages
 */
```

## 2) 编码规范（PHP、JS、CSS、HTML）
- 遵循 **WordPress 编码规范（WPCS）** 并为公共 API 编写 DocBlocks。
- **PHP：** 在适当的情况下优先使用严格比较（`===`, `!==`）。保持数组语法和空格与 WPCS 一致。
- **JS：** 与 WordPress JS 风格一致；优先使用 `@wordpress/*` 包进行区块/编辑器代码开发。
- **CSS：** 在有帮助时使用类似 BEM 的类名命名；避免过于具体的选择器。
- **PHP 7.4+** 兼容模式，除非项目指定了更高的版本。避免使用目标 WP/PHP 版本不支持的功能。

### 代码检查（linting）设置建议
```xml
<!-- phpcs.xml -->
<?xml version="1.0"?>
<ruleset name="项目 WPCS">
  <description>本项目的 WordPress 编码规范。</description>
  <file>./</file>
  <exclude-pattern>vendor/*</exclude-pattern>
  <exclude-pattern>node_modules/*</exclude-pattern>
  <rule ref="WordPress"/>
  <rule ref="WordPress-Docs"/>
  <rule ref="WordPress-Extra"/>
  <rule ref="PHPCompatibility"/>
  <config name="testVersion" value="7.4-"/>
</ruleset>
```

```json
// composer.json（片段）
{
  "require-dev": {
    "dealerdirect/phpcodesniffer-composer-installer": "^1.0",
    "wp-coding-standards/wpcs": "^3.0",
    "phpcompatibility/php-compatibility": "^9.0"
  },
  "scripts": {
    "lint:php": "phpcs -p",
    "fix:php": "phpcbf -p"
  }
}
```

```json
// package.json（片段）
{
  "devDependencies": {
    "@wordpress/eslint-plugin": "^x.y.z"
  },
  "scripts": {
    "lint:js": "eslint ."
  }
}
```

## 3) 安全性与数据处理
- **输出时转义，输入时净化。**
  - 转义：`esc_html()`、`esc_attr()`、`esc_url()`、`wp_kses_post()`。
  - 净化：`sanitize_text_field()`、`sanitize_email()`、`sanitize_key()`、`absint()`、`intval()`。
- **表单、AJAX、REST 的权限与非ces：**
  - 使用 `wp_nonce_field()` 添加非ces，并通过 `check_admin_referer()` / `wp_verify_nonce()` 验证。
  - 使用 `current_user_can( 'manage_options' /* 或特定权限 */ )` 限制数据修改。
- **数据库：** 始终使用 `$wpdb->prepare()` 并配合占位符；**不要拼接不可信的输入**。
- **上传：** 验证 MIME 类型并使用 `wp_handle_upload()`/`media_handle_upload()`。

## 4) 国际化（i18n）
- 使用你的文本域（text domain）将用户可见的字符串包裹在翻译函数中：
  - `__( '文本', 'awesome-feature' )`、`_x()`、`esc_html__()`。
- 使用 `load_plugin_textdomain()` 或 `load_theme_textdomain()` 加载翻译。
- 在 `/languages` 目录中保持 `.pot` 文件，并确保文本域使用的一致性。

## 5) 性能优化
- 将繁重的逻辑延迟到特定钩子（hooks）中；除非必要，否则避免在 `init`/`wp_loaded` 中执行昂贵操作。
- 对于昂贵的查询，使用瞬时变量（transients）或对象缓存（object caching）；规划缓存失效策略。
- 仅加载必要的资源，并根据场景（前端 vs 后台；特定界面/路由）进行条件加载。
- 优先使用分页/参数化查询，而非无限制的循环。

## 6) 管理界面与设置
- 使用 **设置 API** 创建选项页面；为每个设置提供 `sanitize_callback`。
- 对于表格，遵循 `WP_List_Table` 模式。对于通知，使用管理通知 API。
- 避免直接输出复杂界面的 HTML；优先使用模板或小型视图辅助函数，并确保转义。

## 7) REST API
- 通过 `register_rest_route()` 注册 API；始终设置 `permission_callback`。
- 通过 `args` 模式验证/净化请求参数。
- 返回 `WP_REST_Response` 或映射清晰到 JSON 的数组/对象。

## 8) 区块与编辑器（古腾堡）
- 使用 `block.json` + `register_block_type()`；依赖 `@wordpress/*` 包。
- 在需要时提供服务器渲染回调（动态区块）。
- E2E 测试应覆盖：插入区块 → 编辑 → 保存 → 前端渲染。

## 9) 资源加载
```php
add_action('wp_enqueue_scripts', function () {
  wp_enqueue_style(
    'af-frontend',
    plugins_url('assets/frontend.css', __FILE__),
    [],
    '0.1.0'
  );

  wp_enqueue_script(
    'af-frontend',
    plugins_url('assets/frontend.js', __FILE__),
    [ 'wp-i18n', 'wp-element' ],
    '0.1.0',
    true
  );
});
```
- 如果多个组件依赖相同的资源，应先使用 `wp_register_style/script` 注册。
- 对于后台界面，钩入 `admin_enqueue_scripts` 并检查屏幕 ID。

## 10) 测试
### PHP 单元测试/集成测试
- 使用 **WordPress 测试套件** 与 `PHPUnit` 和 `WP_UnitTestCase`。
- 测试内容包括：净化、权限检查、REST 权限、数据库查询、钩子。
- 优先使用工厂（factories）（如 `self::factory()->post->create()` 等）设置测试数据。

```xml
<!-- phpunit.xml.dist（最小化） -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="tests/bootstrap.php" colors="true">
  <testsuites>
    <testsuite name="插件测试套件">
      <directory suffix="Test.php">tests/</directory>
    </testsuite>
  </testsuites>
</phpunit>
```

```php
// tests/bootstrap.php（最小化草图）
<?php
$_tests_dir = getenv('WP_TESTS_DIR') ?: '/tmp/wordpress-tests-lib';
require_once $_tests_dir . '/includes/functions.php';
tests_add_filter( 'muplugins_loaded', function () {
  require dirname(__DIR__) . '/awesome-feature.php';
} );
require $_tests_dir . '/includes/bootstrap.php';
```
### E2E（端到端）测试
- 使用 Playwright（或 Puppeteer）进行编辑器/前端流程测试。
- 覆盖基本用户流程和回归测试（区块插入、设置保存、前端渲染）。

## 11) 文档与提交记录
- 保持 `README.md` 更新：安装、使用、权限、钩子/过滤器以及测试说明。
- 使用明确的、命令式的提交信息；引用问题/工单并总结影响。

## 12) Copilot 必须确保的内容（检查清单）
- ✅ 唯一的前缀/命名空间；无意外的全局变量。
- ✅ 任何写操作（AJAX/REST/表单）均需包含非ces + 权限检查。
- ✅ 输入已净化；输出已转义。
- ✅ 用户可见字符串使用正确的文本域包裹在国际化函数中。
- ✅ 资源通过 API 加载（无内联脚本/样式）。
- ✅ 为新功能添加/更新测试。
- ✅ 代码通过 PHPCS（WPCS）和 ESLint（适用时）检查。
- ✅ 避免直接拼接数据库查询；始终使用预处理查询。