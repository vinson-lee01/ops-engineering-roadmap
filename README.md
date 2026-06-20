# <div align="center">⚙️ Ops Engineering Roadmap</div>

<div align="center">

**从零到架构师 · 运维 / DevOps / SRE 全栈成长路径**

[![Stars](https://img.shields.io/github/stars/vinson-lee01/ops-engineering-roadmap?style=flat&label=Star)](https://github.com/vinson-lee01/ops-engineering-roadmap/stargazers)
[![Forks](https://img.shields.io/github/forks/vinson-lee01/ops-engineering-roadmap?style=flat&label=Fork)](https://github.com/vinson-lee01/ops-engineering-roadmap/network/members)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green?style=flat&logo=creative-commons&logoColor=white)](https://creativecommons.org/licenses/by-sa/4.0/)
[![中文版](https://img.shields.io/badge/🇨🇳-中文版-blue?style=flat)](#-中文版)
[![English](https://img.shields.io/badge/🌍-English-orange?style=flat)](#-english-version)

</div>

---

## 为什么是这份路线图

大多数运维学习路径的问题是：**列了一堆工具名，但没有告诉你先学哪个、学到什么程度、在实际工作中怎么串起来**。

这份路线图来自国内云厂商 + 互联网大厂的一线实践，按 **「能独立干活 → 能设计架构 → 能带团队定规范」** 三个阶段组织。每个模块标注了**实际工作中会用到的深度**，不是教科书目录。

| 维度 | 现状 |
|------|------|
| 语言 | 中英文独立维护，不是机翻 |
| 内容 | 每个模块 15KB+ 实战笔记 |
| 差异 | 国内版：阿里云/腾讯云/等保/基线 · 海外版：AWS/GCP/SRE Book 体系 |

---

## 学习路径

```
入门期（1-3月）                进阶期（4-9月）               高级期（10-18月）
┌──────────────┐             ┌──────────────────┐          ┌──────────────────────┐
│ Linux 基础   │ ──────────▶ │ Docker / K8s     │ ──────▶ │ 架构设计 / SLO 体系  │
│ Shell 编程   │             │ CI/CD 流水线      │          │ 多云管理 / FinOps    │
│ 网络 & DNS   │             │ Prometheus 监控栈  │         │ 故障治理 / 容量规划  │
│ Nginx 部署   │             │ ELK 日志体系       │          │ Service Mesh 落地    │
└──────────────┘             └──────────────────┘          └──────────────────────┘
```

> 💡 每个阶段末尾都有**可验证的输出**——不是「学了」，而是「能做出什么」。

---

## <div align="center">🇨🇳 中文版</div>

**适用场景**：国内企业运维 · 应届求职 · 国产云环境（阿里云 / 腾讯云 / 华为云）· 等保合规 / 基线核查

| # | 模块 | 核心内容 | 关键产出 |
|---:|------|---------|---------|
| 01 | [Linux 基础](./CN_Ops_Roadmap/01_Linux_Basics/) | 系统管理 · 文件权限 · 进程管理 · 内核参数调优 · systemd | 能独立管理 50+ 台服务器的日常运维 |
| 02 | [Shell 编程](./CN_Ops_Roadmap/02_Shell_Scripting/) | Bash 编程 · awk/sed/grep 文本处理 · crontab 自动化 · 脚本健壮性 | 写出生产级自动化脚本，覆盖日志轮转 / 备份 / 告警 |
| 03 | [网络基础](./CN_Ops_Roadmap/03_Network_Basics/) | TCP/IP 协议栈 · DNS 解析链路 · iptables/firewalld · tcpdump/wireshark 抓包 | 排查网络延迟 / 连接超时 / DNS 劫持类故障 |
| 04 | [Docker 容器](./CN_Ops_Roadmap/04_Container_Docker/) | 镜像构建优化 · Dockerfile 最佳实践 · Compose 编排 · 网络 & 存储驱动 | 从零搭建容器化应用，镜像体积缩减 60%+ |
| 05 | [Nginx 实战](./CN_Ops_Roadmap/05_Web_Server_Nginx/) | 反向代理 · 负载均衡算法 · HTTPS / HTTP2 · 性能调优 · access_log 分析 | 承载万级 QPS 的 Web 接入层 |
| 06 | [MySQL 数据库](./CN_Ops_Roadmap/06_Database_MySQL/) | SQL 调优 · 主从复制 / GTID · 备份策略（逻辑 / 物理）· 慢查询定位 | 设计数据库高可用方案，恢复能力验证通过 |
| 07 | [Kubernetes](./CN_Ops_Readmap/07_Container_Orchestration_K8s/) | 架构原理 · Pod 生命周期 · Deployment / StatefulSet · Service / Ingress · PV & 存储 | 在 K8s 上跑起一套有状态服务（含数据库）|
| 08 | [CI/CD 流水线](./CN_Ops_Roadmap/08_CICD_Jenkins_GitLab/) | Pipeline as Code · GitLab CI / Jenkinsfile · 制品管理 · 安全扫描卡点 | 代码提交到上线全自动化，耗时 < 10 分钟 |
| 09 | [监控体系](./CN_Ops_Roadmap/09_Monitoring_ElasticStack/) | Prometheus + Grafana · 指标设计 · 告警分级 / 抑制 / 静默 · ELK 日志 | 故障发现时间 MTTD < 5 分钟，根因定位有据可查 |
| 10 | [公有云实战](./CN_Ops_Roadmap/10_Cloud_Aliyun_Tencent/) | ECS / SLB / OSS / RDS · 高可用架构设计 · 费用优化 · 等保合规 | 用阿里云 / 腾讯云搭建符合等保三级要求的架构 |
| 11 | [SRE 工程化](./CN_Ops_Roadmap/11_SRE_Principles_Practices/) | SLO / SLI / SLA 定义 · Error Budget · 故障复盘（5 Whys）· 容量规划 | 建立团队可用性目标体系和复盘机制 |
| 12 | [Terraform IaC](./CN_Ops_Roadmap/12_IaC_Terraform/) | HCL 语言 · Resource / Data Source · Provider 抽象 · State 管理 · 模块化 | 基础设施代码化，一次 review 即可知变更全貌 |

---

## <div align="center">🌍 English Version</div>

**For**: Site Reliability Engineers · Platform Engineers · DevOps Practitioners · Cloud-native teams working with AWS / GCP / Azure

| # | Module | Key Topics | What You Can Build |
|---:|--------|-----------|-------------------|
| 01 | [Linux Basics](./EN_Global_SRE/01_Linux_Basics/) | System administration · Permissions · Process management · Kernel tuning · systemd | Manage 50+ production servers independently |
| 02 | [Shell Scripting](./EN_Global_SRE/02_Shell_Scripting/) | Bash programming · Text processing (awk/sed/grep) · Automation patterns · Defensive scripting | Production-grade automation scripts for rotation / backup / alerting |
| 03 | [Networking](./EN_Global_SRE/03_Network_Basics/) | TCP/IP stack · DNS resolution chain · firewalls · Packet analysis (tcpdump) | Troubleshoot latency / timeout / DNS issues at the protocol level |
| 04 | [Docker](./EN_Global_SRE/04_Container_Docker/) | Image optimization · Dockerfile best practices · Compose · Network & storage drivers | Containerize applications with 60%+ image size reduction |
| 05 | [Nginx](./EN_Global_SRE/05_Web_Server_Nginx/) | Reverse proxy · Load balancing algorithms · HTTPS / HTTP2 · Performance tuning | Web tier handling 10k+ QPS |
| 06 | [MySQL](./EN_Global_SRE/06_Database_MySQL/) | Query optimization · Replication / GTID · Backup strategies · Slow query analysis | Design HA database solution with verified recovery capability |
| 07 | [Kubernetes](./EN_Global_SRE/07_Container_Orchestration_K8s/) | Architecture · Pod lifecycle · Deployments / StatefulSets · Services / Ingress · Persistence | Run stateful workloads on K8s (including databases) |
| 08 | [CI/CD](./EN_Global_SRE/08_CICD_Jenkins_GitLab/) | Pipeline as Code · GitLab CI / Jenkinsfile · Artifact management · Security gates | Full automated deploy pipeline, sub-10-minute lead time |
| 09 | [Monitoring](./EN_Global_SRE/09_Monitoring_ElasticStack/) | Prometheus + Grafana · Metric design · Alert routing / silencing / inhibition · ELK stack | MTTD < 5 min, root cause traceable from metrics and logs |
| 10 | [Public Cloud](./EN_Global_SRE/10_Cloud_AWS_Azure/) | EC2 / ALB / S3 / RDS · HA architecture · Cost optimization · Well-Architected | Build production-grade cloud infrastructure on AWS or Azure |
| 11 | [SRE](./EN_Global_SRE/11_SRE_Principles_Practices/) | SLO / SLI / SLA definitions · Error budgets · Postmortem culture · Capacity planning | Establish availability targets and blameless review process |
| 12 | [Terraform IaC](./EN_Global_SRE/12_IaC_Terraform/) | HCL language · Resources / Data sources · Provider abstraction · Remote state · Modules | Infrastructure as code — full visibility via code review |

---

## 精选资源

| 类型 | 说明 | 链接 |
|------|------|------|
| 📖 书籍 | 运维 / SRE / 云原生领域必读书单 | [查看书单](./resources/books.md) |
| 🌐 社区 | 国内外活跃的技术社区与论坛 | [社区列表](./resources/communities.md) |
| 🧪 动手实验 | 免费的在线实验环境推荐 | [实验平台](./resources/online-labs.md) |
| 🔥 项目发现 | 每日整理 GitHub 上的优质开源项目 | [中文](./resources/trending_zh.md) · [English](./resources/trending_en.md) |

---

## 参与贡献

- 发现内容错误或过时 → [提 Issue](https://github.com/vinson-lee01/ops-engineering-roadmap/issues)
- 有好项目 / 好资源想推荐 → [提 PR](https://github.com/vinson-lee01/ops-engineering-roadmap/pulls)

---

<div align="center">

**如果这份路线图对你有帮助，考虑 Star ⭐ 支持一下**

[![Stars](https://img.shields.io/github/stars/vinson-lee01/ops-engineering-roadmap?style=social)](https://github.com/vinson-lee01/ops-engineering-roadmap/stargazers)

</div>
