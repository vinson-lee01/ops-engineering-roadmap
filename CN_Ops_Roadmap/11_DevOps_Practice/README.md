# 11 · DevOps 实战经验

> 这个模块是把前面学的所有知识串联起来，用真实项目练手。
> 光看不练假把式——这里有大大小小的实战项目，跟着做一遍，你就有生产经验了。

---

## 🎯 学习目标

完成本模块后，你应该能够：

- [ ] 从零搭建一套完整的 CI/CD 流水线
- [ ] 部署一个高可用的 Web 应用（Nginx + App + Redis + MySQL）
- [ ] 配置生产级监控告警（Prometheus + Grafana + Alertmanager）
- [ ] 会用 Terraform 在云上创建基础设施
- [ ] 能带新人：把运维知识系统化输出
- [ ] 有可以写进简历的实战项目

**这个模块学完，你就可以投简历了。**

---

## 🔧 实战项目清单

### 项目一：部署一个高可用 Web 应用（2-3 天）

#### 架构图
```
                    ┌─────────────────┐
                    │   DNS (域名)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Nginx (LB)     │  × 2 (主备)
                    │  keepalived      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │  Web-01    │ │  Web-02    │ │  Web-03    │
        │  (Nginx)   │ │  (Nginx)   │ │  (Nginx)   │
        └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │   Redis    │ │   Redis    │ │   Redis    │
        │  (主从)    │ │  (主从)    │ │  (主从)    │
        └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │   MySQL    │ │   MySQL    │ │   MySQL    │
        │  (主从)    │ │  (主从)    │ │  (主从)    │
        └────────────┘ └────────────┘ └────────────┘
```

#### 详细步骤

**Step 1：准备服务器（5 台）**
```
Web-01: 2C4G  →  Nginx + App
Web-02: 2C4G  →  Nginx + App
Web-03: 2C4G  →  Nginx + App
Redis:  2C4G  →  Redis (主) + Redis (从)
MySQL:  4C8G  →  MySQL (主) + MySQL (从)
```

**Step 2：部署 Nginx + Keepalived（高可用负载均衡）**
```bash
# 在两台 Nginx 服务器上安装
apt update && apt install -y nginx keepalived

# 配置 Keepalived (主)
# /etc/keepalived/keepalived.conf
global_defs {
   router_id nginx-01
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.1.100/24    # VIP (虚拟 IP)
    }
}

# 配置 Keepalived (备)
# 只需要改：state BACKUP, priority 50

# 启动
systemctl start keepalived
systemctl enable keepalived

# 测试：关闭主节点，VIP 是否漂移到备节点
ip addr show eth0   # 查看是否拿到 VIP
```

**Step 3：部署 Web 应用（3 台）**
```bash
# 安装 Node.js
curl -sL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 部署应用
git clone https://github.com/yourname/web-app.git /app
cd /app && npm install && npm start &

# 配置 Nginx 反向代理（3 台 Web 都配）
# /etc/nginx/conf.d/app.conf
upstream backend {
    server 192.168.1.101:3000;
    server 192.168.1.102:3000;
    server 192.168.1.103:3000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Step 4：部署 Redis（主从）**
```bash
# 主节点
apt install -y redis-server
# /etc/redis/redis.conf
bind 0.0.0.0
requirepass mypassword
appendonly yes

# 从节点
apt install -y redis-server
# /etc/redis/redis.conf
replicaof 192.168.1.201 6379
masterauth mypassword
```

**Step 5：部署 MySQL（主从）**
```bash
# 主节点
apt install -y mysql-server
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
bind-address = 0.0.0.0
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = mydb

# 创建复制用户
mysql -u root -p
CREATE USER 'repl'@'%' IDENTIFIED BY 'replpassword';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;   # 记录 File 和 Position

# 从节点
apt install -y mysql-server
mysql -u root -p
CHANGE MASTER TO
  MASTER_HOST='192.168.1.202',
  MASTER_USER='repl',
  MASTER_PASSWORD='replpassword',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154;
START SLAVE;
SHOW SLAVE STATUS\G   # 检查 Slave_IO_Running 和 Slave_SQL_Running 是否为 Yes
```

**Step 6：配置监控（Prometheus + Grafana）**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'nginx'
    static_configs:
      - targets: ['192.168.1.101:9113', '192.168.1.102:9113']

  - job_name: 'node'
    static_configs:
      - targets: ['192.168.1.101:9100', '192.168.1.102:9100']

  - job_name: 'mysql'
    static_configs:
      - targets: ['192.168.1.202:9104']

  - job_name: 'redis'
    static_configs:
      - targets: ['192.168.1.201:9121']
```

---

### 项目二：用 Terraform 在云上创建基础设施（1 天）

#### 架构
```
Terraform → 腾讯云 API → 自动创建：
  - VPC + 子网
  - 安全组（防火墙规则）
  - 3 台 CVM（Kubernetes 节点）
  - CLB（负载均衡器）
  - CVM（云数据库）
```

#### 详细步骤

**Step 1：安装 Terraform**
```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
mv terraform /usr/local/bin/
terraform version
```

**Step 2：编写 Terraform 配置**
```hcl
# main.tf
terraform {
  required_providers {
    tencentcloud = {
      version = "~> 1.81"
    }
  }
}

provider "tencentcloud" {
  secret_id  = var.secret_id
  secret_key = var.secret_key
  region     = "ap-guangzhou"
}

# VPC
resource "tencentcloud_vpc" "main" {
  name       = "ops-vpc"
  cidr_block = "10.0.0.0/16"
}

# 子网
resource "tencentcloud_subnet" "public" {
  vpc_id            = tencentcloud_vpc.main.id
  name               = "public-subnet"
  cidr_block         = "10.0.1.0/24"
  availability_zone = "ap-guangzhou-3"
}

# 安全组
resource "tencentcloud_security_group" "web" {
  name        = "web-sg"
  description = "Allow HTTP/HTTPS/SSH"
}

resource "tencentcloud_security_group_rule" "web_80" {
  security_group_id = tencentcloud_security_group.web.id
  type              = "ingress"
  protocol          = "tcp"
  port_range        = "80"
  cidr_ip           = "0.0.0.0/0"
}

# CVM（K8s 节点）
resource "tencentcloud_instance" "k8s_nodes" {
  count             = 3
  instance_name     = "k8s-node-${count.index + 1}"
  image_id          = "img-xxx"   # CentOS 7.9 镜像 ID
  instance_type     = "S5.MEDIUM4"   # 4C8G
  availability_zone = "ap-guangzhou-3"
  subnet_id         = tencentcloud_subnet.public.id
  security_groups   = [tencentcloud_security_group.web.id]

  # 自动安装 Docker 和 K8s
  user_data = <<-EOF
    #!/bin/bash
    yum install -y docker kubeadm kubelet kubectl
    systemctl enable docker kubelet
    systemctl start docker kubelet
  EOF
}
```

**Step 3：执行 Terraform**
```bash
terraform init        # 初始化（下载 provider 插件）
terraform plan         # 预览要创建的资源
terraform apply       # 确认后创建（输入 yes）
terraform destroy     # 用完后销毁（避免扣费）
```

---

### 项目三：用 Ansible 批量配置服务器（1 天）

#### 场景
```
有 10 台服务器需要：
  1. 安装 Docker
  2. 配置 Docker 镜像加速
  3. 部署 Nginx
  4. 配置 SSH 安全（禁用密码登录、改端口）
```

#### 详细步骤

**Step 1：安装 Ansible**
```bash
apt update && apt install -y ansible
ansible --version
```

**Step 2：配置 Inventory**
```ini
# /etc/ansible/hosts
[web]
192.168.1.101
192.168.1.102
192.168.1.103

[redis]
192.168.1.201

[mysql]
192.168.1.202

[all:vars]
ansible_user=root
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

**Step 3：编写 Playbook**
```yaml
# install_docker.yml
- name: Install Docker on all hosts
  hosts: all
  become: yes
  tasks:
    - name: Install dependencies
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - software-properties-common
        state: present

    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker repository
      apt_repository:
        repo: deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable
        state: present

    - name: Install Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
        state: latest

    - name: Start Docker
      service:
        name: docker
        state: started
        enabled: yes

    - name: Configure Docker mirror (Tencent Cloud)
      copy:
        content: |
          {
            "registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
          }
        dest: /etc/docker/daemon.json
      notify: Restart Docker

  handlers:
    - name: Restart Docker
      service:
        name: docker
        state: restarted
```

**Step 4：执行 Playbook**
```bash
ansible-playbook -i /etc/ansible/hosts install_docker.yml
```

---

## 🚨 故障排查案例库

### 案例一：Nginx 返回 502 Bad Gateway

**现象**：访问网站返回 502

**排查流程**：
```bash
# 1. 检查 Nginx 错误日志
tail -f /var/log/nginx/error.log
# 常见错误：connect() failed (111: Connection refused) → 后端服务没启动

# 2. 检查后端服务是否运行
systemctl status myapp
ps aux | grep myapp

# 3. 检查端口是否在监听
ss -tlnp | grep :3000

# 4. 检查防火墙
iptables -L -n | grep 3000

# 5. 检查 Nginx 配置
nginx -t
```

**根因**：后端 App 崩溃了

**解决**：重启 App + 配置 systemd 自动重启
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/usr/bin/node /app/app.js
Restart=always
RestartSec=10
User=app

[Install]
WantedBy=multi-user.target
```

---

### 案例二：Redis 主从切换后数据不一致

**现象**：主节点宕机，从节点提升为主，但有数据丢失

**根因**：Redis 主从是异步复制，主节点写入后立刻宕机，未同步的数据会丢失

**解决**：配置 `min-replicas-to-write`
```conf
# redis.conf (主节点)
min-replicas-to-write 1    # 至少 1 个从节点同步成功才返回成功
min-replicas-max-lag 10     # 从节点延迟不超过 10 秒
```

**更好方案**：使用 Redis Sentinel（自动故障转移 + 数据保护）
```bash
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
```

---

### 案例三：MySQL 主从延迟变大

**现象**：`SHOW SLAVE STATUS\G` 显示 `Seconds_Behind_Master` 越来越大

**排查**：
```sql
-- 在主节点查看正在执行的 SQL
SHOW PROCESSLIST;

-- 在从节点查看延迟原因
SELECT * FROM performance_schema.replication_applier_status_by_worker;
```

**常见原因**：
1. 主节点写入压力大（从节点单线程回放跟不上）
   - **解决**：启用多线程回放（`slave_parallel_workers = 8`）
2. 从节点硬件差（CPU/磁盘 IO 差）
   - **解决**：升级从节点硬件
3. 大事务（比如 `DELETE FROM table` 删 100 万行）
   - **解决**：分批删除（`LIMIT 1000` 循环）

---

## 🏭 生产环境最佳实践清单

### 部署
- [ ] 所有部署通过 CI/CD，禁止手动登录服务器
- [ ] 使用蓝绿 / 金丝雀发布，避免全量宕机
- [ ] 每次部署前自动备份（数据库 / 配置文件）
- [ ] 部署后自动 smoke test（检查核心功能）

### 监控
- [ ] 所有服务都有健康检查端点（`/health`）
- [ ] 关键指标配置告警（CPU > 80%、内存 > 90%、磁盘 > 85%）
- [ ] 告警分级（P0 立即打电话、P1 发 Slack、P2 每天摘要）
- [ ] 定期演练（模拟故障，验证告警是否及时）

### 安全
- [ ] 所有服务器禁用密码登录，只用 SSH Key
- [ ] 数据库不允许公网访问，只通过内网
- [ ] 定期漏洞扫描（Nessus / OpenVAS）
- [ ] 所有生产操作有审计日志（谁在什么时候做了什么）

### 备份
- [ ] 数据库每天全量备份 + 每小时增量备份
- [ ] 备份文件加密存储（防止泄露）
- [ ] 每月演练恢复（备份不等于能恢复！）
- [ ] 关键配置版本化（Git + 定期快照）

---

## ✅ 自测：你有生产经验了吗？

- [ ] 能独立从零搭建一套高可用架构（负载均衡 + 数据库主从 + 缓存）
- [ ] 能排查线上故障（网络不通 / 服务崩溃 / 数据库慢查询）
- [ ] 能设计 CI/CD 流水线（构建 → 测试 → 部署 → 验证）
- [ ] 能配置监控告警（Prometheus + Grafana + Alertmanager）
- [ ] 能写 Terraform / Ansible 自动化基础设施
- [ ] 能带新人（把知识系统化输出）

**如果以上 6 条你能做到 4 条，你就是中级 DevOps 工程师了。**
**如果 6 条全能做到，你就是高级 DevOps 工程师，可以投阿里 / 腾讯了。**

---

> 这个模块的项目都做一遍，你的简历就有东西写了。
> 面试官问：「你有生产经验吗？」你可以说：「我独立完成过 XXX 项目，实现了 XXX。」
> 下一步：去考个 CKA 认证，然后把认证写在简历上。
