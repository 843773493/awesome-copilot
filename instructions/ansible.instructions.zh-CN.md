

---
description: 'Ansible规范与最佳实践'
applyTo: '**/*.yaml, **/*.yml'
---

# Ansible规范与最佳实践

## 通用指导原则

- 使用Ansible来配置和管理基础设施。
- 使用版本控制来管理您的Ansible配置。
- 保持简洁；仅在必要时使用高级功能
- 为每个play、block和task提供简洁但描述性的`name`
  - 以表示操作的动词开头，例如"安装"、"配置"或"复制"
  - 任务名称首字母大写
  - 为简洁起见，省略任务名称末尾的句号
  - 在role任务中省略role名称；Ansible在运行role时会自动显示role名称
  - 当从单独文件中包含任务时，可在每个任务名称中包含文件名以方便定位（例如，`<TASK_FILENAME> : <TASK_NAME>`）
- 使用注释来提供关于**做什么**、**如何做**和/或**为什么这么做**的额外上下文信息
  - 避免包含冗余注释
- 使用动态库存来管理云资源
  - 使用标签根据环境、功能、位置等动态创建组
  - 使用`group_vars`根据这些属性设置变量
- 尽可能使用具有幂等性的Ansible模块；避免使用`shell`、`command`和`raw`，因为它们会破坏幂等性
  - 如果必须使用`shell`或`command`，在可行的情况下使用`creates:`或`removes:`参数，以防止不必要的执行
- 使用[完全限定的集合名称 (FQCN)](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Fully-Qualified-Collection-Name-FQCN)以确保选择正确的模块或插件
  - 使用`ansible.builtin`集合来引用[内置模块和插件](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index)
- 将相关任务分组以提高可读性和模块化
- 对于`state`参数为可选的模块，显式设置`state: present`或`state: absent`以提高清晰度和一致性
- 使用完成任务所需的最低权限
  - 仅在play级别或`include:`语句中设置`become: true`，如果所有包含的任务都需要超级用户权限；否则，应在任务级别单独设置`become: true`
  - 仅在任务需要超级用户权限时设置`become: true`

## 密钥管理

- 当单独使用Ansible时，使用Ansible Vault存储密钥
  - 使用以下流程以便轻松找到vaulted变量的定义位置
    1. 创建一个名为组名的`group_vars/`子目录
    2. 在该子目录中创建两个文件，分别命名为`vars`和`vault`
    3. 在`vars`文件中定义所有需要的变量，包括任何敏感变量
    4. 将所有敏感变量复制到`vault`文件中，并在这些变量前添加`vault_`前缀
    5. 使用Jinja2语法调整`vars`文件中的变量，使其指向对应的`vault_`变量：`db_password: "{{ vault_db_password }}"`
    6. 加密`vault`文件以保护其内容
    7. 在playbook中使用`vars`文件中的变量名
- 当与其它工具（如Terraform）一起使用Ansible时，使用第三方密钥管理工具（如Hashicorp Vault、AWS Secrets Manager等）存储密钥
  - 这样可以让所有工具引用同一个密钥真实来源，并防止配置文件不同步

## 风格指南

- 使用2个空格缩进，并始终对列表进行缩进
- 以下内容之间使用单个空行分隔：
  - 两个主机块
  - 两个任务块
  - 主机和包含块
- 使用`snake_case`命名变量
- 在`vars:`映射或变量文件中定义变量时，按字母顺序排序变量
- 无论映射中包含多少对键值，始终使用多行映射语法
  - 这有助于提高可读性，并减少版本控制中的更改集冲突
- 优先使用单引号而非双引号
  - 仅在需要嵌套在单引号中的情况下（例如Jinja映射引用）或字符串需要转义字符时（例如使用"\n"表示换行符）使用双引号
  - 如果必须编写长字符串，请使用折叠块标量语法（即`>`）以将换行符替换为空格，或使用字面块标量语法（即`|`）以保留换行符；省略所有特殊引号
- play的`host`部分应遵循以下一般顺序：
  - `hosts`声明
  - 按字母顺序排列的主机选项（例如`become`、`remote_user`、`vars`）
  - `pre_tasks`
  - `roles`
  - `tasks`
- 每个任务应遵循以下一般顺序：
  - `name`
  - 任务声明（例如`service:`、`package:`）
  - 任务参数（使用多行映射语法）
  - 循环操作符（例如`loop`）
  - 按字母顺序排列的任务选项（例如`become`、`ignore_errors`、`register`）
  - `tags`
- 对于`include`语句，引用文件名并仅在`include`语句为多行时使用空行分隔（例如，它们包含标签）

## 代码检查

- 使用`ansible-lint`和`yamllint`检查语法并强制执行项目标准
- 使用`ansible-playbook --syntax-check`检查语法错误
- 使用`ansible-playbook --check --diff`进行playbook执行的干运行检查

<!-- 
这些指南基于或复制自以下来源：

- [Ansible文档 - 小技巧](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Whitecloud Ansible风格指南](https://github.com/whitecloud/ansible-styleguide)
-->