

---
description: '在Salesforce平台上开发Lightning Web组件（LWC）的指南和最佳实践。'
applyTo: 'force-app/main/default/lwc/**'
---

# LWC开发

## 一般指导

- 每个LWC应位于`force-app/main/default/lwc/`目录下的独立文件夹中。
- 文件夹名称应与组件名称匹配（例如，`myComponent`组件应使用`myComponent`文件夹）。
- 每个组件文件夹应包含以下文件：
    - `myComponent.html`：HTML模板文件。
    - `myComponent.js`：JavaScript控制器文件。
    - `myComponent.js-meta.xml`：元数据配置文件。
    - 可选：`myComponent.css`用于组件特定的样式。
    - 可选：`myComponent.test.js`用于Jest单元测试。

## 核心原则

### 1. 优先使用Lightning组件而非HTML标签
始终优先使用Lightning Web组件库中的组件而非原生HTML元素，以确保一致性、可访问性和未来兼容性。

#### 推荐方法
```html
<!-- 使用Lightning组件 -->
<lightning-button label="保存" variant="brand" onclick={handleSave}></lightning-button>
<lightning-input type="text" label="名称" value={name} onchange={handleNameChange}></lightning-input>
<lightning-combobox label="类型" options={typeOptions} value={selectedType}></lightning-combobox>
<lightning-radio-group name="duration" label="持续时间" options={durationOptions} value={duration} type="radio"></lightning-radio-group>
```

#### 避免使用原生HTML
```html
<!-- 避免使用这些 -->
<button onclick={handleSave}>保存</button>
<input type="text" onchange={handleNameChange} />
<select onchange={handleTypeChange}>
    <option value="option1">选项1</option>
</select>
```

### 2. Lightning组件映射指南

| HTML元素 | Lightning组件 | 关键属性 |
|----------|---------------|----------|
| `<button>` | `<lightning-button>` | `variant`, `label`, `icon-name` |
| `<input>` | `<lightning-input>` | `type`, `label`, `variant` |
| `<select>` | `<lightning-combobox>` | `options`, `value`, `placeholder` |
| `<textarea>` | `<lightning-textarea>` | `label`, `max-length` |
| `<input type="checkbox">` | `<lightning-input type="checkbox">` | `checked`, `label` |
| `<input type="radio">` | `<lightning-radio-group>` | `options`, `type`, `name` |
| `<input type="toggle">` | `<lightning-input type="toggle">` | `checked`, `variant` |
| 自定义标签 | `<lightning-pill>` | `label`, `name`, `onremove` |
| 图标 | `<lightning-icon>` | `icon-name`, `size`, `variant` |

### 3. Lightning设计系统合规性

#### 使用SLDS实用类
始终使用Salesforce Lightning设计系统（SLDS）的实用类，且以`slds-var-`前缀开头，用于现代实现：

```html
<!-- 间距 -->
<div class="slds-var-m-around_medium slds-var-p-top_large">
    <div class="slds-var-m-bottom_small">内容</div>
</div>

<!-- 布局 -->
<div class="slds-grid slds-wrap slds-gutters_small">
    <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-3">
        <!-- 内容 -->
    </div>
</div>

<!-- 字体排版 -->
<h2 class="slds-text-heading_medium slds-var-m-bottom_small">章节标题</h2>
<p class="slds-text-body_regular">描述文本</p>
```

#### SLDS组件模式
```html
<!-- 卡片布局 -->
<article class="slds-card slds-var-m-around_medium">
    <header class="slds-card__header">
        <h2 class="slds-text-heading_small">卡片标题</h2>
    </header>
    <div class="slds-card__body slds-card__body_inner">
        <!-- 卡片内容 -->
    </div>
    <footer class="slds-card__footer">
        <!-- 卡片操作 -->
    </footer>
</article>

<!-- 表单布局 -->
<div class="slds-form slds-form_stacked">
    <div class="slds-form-element">
        <lightning-input label="字段标签" value={fieldValue}></lightning-input>
    </div>
</div>
```

### 4. 避免自定义CSS

#### 使用SLDS类
```html
<!-- 颜色和主题 -->
<div class="slds-theme_success slds-text-color_inverse slds-var-p-around_small">
    成功消息
</div>

<div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
    错误消息
</div>

<div class="slds-theme_warning slds-text-color_inverse slds-var-p-around_small">
    警告消息
</div>
```

#### 避免自定义CSS（反模式）
```css
/* 不要创建覆盖SLDS的自定义样式 */
.custom-button {
    background-color: red;
    padding: 10px;
}

.my-special-layout {
    display: flex;
    justify-content: center;
}
```

#### 当必须使用自定义CSS时
如果必须使用自定义CSS，请遵循以下指南：
- 尽可能使用CSS自定义属性（设计令牌）
- 为自定义类添加前缀以避免冲突
- 永远不要覆盖SLDS基础类

```css
/* 自定义CSS示例 */
.my-component-special {
    border-radius: var(--lwc-borderRadiusMedium);
    box-shadow: var(--lwc-shadowButton);
}
```

### 5. 组件架构最佳实践

#### 反应式属性
```javascript
import { LightningElement, track, api } from 'lwc';

export default class MyComponent extends LightningElement {
    // 使用 @api 用于公共属性
    @api recordId;
    @api title;

    // 原始属性（字符串、数字、布尔值）会自动反应式
    // 不需要装饰器 - 重新赋值会触发重新渲染
    simpleValue = '初始';
    count = 0;

    // 计算属性
    get displayName() {
        return this.name ? `你好, ${this.name}` : '你好, 顾客';
    }

    // @track 不需要用于简单属性重新赋值
    // 这会自动触发反应式：
    handleUpdate() {
        // 不需要 @track，无需重新赋值即可反应式
        this.simpleValue = '更新'; // 无需 @track 即可反应式
        this.count++; // 无需 @track 即可反应式
    }

    // @track 在没有重新赋值的情况下修改嵌套属性时需要
    @track complexData = {
        user: {
            name: 'John',
            preferences: {
                theme: 'dark'
            }
        }
    };

    handleDeepUpdate() {
        // 需要 @track，因为我们正在修改嵌套属性
        this.complexData.user.preferences.theme = 'light';
    }

    // 更好的做法：通过使用不可变模式避免 @track
    regularData = {
        user: {
            name: 'John',
            preferences: {
                theme: 'dark'
            }
        }
    };

    handleImmutableUpdate() {
      // 不需要 @track - 我们正在创建新的对象引用
      this.regularData = {
        ...this.regularData,
        user: {
          ...this.regularData.user,
          preferences: {
            ...this.regularData.user.preferences,
            theme: 'light'
          }
        }
      };
    }

    // 数组：只有在修改方法中才需要 @track
    @track items = ['a', 'b', 'c'];

    handleArrayMutation() {
      // 需要 @track
      this.items.push('d');
      this.items[0] = 'z';
    }

    // 更好的做法：使用不可变数组操作
    regularItems = ['a', 'b', 'c'];

    handleImmutableArray() {
      // 不需要 @track
      this.regularItems = [...this.regularItems, 'd'];
      this.regularItems = this.regularItems.map((item, idx) =>
        idx === 0 ? 'z' : item
      );
    }

    // 只有在修改嵌套属性时才使用 @track 对于复杂对象/数组。
    // 例如，更新 complexObject.details.status 而不重新赋值 complexObject。
    @track complexObject = {
      details: {
        status: 'new'
      }
    };
}
```

#### 事件处理模式
```javascript
// 自定义事件分发
handleSave() {
    const saveEvent = new CustomEvent('save', {
        detail: {
            recordData: this.recordData,
            timestamp: new Date()
        }
    });
    this.dispatchEvent(saveEvent);
}

// Lightning组件事件处理
handleInputChange(event) {
    const fieldName = event.target.name;
    const fieldValue = event.target.value;

    // 对于 lightning-input、lightning-combobox 等
    this[fieldName] = fieldValue;
}

handleRadioChange(event) {
    // 对于 lightning-radio-group
    this.selectedValue = event.detail.value;
}

handleToggleChange(event) {
    // 对于 lightning-input type="toggle"
    this.isToggled = event.detail.checked;
}
```

### 6. 数据处理和Wire服务

#### 使用 @wire 进行数据访问
```javascript
import { getRecord } from 'lightning/uiRecordApi';
import { getObjectInfo } from 'lightning/uiObjectInfoApi';

const FIELDS = ['Account.Name', 'Account.Industry', 'Account.AnnualRevenue'];

export default class MyComponent extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    record;

    @wire(getObjectInfo, { objectApiName: 'Account' })
    objectInfo;

    get recordData() {
        return this.record.data ? this.record.data.fields : {};
    }
}
```

### 7. 错误处理和用户体验

#### 实现适当的错误边界
```javascript
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class MyComponent extends LightningElement {
    isLoading = false;
    error = null;

    async handleAsyncOperation() {
        this.isLoading = true;
        this.error = null;

        try {
            const result = await this.performOperation();
            this.showSuccessToast();
        } catch (error) {
            this.error = error;
            this.showErrorToast(error.body?.message || '发生错误');
        } finally {
            this.isLoading = false;
        }
    }

    performOperation() {
        // 开发者定义的异步操作
    }

    showSuccessToast() {
        const event = new ShowToastEvent({
            title: '成功',
            message: '操作成功完成',
            variant: 'success'
        });
        this.dispatchEvent(event);
    }

    showErrorToast(message) {
        const event = new ShowToastEvent({
            title: '错误',
            message: message,
            variant: 'error',
            mode: 'sticky'
        });
        this.dispatchEvent(event);
    }
}
```

### 8. 性能优化

#### 条件渲染
在API v58.0+中，优先使用`lwc:if`、`lwc:elseif`和`lwc:else`进行条件渲染。旧版`if:true` / `if:false`仍然支持，但应避免在新组件中使用。

```html
<!-- 使用模板指令进行条件渲染 -->
<template lwc:if={isLoading}>
    <lightning-spinner alternative-text="正在加载..."></lightning-spinner>
</template>
<template lwc:elseif={error}>
    <div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
        {error.message}
    </div>
</template>
<template lwc:else>
    <template for:each={items} for:item="item">
        <div key={item.id} class="slds-var-m-bottom_small">
            {item.name}
        </div>
    </template>
</template>
```

```html
<!-- 旧版方法（新组件中避免使用） -->
<template if:true={isLoading}>
    <lightning-spinner alternative-text="正在加载..."></lightning-spinner>
</template>
<template if:true={error}>
    <div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
        {error.message}
    </div>
</template>
<template if:false={isLoading}>
  <template if:false={error}>
    <template for:each={items} for:item="item">
        <div key={item.id} class="slds-var-m-bottom_small">
            {item.name}
        </div>
    </template>
  </template>
</template>
```

### 9. 可访问性最佳实践

#### 使用正确的ARIA标签和语义化HTML
```html
<!-- 使用语义化结构 -->
<section aria-label="产品选择">
    <h2 class="slds-text-heading_medium">产品</h2>

    <lightning-input
        type="search"
        label="搜索产品"
        placeholder="输入产品名称..."
        aria-describedby="search-help">
    </lightning-input>

    <div id="search-help" class="slds-assistive-text">
        输入内容以过滤产品列表
    </div>
</section>
```

## 需要避免的常见反模式
- **直接操作DOM**：绝不使用`document.querySelector()`或类似方法
- **jQuery或外部库**：避免使用与Lightning不兼容的库
- **内联样式**：使用SLDS类而非`style`属性
- **全局CSS**：所有样式应限制在组件作用域内
- **硬编码值**：使用自定义标签、自定义元数据或常量
- **显式API调用**：尽可能使用`@wire`而非显式`import`调用
- **内存泄漏**：始终在`disconnectedCallback()`中清理事件监听器