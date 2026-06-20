# 05 · Kubernetes 容器编排

> K8s 是云原生的操作系统。学会 K8s，你就掌握了现代基础设施的通用语言。
> 这个模块是我花时间最多的，因为 K8s 是现在运维工程师的核心竞争力。

---

## 🎯 学习目标

完成本模块后，你应该能够：

- [ ] 理解 K8s 整体架构（Master/Worker、etcd、API Server、Scheduler、Controller）
- [ ] 熟练操作 Pod/Deployment/Service/Ingress 等核心资源
- [ ] 编写和调试 YAML 配置文件（手写，不依赖代码生成）
- [ ] 使用 ConfigMap/Secret 管理配置和敏感信息
- [ ] 掌握 Helm 包管理工具（添加仓库、安装、自定义 values.yaml）
- [ ] 了解 StatefulSet/DaemonSet/Job/CronJob 等高级控制器
- [ ] 配置 PersistentVolume 和 PersistentVolumeClaim
- [ ] 理解并实现服务发现和负载均衡
- [ ] 掌握 Ingress 控制器（Nginx Ingress / Traefik / Istio）
- [ ] 了解 RBAC 权限控制机制
- [ ] 会做集群维护：升级、备份（etcd）、节点管理
- [ ] 能排查常见故障：Pod 起不来、网络不通、存储挂载失败
- [ ] 理解网络模型：CNI 插件、Service IP、Pod IP、Ingress 转发
- [ ] 会配置资源配额（ResourceQuota）和限额（LimitRange）
- [ ] 了解 K8s 安全：Pod Security Standards、Network Policy

**学完这个模块，你值 25K+。**

---

## 📺 推荐视频教程

| 教程 | 讲师 | 链接 | 播放量 | 推荐度 |
|------|------|------|--------|---------|
| K8s 教程由浅入深 | 尚硅谷 | [B站 BV1Qv41167ck](https://www.bilibili.com/video/BV1Qv41167ck) | 100万+ | ⭐⭐⭐⭐⭐ |
| K8s 入门到精通 | 黑马程序员 | [B站 BV1cK4y1L7Tb](https://www.bilibili.com/video/BV1cK4y1L7Tb) | 50万+ | ⭐⭐⭐⭐⭐ |
| K8s 实战 | 马哥 | [B站](https://space.bilibili.com/387633139) | 30万+ | ⭐⭐⭐⭐ |
| 狂神说 K8s | 狂神 | [B站 BV1GT4y1A756](https://www.bilibili.com/video/BV1GT4y1A756) | 200万+ | ⭐⭐⭐⭐ |
| Helm 包管理 | 阳阳羊 | [B站](https://www.bilibili.com/video/BV1SAR7Y7oj) | 10万+ | ⭐⭐⭐ |
| K8s 网络管透 | 阿里云 | [B站](https://www.bilibili.com/video/BV1bK4y1a7tB) | 20万+ | ⭐⭐⭐⭐ |
| CKA 认证备考 | 姿势喵 | [B站](https://www.bilibili.com/video/BV1vQ4y1P7yA) | 30万+ | ⭐⭐⭐⭐ |

**学习顺序建议**：先看完「尚硅谷」打基础，再跟「狂神」做实战，最后用「Helm」学包管理。

---

## 📖 推荐书籍

| 书名 | 作者 | 适合阶段 | 一句话评价 |
|------|------|---------|-------------|
| 《Kubernetes 权威指南》 | 龚正等 | 高级 | 国内 K8s 最系统的书，配合官网文档一起看 |
| 《Kubernetes in Action（第2版）》 | Marko Lukša | 高级 | 最好的 K8s 英文书，有中文版 |
| 《深入解析 Kubernetes》 | 张磊 | 高级 | 阿里云 K8s 团队出品，原理讲得深 |
| 《Helm 学习指南》 | O'Reilly | 高级 | Helm 专题，够用 |
| 《Kubernetes 网络权威指南》 | 杜军 | 专家 | 网络专题，CNI/Service/Ingress 讲得细 |
| 《Kubernetes 实战》 | 马永亮 | 中级 | 实战向，有具体集群搭建步骤 |
| 《CKA 认证考试指南》 | Dario Reed | 中级 | 考证必备 |

---

## 🌐 在线参考资源

| 资源 | 链接 | 特点 |
|------|------|------|
| K8s 官方文档（中文） | https://kubernetes.io/zh-cn/docs/ | 最权威，必看 |
| K8s 中文社区 | https://kubernetes.org.cn/ | 中文翻译，更新及时 |
| guangzhengli/k8s-tutorials | https://github.com/guangzhengli/k8s-tutorials | ⭐5.8k，最好的中文教程 |
| kubernetes/minikube | https://github.com/kubernetes/minikube | 本地实验环境 |
| helm/helm | https://github.com/helm/helm | Helm 官方仓库 |
| 阿里云 K8s 最佳实践 | https://help.aliyun.com/product/85222.html | 国内云厂商实战经验 |
| Play with K8s | https://labs.play-with-k8s.com/ | 在线实验平台 |
| K8s the Hard Way | https://github.com/kelseyhightower/kubernetes-the-hard-way | ⭐32k，从零手动搭建 |
| CNI 插件对比 | https://www.cni.dev/ | 网络插件选型参考 |
| Istio 官方文档（中文） | https://istio.io/latest/zh/docs/ | Service Mesh 学习 |

---

## 📝 核心知识点清单

### 第一阶段：K8s 架构和基础（1-2 周）

- K8s 是什么，解决什么问题（容器编排、自愈、弹性伸缩）
- 整体架构：Master 节点组件 vs Worker 节点组件
  - Master：API Server（网关）、etcd（状态存储）、Scheduler（调度）、Controller Manager（控制循环）
  - Worker：kubelet（Pod 管家）、kube-proxy（网络代理）、Container Runtime（容器运行时）
- 安装方式对比：
  - `kubeadm init`：官方推荐，适合生产
  - 二进制部署：最理解原理，但费时
  - 云厂商托管（EKS/GKE/AKS/ACK）：生产首选，省心
  - minikube/kind：本地开发测试
- 使用 minikube 搭建本地实验环境
  ```bash
  minikube start --cpus=4 --memory=8192 --driver=docker
  kubectl get nodes
  ```
- kubectl 基础命令：
  ```bash
  kubectl get pods -A                          # 查看所有命名空间的 Pod
  kubectl get pods -n kube-system              # 查看指定命名空间
  kubectl describe pod <name>                  # 查看 Pod 详情（排错必用）
  kubectl logs <pod-name>                      # 查看日志
  kubectl logs <pod-name> -c <container-name> # 多容器 Pod 查看指定容器日志
  kubectl exec -it <pod-name> -- /bin/bash   # 进入容器
  kubectl apply -f xxx.yaml                   # 声明式部署
  kubectl delete -f xxx.yaml                  # 删除资源
  kubectl edit deployment <name>              # 在线编辑
  kubectl scale deployment <name> --replicas=5  # 扩缩容
  kubectl rollout status deployment <name>     # 查看滚动更新状态
  kubectl rollout undo deployment <name>      # 回滚
  kubectl port-forward <pod-name> 8080:80   # 端口转发（调试神器）
  ```

### 第二阶段：核心资源对象（2-3 周）

#### Pod — K8s 的最小调度单元
- Pod 的定义：一个或多个容器的集合（共享网络/存储）
- 为什么需要 Pod（vs 直接跑容器）：协同调度、共享卷、边车模式
- 镜像拉取策略：`Always` / `IfNotPresent` / `Never`
- 重启策略：`Always` / `OnFailure` / `Never`
- 资源限制：`requests`（调度依据）vs `limits`（硬上限）
  ```yaml
  resources:
    requests:
      memory: "64Mi"
      cpu: "250m"
    limits:
      memory: "128Mi"
      cpu: "500m"
  ```
- 健康检查：
  - `livenessProbe`：存活探针（失败则重启容器）
  - `readinessProbe`：就绪探针（失败则从 Service 摘流）
  - `startupProbe`：启动探针（保护慢启动应用）
- 初始化容器（initContainers）：主容器启动前执行，适合做初始化工作

#### Deployment — 无状态应用部署
- Deployment 的作用：声明式更新、滚动升级、回滚、副本控制
- 副本数控制（replicas）
- 更新策略：
  - `RollingUpdate`：滚动更新（默认，maxSurge/maxUnavailable 控制节奏）
  - `Recreate`：先删再建（适合不能并行跑的旧应用）
- 回滚操作：
  ```bash
  kubectl rollout history deployment <name>    # 查看历史版本
  kubectl rollout undo deployment <name>       # 回滚到上一版
  kubectl rollout undo deployment <name> --to-revision=2  # 回滚到指定版本
  ```
- 暂停/恢复滚动更新：
  ```bash
  kubectl rollout pause deployment <name>     # 暂停（调试用）
  kubectl rollout resume deployment <name>    # 恢复
  ```

#### Service — 服务发现和负载均衡
- Service 的四种类型：
  - `ClusterIP`：默认，集群内访问
  - `NodePort`：每个节点开放固定端口
  - `LoadBalancer`：云厂商负载均衡器
  - `ExternalName`：DNS CNAME 映射
- Service 与 Pod 的关联：通过 `selector` 标签选择器
- Headless Service（clusterIP: None）：用于 StatefulSet 或者需要直接访问 Pod IP 的场景
- DNS 解析规则：`<service>.<namespace>.svc.cluster.local`

#### Ingress — HTTP/HTTPS 路由
- Ingress 的作用：7层负载均衡，域名路由，TLS 终止
- Ingress Controller vs Ingress Resource：
  - Ingress Controller：实际干活的反向代理（Nginx/Traefik/Istio）
  - Ingress Resource：路由规则定义
- Nginx Ingress 安装：
  ```bash
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm install ingress-nginx ingress-nginx/ingress-nginx
  ```
- Ingress 示例：
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: example-ingress
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
  spec:
    tls:
    - hosts:
      - example.com
      secretName: example-tls
    rules:
    - host: example.com
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: web-service
              port:
                number: 80
  ```

---

## 🔧 实战：从零部署一个完整应用（Nginx + Redis + 配置）

```yaml
# 1. ConfigMap（Nginx 配置）
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-conf
data:
  nginx.conf: |
    server {
        listen 80;
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
        location /api {
            proxy_pass http://redis-service:6379;
        }
    }

---
# 2. Deployment（Nginx）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        volumeMounts:
        - name: conf
          mountPath: /etc/nginx/conf.d
        - name: html
          mountPath: /usr/share/nginx/html
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
      volumes:
      - name: conf
        configMap:
          name: nginx-conf
      - name: html
        configMap:
          name: nginx-html

---
# 3. Service（Nginx）
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP

---
# 4. Redis Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        emptyDir: {}

---
# 5. Redis Service
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  type: ClusterIP
```

应用：
```bash
kubectl apply -f nginx-redis.yaml
kubectl get all
kubectl port-forward svc/nginx-service 8080:80
# 浏览器访问 localhost:8080
```

---

## 🚨 常见故障排查手册

### Pod 起不来（Pending / CrashLoopBackOff / ImagePullBackOff）

```bash
# 1. 查看 Pod 状态和事件
kubectl describe pod <pod-name> -n <namespace>
# 重点看 Events 部分

# 2. 常见的 Pending 原因
# - 资源不足（ nodes have insufficient...）
# - 节点选择器不匹配
# - PVC 挂载失败

# 3. 常见的 ImagePullBackOff 原因
# - 镜像名写错
# - 私有仓库没配置 imagePullSecrets
# - 网络不通（节点无法访问镜像仓库）

# 4. 查看容器日志
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -c <container-name> -n <namespace>  # 多容器
```

### 网络不通（Service 无法访问 Pod / Pod 无法访问外网）

```bash
# 1. 检查 Service 的 Endpoints（最关键！）
kubectl get endpoints <service-name> -n <namespace>
# 如果 Endpoints 为空，说明 Service 的 selector 和 Pod 的 labels 不匹配

# 2. 在 Pod 里测试网络
kubectl exec -it <pod-name> -- nslookup kubernetes.default.svc.cluster.local
kubectl exec -it <pod-name> -- ping <service-ip>
kubectl exec -it <pod-name> -- curl <service-name>:<port>

# 3. 检查 NetworkPolicy（是否被拦截）
kubectl get networkpolicy -n <namespace>

# 4. 检查 CNI 插件状态
kubectl get pods -n kube-system | grep -E "calico|flannel|weave|cilium"
```

### 存储挂载失败（PVC Pending）

```bash
# 1. 检查 StorageClass 是否存在
kubectl get sc

# 2. 检查 PVC 状态
kubectl get pvc -n <namespace>
# Pending 说明没有可用的 PV 或者 StorageClass 配置错误

# 3. 查看 PVC 事件
kubectl describe pvc <pvc-name> -n <namespace>
```

---

## 🏭 生产环境最佳实践

### 资源配额和限额
```yaml
# ResourceQuota：命名空间级别资源总量限制
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
    services: "20"

---
# LimitRange：单个容器默认资源限制
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

### Pod 中断预算（PDB）— 保证滚动更新时服务不中断
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: nginx-pdb
spec:
  minAvailable: 2        # 至少保持 2 个 Pod 可用
  selector:
    matchLabels:
      app: nginx
```

### 安全加固
```yaml
# 1. 不以 root 运行
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true

# 2. 网络策略（只允许特定 Pod 访问）
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

---

## 🎓 认证考试指南（CKA / CKAD）

| 认证 | 侧重 | 备考建议 |
|------|------|---------|
| CKA (Certified Kubernetes Administrator) | 集群运维、故障排查、网络存储 | 重点练 `kubectl` 命令速度，会徒手写 YAML |
| CKAD (Certified Kubernetes Application Developer) | 应用部署、ConfigMap/Secret、Ingress、HPA | 重点练 Helm、标签选择器、健康检查配置 |
| CKS (Certified Kubernetes Security Specialist) | 安全加固、网络策略、镜像安全 | 重点练 Pod Security Standards、RBAC、Network Policy |

**备考资源**：
- [Killer Shell](https://killer.sh/) — 模拟考试环境（强烈推荐）
- [CKA 备考笔记](https://github.com/stefanprodan/Kubernetes-CKA) — ⭐14k
- [CKAD 练习题](https://github.com/dgkanatsio/Kubernetes-CKAD) — ⭐8k

---

## 📊 进阶路线

```
K8s 基础
  └── K8s 网络（CNI、Service、Ingress、Istio）
        └── K8s 存储（PV/PVC/StorageClass/CSI）
              └── Helm 包管理
                    └── GitOps（Argo CD / Flux）
                          └── Service Mesh（Istio / Linkerd）
                                └── 可观测性（Prometheus + Grafana + Jaeger）
```

**推荐下一个模块**：[06_CI_CD](./06_CI_CD/) — 学会用 GitHub Actions / GitLab CI 自动化部署 K8s 应用。

---

## ✅ 自测清单

学完之后，试试能不能回答这些问题：

- [ ] 说说 K8s 的架构，每个组件的作用是什么？
- [ ] Pod 的 `requests` 和 `limits` 有什么区别？
- [ ] Deployment 的滚动更新流程是怎样的？如何回滚？
- [ ] Service 的 `ClusterIP` / `NodePort` / `LoadBalancer` 有什么区别？
- [ ] Ingress 和 Service 有什么关系？
- [ ] `livenessProbe` 和 `readinessProbe` 的区别？
- [ ] PVC 绑定 PV 的流程是怎样的？
- [ ] StatefulSet 和 Deployment 有什么区别？
- [ ] RBAC 里的 Role / ClusterRole / RoleBinding / ClusterRoleBinding 是什么关系？
- [ ] 如何排查 Pod 网络不通的问题？

---

> 学完这个模块，去考个 CKA 认证，简历上写「熟悉 K8s 架构和运维」，薪资直接上一个台阶。
> 下一步推荐：[06_CI_CD](./06_CI_CD/) — 把代码自动部署到 K8s 集群。
