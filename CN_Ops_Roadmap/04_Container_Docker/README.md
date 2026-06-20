# 04 · Docker 容器化

> Docker 是容器化的事实标准。学会 Docker，你就掌握了现代化应用打包和分发的核心技能。
> 这个模块是后续 Kubernetes 学习的基础，务必熟练掌握。

---

## 🎯 学习目标

完成本模块后，你应该能够：

- [ ] 理解容器和虚拟机的区别（为什么容器更轻量）
- [ ] 熟练使用 Docker 基础命令（run/exec/ps/logs/rm）
- [ ] 编写高质量 Dockerfile（多阶段构建、缓存优化、安全最佳实践）
- [ ] 使用 Docker Compose 编排多容器应用
- [ ] 理解 Docker 网络（bridge/host/none/overlay）
- [ ] 掌握 Docker 数据卷（volume/bind mount/tmpfs）
- [ ] 操作 Docker 镜像仓库（tag/push/pull/save/load）
- [ ] 配置 Docker Daemon（镜像加速、日志限制、存储驱动）
- [ ] 排查常见故障（容器起不来、磁盘爆满、网络不通）
- [ ] 理解 Docker 安全（非 root 运行、镜像扫描、seccomp/AppArmor）
- [ ] 会使用 docker scan 扫描镜像漏洞
- [ ] 了解 containerd / Podman 等 Docker 替代方案

**学完这个模块，你能独立容器化任何应用。**

---

## 📺 推荐视频教程

| 教程 | 讲师 | 链接 | 播放量 | 推荐度 |
|------|------|------|--------|---------|
| Docker 基础教程 | 尚硅谷 | [B站 BV1Sv411r7vd](https://www.bilibili.com/video/BV1Sv411r7vd) | 80万+ | ⭐⭐⭐⭐⭐ |
| Docker 实战 | 黑马程序员 | [B站 BV1xK4y1w7Vs](https://www.bilibili.com/video/BV1xK4y1w7Vs) | 40万+ | ⭐⭐⭐⭐ |
| Dockerfile 最佳实践 | 狂神 | [B站 BV1gJ411p7tT](https://www.bilibili.com/video/BV1gJ411p7tT) | 150万+ | ⭐⭐⭐⭐⭐ |
| Docker Compose 实战 | 阳阳羊 | [B站](https://www.bilibili.com/video/BV1Sb4y1p7SET) | 8万+ | ⭐⭐⭐⭐ |
| 容器技术深入 | 阿里云 | [B站](https://www.bilibili.com/video/BV1F44y1m7LL) | 15万+ | ⭐⭐⭐⭐ |

**学习顺序建议**：先看完「尚硅谷」打基础，再跟「狂神」学 Dockerfile，最后用「Docker Compose」学多容器编排。

---

## 📖 推荐书籍

| 书名 | 作者 | 适合阶段 | 一句话评价 |
|------|------|---------|-------------|
| 《Docker 深入浅出》 | Nigel Poulton | 中级 | 最好的 Docker 入门书，薄而精 |
| 《Docker 实战（第2版）》 | Jeff Nickoloff | 中级 | 实战向，有完整项目示例 |
| 《Docker 进阶与实战》 | 华为云 | 高级 | 国内团队出品，生产经验丰富 |
| 《Docker 安全》 | Adrian Mouat | 高级 | 容器安全专题，必读 |
| 《Container Security》 | Liz Rice | 专家 | 容器安全原理深度解析 |

---

## 🌐 在线参考资源

| 资源 | 链接 | 特点 |
|------|------|------|
| Docker 官方文档 | https://docs.docker.com/ | 最权威，必看 |
| Docker 官方最佳实践 | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ | Dockerfile 编写规范 |
| docker/library | https://github.com/docker-library/official-images | 官方镜像源码 |
| Awesome Docker | https://github.com/veggiemonk/awesome-docker | ⭐12k，精选资源合集 |
| Docker Cheat Sheet | https://dockercheatsheet.com/ | 快速查阅命令 |
| Play with Docker | https://labs.play-with-docker.com/ | 在线实验平台 |
| hadolint | https://github.com/hadolint/hadolint | Dockerfile Linter |
| trivy | https://github.com/aquasecurity/trivy | 镜像漏洞扫描工具 |

---

## 📝 核心知识点清单

### 第一阶段：Docker 基础和命令（1周）

#### 容器 vs 虚拟机
```
虚拟机：Hypervisor → Guest OS → App  (重量级，GB 级)
容器：  Docker Engine → Container → App  (轻量级，MB 级)
```
- 容器共享宿主机内核，隔离通过 Namespace + Cgroups 实现
- 启动快（秒级 vs 分钟级），资源占用少

#### Docker 基础命令
```bash
# 镜像操作
docker pull nginx:1.25                 # 拉取镜像
docker images                              # 查看本地镜像
docker rmi nginx:1.25                    # 删除镜像
docker tag myapp:v1 myapp:v1.0          # 打标签
docker push myregistry.com/myapp:v1        # 推送到仓库
docker save myapp:v1 -o myapp.tar        # 导出镜像
docker load -i myapp.tar                 # 导入镜像

# 容器操作
docker run -d --name web -p 8080:80 nginx:1.25   # 启动容器
docker ps                                     # 查看运行中的容器
docker ps -a                                  # 查看所有容器
docker exec -it web /bin/bash                 # 进入容器
docker logs web                                # 查看日志
docker logs -f --tail=100 web                 # 实时查看最后100行日志
docker stop web                                # 停止容器
docker start web                               # 启动已停止的容器
docker restart web                             # 重启容器
docker rm -f web                              # 强制删除容器
docker inspect web                             # 查看容器详情
docker stats web                               # 查看资源占用

# 清理
docker system df                               # 查看磁盘占用
docker system prune -a                         # 清理所有未使用资源（慎重！）
```

### 第二阶段：Dockerfile 编写（1-2周）

#### Dockerfile 核心指令
```dockerfile
# 1. FROM — 指定基础镜像（必须在第一行，除了 ARG）
FROM node:18-alpine

# 2. WORKDIR — 设置工作目录（会自动创建）
WORKDIR /app

# 3. COPY vs ADD
COPY package*.json ./       # 推荐：简单复制
ADD https://example.com/file.tar.gz /     # 慎用：会自动解压 URL

# 4. RUN — 构建时执行命令
RUN npm install
RUN apk add --no-cache python3

# 5. ENV — 环境变量
ENV NODE_ENV=production \
    PORT=3000

# 6. EXPOSE — 声明端口（文档作用，实际映射靠 -p）
EXPOSE 3000

# 7. CMD vs ENTRYPOINT
CMD ["node", "app.js"]              # 可被 docker run 覆盖
ENTRYPOINT ["node", "app.js"]     # 不可被覆盖，但可追加参数

# 8. USER — 非 root 运行（安全最佳实践）
RUN addgroup -S app && adduser -S app -G app
USER app

# 9. HEALTHCHECK — 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# 10. .dockerignore — 排除不需要的文件
node_modules
*.log
.git
.DS_Store
```

#### 多阶段构建（Multi-stage Build）— 减小镜像体积
```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
**效果**：构建产物只包含 Nginx + 静态文件，镜像从 1GB+ 降到 20MB。

#### 缓存优化技巧
```dockerfile
# ❌ 错误：每次代码改动都会重新 npm install
COPY . .
RUN npm install

# ✅ 正确：利用缓存，只有 package.json 变化才重新安装
COPY package*.json ./
RUN npm install
COPY . .
```

### 第三阶段：Docker Compose 多容器编排（1周）

#### docker-compose.yml 示例
```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src       # 开发时热重载
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://db:5432/mydb
    depends_on:
      - db
      - redis
    networks:
      - app-net

  db:
    image: postgres:15-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    networks:
      - app-net

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - app-net

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
    networks:
      - app-net

volumes:
  db-data:
  redis-data:

networks:
  app-net:
    driver: bridge
```

#### Compose 常用命令
```bash
docker-compose up -d                # 后台启动所有服务
docker-compose ps                     # 查看服务状态
docker-compose logs -f web           # 查看指定服务日志
docker-compose exec web /bin/bash    # 进入容器
docker-compose down                   # 停止并删除所有容器/网络
docker-compose down -v               # 同时删除数据卷（慎用！）
docker-compose pull                   # 拉取最新镜像
docker-compose build                  # 重新构建
```

---

## 🔧 实战：从零容器化一个 Node.js 应用

### 项目结构
```
myapp/
├── Dockerfile
├── docker-compose.yml
├── package.json
├── app.js
└── .dockerignore
```

### app.js
```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Docker!');
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

RUN addgroup -S nodejs && adduser -S nodejs -G nodejs
USER nodejs

HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})" || exit 1

EXPOSE 3000
CMD ["node", "app.js"]
```

### 构建和运行
```bash
# 构建镜像
docker build -t myapp:v1 .

# 运行容器
docker run -d --name myapp -p 3000:3000 myapp:v1

# 查看日志
docker logs -f myapp

# 查看健康状态
docker inspect myapp | grep -A 10 Health

# 浏览器访问 localhost:3000
```

---

## 🚨 常见故障排查手册

### 容器起不来（Exited immediately）

```bash
# 1. 查看退出码和日志
docker logs <container-name>

# 常见退出原因：
# - 应用配置错误（端口被占、配置文件缺失）
# - 权限问题（非 root 用户访问 root 文件）
# - 依赖缺失（容器内没装所需软件）

# 2. 交互式调试（覆盖 entrypoint）
docker run -it --entrypoint /bin/sh myimage:tag
# 然后手动运行命令，看哪里报错
```

### 磁盘爆满（No space left on device）

```bash
# 1. 查看磁盘占用
docker system df

# 2. 清理未使用资源
docker system prune          # 删除停止的容器、未使用的网络、悬挂镜像
docker system prune -a      # 删除所有未使用的镜像（不仅仅是悬挂镜像）
docker volume prune         # 删除未使用的数据卷

# 3. 查看哪个容器占用最多空间
docker ps -s

# 4. 限制容器日志大小（在 daemon.json 或 docker-compose 中配置）
# daemon.json:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 网络不通（容器无法访问外网 / 容器之间无法通信）

```bash
# 1. 检查 Docker 网络
docker network ls
docker network inspect bridge

# 2. 进入容器测试网络
docker exec -it <container> ping 8.8.8.8
docker exec -it <container> nslookup google.com

# 3. 检查宿主机防火墙
sudo iptables -L -n | grep DOCKER

# 4. 重启 Docker daemon
sudo systemctl restart docker
```

---

## 🏭 生产环境最佳实践

### 1. 使用非 root 用户运行容器
```dockerfile
FROM node:18-alpine

RUN addgroup -S app && adduser -S app -G app

WORKDIR /app
COPY --chown=app:app . .

USER app

CMD ["node", "app.js"]
```

### 2. 镜像漏洞扫描
```bash
# 使用 docker scan（需要 Docker Hub 账号）
docker scan myapp:v1

# 或者使用 trivy
trivy image myapp:v1
```

### 3. 限制容器资源
```bash
docker run -d \
  --name web \
  --memory="512m" \              # 内存上限
  --cpus="1.5" \                 # CPU 上限（1.5 个核心）
  --pids-limit=100 \              # 进程数上限
  myapp:v1
```

### 4. 配置 Docker Daemon 镜像加速（国内必配）
```json
// /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```
重启：`sudo systemctl restart docker`

### 5. 使用多阶段构建减小镜像体积
（见上文「多阶段构建」章节）

---

## 🌿 进阶：Docker 替代方案

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| **containerd** | K8s 默认运行时，更轻量 | 生产环境 K8s 集群 |
| **Podman** | 无 daemon，非 root 运行，兼容 Docker CLI | 安全敏感环境 |
| **Buildah** | 构建容器镜像，无 daemon | CI/CD 流水线 |
| **Kaniko** | 在无 Docker daemon 环境中构建镜像 | K8s 集群内构建 |

**趋势**：K8s 已弃用 Docker Shim，生产环境建议使用 containerd。

---

## ✅ 自测清单

学完之后，试试能不能回答这些问题：

- [ ] 容器和虚拟机的核心区别是什么？
- [ ] COPY 和 ADD 指令有什么区别？
- [ ] CMD 和 ENTRYPOINT 有什么区别？
- [ ] 多阶段构建的好处是什么？如何编写？
- [ ] Docker 的四种网络模式（bridge/host/none/overlay）分别适用于什么场景？
- [ ] volume 和 bind mount 有什么区别？
- [ ] 如何减小 Docker 镜像的体积？
- [ ] 如何排查容器起不来的问题？
- [ ] 生产环境中运行容器需要注意哪些安全问题？
- [ ] Docker Compose 和 Kubernetes 的关系是什么？

---

> 学完这个模块，你已经掌握了容器化的核心技能。
> 下一步推荐：[05_Kubernetes](./05_Kubernetes/) — 学会容器编排，让容器在生产环境中自动化运行。
