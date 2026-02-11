# Python Flask 表单参考指南

> 来源: <https://testdriven.io/courses/learn-flask/forms/>

本参考指南涵盖了如何在 Flask 中处理表单，包括处理 GET 和 POST 请求、使用 WTForms 创建和验证表单、实现 CSRF 保护以及管理文件上传。

---

## 概述

Flask 提供了处理网络表单的工具，包括：

- `request` 对象用于访问提交的表单数据
- **Flask-WTF** 和 **WTForms** 用于声明式表单创建、验证和 CSRF 保护
- Jinja2 模板用于渲染表单 HTML
- Flash 消息用于用户反馈

---

## Flask 中的基本表单处理

### 处理 GET 和 POST 请求

```python
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'secret':
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('无效凭证。', 'error')

    return render_template('login.html')
```

### `request.form` 对象

`request.form` 是一个 `ImmutableMultiDict`，它包含从 POST 和 PUT 请求中解析的表单数据。

| 方法 | 描述 |
|------|------|
| `request.form['key']` | 通过键访问值；如果键不存在则引发 400 Bad Request 错误 |
| `request.form.get('key')` | 通过键访问值；如果键不存在则返回 `None` |
| `request.form.get('key', 'default')` | 通过键访问值并提供默认值 |
| `request.form.getlist('key')` | 返回键的所有值（用于多选字段） |

### `request.method` 属性

用于区分 GET（显示表单）和 POST（处理提交）：

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 处理表单提交
        pass
    # GET: 显示表单
    return render_template('register.html')
```

---

## 使用 Flask-WTF 和 WTForms

### 安装

```bash
pip install Flask-WTF
```

Flask-WTF 是一个 Flask 扩展，集成了 WTForms。它提供了以下功能：

- 开箱即用的 CSRF 保护
- 与 Flask 的 `request` 对象集成
- Jinja2 模板助手
- 文件上传支持

### 配置

```python
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # 用于 CSRF 的必要配置
app.config['WTF_CSRF_ENABLED'] = True          # 默认启用
```

---

## 使用 WTForms 定义表单

### 基础表单类

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=3, max=25)
    ])
    email = StringField('电子邮件', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='密码必须匹配。')
    ])
    submit = SubmitField('注册')
```

### 常见字段类型

| 字段类型 | 描述 |
|----------|------|
| `StringField` | 单行文本输入 |
| `PasswordField` | 密码输入（隐藏字符） |
| `TextAreaField` | 多行文本输入 |
| `IntegerField` | 带内置类型转换的整数输入 |
| `FloatField` | 带内置类型转换的浮点数输入 |
| `BooleanField` | 复选框（True/False） |
| `SelectField` | 下拉选择菜单 |
| `SelectMultipleField` | 多选下拉菜单 |
| `RadioField` | 单选按钮组 |
| `FileField` | 文件上传输入 |
| `HiddenField` | 隐藏输入字段 |
| `SubmitField` | 提交按钮 |
| `DateField` | 日期选择器输入 |

### 常见验证器

| 验证器 | 描述 |
|--------|------|
| `DataRequired()` | 字段不能为空 |
| `Email()` | 必须是有效的电子邮件格式 |
| `Length(min, max)` | 字符串长度必须在指定范围内 |
| `EqualTo('field')` | 必须与另一个字段的值匹配 |
| `NumberRange(min, max)` | 数值必须在指定范围内 |
| `Regexp(regex)` | 必须匹配提供的正则表达式 |
| `URL()` | 必须是有效的 URL |
| `Optional()` | 字段允许为空 |
| `InputRequired()` | 原始输入数据必须存在 |
| `AnyOf(values)` | 必须是提供的值之一 |
| `NoneOf(values)` | 必须不是提供的值之一 |

---

## 在路由中使用表单

### 使用 WTForms 的路由

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # form.validate_on_submit() 检查：
        # 1. 请求方法是否为 POST？
        # 2. 表单是否通过所有验证？
        # 3. CSRF 令牌是否有效？

        username = form.username.data
        email = form.email.data
        password = form.password.data

        # 处理数据（例如保存到数据库）
        flash(f'已为 {username} 创建账户！', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
```

### `validate_on_submit()` 方法

此方法结合了两个检查：

1. `request.method == 'POST'` -- 确保表单确实被提交
2. `form.validate()` -- 在表单字段上运行所有验证器并检查 CSRF 令牌

只有在两个条件都满足时才会返回 `True`。

---

## 在模板中渲染表单

### 基础模板渲染

```html
<form method="POST" action="{{ url_for('register') }}">
    {{ form.hidden_tag() }}

    <div>
        {{ form.username.label }}
        {{ form.username(class="form-control", placeholder="输入用户名") }}
        {% for error in form.username.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        {{ form.email.label }}
        {{ form.email(class="form-control", placeholder="输入电子邮件") }}
        {% for error in form.email.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        {{ form.password.label }}
        {{ form.password(class="form-control") }}
        {% for error in form.password.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        {{ form.confirm_password.label }}
        {{ form.confirm_password(class="form-control") }}
        {% for error in form.confirm_password.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    {{ form.submit(class="btn btn-primary") }}
</form>
```

### 模板关键元素

| 元素 | 用途 |
|------|------|
| `{{ form.hidden_tag() }}` | 渲染隐藏的 CSRF 令牌字段 |
| `{{ form.field.label }}` | 渲染字段的 `<label>` 元素 |
| `{{ form.field() }}` | 渲染字段的 `<input>` 元素 |
| `{{ form.field(class="...") }}` | 通过附加 HTML 属性渲染输入字段 |
| `{{ form.field.errors }}` | 字段的验证错误信息列表 |
| `{{ form.field.data }}` | 字段的当前值 |

---

## CSRF 保护

### CSRF 保护的工作原理

Flask-WTF 会自动包含 CSRF 保护：

1. 每个会话生成一个唯一的令牌，并嵌入为隐藏表单字段。
2. 提交表单时，Flask-WTF 会验证令牌是否与会话令牌匹配。
3. 如果令牌缺失或无效，请求将被拒绝并返回 `400 Bad Request` 错误。

### 包含 CSRF 令牌

在模板中始终包含以下内容之一：

```html
<!-- 选项 1: 隐藏标签（包含 CSRF + 所有隐藏字段） -->
{{ form.hidden_tag() }}

<!-- 选项 2: 仅 CSRF 令牌 -->
{{ form.csrf_token }}
```

### AJAX 请求的 CSRF 保护

对于基于 JavaScript 的表单提交：

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

```javascript
fetch('/api/submit', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
    },
    body: JSON.stringify(data)
});
```

---

## 自定义验证器

### 内联自定义验证器

在表单类上定义一个遵循 `validate_<fieldname>` 命名模式的方法：

```python
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('电子邮件', validators=[DataRequired(), Email()])

    def validate_username(self, field):
        if field.data.lower() in ['admin', 'root', 'superuser']:
            raise ValidationError('该用户名已被保留。')

    def validate_email(self, field):
        # 检查电子邮件是否已存在于数据库中
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮件已注册。')
```

### 可重用的自定义验证器

```python
from wtforms import ValidationError

def validate_no_special_chars(form, field):
    if not field.data.isalnum():
        raise ValidationError('字段只能包含字母和数字。')

class MyForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        validate_no_special_chars
    ])
```

---

## 文件上传

### 包含文件上传的表单

```python
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(FlaskForm):
    photo = FileField('个人照片', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], '仅支持图片！')
    ])
    submit = SubmitField('上传')
```

### 在路由中处理文件上传

```python
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        flash('文件上传成功！', 'success')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)
```

### 多部分表单编码

文件上传表单必须使用 `enctype="multipart/form-data"`：

```html
<form method="POST" enctype="multipart/form-data">
    {{ form.hidden_tag() }}
    {{ form.photo.label }}
    {{ form.photo() }}
    {{ form.submit() }}
</form>
```

---

## Flash 消息

### 设置 Flash 消息

```python
from flask import flash

flash('操作成功！', 'success')
flash('发生错误。', 'error')
flash('请检查您的输入。', 'warning')
```

### 在模板中显示 Flash 消息

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

## 关键要点

1. **使用 Flask-WTF** 进行表单处理 -- 它提供了 CSRF 保护、验证和清晰的表单定义。
2. **`validate_on_submit()`** 是检查提交和验证的主要方法。
3. **始终在模板中包含 `{{ form.hidden_tag() }}`** 以启用 CSRF 保护。
4. **使用 WTForms 验证器** 进行清晰的声明式服务器端验证。
5. **自定义验证器** 可以在表单类中内联定义，也可以作为可重用的函数定义。
6. **Flash 消息** 提供表单操作的用户反馈。
7. **文件上传** 需要 `enctype="multipart/form-data"`，并应使用 `secure_filename()` 以确保安全性。
8. **在 Flask 配置中设置 `SECRET_KEY`** -- 它是 CSRF 令牌和会话管理的必需配置。
