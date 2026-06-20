<div align="center">

# ⚙️ Ops Engineering Roadmap

### 从零基础到生产架构师 · From Zero to Production Architect

<br>

[![GitHub stars](https://img.shields.io/github/stars/vinson-lee01/ops-engineering-roadmap?style=for-the-badge&logo=github&color=yellow)](https://github.com/vinson-lee01/ops-engineering-roadmap/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vinson-lee01/ops-engineering-roadmap?style=for-the-badge&logo=github&color=blue)](https://github.com/vinson-lee01/ops-engineering-roadmap/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/vinson-lee01/ops-engineering-roadmap?style=for-the-badge&logo=github&color=green)](https://github.com/vinson-lee01/ops-engineering-roadmap)

<br>

[![🇨🇳 中文版](https://img.shields.io/badge/%F0%9F%87%A8%F0%9F%87%B3_%E4%B8%AD%E6%96%87%E7%89%88-%E8%BF%9B%E5%85%A5%E4%B8%AD%E6%96%87%E7%89%88-blue?style=for-the-badge)](./CN_Ops_Roadmap/)
[![🌍 English](https://img.shields.io/badge/%F0%9F%8C%8D_English-Enter_EN_Version-orange?style=for-the-badge)](./EN_Global_SRE/)

</div>

---

## 🔥 Daily Discovery · 每日发现

<table>
<tr>
<td width="50%" valign="top">

### 🇨🇳 中文精选

| 项目 | Stars | 说明 |
|------|-------|------|
| [the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 229k | 安全/运维知识大全 |
| [free-for-dev](https://github.com/ripienaar/free-for-dev) | 123k | 免费开发者资源合集 |
| [devops-exercises](https://github.com/bregman-arie/devops-exercises) | 83k | DevOps 实战练习题 |
| [netdata](https://github.com/netdata/netdata) | 79k | AI 驱动全栈可观测性 |
| [awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | 72k | 大规模系统设计模式 |

</td>
<td width="50%" valign="top">

### 🌍 English Picks

| Project | Stars | Description |
|---------|-------|-------------|
| [the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 229k | Security & Ops knowledge base |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | 123k | Container orchestration |
| [free-for-dev](https://github.com/ripienaar/free-for-dev) | 123k | Free dev resources catalog |
| [devops-exercises](https://github.com/bregman-arie/devops-exercises) | 83k | Hands-on DevOps exercises |
| [netdata](https://github.com/netdata/netdata) | 79k | AI-powered observability |

</td>
</tr>
</table>

<div align="center">
<sub>Updated daily · <a href="./resources/trending_zh.md">View full CN list →</a> &nbsp;·&nbsp; <a href="./resources/trending_en.md">View full EN list →</a></sub>
</div>

---

## 💡 Why This Roadmap · 为什么值得收藏

> 市面上 90% 的运维学习路线，只告诉你「学什么」，却不说「学到什么程度」和「怎么用在生产上」。

<table>
<tr valign="top">
<td width="33%">

**🇨🇳 你在国内做运维**

会遇到这些独特的场景：
- 阿里云/腾讯云/华为云，各家产品逻辑不一样
- 等保2.0 合规检查，有固定的核查项
- 基线扫描（S3A3G3 规范），用 Linux 脚本落地
- 国产化替代（TiDB / OceanBase / OpenGauss）

**这份路线图为这些场景单独写了模块。**

</td>
<td width="33%">

**🌍 你在海外做 SRE**

需要掌握另一套方法论：
- Google SRE Book 体系（SLO/Error Budget）
- AWS/GCP/Azure 多云架构
- Incident Command System（ICS）框架
- Chaos Engineering 成熟度模型

**英文版模块覆盖以上内容，不是翻译版。**

</td>
<td width="33%">

**18 个月后，你能做到：**

| Before | After |
|:------|:------|
| 故障靠猜 | MTTD < 5分钟，根因有据可查 |
| 手动登服务器 | 全自动化，提交代码即上线 |
| 不知道学什么 | 清晰的阶段目标 + 可验证的产出 |
| 面试说不清楚 | 能用真实项目讲架构决策 |

</td>
</tr>
</table>

> 💬 *"不是教你考证书，而是让你在生产环境里真的能用。"*

---

## 📖 About This Roadmap · 关于本路线图

### 🇨🇳 中文简介

市面上大多数运维学习路线存在同一个问题：**只列工具名，不讲顺序、不讲深度、不讲在生产环境中怎么串联使用。**

这份路线图不一样。它基于国内云厂商和大型互联网公司的实际运维经验编写，围绕三个递进阶段展开。**每个模块都标注了真实生产环境需要掌握的深度——不是教材目录。**

### 🌍 English Introduction

Most online learning paths share a common problem: **they list tools without explaining the order, depth, or how they connect in real production environments.**

This roadmap is built differently — from hands-on experience at cloud vendors and large-scale internet companies, structured around three progressive stages. **Every module explicitly marks the depth needed in real work**, not a textbook table of contents.**

<table>
<tr align="center">
<td width="30%" valign="top">
<strong>Stage 1</strong><br><br>
<b>Can work<br>independently</b><br><br>
<i>独立胜任日常工作</i>
</td>
<td width="5%" valign="middle" style="font-size:24px;">
➜
</td>
<td width="30%" valign="top">
<strong>Stage 2</strong><br><br>
<b>Can design<br>architecture</b><br><br>
<i>能够设计系统架构</i>
</td>
<td width="5%" valign="middle" style="font-size:24px;">
➜
</td>
<td width="30%" valign="top">
<strong>Stage 3</strong><br><br>
<b>Can define<br>team standards</b><br><br>
<i>定义团队标准与规范</i>
</td>
</tr>
</table>

| | |
|:---|:---|
| **Language / 语言** | CN & EN maintained independently · 非机器翻译 · Not machine-translated |
| **Content / 内容** | 15KB+ production notes per module · 每模块 15KB+ 生产实战笔记 |
| **CN Focus / 中文侧重** | Aliyun / Tencent Cloud / 等保合规 Compliance / 基线扫描 Baseline / 国产化 Localization |
| **EN Focus / 英文侧重** | AWS / GCP / SRE Book methodology / Global best practices |

---

## 🗺️ Learning Path Overview · 学习路径总览

<table>
<tr align="center" bgcolor="#1e293b">
<th colspan="3" style="color:#e2e8f0;padding:12px;">Learning Timeline</th>
</tr>
<tr align="left" valign="top">
<td width="33%">
<details open><summary><b>📚 Phase 1 : Foundation</b></summary><small>(Month 1~3)</small>

- **Linux Basics** — 系统管理 / 权限 / 内核调优 / systemd
- **Shell Scripting** — Bash / 文本处理 / 自动化脚本
- **Networking** — TCP/IP / DNS / iptables / 抓包分析
- **Nginx Deploy** — 反向代理 / 负载均衡 / HTTPS 调优

*产出：独立管理 50+ 台服务器日常运维*
</details>
</td>
<td width="33%">
<details open><summary><b>🔧 Phase 2 : Growth</b></summary><small>(Month 4~9)</small>

- **Docker & K8s** — 容器化 / 编排 / Service Mesh
- **CI/CD Pipeline** — 流水线 / 制品管理 / 安全门禁
- **Prometheus + Grafana** — 指标设计 / 告警规则 / 仪表盘
- **ELK Stack** — 日志采集 / 分析 / 可视化

*产出：代码提交到上线全自动化，耗时 <10 分钟*
</details>
</td>
<td width="33%">
<details open><summary><b>🚀 Phase 3 : Advanced</b></summary><small>(Month 10~18+)</small>

- **Architecture** — 架构设计 / 多云 / FinOps
- **SLO & Error Budget** — 可用性目标 / 错误预算体系
- **Multi-cloud** — 混合云架构 / 成本优化
- **Chaos Engineering** — 故障演练 / 弹性验证

*产出：建立团队可用性目标体系与 SRE 文化*
</details>
</td>
</tr>
</table>

> Each stage concludes with verifiable deliverables — not *studied*, but *can build*.
> 每个阶段都有可验证的产出 —— 不是"学过了"，而是"能做出来"。

---

# 🇨🇳 中文版 · CN Version

### 国内运维工程师完整成长路径

*适用场景：国内企业运维 · 应届求职 · 国产云（阿里云/腾讯云/华为云）· 等保合规 / 基线核查*

**[→ 进入中文版完整目录](./CN_Ops_Roadmap/)**

<table>
<tr>
<td width="50"><strong>#</strong></td>
<td width="210"><strong>模块</strong></td>
<td><strong>核心内容</strong></td>
<td width="250"><strong>学习产出</strong></td>
</tr>
<tr><td align="center"><code>01</code></td><td><a href="./CN_Ops_Roadmap/01_Linux_Basics/"><b>Linux 基础</b></a></td><td>系统管理 · 文件权限 · 进程管理 · 内核调优 · systemd</td><td>独立管理 50+ 台服务器日常运维</td></tr>
<tr><td align="center"><code>02</code></td><td><a href="./CN_Ops_Roadmap/02_Shell_Scripting/"><b>Shell 编程</b></a></td><td>Bash 编程 · awk/sed/grep · crontab 自动化 · 脚本健壮性</td><td>生产级自动化脚本（日志轮转/备份/告警）</td></tr>
<tr><td align="center"><code>03</code></td><td><a href="./CN_Ops_Roadmap/03_Network_Basics/"><b>网络基础</b></a></td><td>TCP/IP · DNS 解析链路 · iptables · tcpdump/wireshark</td><td>排查网络延迟/超时/DNS 劫持类故障</td></tr>
<tr><td align="center"><code>04</code></td><td><a href="./CN_Ops_Roadmap/04_Container_Docker/"><b>Docker 容器</b></a></td><td>镜像优化 · Dockerfile 最佳实践 · Compose · 网络存储</td><td>容器化应用，镜像体积缩减 60%+</td></tr>
<tr><td align="center"><code>05</code></td><td><a href="./CN_Ops_Roadmap/05_Web_Server_Nginx/"><b>Nginx 实战</b></a></td><td>反向代理 · 负载均衡 · HTTPS/HTTP2 · 性能调优</td><td>承载万级 QPS 的 Web 接入层</td></tr>
<tr><td align="center"><code>06</code></td><td><a href="./CN_Ops_Roadmap/06_Database_MySQL/"><b>MySQL 数据库</b></a></td><td>SQL 调优 · 主从复制/GTID · 备份策略 · 慢查询</td><td>设计 HA 数据库方案，恢复能力验证通过</td></tr>
<tr><td align="center"><code>07</code></td><td><a href="./CN_Ops_Roadmap/07_Container_Orchestration_K8s/"><b>Kubernetes</b></a></td><td>架构原理 · Pod 生命周期 · Deployment · Service/Ingress</td><td>在 K8s 上跑起有状态服务（含数据库）</td></tr>
<tr><td align="center"><code>08</code></td><td><a href="./CN_Ops_Roadmap/08_CICD_Jenkins_GitLab/"><b>CI/CD 流水线</b></a></td><td>Pipeline as Code · GitLab CI · 制品管理 · 安全扫描</td><td>代码提交到上线全自动化，耗时 < 10 分钟</td></tr>
<tr><td align="center"><code>09</code></td><td><a href="./CN_Ops_Roadmap/09_Monitoring_ElasticStack/"><b>监控体系</b></a></td><td>Prometheus+Grafana · 指标设计 · 告警体系 · ELK 日志</td><td>MTTD < 5 分钟，根因定位有据可查</td></tr>
<tr><td align="center"><code>10</code></td><td><a href="./CN_Ops_Roadmap/10_Cloud_Native/"><b>公有云 & 云原生</b></a></td><td>阿里云/腾讯云 · Terraform IaC · <b>等保2.0</b> · <b>国产化替代</b> · <b>基线扫描</b></td><td>搭建符合等保三级要求的云架构</td></tr>
<tr><td align="center"><code>11</code></td><td><a href="./CN_Ops_Roadmap/11_SRE_Principles_Practices/"><b>SRE 工程化</b></a></td><td>SLO/SLI/SLA · Error Budget · 故障复盘 · 容量规划</td><td>建立团队可用性目标体系和复盘机制</td></tr>
<tr><td align="center"><code>12</code></td><td><a href="./CN_Ops_Roadmap/12_IaC_Terraform/"><b>Terraform IaC</b></a></td><td>HCL · Resource/Data Source · State 管理 · 模块化</td><td>基础设施代码化，变更全貌一目了然</td></tr>
</table>

---

# 🌍 English Version

### Complete SRE / DevOps Career Path

*For: Site Reliability Engineers · Platform Engineers · DevOps Practitioners · Cloud-native teams (AWS/GCP/Azure)*

**[→ Enter English Version](./EN_Global_SRE/)**

<table>
<tr>
<td width="50"><strong>#</strong></td>
<td width="260"><strong>Module</strong></td>
<td><strong>Key Topics</strong></td>
<td width="280"><strong>What You Build</strong></td>
</tr>
<tr><td align="center"><code>01</code></td><td><a href="./EN_Global_SRE/01_Linux_Fundamentals/"><b>Linux Fundamentals</b></a></td><td>System admin · Permissions · Processes · Kernel tuning · systemd</td><td>Manage 50+ production servers independently</td></tr>
<tr><td align="center"><code>02</code></td><td><a href="./EN_Global_SRE/03_Shell_Automation/"><b>Shell & Automation</b></a></td><td>Bash scripting · Text processing · Cron patterns · Defensive scripts</td><td>Production-grade automation (rotation/backup/alerting)</td></tr>
<tr><td align="center"><code>03</code></td><td><a href="./EN_Global_SRE/02_Networking/"><b>Networking</b></a></td><td>TCP/IP stack · DNS chain · Firewalls · Packet analysis</td><td>Troubleshoot latency/timeout/DNS at protocol level</td></tr>
<tr><td align="center"><code>04</code></td><td><a href="./EN_Global_SRE/04_Container_Docker/"><b>Docker</b></a></td><td>Image optimization · Dockerfile best practices · Compose</td><td>Containerize apps with 60%+ image size reduction</td></tr>
<tr><td align="center"><code>05</code></td><td><a href="./EN_Global_SRE/07_Web_Servers/"><b>Nginx</b></a></td><td>Reverse proxy · Load balancing · HTTPS/HTTP2 · Tuning</td><td>Web tier handling 10k+ QPS</td></tr>
<tr><td align="center"><code>06</code></td><td><a href="./EN_Global_SRE/09_Database/"><b>MySQL</b></a></td><td>Query optimization · Replication/GTID · Backups · Slow queries</td><td>Design HA database with verified recovery</td></tr>
<tr><td align="center"><code>07</code></td><td><a href="./EN_Global_SRE/05_Kubernetes/"><b>Kubernetes</b></a></td><td>Architecture · Pod lifecycle · Deployments · Ingress · Storage</td><td>Run stateful workloads on K8s (including DBs)</td></tr>
<tr><td align="center"><code>08</code></td><td><a href="./EN_Global_SRE/06_CI_CD/"><b>CI/CD</b></a></td><td>Pipeline as Code · GitLab CI · Artifact mgmt · Security gates</td><td>Full automated deploy, sub-10-minute lead time</td></tr>
<tr><td align="center"><code>09</code></td><td><a href="./EN_Global_SRE/08_Monitoring_Observability/"><b>Monitoring & Observability</b></a></td><td>Prometheus+Grafana · Metric design · Alerting · ELK</td><td>MTTD < 5 min, root cause traceable</td></tr>
<tr><td align="center"><code>10</code></td><td><a href="./EN_Global_SRE/10_Cloud_Native_IaC/"><b>Cloud Native & IaC</b></a></td><td>AWS/GCP/Azure · Terraform · Ansible · Service Mesh · FinOps</td><td>Production-grade multi-cloud infrastructure</td></tr>
<tr><td align="center"><code>11</code></td><td><a href="./EN_Global_SRE/11_SRE_Handbook/"><b>SRE Handbook</b></a></td><td><b>SLO/SLI Engineering</b> · Incident Command · Blameless Postmortem · On-call · Toil Elimination · Chaos Eng.</td><td>Establish availability targets, error budgets, blameless culture</td></tr>
<tr><td align="center"><code>12</code></td><td><a href="./EN_Global_SRE/12_Interview_Prep/"><b>Interview Prep</b></a></td><td>Behavioral questions · System design · Tech deep-dives · Compensation</td><td>Confidently pass SRE interviews at tier-1 companies</td></tr>
</table>

---

## 📚 Resources · 资源

<div align="center">

| Resource | Description | Link |
|:---|:---|:---|
| 📖 **Books / 书单** | Curated reading list for Ops / SRE / Cloud-native | [View →](./resources/books.md) |
| 🌐 **Communities / 社区** | Active technical communities & forums | [View →](./resources/communities.md) |
| 🧪 **Labs / 实验** | Free online lab environments | [View →](./resources/online-labs.md) |
| 🔥 **Daily Discovery / 每日发现** | Full curated GitHub project lists | [中文 →](./resources/trending_zh.md) · [EN →](./resources/trending_en.md) |

</div>

---

## 🤝 Contributing · 参与贡献

Found an issue or have a great resource to share?
发现错误或有优质资源推荐？

- 🐛 Report issues / 提交问题 → [Open an Issue](https://github.com/vinson-lee01/ops-engineering-roadmap/issues)
- 💡 Share resources / 分享资源 → [Submit a PR](https://github.com/vinson-lee01/ops-engineering-roadmap/pulls)

---

<br>

<div align="center">

### ⭐ If this roadmap helps you, please consider giving it a Star

如果这份路线图对你有帮助，欢迎点个 Star 支持一下

<br>

[![Star this repo](https://img.shields.io/github/stars/vinson-lee01/ops-engineering-roadmap?style=social)](https://github.com/vinson-lee01/ops-engineering-roadmap/stargazers)

</div>
