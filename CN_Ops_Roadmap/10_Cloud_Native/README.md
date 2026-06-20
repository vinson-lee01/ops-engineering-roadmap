# 10 · 云原生实践

> 云原生不只是"上云"，是一套架构思想和工程实践。
> 这个模块涵盖国内主流云厂商实战、Terraform、Ansible、Service Mesh、等保合规与基线核查。

---

## 🎯 学习目标

完成本模块后，你应该能够：

- [ ] 理解云原生的核心理念（容器、微服务、DevOps、持续交付）
- [ ] 熟练使用阿里云/腾讯云核心产品（ECS、SLB、RDS、OSS）
- [ ] 用 Terraform 管理云基础设施（IaC）
- [ ] 用 Ansible 做配置管理和应用部署
- [ ] 理解并部署 Service Mesh（Istio）
- [ ] 配置多集群管理（Rancher / KubeFed）
- [ ] 了解 FinOps（云成本优化）
- [ ] **掌握等保2.0合规要点和基线扫描方法**
- [ ] **了解国产化替代方案（OceanBase / TiDB / OpenGauss）**
- [ ] 能设计符合国内合规要求的云架构方案

---

## 第一部分：国内主流云产品实战

### 云产品对照表

| 产品类型 | 阿里云 | 腾讯云 | 华为云 | AWS | 适用场景 |
|-----------|--------|--------|--------|-----|---------|
| 云服务器 | ECS | CVM | ECS | EC2 | 计算资源 |
| 对象存储 | OSS | COS | OBS | S3 | 静态文件 / 备份 |
| 关系型数据库 | RDS MySQL | TencentDB | RDS GaussDB | RDS MySQL | 业务数据 |
| 负载均衡 | SLB | CLB | ELB | ALB | 流量分发 |
| 容器服务 | ACK | TKE | CCE | EKS | K8s 托管 |
| 函数计算 | FC | SCF | FunctionGraph | Lambda | Serverless |
| 专有云 | Apsara Stack | TStack | HCS | Outposts | 私有化部署 |
| 政务云 | 政务云 | 政务云 | 华为政务云 | GovCloud | 政府 / 国企 |

### 阿里云 ECS 实战：从购买到生产就绪

```bash
# 1. 创建 ECS 实例（通过 CLI 或控制台）
# 关键选型参数：
#   实例规格：ecs.c6.large（2C4G）适合中小 Web 服务
#   镜像：CentOS 7.9 / Alibaba Cloud Linux 3（推荐，阿里优化过内核）
#   存储：系统盘 SSD 40GB + 数据盘 ESSD PL1 100GB
#   网络：VPC + 交换机 + 安全组

# 2. 登录后的初始化脚本（必须执行）
# 更新系统
yum update -y

# 安装基础工具
yum install -y vim wget curl net-tools telnet git htop jq lsof strace tcpdump

# 时区设置
timedatectl set-timezone Asia/Shanghai

# 内核参数调优（生产环境必须）
cat >> /etc/sysctl.conf << 'EOF'
# 网络调优
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
# 文件描述符
fs.file-max = 1048576
EOF
sysctl -p

# 文件描述符限制
cat >> /etc/security/limits.conf << 'EOF'
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535
EOF

# 3. 安全加固（基线要求）
# 禁用 root 远程登录
sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
# 修改默认 SSH 端口（建议）
sed -i 's/#Port 22/Port 22022/' /etc/ssh/sshd_config
systemctl restart sshd

# 4. 安装 Docker
yum install -y yum-utils
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": ["https://registry.cn-hangzhou.aliyuncs.com"],
  "log-driver": "json-file",
  "log-opts": {"max-size": "100m", "max-file": "3"},
  "storage-driver": "overlay2",
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
systemctl enable --now docker
```

### 腾讯云实战差异点

腾讯云和阿里云在以下方面有明显差异，切换时注意：

| 差异项 | 阿里云 | 腾讯云 |
|--------|--------|--------|
| 内网域名 | `.internal` 结尾 | 不支持内网 DNS 解析 |
| 安全组规则 | 支持 IP 组引用 | 仅支持 CIDR |
| RDS 备份 | 自动备份免费（7天） | 基础备份收费 |
| COS SDK | `cos-sdk-python-v5` | 同 |
| K8s 版本 | ACK 支持到 1.30+ | TKE 通常滞后 1-2 个小版本 |
| 监控集成 | CloudMonitor 默认集成 | 需要单独安装 agent |

### 多云架构设计思路

国内企业常见场景：**主用阿里云 + 腾讯云灾备**

```
                    ┌─────────────────┐
                    │   用户请求       │
                    └───────┬─────────┘
                            │
                   ┌────────▼────────┐
                   │  DNS 智能解析     │
                   │  （阿里 DNS）     │
                   └───────┬────────┘
                           │
              ┌────────────┼────────────┐
              │                         │
    ┌─────────▼──────┐      ┌───────────▼────────┐
    │   阿里云主集群    │      │   腾讯云灾备集群     │
    │   · ECS × N     │      │   · CVM × N/2      │
    │   · RDS 主从    │      │   · TencentDB 只读  │
    │   · OSS 存储桶   │◄────►│   · COS 数据同步    │
    │   · SLB 负载    │      │   · CLB 待命         │
    └────────────────┘      └────────────────────┘
```

关键实现：
- **数据同步**：RDS 通过 DTS（Data Transmission Service）做实时同步
- **静态文件**：OSS ↔ COS 通过跨区域复制或自定义同步任务
- **流量切换**：DNS 切换 TTL 设为 60s，故障时手动/自动切流

---

## 第二部分：Terraform IaC 实战

### Terraform 管理阿里云基础设施

```hcl
# ====== 生产环境 VPC 架构 ======

# VPC（172.16.0.0/16）
resource "aliyun_vpc" "prod" {
  vpc_name   = "prod-vpc"
  cidr_block = "172.16.0.0/16"
}

# 交换机划分
resource "aliyun_vswitch" "web" {
  vpc_id       = aliyun_vpc.prod.id
  cidr_block   = "172.16.1.0/24"
  zone_id      = data.aliyun_zones.default.zones[0].id
}

resource "aliyun_vswitch" "app" {
  vpc_id       = aliyun_vpc.prod.id
  cidr_block   = "172.16.2.0/24"
  zone_id      = data.aliyun_zones.default.zones[0].id
}

resource "aliyun_vswitch" "db" {
  vpc_id       = aliyun_vpc.prod.id
  cidr_block   =172.16.10.0/24
  zone_id      = data.aliyun_zones.default.zones[0].id
}

# NAT 网关（ECS 出外网用）
resource "aliyun_nat_gateway" "prod" {
  vpc_id          = aliyun_vpc.prod.id
  nat_gateway_name = "prod-nat"
  specification   = "Small"
  # 绑定 EIP
  allocation_ids  = [aliyun_eip_nat.id]
}

# EIP
resource "alicloud_eip" "nat" {
  bandwidth            = "10"
  internet_charge_type = "PayByBandwidth"
}

# 安全组 — 最小权限原则
resource "aliyun_security_group" "web_sg" {
  name   = "web-servers"
  vpc_id = aliyun_vpc.prod.id
  # 仅允许入站 HTTP/HTTPS
  ingress = [
    { protocol = "tcp", port_range = "80/80", priority = 1, cidr_ip = "0.0.0.0/0", policy = "accept" },
    { protocol = "tcp", port_range = "443/443", priority = 2, cidr_ip = "0.0.0.0/0", policy = "accept" }
  ]
  # 出站全部允许
  egress = [
    { protocol = "all", port_range = "-1/-1", priority = 1, cidr_ip = "0.0.0.0/0", policy = "accept" }
  ]
}

# ECS 实例
resource "aliyun_instance" "web_01" {
  instance_name        = "web-01"
  image_id             = "ubuntu_22_04_x64_20G_alibase_20230601.vhd"
  instance_type        = "ecs.c6.xlarge"
  security_groups      = [aliyun_security_group.web_sg.id]
  vswitch_id           = aliyun_vswitch.web.id
  system_disk_category = "cloud_essd"

  user_data = base64encode(<<EOF
#!/bin/bash
# 自动安装 Docker 和基础工具
apt-get update && apt-get install -y docker.io curl
systemctl enable --now docker
EOF
)

  tags = {
    Name      = "web-01"
    Env       = "prod"
    ManagedBy = "terraform"
  }
}

# SLB（应用型负载均衡 ALB）
resource "alb_load_balancer" "frontend" {
  vpc_id           = aliyun_vpc.prod.id
  address_type     = "Intranet"
  load_balancer_name = "alb-frontend"
}

resource "alb_server_group" "web_pool" {
  load_balancer_id = alb_load_balancer.frontend.id
  # 关联后端 ECS...
}
```

### State 管理最佳实践

**千万不要把 `.tfstate` 提交到 Git！**

```hcl
# 方案一：OSS 后端（推荐阿里云用户）
terraform {
  backend "oss" {
    bucket   = "your-tf-state-bucket"
    key      = "prod/terraform.tfstate"
    endpoint = "oss-cn-hangzhou.aliyuncs.com"
    acl      = "private"

    # 加密存储
    encrypt = true
  }
}

# 方案二：远程 state 锁定（团队协作必开）
# 用 DynamoDB（AWS）或 TableStore（阿里云）做状态锁定
# 防止两人同时 apply 冲突
```

### Workspace 管理多环境

```bash
# 创建环境
terraform workspace new prod
terraform workspace new staging
terraform workspace new dev

# 每个 workspace 使用不同的变量文件
# variables.tfvars.prod  — 生产环境配置
# variables.tfvars.staging — 测试环境配置

terraform plan -var-file="variables.tfvars.prod"
terraform apply -var-file="variables.tfvars.prod"
```

---

## 第三部分：Ansible 配置管理

### Ansible Playbook — 批量基线加固

这是国内运维最常见的场景之一：**批量对服务器做等保合规加固**

```yaml
# === basline_hardening.yml ===
# 等保2.0 基线加固 Playbook
# 适用场景：新购入的 ECS/CVM 需要统一做安全加固

- name: Security Baseline Hardening (等保2.0 基线)
  hosts: all
  become: yes
  tasks:

  # ---- 账号安全 ----
  - name: Remove unused accounts
    user:
      name: "{{ item }}"
      state: absent
    loop:
      - games
      - ftp
      - operator

  - name: Set password policy
    lineinfile:
      path: /etc/security/pwquality.conf
      regexp: "^minlen"
      line: "minlen = 12"
      create: yes

  # ---- SSH 加固 ----
  - name: Disable root SSH login
    lineinfile:
      path: /etc/ssh/sshd_config
      regexp: "^PermitRootLogin"
      line: "PermitRootLogin no"
    notify: Restart SSH

  - name: Set max auth tries
    lineinfile:
      path: /etc/ssh/sshd_config
      regexp: "^MaxAuthTries"
      line: "MaxAuthTries 3"
    notify: Restart SSH

  # ---- 权限控制 ----
  - name: Set umask 027
    lineinfile:
      path: /etc/profile
      regexp: "^umask"
      line: "umask 027"

  - name: Restrict su to wheel group only
    replace:
      path: /etc/pam.d/su
      regexp: '^#auth.*required.*pam_wheel.so'
      replace: 'auth required pam_wheel.so use_uid'

  # ---- 审计开启 ----
  - name: Enable auditd service
    service:
      name: auditd
      state: started
      enabled: yes

  - name: Configure audit rules for critical files
    blockinfile:
      path: /etc/rules.d/baseline.rules
      create: yes
      block: |
        -w /etc/passwd -p wa -k identity_modification
        -w /etc/shadow -p wa -k identity_modification
        -w /etc/group -p wa -k identity_modification
        -w /etc/sudoers -p wa - privilege_modification
        -w /etc/ssh/sshd_config -p wa -k ssh_config_change
        -w /var/log/audit/ -p rwxa -k audit_log_access

  # ---- 防火墙 ----
  - name: Install firewalld
    yum:
      name: firewalld
      state: present

  - name: Enable firewalld
    service:
      name: firewalld
      state: started
      enabled: yes

  # ---- 日志集中 ----
  - name: Configure rsyslog remote forwarding
    blockinfile:
      path: /etc/rsyslog.d/remote.conf
      create: yes
      block: |
        *.* @{{ log_server_ip }}:514

  handlers:
    - name: Restart SSH
      service:
        name: sshd
        state: restarted
```

---

## 第四部分：等保2.0 合规要点

> **重要背景**：国内企业（尤其是金融、政府、医疗、教育）必须通过等级保护测评。
> 作为运维工程师，你需要知道哪些是系统层面要做的。

### 等保2.0 二级/三级 — 运维相关检查项

| 等级 | 类别 | 检查项 | 运维操作 | 自动化方案 |
|------|------|--------|---------|-----------|
| 二级 | 身份鉴别 | 强密码策略 + 失效处理 | 修改 `/etc/login.defs` | Ansible 批量下发 |
| 二级 | 访问控制 | 最小权限原则 | 收敛 sudo / 文件权限 | Ansible Role |
| 二级 | 安全审计 | 操作日志保留 ≥ 6 个月 | auditd + rsyslog 远传 | ELK / Splunk |
| 三级 | 入侵防范 | 补丁更新 + 漏洞扫描 | 定期 yum update + OpenVAS | OpenSCAP 自动扫描 |
| 三级 | 恶意代码 | 防病毒软件 | 安装 ClamAV / 企业杀软 | YUM 自动更新病毒库 |
| 三级 | 数据完整性 | 备份恢复策略 | 每日全量备份 + 异地 | Cron + Rsync / DTS |
| 三级 | 数据保密性 | 传输加密 + 存储加密 | TLS 1.2+ / LUKS 加密盘 | Certbot 自动续签 |

### 基线扫描实操

国内常用的基线扫描工具：

```bash
# === 方案一：Lynis（开源，推荐）===
# 安装
yum install -y lynis || (cd /opt && git clone https://github.com/CISOFy/Lynis.git)

# 执行扫描
lynis audit system

# 输出报告到 /var/log/lynis-report.dat
# 关注 WARN 和 SUGGEST 级别的问题

# === 方案二：OpenSCAP（红帽体系，CentOS/RHEL 推荐）===
yum install -y openscap-scanner scap-security-guide

# 扫描 CIS CentOS 7 Benchmark
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_stig-rhel7-server-upstream \
  --report scan_report.html \
  /usr/share/xml/scap/ssg-centos7-ds.xml

# 报告在当前目录 scan_report.html

# === 方案三：自行编写基线扫描 Shell 脚本 ===
# 这是最常见的做法——根据等保要求逐项检查：
#!/bin/bash
# baseline_scan.sh — Linux 等保基线快速检查

echo "=== 等保2.0 Linux 基线检查 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

PASS=0; FAIL=0; WARN=0

check() {
  if [ "$1" == "$2" ]; then
    echo "[PASS] $3"
    ((PASS++))
  else
    echo "[FAIL] $3  (期望: $2, 实际: $1)"
    ((FAIL++))
  fi
}

# 1. 密码复杂度
PW_MINLEN=$(grep -E "^minlen" /etc/security/pwquality.conf 2>/dev/null | awk '{print $3}')
check "${PW_MINLEN:-0}" "12" "密码最小长度 >= 12 位"

# 2. Root 远程登录
ROOT_LOGIN=$(grep -E "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
check "$ROOT_LOGIN" "no" "禁止 Root 远程登录"

# 3. 空口令用户
EMPTY_PW=$(awk -F: '$2=="" || $2=="!" || $2=="*"' /etc/shadow | wc -l)
check "$EMPTY_PW" "0" "不存在空口令账号"

# 4. 文件权限 777
WORLD_WRITABLE=$(find / -perm -0002 -type f 2>/dev/null | wc -l)
if [ "$WORLD_WRITABLE" -eq 0 ]; then
  check "0" "0" "无全局可写文件"
else
  echo "[WARN] 发现 $WORLD_WRITABLE 个全局可写文件"
  ((WARN++))
fi

# 5. auditd 运行状态
AUDIT_STATUS=$(systemctl is-active auditd 2>/dev/null)
check "$AUDIT_STATUS" "active" "审计服务 auditd 已启用"

# 6. 防火墙状态
FW_STATUS=$(systemctl is-active firewalld 2>/dev/null)
check "$FW_STATUS" "active" "防火墙已启用"

# 7. SELinux（等保三级要求）
SELINUX=$(getenforce 2>/dev/null)
if [ "$SELINUX" == "Enforcing" ]; then
  check "$SELINUX" "Enforcing" "SELinux 处于强制模式"
elif [ "$SELINUX" == "Disabled" ]; then
  echo "[WARN] SELinux 未启用（等保三级可能扣分）"
  ((WARN++))
fi

# 8. SSH 协议版本
SSH_PROTO=$(grep -E "^Protocol" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
check "${SSH_PROTO:-2}" "2" "SSH 仅使用 Protocol 2"

# 结果汇总
echo ""
echo "=== 检查结果 ==="
echo "PASS: $PASS  |  FAIL: $FAIL  |  WARN: $WARN"
echo ""
if [ $FAIL -gt 0 ]; then
  echo "⚠️  有 $FAIL 项不合规，请处理后重新扫描"
  exit 1
else
  echo "✅ 基本合规（$WARN 项建议关注）"
  exit 0
fi
```

---

## 第五部分：国产化替代方案

### 为什么需要了解国产化？

- **信创政策驱动**：党政军企逐步替换国外技术栈
- **数据主权**：金融、电信等行业要求数据不出境
- **供应链安全**：避免被"卡脖子"
- **实际岗位需求**：越来越多运维岗要求有国产化经验

### 国产技术栈对照

| 领域 | 国际通用 | 国内替代 | 成熟度 | 代表用户 |
|------|---------|---------|-------|---------|
| 操作系统 | CentOS / RHEL | Anolis OS / openEuler / Kylin | 高（阿里/华为/麒麟） | 阿里云默认、华为云、政府 |
| 容器编排 | Kubernetes（上游） | KubeEdge / Kindling | 高（CNCF项目） | 边缘计算场景 |
| 数据库 | MySQL / PostgreSQL | OceanBase / TiDB / OpenGauss / 达梦 | 高 | 支付宝、字节、银行 |
| 中间件 | Redis | Codis / KVStore | 中 | 大厂自研多 |
| 消息队列 | Kafka / RabbitMQ | RocketMQ | 高 | 阿里系、大量互联网公司 |
| API 网关 | Kong / Nginx | Apache APISIX / Soul | 高 | 国内大量使用 |
| 监控 | Prometheus + Grafana | Open-Falcon / Cat（点评） | 中 | 美团早期、部分大厂 |
| 服务网格 | Istio | MOSN / Envoy（参与贡献） | 高 | MOSN 是蚂蚁金服开源 |
| 堡垒机 | JumpServer | JumpServer（本身就是国产）| 高 | 金融行业标配 |

### OceanBase vs TiDB vs OpenGauss

| 维度 | OceanBase（蚂蚁） | TiDB（PingCAP） | OpenGauss（华为） |
|------|-------------------|------------------|-------------------|
| 架构 | 共享 nothing + Paxos | Raft + HTAP | 主备 + LSM-tree |
| 兼容性 | MySQL 协议兼容 | MySQL 协议兼容 | PostgreSQL / Oracle 兼容 |
| 部署形态 | 商业版为主 | 开源社区版可用 | 开源高斯 |
| 优势场景 | 金融交易（强一致） | HTAP 混合负载 | 分析型查询 |
| 学习曲线 | 中等（文档完善） | 低（MySQL 体验） | 中等（PG 生态） |
| 运维工具 | OCP 平台 | TiUP / TiDB Dashboard | OM 平台 |

### 在 K8s 上运行 TiDB 的实战示例

```yaml
# tidb-cluster.yaml — 在 K8s 上部署 TiDB
apiVersion: pingcap.com/v1alpha1
kind: TidbCluster
metadata:
  name: basic
spec:
  version: "v7.5.0"
  timezone: Asia/Shanghai
  pvReclaimPolicy: Retain
  
  pd:
    replicas: 3
    requests:
      cpu: "1"
      memory: "2Gi"
    
  tikv:
    replicas: 3
    requests:
      cpu: "2"
      memory: "4Gi"
    storageClassName: local-storage
    
  tidb:
    replicas: 2
    service:
      type: NodePort
    requests:
      cpu: "2"
      memory: "4Gi"
---
# 暴露给外部访问
apiVersion: v1
kind: Service
metadata:
  name: tidb-service
spec:
  type: LoadBalancer
  ports:
  - port: 4000
    targetPort: 4000
  selector:
    app.kubernetes.io/name: basic
    app.kubernetes.io/component: tidb
```

---

## 第六部分：堡垒机与日志审计

### 堡垒机（JumpServer）

国内等保合规**强制要求**：所有运维操作必须经过堡垒机审计。

```bash
# JumpServer Docker 快速部署（测试环境）
# 生产环境请参考官方文档做高可用部署
docker run -d \
  --name jms_all \
  -p 8080:80 \
  -p 2222:2222 \
  -e SECRET_KEY=aabbccddeeff \
  -e BOOTSTRAP_TOKEN=aabbccddeeff \
  jumpserver/jms_all:v3.7.0

# 访问 http://<你的IP>:8080
# 默认账号: admin / admin
```

JumpServer 核心功能：

| 功能 | 说明 | 等保对应 |
|------|------|---------|
| 集中认证 | LDAP / AD / 飞书对接 | 身份鉴别 |
| 资产管理 | 纳管所有服务器资产清单 | 资产台账 |
| 命令审计 | 记录每一条操作命令 | 安全审计（≥6个月） |
| 会话录像 | 录屏回放，可追溯 | 安全审计 |
| 工单审批 | 临时授权需审批 | 访问控制 |

### 日志审计方案（ELK）

等保要求**操作日志至少保留 6 个月**：

```bash
# Filebeat 配置 — 收集各服务器日志
cat > /etc/filebeat/filebeat.yml << 'EOF'
filebeat.inputs:
- type: log
  paths:
    - /var/log/secure
    - /var/log/messages
    - /var/log/audit/audit.log
  fields:
    env: production
    host_type: ecs
  fields_under_root: true

output.elasticsearch:
  hosts: ["https://es-node1:9200"]
  ssl.certificate_authorities: ["/etc/ca.crt"]
  username: "elastic"
  password: "changeme"
  index: "ops-audit-%{+yyyy.MM}"
EOF
```

---

## 第七部分：FinOps 与成本优化

### 国内云成本常见浪费

| 浪费类型 | 占比估算 | 解决方案 | 年省预估 |
|---------|---------|---------|---------|
| 闲置 ECS | ~25% | 定时巡检释放 | ¥数万~数十万 |
| 未优化的 RDS 规格 | ~20% | VPA + 压测验证真实需求 | ¥数万 |
| OSS 无生命周期策略 | ~15% | 设置自动转低频/归档 | 数千元 |
| SLB / EIP 闲置 | ~10% | 资源标签化管理 | 数千元 |
| 按量转包年/包月 | — | 长期运行的资源转预付费 | 30%~60% |

### 阿里云费用分析命令

```bash
# 通过 Aliyun CLI 查询本月费用
# 安装: pip3 install aliyun-python-sdk-core aliyun-python-sdk-bssopenapi

python3 << 'PYEOF'
from aliyunsdkcore.client import AcsClient
from aliyunsdkbssopenapi.request.v20171214.QueryBillOverviewRequest import QueryBillOverviewRequest

client = AcsClient("<AccessKeyID>", "<AccessKeySecret>", "cn-hangzhou")
req = QueryBillOverviewRequest()
req.set_BillingDate("2026-06-20")
resp = client.do_action_with_exception(req)
print(resp.decode())
PYEOF
```

---

## 🧪 实战项目

### 项目 1：从零搭建符合等保要求的云架构

**目标**：用 Terraform 在阿里云上创建一套通过等保三级预审的架构

**交付物**：
1. VPC 三层隔离（DMZ / APP / DB）
2. 安全组最小权限规则
3. 所有 ECS 通过 JumpServer 管控
4. 操作日志统一收集到 ES（≥ 6 个月）
5. RDS 每日自动备份 + 异地容灾
6. WAF + DDoS 防护

### 项目 2：国产数据库迁移（MySQL → TiDB）

**目标**：将现有 MySQL 业务平滑迁移到 TiDB

**步骤**：
1. 搭建 TiDB Cluster（K8s 上或裸金属）
2. 用 DM（Data Migration）做全量 + 增量同步
3. 双写验证（MySQL 写入同时同步到 TiDB）
4. 读流量逐步切换到 TiDB
5. 验证一致性后停掉 MySQL

---

## 💼 面试高频题

1. **等保二级和三级的区别？**
   - 三级要求更多：入侵防范、恶意代码防范、数据完整性和保密性
   - 三级要求每年做一次测评，二级每两年一次
   - 三级需要专职安全管理员

2. **基线扫描怎么自动化？**
   - Lynis / OpenSCAP 定期跑 + Ansible Playbook 自动修复
   - 扫描结果推送到钉钉/飞书告警
   - 不合规项自动生成整改工单

3. **Terraform 和 Ansible 的分工？**
   - Terraform 管「有什么」（资源创建/销毁）
   - Ansible 管「里面装什么」（软件/配置/应用部署）
   - 两者配合：Terraform 创建 ECS → 输出 IP → Ansible 配置

4. **国产数据库怎么选？**
   - 金融交易类：OceanBase（支付宝验证过的强一致）
   - HTAP 混合负载：TiDB（兼容 MySQL，迁移成本低）
   - Oracle 替代：OpenGauss 或达梦（PG/Oracle 兼容性好）

---

## 🔗 相关资源

- [← 返回中文版首页](../README.md)
- [CN 05 Kubernetes](../05_Kubernetes/)
- [CN 06 CI/CD](../06_CI_CD/)
- [CN 08 监控体系](../08_Monitoring/)
