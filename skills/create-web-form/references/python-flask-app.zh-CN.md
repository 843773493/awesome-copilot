# Python Flask 应用参考

> 源自: <https://realpython.com/python-web-applications/>

本参考文档涵盖构建 Python Web 应用程序，包括网络工作原理、框架选择、Flask 应用的构建与部署，以及理解关键的 Web 开发概念。

---

## 概述

Python 提供了多种 Web 开发方法：

- **Web 框架**（Flask、Django、FastAPI）处理路由、模板和数据
- **托管平台**（Google App Engine、PythonAnywhere、Heroku 等）用于部署
- **WSGI**（Web 服务器网关接口）作为 Web 服务器和 Python 应用程序之间的标准接口

---

## 网络工作原理

### HTTP 请求-响应周期

1. 客户端（浏览器）向服务器发送一个 **HTTP 请求**
2. 服务器处理请求并返回一个 **HTTP 响应**
3. 浏览器渲染响应内容

### HTTP 方法

| 方法 | 用途 |
|------|------|
| `GET` | 从服务器检索数据 |
| `POST` | 向服务器提交数据 |
| `PUT` | 更新服务器上的现有数据 |
| `DELETE` | 从服务器删除数据 |

### URL 结构

```
https://example.com:443/path/to/resource?key=value#section
  |         |        |        |              |        |
协议     主机     端口     路径          查询   片段
```

---

## 选择 Python Web 框架

### Flask

- **微框架** -- 最小核心，通过扩展实现更多功能
- 适合小型到中型应用、API 和学习
- 未内置数据库抽象层、表单验证等组件
- 所有功能都有扩展可用（SQLAlchemy、WTForms、登录等）

### Django

- **全栈框架** -- 提供了所有内置功能
- 适合大型应用，内置 ORM、管理面板和认证功能
- 项目结构具有指导性

### FastAPI

- **现代、快速、异步框架** -- 基于 Starlette 和 Pydantic 构建
- 适合构建具有自动文档功能的 API
- 内置数据验证和序列化功能

---

## 构建 Flask 应用

### 安装

```bash
python -m pip install flask
```

### 最小化应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 运行应用

```bash
# 方法 1：直接执行
python app.py

# 方法 2：使用 Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

---

## 路由

### 基本路由

```python
@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'
```

### 带 URL 参数的动态路由

```python
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id}'
```

### URL 转换器

| 转换器 | 描述 |
|--------|------|
| `string` | 接受不含斜杠的任意文本（默认） |
| `int` | 接受正整数 |
| `float` | 接受正浮点数 |
| `path` | 类似 `string`，但也可接受斜杠 |
| `uuid` | 接受 UUID 字符串 |

### 指定 HTTP 方法

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    return show_login_form()
```

---

## 使用 Jinja2 模板

### 基本模板渲染

```python
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

### 模板继承

**基础模板 (`templates/base.html`):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('about') }}">About</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>My Web App</p>
    </footer>
</body>
</html>
```

**子模板 (`templates/home.html`):**

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Welcome to My App</h1>
    <p>This is the home page.</p>
{% endblock %}
```

### Jinja2 模板语法

| 语法 | 用途 |
|------|------|
| `{{ variable }}` | 输出变量的值 |
| `{% statement %}` | 执行控制流语句 |
| `{# comment #}` | 模板注释（不渲染） |
| `{{ url_for('func') }}` | 动态生成视图函数的 URL |
| `{{ url_for('static', filename='style.css') }}` | 动态生成静态文件的 URL |

### 模板中的控制流

```html
{% if user %}
    <h1>Hello, {{ user.name }}!</h1>
{% else %}
    <h1>Hello, stranger!</h1>
{% endif %}

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

---

## 项目结构

### 推荐的 Flask 项目布局

```
my_flask_app/
    app.py                  # 应用入口
    config.py               # 配置设置
    requirements.txt        # Python 依赖
    static/                 # 静态文件（CSS、JS、图片）
        style.css
        script.js
    templates/              # Jinja2 HTML 模板
        base.html
        home.html
        about.html
    models.py               # 数据库模型（如果使用数据库）
    forms.py                # WTForms 表单类
```

### 更大型应用结构（蓝图）

```
my_flask_app/
    app/
        __init__.py         # 应用工厂
        models.py
        auth/
            __init__.py
            routes.py
            forms.py
            templates/
                login.html
                register.html
        main/
            __init__.py
            routes.py
            templates/
                home.html
                about.html
    config.py
    requirements.txt
    run.py
```

---

## 处理静态文件

Flask 会自动从 `static/` 目录提供静态文件。

### 在模板中引用静态文件

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="{{ url_for('static', filename='script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

---

## 数据库集成

### 使用 Flask-SQLAlchemy

```bash
pip install Flask-SQLAlchemy
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

### 创建数据库

```python
with app.app_context():
    db.create_all()
```

---

## 部署

### 部署到 PythonAnywhere

1. 在 pythonanywhere.com 创建一个免费账户
2. 通过 Git 或文件浏览器上传代码
3. 设置虚拟环境并安装依赖项
4. 配置指向 Flask 应用的 WSGI 文件
5. 重新加载 Web 应用

### 部署到 Heroku

1. 创建 `Procfile`:

```
web: gunicorn app:app
```

1. 创建 `requirements.txt`:

```bash
pip freeze > requirements.txt
```

1. 部署:

```bash
heroku create
git push heroku main
```

### 部署到 Google App Engine

创建 `app.yaml` 配置文件:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

handlers:
  - url: /static
    static_dir: static
  - url: /.*
    script: auto
```

### WSGI 服务器

生产环境中应使用 WSGI 服务器而不是 Flask 内置的开发服务器：

| 服务器 | 描述 |
|--------|------|
| **Gunicorn** | 用于 Unix 的生产级 WSGI 服务器 |
| **Waitress** | 用于 Windows 和 Unix 的生产级 WSGI 服务器 |
| **uWSGI** | 功能丰富的 WSGI 服务器，具有多种部署选项 |

```bash
# 使用 Gunicorn
pip install gunicorn
gunicorn app:app

# 使用 Waitress
pip install waitress
waitress-serve --port=5000 app:app
```

---

## 环境配置

### 使用环境变量

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    DEBUG = os.environ.get('FLASK_DEBUG', False)
```

### 使用 python-dotenv

```bash
pip install python-dotenv
```

创建 `.env` 文件:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///site.db
FLASK_DEBUG=1
```

在应用中加载:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 关键要点

1. **Flask 是一个微框架** -- 提供路由、模板和请求处理功能，其他选择（数据库、表单、认证）通过扩展实现。
2. **使用 Jinja2 模板继承** 来通过基础模板和子块保持 HTML 的简洁性。
3. **以清晰的结构组织项目**：将 `templates/`、`static/` 和 Python 模块分开。
4. **使用蓝图** 来组织大型应用，以便分组相关路由和模板。
5. **不要在生产环境中使用 Flask 开发服务器** -- 使用 Gunicorn、Waitress 或 uWSGI。
6. **使用环境变量存储配置**，通过 `python-dotenv` 或平台特定配置实现。
7. **使用 `url_for()`** 来动态生成 URL，而不是硬编码路径。
8. **Flask-SQLAlchemy** 提供了方便的 ORM 层用于数据库操作。
9. **多种托管平台** 支持 Flask 应用：PythonAnywhere、Heroku、Google App Engine 等。
