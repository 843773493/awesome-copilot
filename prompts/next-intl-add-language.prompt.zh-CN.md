

---
agent: 'agent'
tools: ['changes','search/codebase', 'edit/editFiles', 'findTestFiles', 'search', 'writeTest']
description: '在 Next.js + next-intl 应用程序中添加新语言'
---

本指南介绍如何使用 next-intl 为 Next.js 项目添加新语言以实现国际化功能：

- 对于国际化（i18n），应用程序使用 next-intl。
- 所有翻译内容都位于 `./messages` 目录中。
- 用户界面组件是 `src/components/language-toggle.tsx`。
- 路由和中间件配置处理如下：
  - `src/i18n/routing.ts`
  - `src/middleware.ts`

在添加新语言时：

- 将 `en.json` 中的所有内容翻译为新语言。目标是确保新语言中包含所有 JSON 条目，以实现完整的翻译。
- 在 `routing.ts` 和 `middleware.ts` 中添加对应路径。
- 将新语言添加到 `language-toggle.tsx` 中。