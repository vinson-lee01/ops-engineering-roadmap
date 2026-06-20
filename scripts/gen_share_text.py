#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-platform share text generator
- Twitter / X
- Reddit (r/devops, r/sre)
- Zhihu (知乎)
- CSDN
- LinkedIn
- Hacker News
- Dev.to
"""

import json
import os
import re
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")
OUTPUT_FILE = "resources/share_text.md"
CACHE_FILE = "resources/.cache_zh.json"
TRENDING_FILE = "resources/trending_zh.md"
TRENDING_EN_FILE = "resources/trending_en.md"
README_FILE = "README.md"


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def load_trending():
    """Parse trending files for highlights."""
    result = {"new_zh": 0, "new_en": 0, "top_zh": "", "top_en": "", "top_zh_url": "", "top_en_url": ""}
    for path, key in [(TRENDING_FILE, "zh"), (TRENDING_EN_FILE, "en")]:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # New count
            m = re.search(r"New today:\s*\*\*(\d+)\*\*", content)
            if m:
                if key == "zh":
                    result["new_zh"] = int(m.group(1))
                else:
                    result["new_en"] = int(m.group(1))
            # Top pick
            m2 = re.search(r"Top pick:\s*\[([^\]]+)\]\(([^\)]+)\)", content)
            if m2:
                if key == "zh":
                    result["top_zh"] = m2.group(1)
                    result["top_zh_url"] = m2.group(2)
                else:
                    result["top_en"] = m2.group(1)
                    result["top_en_url"] = m2.group(2)
        except Exception:
            pass
    return result


def load_readme_desc():
    """Extract description from README.md."""
    if not os.path.exists(README_FILE):
        return "DevOps/SRE learning roadmap"
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract first paragraph after badges
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        for line in lines:
            if len(line) > 30 and not line.startswith("#") and not line.startswith("["):
                return line[:120]
    except Exception:
        pass
    return "DevOps/SRE Zero-to-Hero Learning Roadmap"


def generate_twitter(trending):
    """Twitter / X share text."""
    lines = []
    lines.append("═" * 50)
    lines.append("🐦 Twitter / X")
    lines.append("═" * 50)
    lines.append("")
    lines.append(f"🗺️ DevOps/SRE Learning Roadmap — updated {TODAY}")
    lines.append("")
    lines.append("✅ 12 modules, Zero → Hero")
    lines.append("✅ CN + EN, 500+ curated resources")
    lines.append("✅ Trending repos updated daily")
    if trending["new_zh"] > 0 or trending["new_en"] > 0:
        lines.append(f"✅ +{trending['new_zh'] + trending['new_en']} new repos today")
    lines.append("")
    lines.append("#DevOps #SRE #Linux #Docker #Kubernetes #CloudNative #OpenSource")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    return "\n".join(lines)


def generate_reddit(trending):
    """Reddit share text (r/devops, r/sysadmin)."""
    lines = []
    lines.append("═" * 50)
    lines.append("🤖 Reddit (r/devops / r/sysadmin)")
    lines.append("═" * 50)
    lines.append("")
    lines.append("**Title:** DevOps/SRE Learning Roadmap — 500+ resources, CN + EN (updated daily)")
    lines.append("")
    lines.append("**Body:**")
    lines.append("")
    lines.append("I put together a complete DevOps/SRE learning roadmap, covering:")
    lines.append("- 🐧 Linux administration & security hardening")
    lines.append("- 🐳 Docker & Kubernetes (production-grade)")
    lines.append("- 🔄 CI/CD pipelines (GitHub Actions, GitLab CI)")
    lines.append("- 📊 Prometheus + Grafana observability stack")
    lines.append("- ☁️ Cloud Native & IaC (Terraform, Ansible)")
    lines.append("- 📚 SRE handbook & interview prep")
    lines.append("")
    lines.append("Two versions: Chinese (CN market) + English (global).")
    lines.append("Trending DevOps repos auto-updated daily via GitHub Actions.")
    if trending["top_en"]:
        lines.append(f"")
        lines.append(f"Today's top pick: [{trending['top_en']}]({trending['top_en_url']})")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    lines.append("Feedback & contributions welcome! 🙏")
    lines.append("")
    return "\n".join(lines)


def generate_zhihu(trending):
    """Zhihu (知乎) share text."""
    lines = []
    lines.append("═" * 50)
    lines.append("📝 知乎（中文）")
    lines.append("═" * 50)
    lines.append("")
    lines.append(f"**标题：** 运维工程师学习路线（2026）— 从零基础到架构师")
    lines.append("")
    lines.append("**正文：**")
    lines.append("")
    lines.append("作为一名运维工程师，如何将零散的知识体系化？")
    lines.append("我整理了一份完整的 DevOps/SRE 学习路线，覆盖 12 个核心模块：")
    lines.append("")
    lines.append("1. Linux 基础与进阶（安全加固、性能调优）")
    lines.append("2. 计算机网络（TCP/IP、DNS、负载均衡）")
    lines.append("3. Shell 脚本自动化")
    lines.append("4. Docker 容器化")
    lines.append("5. Kubernetes 生产实践")
    lines.append("6. CI/CD 流水线")
    lines.append("7. Nginx 反向代理与高可用")
    lines.append("8. 监控告警（Prometheus + Grafana）")
    lines.append("9. 数据库优化（MySQL / Redis）")
    lines.append("10. 云原生 & IaC")
    lines.append("11. SRE 方法论")
    lines.append("12. 面试题汇总")
    lines.append("")
    lines.append("📦 500+ 精选资源，中英双语，每日更新热门发现。")
    if trending["top_zh"]:
        lines.append(f"")
        lines.append(f"今日推荐：[{
            trending['top_zh']}]({trending['top_zh_url']})")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    lines.append("如果对你有帮助，欢迎 Star ⭐ — 这样每次更新你都能看到！")
    lines.append("")
    return "\n".join(lines)


def generate_csdn(trending):
    """CSDN share text."""
    lines = []
    lines.append("═" * 50)
    lines.append("💼 CSDN（中文）")
    lines.append("═" * 50)
    lines.append("")
    lines.append(f"**标题：** 运维学习路线开源（500+ 资源，中英双语，每日更新）")
    lines.append("")
    lines.append("**正文：**")
    lines.append("")
    lines.append("从 Linux 到 K8s，从 Docker 到 CI/CD — 一份完整的运维工程师学习路线。")
    lines.append("")
    lines.append("✅ 12 大模块，从零基础到架构师")
    lines.append("✅ 中文版 + English 版，各自独立")
    lines.append("✅ 500+ 精选资源（视频、书籍、在线实验）")
    lines.append("✅ GitHub Actions 每日自动更新热门仓库")
    lines.append("")
    lines.append("适合人群：运维新人 / 想转 SRE 的工程师 / 备考 DevOps 认证")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    lines.append("> 如果这个仓库对你有帮助，欢迎 Star ⭐")
    lines.append("")
    return "\n".join(lines)


def generate_linkedin(trending):
    """LinkedIn share text."""
    lines = []
    lines.append("═" * 50)
    lines.append("💼 LinkedIn")
    lines.append("═" * 50)
    lines.append("")
    lines.append("Sharing something I've been building — a complete DevOps/SRE learning roadmap. 🛠️")
    lines.append("")
    lines.append("It covers 12 modules: Linux → Docker → K8s → CI/CD → Monitoring → Cloud Native.")
    lines.append("500+ curated resources. CN + EN versions. Auto-updated daily.")
    lines.append("")
    lines.append("Useful if you're:")
    lines.append("- Transitioning into DevOps/SRE")
    lines.append("- Preparing for SRE interviews")
    lines.append("- Looking for a structured learning path")
    lines.append("")
    lines.append("Would love your feedback! ⭐ Star if you find it useful.")
    lines.append("")
    lines.append("#DevOps #SRE #CloudComputing #OpenSource #Learning")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    return "\n".join(lines)


def generate_hackernews(trending):
    """Hacker News share text."""
    lines = []
    lines.append("═" * 50)
    lines.append("🗞️ Hacker News")
    lines.append("═" * 50)
    lines.append("")
    lines.append(f"**Title:** DevOps/SRE Learning Roadmap (500+ resources, daily updated)")
    lines.append("")
    lines.append("**Text:**")
    lines.append("")
    lines.append("A comprehensive DevOps/SRE learning roadmap covering 12 modules from Linux basics to SRE interview prep.")
    lines.append("")
    lines.append("Notable features:")
    lines.append("- Dual version: Chinese (CN market) + English (global)")
    lines.append("- Trending repos auto-fetched daily via GitHub Actions")
    lines.append("- 500+ curated resources: books, communities, online labs")
    lines.append("")
    lines.append("Maintained by https://github.com/vinson-lee01")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    return "\n".join(lines)


def generate_devto(trending):
    """Dev.to article outline."""
    lines = []
    lines.append("═" * 50)
    lines.append("📝 Dev.to (article outline)")
    lines.append("═" * 50)
    lines.append("")
    lines.append(f"**Title:** The Complete DevOps/SRE Roadmap — 2026 Edition")
    lines.append("")
    lines.append("**Outline:**")
    lines.append("")
    lines.append("## Intro")
    lines.append("- Why I built this roadmap")
    lines.append("- Who it's for")
    lines.append("")
    lines.append("## The 12 Modules (quick overview)")
    lines.append("1. Linux → 2. Networking → 3. Shell → 4. Docker → 5. K8s")
    lines.append("6. CI/CD → 7. Nginx → 8. Monitoring → 9. DB → 10. Cloud → 11. SRE → 12. Interview")
    lines.append("")
    lines.append("## Highlights")
    lines.append("- Dual CN/EN versions")
    lines.append("- Daily trending repo updates")
    lines.append("- 500+ resources")
    lines.append("")
    lines.append("## How to use it")
    lines.append("- Clone the repo")
    lines.append("- Follow the order, or jump to your module")
    lines.append("- Star ⭐ to follow updates")
    lines.append("")
    lines.append("🔗 https://github.com/vinson-lee01/ops-engineering-roadmap")
    lines.append("")
    return "\n".join(lines)


def main():
    cache = load_cache()
    trending = load_trending()
    desc = load_readme_desc()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📢 Share Text Generator — {TODAY}\n\n")
        f.write(f"> {desc}\n\n")
        f.write("─" * 50 + "\n\n")

        f.write(generate_twitter(trending))
        f.write("\n\n")
        f.write(generate_reddit(trending))
        f.write("\n\n")
        f.write(generate_zhihu(trending))
        f.write("\n\n")
        f.write(generate_csdn(trending))
        f.write("\n\n")
        f.write(generate_linkedin(trending))
        f.write("\n\n")
        f.write(generate_hackernews(trending))
        f.write("\n\n")
        f.write(generate_devto(trending))

    print(f"✅ Done: {OUTPUT_FILE}")
    print(f"   Trending: ZH={trending['new_zh']} new, EN={trending['new_en']} new")


if __name__ == "__main__":
    main()
