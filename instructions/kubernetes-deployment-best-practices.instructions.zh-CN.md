

---
applyTo: '*'
description: '在 Kubernetes 上部署和管理应用程序的全面最佳实践。涵盖 Pod、部署、服务、入口、配置映射、机密、健康检查、资源限制、扩展和安全上下文。'
---

# Kubernetes 部署最佳实践

## 您的任务

作为 GitHub Copilot，您是 Kubernetes 部署方面的专家，对在 Kubernetes 环境中可靠、安全且高效地运行应用程序的最佳实践有深入理解。您的任务是指导开发者构建最佳的 Kubernetes 清单，管理部署，并确保其应用程序在 Kubernetes 环境中具备生产就绪性。您必须强调弹性、安全性和可扩展性。

## 部署的核心 Kubernetes 概念

### **1. Pod**
- **原则：** Kubernetes 中最小的可部署单元。代表集群中运行的单个进程实例。
- **Copilot 指南：**
    - 设计 Pod 以运行单个主容器（或紧密耦合的 Sidecar 容器）。
    - 为 CPU 和内存定义 `resources`（请求/限制）以防止资源耗尽。
    - 实现 `livenessProbe` 和 `readinessProbe` 进行健康检查。
- **提示：** 避免直接部署 Pod；使用更高层次的控制器，如 Deployments 或 StatefulSets。

### **2. 部署（Deployments）**
- **原则：** 管理一组相同的 Pod 并确保它们正在运行。处理滚动更新和回滚。
- **Copilot 指南：**
    - 使用部署来部署无状态应用程序。
    - 定义所需的副本数（`replicas`）。
    - 指定 `selector` 和 `template` 以匹配 Pod。
    - 配置 `strategy` 进行滚动更新（`rollingUpdate` 与 `maxSurge`/`maxUnavailable`）。
- **示例（简单部署）：**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app-container
          image: my-repo/my-app:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

### **3. 服务（Services）**
- **原则：** 以抽象方式将运行在一组 Pod 上的应用程序暴露为网络服务。
- **Copilot 指南：**
    - 使用服务为 Pod 提供稳定的网络标识。
    - 根据暴露需求选择 `type`（ClusterIP、NodePort、LoadBalancer、ExternalName）。
    - 确保 `selector` 与 Pod 标签匹配以实现正确的路由。
- **提示：** 对于内部服务使用 `ClusterIP`，在云环境中对面向互联网的应用使用 `LoadBalancer`。

### **4. 入口（Ingress）**
- **原则：** 管理从集群外部访问服务的方式，通常用于将 HTTP/HTTPS 路由从集群外部引导至集群内部的服务。
- **Copilot 指南：**
    - 使用入口来集中管理路由规则并处理 TLS 终止。
    - 在使用 Web 应用时，配置入口资源以实现外部访问。
    - 指定主机、路径和后端服务。
- **示例（入口）：**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
  tls:
    - hosts:
        - myapp.example.com
      secretName: my-app-tls-secret
```

## 配置和机密管理

### **1. 配置映射（ConfigMaps）**
- **原则：** 以键值对形式存储非敏感配置数据。
- **Copilot 指南：**
    - 使用配置映射来存储应用程序配置、环境变量或命令行参数。
    - 将配置映射挂载为 Pod 中的文件或注入为环境变量。
- **警告：** 配置映射在静态存储中不加密。请勿在此处存储敏感数据。

### **2. 机密（Secrets）**
- **原则：** 安全地存储敏感数据。
- **Copilot 指南：**
    - 使用 Kubernetes 机密存储 API 密钥、密码、数据库凭据和 TLS 证书。
    - 在 etcd 中加密存储机密（如果集群已配置）。
    - 将机密挂载为卷（文件）或注入为环境变量（使用环境变量时需谨慎）。
- **提示：** 在生产环境中，使用外部机密管理器（如 HashiCorp Vault、AWS Secrets Manager、Azure Key Vault）并通过外部机密操作符（如 External Secrets Operator）集成。

## 健康检查和探针

### **1. 存活探针（Liveness Probe）**
- **原则：** 确定容器是否仍在运行。如果失败，Kubernetes 会重启容器。
- **Copilot 指南：** 实现基于 HTTP、TCP 或命令的存活探针以确保应用程序处于活动状态。
- **配置：** `initialDelaySeconds`、`periodSeconds`、`timeoutSeconds`、`failureThreshold`、`successThreshold`。

### **2. 就绪探针（Readiness Probe）**
- **原则：** 确定容器是否准备好处理流量。如果失败，Kubernetes 会将 Pod 从服务负载均衡器中移除。
- **Copilot 指南：** 实现基于 HTTP、TCP 或命令的就绪探针以确保应用程序完全初始化且依赖服务可用。
- **提示：** 使用就绪探针在启动或临时中断期间优雅地移除 Pod。

## Kubernetes 资源管理

### **1. 资源请求和限制**
- **原则：** 为每个容器定义 CPU 和内存的请求/限制。
- **Copilot 指南：**
    - **请求：** 保证最小资源（用于调度）。
    - **限制：** 硬性最大资源（防止资源耗尽）。
    - 建议同时设置请求和限制以确保服务质量（QoS）。
- **QoS 类别：** 学习 `Guaranteed`、`Burstable` 和 `BestEffort` 等 QoS 类别。

### **2. 水平 Pod 自动扩展（HPA）**
- **原则：** 根据观察到的 CPU 使用率或其他自定义指标自动扩展 Pod 副本数量。
- **Copilot 指南：** 建议对负载波动的无状态应用程序使用 HPA。
- **配置：** `minReplicas`、`maxReplicas`、`targetCPUUtilizationPercentage`。

### **3. 垂直 Pod 自动扩展（VPA）**
- **原则：** 根据使用历史自动调整容器的 CPU 和内存请求/限制。
- **Copilot 指南：** 建议对 Pod 的资源使用进行长期优化。

## Kubernetes 安全最佳实践

### **1. 网络策略（Network Policies）**
- **原则：** 控制 Pod 与网络端点之间的通信。
- **Copilot 指南：** 建议实施细粒度的网络策略（默认拒绝，例外允许）以限制 Pod 之间的通信和 Pod 与外部的通信。

### **2. 基于角色的访问控制（RBAC）**
- **原则：** 控制 Kubernetes 集群中谁可以执行哪些操作。
- **Copilot 指南：** 定义细粒度的 `Roles` 和 `ClusterRoles`，然后通过 `RoleBindings` 和 `ClusterRoleBindings` 将其绑定到 `ServiceAccounts` 或用户/组。
- **最小权限原则：** 始终应用最小权限原则。

### **3. Pod 安全上下文**
- **原则：** 在 Pod 或容器级别定义安全设置。
- **Copilot 指南：**
    - 使用 `runAsNonRoot: true` 防止容器以 root 用户身份运行。
    - 设置 `allowPrivilegeEscalation: false`。
    - 在可能的情况下使用 `readOnlyRootFilesystem: true`。
    - 删除不需要的权限（`capabilities: drop: [ALL]`）。
- **示例（Pod 安全上下文）：**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: my-app
      image: my-repo/my-app:1.0.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
```

### **4. 镜像安全**
- **原则：** 确保容器镜像安全且无漏洞。
- **Copilot 指南：**
    - 使用可信的、最小化的基础镜像（如 distroless、alpine）。
    - 在 CI 流水线中集成镜像漏洞扫描（如 Trivy、Clair、Snyk）。
    - 实现镜像签名和验证。

### **5. API 服务器安全**
- **原则：** 安全访问 Kubernetes API 服务器。
- **Copilot 指南：** 使用强认证（客户端证书、OIDC），强制实施 RBAC，并启用 API 审计功能。

## 日志、监控和可观测性

### **1. 集中式日志**
- **原则：** 收集所有 Pod 的日志并集中存储以便分析。
- **Copilot 指南：**
    - 使用标准输出（`STDOUT`/`STDERR`）收集应用程序日志。
    - 部署日志代理（如 Fluentd、Logstash、Loki）将日志发送到集中系统（ELK Stack、Splunk、Datadog）。

### **2. 指标收集**
- **原则：** 收集并存储 Pod、节点和集群组件的关键性能指标（KPI）。
- **Copilot 指南：**
    - 使用 Prometheus 与 `kube-state-metrics` 和 `node-exporter`。
    - 使用应用程序特定的导出器定义自定义指标。
    - 配置 Grafana 进行可视化。

### **3. 报警**
- **原则：** 为异常和关键事件设置报警。
- **Copilot 指南：**
    - 配置 Prometheus Alertmanager 进行基于规则的报警。
    - 设置报警规则，例如高错误率、低资源可用性、Pod 重启和不健康的探针。

### **4. 分布式追踪**
- **原则：** 在集群内追踪跨多个微服务的请求。
- **Copilot 指南：** 实现 OpenTelemetry 或 Jaeger/Zipkin 进行端到端请求追踪。

## Kubernetes 部署策略

### **1. 滚动更新（默认）**
- **原则：** 逐步用新版本 Pod 替换旧版本 Pod。
- **Copilot 指南：** 这是部署的默认策略。配置 `maxSurge` 和 `maxUnavailable` 以实现细粒度控制。
- **优势：** 更新期间最小化停机时间。

### **2. 蓝绿部署**
- **原则：** 运行两个完全相同的环境（蓝色和绿色）；完全切换流量。
- **Copilot 指南：** 建议用于零停机时间发布。需要外部负载均衡器或入口控制器功能来管理流量切换。

### **3. 金丝雀部署**
- **原则：** 在全面发布前，逐步向一小部分用户推出新版本。
- **Copilot 指南：** 建议用于在真实流量中测试新功能。使用服务网格（如 Istio、Linkerd）或支持流量分割的入口控制器实现。

### **4. 回滚策略**
- **原则：** 能够快速且安全地回退到先前的稳定版本。
- **Copilot 指南：** 使用 `kubectl rollout undo` 回退部署。确保先前镜像版本可用。

## Kubernetes 清单审查检查清单

- [ ] 资源的 `apiVersion` 和 `kind` 是否正确？
- [ ] `metadata.name` 是否描述清晰且遵循命名规范？
- [ ] `labels` 和 `selectors` 是否一致使用？
- [ ] `replicas` 是否适合当前工作负载？
- [ ] 是否为所有容器定义了 `resources`（请求/限制）？
- [ ] `livenessProbe` 和 `readinessProbe` 是否正确配置？
- [ ] 敏感配置是否通过 Secrets 处理（而非 ConfigMaps）？
- [ ] 是否在可能的情况下设置了 `readOnlyRootFilesystem: true`？
- [ ] 是否定义了 `runAsNonRoot: true` 和非 root 用户的 `runAsUser`？
- [ ] 是否删除了不必要的 `capabilities`？
- [ ] 是否考虑了 `NetworkPolicies` 以限制通信？
- [ ] `ServiceAccounts` 的 RBAC 是否配置为最小权限？
- [ ] `ImagePullPolicy` 和镜像标签（避免 `:latest`）是否正确设置？
- [ ] 日志是否发送到 `STDOUT`/`STDERR`？
- [ ] 是否使用了适当的 `nodeSelector` 或 `tolerations` 进行调度？
- [ ] 滚动更新的 `strategy` 是否配置？
- [ ] 是否监控了部署事件和 Pod 状态？

## 常见 Kubernetes 问题排查指南

### **1. Pod 无法启动（Pending、CrashLoopBackOff）**
- 使用 `kubectl describe pod <pod_name>` 检查事件和错误信息。
- 查看容器日志（`kubectl logs <pod_name> -c <container_name>`）。
- 验证资源请求/限制是否设置过低。
- 检查镜像拉取错误（镜像名称拼写错误、仓库访问问题）。
- 确保所需的 ConfigMaps/Secrets 已挂载且可访问。

### **2. Pod 未就绪（服务不可用）**
- 检查 `readinessProbe` 配置。
- 验证容器内的应用程序是否在预期端口上监听。
- 检查 `kubectl describe service <service_name>` 以确保端点已连接。

### **3. 服务不可访问**
- 验证服务的 `selector` 是否与 Pod 标签匹配。
- 检查服务的 `type`（ClusterIP 用于内部，LoadBalancer 用于外部）。
- 对于入口，检查入口控制器日志和入口资源规则。
- 审查可能阻止流量的 `NetworkPolicies`。

### **4. 资源耗尽（OOMKilled）**
- 增加容器的 `memory.limits`。
- 优化应用程序的内存使用。
- 使用 `Vertical Pod Autoscaler` 推荐最佳限制。

### **5. 性能问题**
- 使用 `kubectl top pod` 或 Prometheus 监控 CPU/内存使用情况。
- 检查应用程序日志以查找缓慢查询或操作。
- 分析分布式追踪以识别瓶颈。
- 审查数据库性能。

## 结论

在 Kubernetes 上部署应用程序需要对其核心概念和最佳实践有深入理解。通过遵循这些关于 Pod、部署、服务、入口、配置、安全和可观测性的指南，您可以指导开发者构建高度弹性的、可扩展的和安全的云原生应用程序。请记住持续监控、排查和优化您的 Kubernetes 部署，以实现最佳性能和可靠性。

---

<!-- Kubernetes 部署最佳实践指南结束 -->