

---
description: '使用 Fluent UI 对组件进行现代主题样式设计'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 使用现代主题样式设计组件（预览）

[本主题是预发布文档，可能会有所更改。]

开发者需要能够为其组件设置样式，使其与所包含的应用程序的其他部分保持一致。当在画布应用（通过 [现代控件和主题](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/overview-modern-controls)功能）或模型驱动型应用（通过 [新刷新外观](https://learn.microsoft.com/en-us/power-apps/user/modern-fluent-design)）中启用了现代主题时，他们可以实现这一点。

使用基于 [Fluent UI React v9](https://react.fluentui.dev/) 的现代主题来设置组件样式。这种方法被推荐用于获得最佳的性能和主题体验。

## 应用现代主题的四种方式

1. **Fluent UI v9 控件**
2. **Fluent UI v8 控件**
3. **非 Fluent UI 控件**
4. **自定义主题提供者**

## Fluent UI v9 控件

将 Fluent UI v9 控件封装为组件是使用现代主题的最简单方法，因为现代主题会自动应用到这些控件上。唯一前提条件是确保您的组件添加对 [React 控件和平台库](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries)的依赖。

这种方法允许您的组件使用与平台相同的 React 和 Fluent 库，因此可以共享传递主题令牌到组件的 React 上下文。

```xml
<resources>
  <code path="index.ts" order="1"/>
  <!-- 对 React 控件和平台库的依赖 -->
  <platform-library name="React" version="16.14.0" />
  <platform-library name="Fluent" version="9.46.2" />
</resources>
```

## Fluent UI v8 控件

Fluent 提供了一条迁移路径，当您在组件中使用 Fluent UI v8 控件时，可以应用 v9 主题构造。使用 [Fluent 的 v8 到 v9 迁移包](https://www.npmjs.com/package/@fluentui/react-migration-v8-v9)中包含的 `createV8Theme` 函数，根据 v9 主题令牌创建一个 v8 主题：

```typescript
const theme = createV8Theme(
  context.fluentDesignLanguage.brand,
  context.fluentDesignLanguage.theme
);
return <ThemeProvider theme={theme}></ThemeProvider>;
```

## 非 Fluent UI 控件

如果您的组件不使用 Fluent UI，您可以直接依赖于通过 `fluentDesignLanguage` 上下文参数提供的 v9 主题令牌。使用此参数访问所有 [主题](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/theming)令牌，以便根据主题的任何方面进行样式设置。

```typescript
<span style={{ fontSize: context.fluentDesignLanguage.theme.fontSizeBase300 }}>
  {"使用平台提供的主题样式化 HTML。"}
</span>
```

## 自定义主题提供者

当您的组件需要与应用程序当前主题不同的样式时，您可以创建自己的 `FluentProvider`，并将自己的主题令牌传递给组件以供使用。

```typescript
<FluentProvider theme={context.fluentDesignLanguage.tokenTheme}>
  {/* 您的控件 */}
</FluentProvider>
```

## 示例控件

这些使用案例的示例可在 [现代主题样式 API 控件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/sample-controls/modern-theming-api-control) 中找到。

## 常见问题解答

### Q: 我的控件使用 Fluent UI v9 并依赖于平台库，但我不想使用现代主题。如何禁用该功能？

A: 您可以通过以下两种方式之一实现：

**选项 1**：创建自己的组件级 `FluentProvider`

```typescript
<FluentProvider theme={customFluentV9Theme}>
  {/* 您的控件 */}
</FluentProvider>
```

**选项 2**：将您的控件包裹在 `IdPrefixContext.Provider` 中，并设置自己的 `idPrefix` 值。这会阻止您的组件从平台获取主题令牌。

```typescript
<IdPrefixProvider value="custom-control-prefix">
  <Label weight="semibold">此标签不会应用现代主题</Label>
</IdPrefixProvider>
```

### Q: 我的一些 Fluent UI v9 控件没有获取到样式

A: 依赖于 React 门户的 Fluent v9 控件需要重新包裹在主题提供者中，以确保样式正确应用。您可以使用 `FluentProvider`。

### Q: 如何检查现代主题是否已启用？

A: 您可以检查主题令牌是否可用：`context.fluentDesignLanguage?.tokenTheme`。或者在模型驱动型应用中，您可以检查应用设置：`context.appSettings.getIsFluentThemingEnabled()`。

## 相关文章

- [主题（Power Apps 组件框架 API 参考）](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/theming)
- [现代主题样式 API 控件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/sample-controls/modern-theming-api-control)
- [在画布应用中使用现代主题（预览）](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming)