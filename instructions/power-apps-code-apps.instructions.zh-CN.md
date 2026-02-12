---
description: 'Power Apps 代码应用开发标准和最佳实践，适用于 TypeScript、React 和 Power Platform 集成'
applyTo: '**/*.{ts,tsx,js,jsx}, **/vite.config.*, **/package.json, **/tsconfig.json, **/power.config.json'
---

# Power Apps 代码应用开发指南

使用 TypeScript、React 和 Power Platform SDK 开发高质量 Power Apps 代码应用的指南，遵循 Microsoft 官方的最佳实践和预览功能。

## 项目背景

- **Power Apps 代码应用**：基于代码的 Web 应用开发，集成 Power Platform
- **TypeScript + React**：推荐的前端技术栈，使用 Vite 打包工具
- **Power Platform SDK**：@microsoft/power-apps（当前版本 ^1.0.3）用于连接器集成
- **PAC CLI**：Power Platform CLI 用于项目管理和部署
- **端口 3000**：与 Power Platform SDK 本地开发所需的端口
- **Power Apps 企业版**：生产环境中用户许可的必需条件

## 开发标准

### 项目结构

- 使用清晰的职责划分结构：
  ```
  src/
  ├── components/          # 可重用的 UI 组件
  ├── hooks/              # 用于 Power Platform 的自定义 React hooks
  ├── generated/
  │   ├── services/       # 生成的连接器服务（PAC CLI）
  │   └── models/         # 生成的 TypeScript 模型（PAC CLI）
  ├── utils/             # 工具函数和辅助函数
  ├── types/             # TypeScript 类型定义
  ├── PowerProvider.tsx  # Power Platform 上下文包装器
  └── main.tsx          # 应用程序入口点
  ```
- 将生成的文件（`generated/services/`，`generated/models/`）与自定义代码分离
- 使用一致的命名约定（文件使用 kebab-case，组件使用 PascalCase）

### TypeScript 配置

- 在 tsconfig.json 中设置 `verbatimModuleSyntax: false` 以兼容 Power Apps SDK
- 启用严格模式以确保类型安全，推荐的 tsconfig.json 配置：
  ```json
  {
    "compilerOptions": {
      "target": "ES2020",
      "useDefineForClassFields": true,
      "lib": ["ES2020", "DOM", "DOM.Iterable"],
      "module": "ESNext",
      "skipLibCheck": true,
      "verbatimModuleSyntax": false,
      "moduleResolution": "bundler",
      "allowImportingTsExtensions": true,
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noEmit": true,
      "jsx": "react-jsx",
      "strict": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noFallthroughCasesInSwitch": true,
      "baseUrl": ".",
      "paths": {
        "@/*": ["./src/*"]
      }
    }
  }
  ```
- 为 Power Platform 连接器响应使用适当的类型
- 使用 `"@": path.resolve(__dirname, "./src")` 配置路径别名以实现更简洁的导入
- 为应用特定的数据结构定义接口
- 实现错误边界和适当的错误处理类型

### 高级 Power Platform 集成

#### 自定义控件框架（PCF 控件）
- **集成 PCF 控件**：在代码应用中嵌入 Power Apps Component Framework 控件
  ```typescript
  // 示例：使用自定义 PCF 控件进行数据可视化
  import { PCFControlWrapper } from './components/PCFControlWrapper';

  const MyComponent = () => {
    return (
      <PCFControlWrapper
        controlName="CustomChartControl"
        dataset={chartData}
        configuration={chartConfig}
      />
    );
  };
  ```
- **PCF 控件通信**：处理 PCF 与 React 之间的事件和数据绑定
- **自定义控件部署**：将 PCF 控件与代码应用一起打包和部署

#### Power BI 嵌入分析
- **嵌入 Power BI 报表**：集成交互式仪表板和报表
  ```typescript
  import { PowerBIEmbed } from 'powerbi-client-react';

  const DashboardComponent = () => {
    return (
      <PowerBIEmbed
        embedConfig={{
          type: 'report',
          id: reportId,
          embedUrl: embedUrl,
          accessToken: accessToken,
          tokenType: models.TokenType.Aad,
          settings: {
            panes: { filters: { expanded: false, visible: false } }
          }
        }}
      />
    );
  };
  ```
- **动态报表过滤**：根据代码应用上下文过滤 Power BI 报表
- **报表导出功能**：启用 PDF、Excel 和图像导出

#### AI Builder 集成
- **认知服务集成**：使用 AI Builder 模型进行表单处理、对象检测
  ```typescript
  // 示例：使用 AI Builder 进行文档处理
  const processDocument = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const result = await AIBuilderService.ProcessDocument({
      modelId: 'document-processing-model-id',
      document: formData
    });

    return result.extractedFields;
  };
  ```
- **预测模型**：集成自定义 AI 模型以进行业务预测
- **情感分析**：使用 AI Builder 分析文本情感
- **对象检测**：实现图像分析和对象识别

#### Power Virtual Agents 集成
- **聊天机器人嵌入**：在代码应用中集成 Power Virtual Agents 机器人
  ```typescript
  import { DirectLine } from 'botframework-directlinejs';
  import { WebChat } from 'botframework-webchat';

  const ChatbotComponent = () => {
    const directLine = new DirectLine({
      token: chatbotToken
    });

    return (
      <div style={{ height: '400px', width: '100%' }}>
        <WebChat directLine={directLine} />
      </div>
    );
  };
  ```
- **上下文传递**：将代码应用上下文传递给聊天机器人对话
- **自定义机器人操作**：从机器人交互中触发代码应用功能
- 使用 PAC CLI 生成的 TypeScript 服务进行连接器操作
- 实现与 Microsoft Entra ID 的适当认证流程
- 处理连接器授权对话框和权限管理
- PowerProvider 实现模式（v1.0 不需要 SDK 初始化）：
  ```typescript
  import type { ReactNode } from "react";

  export default function PowerProvider({ children }: { children: ReactNode }) {
    return <>{children}</>;
  }
  ```
- 遵循官方支持的连接器模式：
  - SQL Server（包括 Azure SQL）
  - SharePoint
  - Office 365 用户/组
  - Azure 数据资源管理器
  - Microsoft Teams
  - Dataverse（CRUD 操作）

### React 模式

- 所有新开发使用功能组件和 hooks
- 为连接器操作实现适当的加载和错误状态
- 考虑使用 Fluent UI React 组件（如官方示例所示）
- 在适当情况下使用 React Query 或 SWR 进行数据获取和缓存
- 遵循 React 的最佳实践进行组件组合
- 使用移动优先方法实现响应式设计
- 按照官方示例安装关键依赖项：
  - `@microsoft/power-apps` 用于 Power Platform SDK
  - `@fluentui/react-components` 用于 UI 组件
  - `concurrently` 用于并行脚本执行（开发依赖项）

### 数据管理

- 将敏感数据存储在数据源中，而不是应用代码中
- 使用 PAC CLI 生成的模型进行类型安全的连接器操作
- 实现适当的数据验证和清理
- 在可能的情况下优雅处理离线场景
- 适当缓存频繁访问的数据

#### 高级 Dataverse 关系
- **多对多关系**：实现关联表和关系服务
  ```typescript
  // 示例：用户到角色的多对多关系
  const userRoles = await UserRoleService.getall();
  const filteredRoles = userRoles.filter(ur => ur.userId === currentUser.id);
  ```
- **多态查找**：处理可以引用多个实体类型的客户字段
  ```typescript
  // 处理多态客户查找（账户或联系人）
  const customerType = record.customerType; // 'account' 或 'contact'
  const customerId = record.customerId;
  const customer = customerType === 'account'
    ? await AccountService.get(customerId)
    : await ContactService.get(customerId);
  ```
- **复杂关系查询**：使用 $expand 和 $filter 进行高效数据检索
- **关系验证**：实现关系约束的业务规则

### 性能优化

- 使用 React.memo 和 useMemo 进行昂贵计算的优化
- 对大型应用实现代码分割和懒加载
- 使用 tree shaking 优化捆绑包大小
- 使用高效的连接器查询模式以减少 API 调用
- 对大型数据集实现适当的分页

#### 离线优先架构与同步模式
- **Service Worker 实现**：启用离线功能
  ```typescript
  // 示例：Service Worker 注册
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => console.log('SW 注册成功:', registration))
        .catch(error => console.log('SW 注册失败:', error));
    });
  }
  ```
- **本地数据存储**：使用 IndexedDB 进行离线数据持久化
  ```typescript
  // 示例：IndexedDB 的离线存储包装器
  class OfflineDataStore {
    async saveData(key: string, data: any) {
      const db = await this.openDB();
      const transaction = db.transaction(['data'], 'readwrite');
      transaction.objectStore('data').put({ id: key, data, timestamp: Date.now() });
    }

    async loadData(key: string) {
      const db = await this.openDB();
      const transaction = db.transaction(['data'], 'readonly');
      return transaction.objectStore('data').get(key);
    }
  }
  ```
- **同步冲突解决**：处理重新联网时的数据冲突
- **后台同步**：实现定期数据同步
- **渐进式 Web 应用 (PWA)**：启用应用安装和离线功能

## 安全最佳实践

- 绝对不要在代码中存储机密或敏感配置
- 使用 Power Platform 的内置认证和授权
- 实现适当的输入验证和清理
- 遵循 OWASP 对 Web 应用的安全指南
- 尊重 Power Platform 的数据丢失防护策略
- 实现仅 HTTPS 的通信

## 错误处理

- 在 React 中实现全面的错误边界
- 优雅处理连接器特定的错误
- 向用户提供有意义的错误消息
- 适当记录错误，避免暴露敏感信息
- 实现瞬态故障的重试逻辑
- 处理网络连接问题

## 测试策略

- 为业务逻辑和工具函数编写单元测试
- 使用 React Testing Library 测试 React 组件
- 在测试中模拟 Power Platform 连接器
- 为关键用户流程实现集成测试
- 使用 TypeScript 提高测试安全性
- 测试错误场景和边缘情况

## 开发工作流程

- 使用 PAC CLI 进行项目初始化和连接器管理
- 根据团队规模遵循适当的 Git 分支策略
- 实现适当的代码审查流程
- 使用代码检查和格式化工具（ESLint、Prettier）
- 使用 concurrently 配置开发脚本：
  - `"dev": "concurrently \"vite\" \"pac code run\""`
  - `"build": "tsc -b && vite build"`
- 在 CI/CD 流水线中实现自动化测试
- 遵循语义化版本控制进行发布

## 部署和 DevOps

- 使用 `npm run build` 后再执行 `pac code push` 进行部署
- 实现适当的环境管理（开发、测试、生产）
- 使用环境特定的配置文件
- 在可能的情况下实现蓝绿部署或金丝雀部署策略
- 在生产环境中监控应用性能和错误
- 实现适当的备份和灾难恢复程序

#### 多环境部署流水线
- **环境特定配置**：管理开发/测试/预发布/生产环境
  ```json
  // 示例：环境特定配置文件
  // config/development.json
  {
    "powerPlatform": {
      "environmentUrl": "https://dev-env.crm.dynamics.com",
      "apiVersion": "9.2"
    },
    "features": {
      "enableDebugMode": true,
      "enableAnalytics": false
    }
  }
  ```
- **自动化部署流水线**：使用 Azure DevOps 或 GitHub Actions
  ```yaml
  # 示例 Azure DevOps 流水线步骤
  - task: PowerPlatformToolInstaller@2
  - task: PowerPlatformSetConnectionVariables@2
    inputs:
      authenticationType: 'PowerPlatformSPN'
      applicationId: '$(AppId)'
      clientSecret: '$(ClientSecret)'
      tenantId: '$(TenantId)'
  ```
- **环境提升**：自动化从开发 → 测试 → 预发布 → 生产的环境提升
- **回滚策略**：在部署失败时实现自动化回滚
- **配置管理**：使用 Azure Key Vault 管理环境特定的机密

## 代码质量指南

### 组件开发

- 创建具有清晰 props 接口的可重用组件
- 使用组合而非继承
- 使用 TypeScript 实现适当的 prop 验证
- 遵循单一职责原则
- 编写自我文档化的代码，使用清晰的命名

### 状态管理

- 对简单场景使用 React 内置的状态管理
- 对复杂状态管理考虑使用 Redux Toolkit
- 实现适当的状态规范化
- 避免使用 prop drilling，使用上下文或状态管理库
- 高效使用派生状态和计算值

### API 集成

- 使用 PAC CLI 生成的服务进行一致性集成
- 实现适当的请求/响应拦截器
- 处理认证令牌管理
- 实现请求去重和缓存
- 使用适当的 HTTP 状态码处理

### 样式和 UI

- 使用一致的设计系统或组件库
- 使用 CSS Grid/Flexbox 实现响应式设计
- 遵循无障碍指南（WCAG 2.1）
- 使用 CSS-in-JS 或 CSS 模块进行组件样式
- 在适当情况下实现深色模式支持
- 确保移动友好的用户界面

#### 高级 UI/UX 模式

##### 使用组件库实现设计系统
- **组件库结构**：构建可重用的组件系统
  ```typescript
  // 示例：设计系统按钮组件
  interface ButtonProps {
    variant: 'primary' | 'secondary' | 'danger';
    size: 'small' | 'medium' | 'large';
    disabled?: boolean;
    onClick: () => void;
    children: React.ReactNode;
  }

  export const Button: React.FC<ButtonProps> = ({
    variant, size, disabled, onClick, children
  }) => {
    const classes = `btn btn-${variant} btn-${size} ${disabled ? 'btn-disabled' : ''}`;
    return <button className={classes} onClick={onClick} disabled={disabled}>{children}</button>;
  };
  ```
- **设计令牌**：实现一致的间距、颜色、字体
- **组件文档**：使用 Storybook 进行组件文档

##### 深色模式和主题系统
- **主题提供者实现**：支持多种主题
  ```typescript
  // 示例：主题上下文和提供者
  const ThemeContext = createContext({
    theme: 'light',
    toggleTheme: () => {}
  });

  export const ThemeProvider: React.FC<{children: ReactNode}> = ({ children }) => {
    const [theme, setTheme] = useState<'light' | 'dark'>('light');

    const toggleTheme = () => {
      setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    return (
      <ThemeContext.Provider value={{ theme, toggleTheme }}>
        <div className={`theme-${theme}`}>{children}</div>
      </ThemeContext.Provider>
    );
  };
  ```
- **CSS 自定义属性**：使用 CSS 变量实现动态主题
- **系统偏好检测**：尊重用户的操作系统主题偏好

##### 响应式设计高级模式
- **容器查询**：使用基于容器的响应式设计
  ```css
  /* 示例：容器查询用于响应式组件 */
  .card-container {
    container-type: inline-size;
  }

  @container (min-width: 400px) {
    .card {
      display: grid;
      grid-template-columns: 1fr 1fr;
    }
  }
  ```
- **流体字体**：实现响应式字体缩放
- **自适应布局**：根据屏幕尺寸和上下文更改布局模式

##### 动画和微交互
- **Framer Motion 集成**：平滑的动画和过渡效果
  ```typescript
  import { motion, AnimatePresence } from 'framer-motion';

  const AnimatedCard = () => {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
        whileHover={{ scale: 1.02 }}
        className="card"
      >
        卡片内容
      </motion.div>
    );
  };
  ```
- **加载状态**：动画骨架和进度指示器
- **手势识别**：滑动、捏合和触摸交互
- **性能优化**：使用 CSS 变换和 will-change 属性

##### 可访问性自动化和测试
- **ARIA 实现**：正确的语义标记和 ARIA 属性
  ```typescript
  // 示例：可访问的模态组件
  const Modal: React.FC<{isOpen: boolean, onClose: () => void, children: ReactNode}> = ({
    isOpen, onClose, children
  }) => {
    useEffect(() => {
      if (isOpen) {
        document.body.style.overflow = 'hidden';
        const focusableElement = document.querySelector('[data-autofocus]') as HTMLElement;
        focusableElement?.focus();
      }
      return () => { document.body.style.overflow = 'unset'; };
    }, [isOpen]);

    return (
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className={isOpen ? 'modal-open' : 'modal-hidden'}
      >
        {children}
      </div>
    );
  };
  ```
- **自动化可访问性测试**：集成 axe-core 进行可访问性测试
- **键盘导航**：实现完整的键盘可访问性
- **屏幕阅读器优化**：使用 NVDA、JAWS 和 VoiceOver 进行测试

##### 国际化 (i18n) 和本地化
- **React-intl 集成**：多语言支持
  ```typescript
  import { FormattedMessage, useIntl } from 'react-intl';

  const WelcomeMessage = ({ userName }: { userName: string }) => {
    const intl = useIntl();

    return (
      <h1>
        <FormattedMessage
          id="welcome.title"
          defaultMessage="欢迎，{userName}！"
          values={{ userName }}
        />
      </h1>
    );
  };
  ```
- **语言检测**：自动语言检测和切换
- **RTL 支持**：阿拉伯语、希伯来语等从右到左语言支持
- **日期和数字格式化**：本地化格式
- **翻译管理**：集成翻译服务

## 当前限制和解决方法

### 已知限制

- 内容安全策略 (CSP) 仍不支持
- 存储 SAS IP 限制不支持
- 没有 Power Platform 的 Git 集成
- 支持 Dataverse 解决方案，但解决方案打包器和源代码集成有限
- 通过 SDK 日志器配置支持 Application Insights（没有内置原生集成）

### 解决方法

- 如有需要，使用替代的错误跟踪解决方案
- 实现手动部署工作流程
- 使用外部工具进行高级分析
- 规划未来迁移到支持功能的更新

## 文档标准

- 保持全面的 README.md 并包含设置说明
- 文档所有自定义组件和 hooks
- 包含常见问题的故障排除指南
- 文档部署流程和要求
- 保持版本更新的变更日志
- 包含重大决策的架构决策记录

## 常见问题排查

### 开发问题

- **端口 3000 冲突**：使用 `netstat -ano | findstr :3000` 杀掉现有进程，然后使用 `taskkill /PID {PID} /F`
- **认证失败**：使用 `pac auth list` 验证环境设置和用户权限
- **包安装失败**：使用 `npm cache clean --force` 清除 npm 缓存并重新安装
- **TypeScript 编译错误**：检查 `verbatimModuleSyntax` 设置和 SDK 兼容性
- **连接器权限错误**：确保正确的授权流程和管理员权限
- **PowerProvider 问题**：确保 v1.0 应用程序不等待 SDK 初始化
- **Vite 开发服务器问题**：确保主机和端口配置符合要求

### 部署问题

- **构建失败**：使用 `npm audit` 验证所有依赖项并检查构建配置
- **认证错误**：使用 `pac auth clear` 清除 PAC CLI 认证，然后重新创建
- **连接器不可用**：在 Power Platform 中验证连接器设置和连接状态
- **性能问题**：使用 `npm run build --report` 优化捆绑包大小并实现缓存
- **环境不匹配**：使用 `pac env list` 确认正确的环境选择
- **应用超时错误**：检查构建输出和网络连接

### 运行时问题

- **"应用超时" 错误**：验证是否执行了 `npm run build` 并且部署输出有效
- **连接器认证提示**：确保正确的授权流程实现
- **数据加载失败**：检查网络请求和连接器权限
- **UI 渲染问题**：验证 Fluent UI 兼容性和响应式设计实现

## 最佳实践总结

1. **遵循 Microsoft 官方文档和最佳实践**
2. **使用 TypeScript 实现类型安全和更好的开发体验**
3. **实现适当的错误处理和用户反馈**
4. **优化性能和用户体验**
5. **遵循安全最佳实践和 Power Platform 政策**
6. **编写可维护、可测试和文档齐全的代码**
7. **使用 PAC CLI 生成的服务和模型**
8. **规划未来功能更新和迁移**
9. **实现全面的测试策略**

10. **遵循适当 DevOps 和部署实践**
