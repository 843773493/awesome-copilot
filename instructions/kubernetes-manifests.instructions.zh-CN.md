

---
applyTo: 'k8s/**/*.yaml,k8s/**/*.yml,manifests/**/*.yaml,manifests/**/*.yml,deploy/**/*.yaml,deploy/**/*.yml,charts/**/templates/**/*.yaml,charts/**/templates/**/*.yml'
description: 'Kubernetes YAML清单的最佳实践，包括标签规范、安全上下文、Pod安全、资源管理、探针和验证命令'
---

# Kubernetes清单指南

## 您的任务

创建生产就绪的Kubernetes清单，通过一致的标签、正确的资源管理以及全面的健康检查，优先考虑安全性、可靠性和运营卓越。

## 标签规范

**必需标签**（Kubernetes推荐）：
- `app.kubernetes.io/name`: 应用名称
- `app.kubernetes.io/instance`: 实例标识符
- `app.kubernetes.io/version`: 版本
- `app.kubernetes.io/component`: 组件角色
- `app.kubernetes.io/part-of`: 应用组
- `app.kubernetes.io/managed-by`: 管理工具

**附加标签**：
- `environment`: 环境名称
- `team`: 所属团队
- `cost-center`: 用于计费

**有用的注解**：
- 文档和所有权信息
- 监控：`prometheus.io/scrape`, `prometheus.io/port`, `prometheus.io/path`
- 变更追踪：git提交记录，部署日期

## 安全上下文默认值

**Pod级别**：
- `runAsNonRoot: true`
- `runAsUser`和`runAsGroup`: 特定ID
- `fsGroup`: 文件系统组
- `seccompProfile.type: RuntimeDefault`

**容器级别**：
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`（使用tmpfs挂载可写目录）
- `capabilities.drop: [ALL]`（仅添加所需功能）

## Pod安全标准

使用Pod安全准入：
- **受限**（推荐用于生产环境）：强制执行安全加固
- **基础**：最低安全要求
- 在命名空间级别应用

## 资源请求和限制

**始终定义**：
- 请求：保证最低资源（用于调度）
- 限制：允许的最大资源（防止资源耗尽）

**QoS等级**：
- **保证型**：请求 == 限制（适用于关键应用）
- **突发型**：请求 < 限制（灵活资源使用）
- **尽力而为型**：未定义资源（避免在生产环境中使用）

## 健康检查探针

**存活探针**：重启不健康的容器  
**就绪探针**：控制流量路由  
**启动探针**：保护启动缓慢的应用程序

为每个探针配置适当的延迟、周期、超时和阈值。

## 部署策略

**部署策略**：
- 使用`RollingUpdate`并设置`maxSurge`和`maxUnavailable`
- 设置`maxUnavailable: 0`以实现零停机时间

**高可用性**：
- 最小2-3个副本
- Pod中断预算（PDB）
- 反亲和性规则（跨节点/区域分布）
- 水平Pod自动扩展器（HPA）用于可变负载

## 验证命令

**预部署验证**：
- `kubectl apply --dry-run=client -f manifest.yaml`
- `kubectl apply --dry-run=server -f manifest.yaml`
- `kubeconform -strict manifest.yaml`（模式验证）
- `helm template ./chart | kubeconform -strict`（用于Helm）

**策略验证**：
- OPA Conftest、Kyverno或Datree

## 部署与回滚

**部署**：
- `kubectl apply -f manifest.yaml`
- `kubectl rollout status deployment/NAME`

**回滚**：
- `kubectl rollout undo deployment/NAME`
- `kubectl rollout undo deployment/NAME --to-revision=N`
- `kubectl rollout history deployment/NAME`

**重启**：
- `kubectl rollout restart deployment/NAME`

## 清单检查清单

- [ ] 标签：应用标准标签
- [ ] 注解：文档和监控信息
- [ ] 安全性：runAsNonRoot、readOnlyRootFilesystem、已删除的功能
- [ ] 资源：定义请求和限制
- [ ] 探针：配置存活、就绪、启动探针
- [ ] 镜像：使用特定标签（避免使用:latest）
- [ ] 副本：生产环境至少2-3个副本
- [ ] 策略：使用RollingUpdate并设置适当的surge/unavailable
- [ ] PDB：生产环境已定义
- [ ] 反亲和性：已配置用于高可用性
- [ ] 温和关闭：设置terminationGracePeriodSeconds
- [ ] 验证：干运行和kubeconform通过
- [ ] 密钥：使用Secret资源，而非ConfigMaps
- [ ] 网络策略：最小权限访问（如适用）

## 最佳实践总结

1. 使用标准标签和注解  
2. 始终以非root用户运行并删除不必要的功能  
3. 定义资源请求和限制  
4. 实现所有三种探针类型  
5. 固定镜像标签到特定版本  
6. 为高可用性配置反亲和性规则  
7. 设置Pod中断预算  
8. 使用滚动更新并实现零不可用  
9. 在应用前验证清单  
10. 在可能的情况下启用只读根文件系统