# Python 联系表单参考指南

> 来源: <https://mailtrap.io/blog/python-contact-form/>

本参考指南涵盖了如何使用 Python 构建联系表单，包括创建 HTML 表单、使用 Flask 处理表单提交、使用 `smtplib` 发送邮件以及验证用户输入。

---

## 概述

一个典型的 Python 联系表单通常包括以下部分：

- 一个 **HTML 前端**，用于用户输入（姓名、电子邮件、信息）
- 一个 **Python 后端**（通常为 Flask 或 Django）用于接收和处理表单数据
- 一个 **邮件发送机制**（使用 `smtplib` 或事务性邮件 API）用于传递表单提交内容
- **客户端验证**（HTML5 属性）和 **服务器端验证**（Python 逻辑）的输入验证

---

## 设置 Flask 项目

### 安装 Flask

```bash
pip install Flask
```

### 基本项目结构

```
contact-form/
    app.py
    templates/
        contact.html
        success.html
    static/
        style.css
```

### 最小化的 Flask 应用程序

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 创建 HTML 联系表单

### 基本联系表单模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>联系我们</title>
</head>
<body>
    <h1>联系我们</h1>
    <form method="POST" action="/contact">
        <div>
            <label for="name">姓名：</label>
            <input type="text" id="name" name="name" required />
        </div>
        <div>
            <label for="email">电子邮件：</label>
            <input type="email" id="email" name="email" required />
        </div>
        <div>
            <label for="subject">主题：</label>
            <input type="text" id="subject" name="subject" required />
        </div>
        <div>
            <label for="message">信息：</label>
            <textarea id="message" name="message" rows="5" required></textarea>
        </div>
        <button type="submit">发送信息</button>
    </form>
</body>
</html>
```

### 关键 HTML 表单属性

| 属性      | 描述 |
|-----------|------|
| `method`  | HTTP 方法 -- 使用 `POST` 以避免数据暴露在 URL 中 |
| `action`  | 处理表单数据的服务器端点 |
| `required` | 强制执行客户端验证的 HTML5 属性 |
| `name`    | 识别提交表单数据中的每个字段 |

---

## 在 Flask 中处理表单提交

### 处理 POST 请求

```python
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # 验证输入
        if not name or not email or not message:
            flash('请填写所有必填字段。', 'error')
            return redirect(url_for('contact'))

        # 发送邮件
        send_email(name, email, subject, message)

        flash('您的信息已成功发送！', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')
```

### 访问表单数据

Flask 提供 `request.form` 来访问提交的表单数据：

| 方法 | 描述 |
|------|------|
| `request.form['key']` | 如果键不存在则引发 `KeyError` |
| `request.form.get('key')` | 如果键不存在则返回 `None`（更安全） |
| `request.form.get('key', 'default')` | 如果键不存在则返回默认值 |

---

## 使用 `smtplib` 发送邮件

### 基本邮件发送函数

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(name, email, subject, message):
    sender_email = "your-email@example.com"
    receiver_email = "recipient@example.com"
    password = "your-email-password"

    # 创建邮件消息
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"联系表单: {subject}"

    # 邮件正文
    body = f"""
    新的联系表单提交：

    姓名: {name}
    电子邮件: {email}
    主题: {subject}
    信息: {message}
    """
    msg.attach(MIMEText(body, 'plain'))

    # 发送邮件
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
    except Exception as e:
        print(f"发送邮件时出错: {e}")
        raise
```

### 常见 SMTP 服务器设置

| 提供商 | SMTP 服务器 | TLS 端口 | SSL 端口 |
|--------|-------------|---------|---------|
| Gmail | `smtp.gmail.com` | 587 | 465 |
| Outlook | `smtp-mail.outlook.com` | 587 | -- |
| Yahoo | `smtp.mail.yahoo.com` | 587 | 465 |
| Mailtrap（测试） | `sandbox.smtp.mailtrap.io` | 587 | 465 |

### 使用环境变量存储凭证

永远不要硬编码电子邮件凭证。请改用环境变量：

```python
import os

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
```

---

## 服务器端验证

### 验证表单输入

```python
import re

def validate_contact_form(name, email, message):
    errors = []

    if not name or len(name.strip()) < 2:
        errors.append('姓名至少需要 2 个字符。')

    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append('请输入有效的电子邮件地址。')

    if not message or len(message.strip()) < 10:
        errors.append('信息至少需要 10 个字符。')

    return errors
```

### 将验证集成到路由中

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        errors = validate_contact_form(name, email, message)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html',
                                   name=name, email=email,
                                   subject=subject, message=message)

        send_email(name, email, subject, message)
        flash('信息已成功发送！', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')
```

---

## 使用 Mailtrap 进行邮件测试

Mailtrap 提供了一个安全的沙箱 SMTP 服务器，用于在不发送到真实收件箱的情况下测试邮件发送功能。

### Mailtrap 配置

```python
import smtplib
from email.mime.text import MIMEText

def send_test_email(name, email, subject, message):
    sender = "from@example.com"
    receiver = "to@example.com"

    body = f"姓名: {name}\n电子邮件: {email}\n主题: {subject}\n信息: {message}"

    msg = MIMEText(body)
    msg['Subject'] = f"联系表单: {subject}"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("your_mailtrap_username", "your_mailtrap_password")
        server.sendmail(sender, receiver, msg.as_string())
```

---

## 使用 Flask-Mail 扩展

Flask-Mail 简化了 Flask 应用程序中的邮件配置和发送过程。

### 安装和设置

```bash
pip install Flask-Mail
```

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
```

### 使用 Flask-Mail 发送邮件

```python
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message_body = request.form.get('message')

    msg = Message(
        subject=f"联系表单: {subject}",
        recipients=['admin@example.com'],
        reply_to=email
    )
    msg.body = f"From: {name} ({email})\n\n{message_body}"

    try:
        mail.send(msg)
        flash('信息已成功发送！', 'success')
    except Exception as e:
        flash('发生错误。请稍后再试一次。', 'error')

    return redirect(url_for('contact'))
```

---

## CSRF 保护

跨站请求伪造（CSRF）保护可防止恶意网站代表用户提交表单。

### 使用 Flask-WTF 进行 CSRF 保护

```bash
pip install Flask-WTF
```

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    email = StringField('电子邮件', validators=[DataRequired(), Email()])
    subject = StringField('主题', validators=[DataRequired()])
    message = TextAreaField('信息', validators=[DataRequired()])
    submit = SubmitField('发送信息')
```

在模板中包含 CSRF 令牌：

```html
<form method="POST" action="/contact">
    {{ form.hidden_tag() }}
    <!-- 表单字段 -->
</form>
```

---

## 完整示例应用程序

```python
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

def send_email(name, email, subject, message):
    sender = os.environ.get('MAIL_USERNAME')
    receiver = os.environ.get('MAIL_RECIPIENT')
    password = os.environ.get('MAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"联系表单: {subject}"

    body = f"姓名: {name}\n电子邮件: {email}\n主题: {subject}\n\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(os.environ.get('SMTP_SERVER', 'smtp.gmail.com'), 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

@app.route('/')
def home():
    return redirect(url_for('contact'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, message]):
            flash('请填写所有必填字段。', 'error')
            return render_template('contact.html')

        try:
            send_email(name, email, subject, message)
            flash('您的信息已成功发送！', 'success')
        except Exception:
            flash('发送信息失败。请稍后再试一次。', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 关键要点

1. **使用 Flask** 作为轻量级的 Python Web 框架，通过 `request.form` 处理联系表单提交。
2. **使用 `smtplib`** 或 **Flask-Mail** 从联系表单发送电子邮件。
3. **在客户端**（HTML5 `required`, `type="email"`）和 **服务器端**（Python 正则表达式、长度检查）进行输入验证。
4. **不要硬编码凭证** -- 使用环境变量或 `.env` 文件。
5. **使用 Mailtrap** 或类似服务，在不发送到真实收件箱的情况下测试邮件传递。
6. **使用 Flask-WTF** 添加 CSRF 保护，以防止跨站请求伪造攻击。
7. **Flash 消息** 为成功提交和验证错误提供用户反馈。
8. **使用 `MIMEMultipart`** 构建包含标题和正文内容的格式良好的电子邮件消息。
