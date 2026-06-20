# 🔥 每日发现 · Daily Discovery

> 自动化脚本每日从 GitHub 抓取运维/DevOps/SRE 领域热门项目，自动更新。
> Updated daily by GitHub Actions.

---

## 📄 分语言版本

- 🇨🇳 [中文版 · 国内热门](./trending_zh.md)
- 🌍 [English · Global Trending](./trending_en.md)

---

## 🏆 最近更新（最近 7 天）

*由脚本自动生成，每日 UTC 00:05 更新。*

> ⚠️ **首次运行提示**：仓库刚创建，脚本将在明天自动运行。如果你想立即看到效果，可以在 GitHub Actions 页面手动触发 `update-resources` workflow。

---

## 📊 本周热门项目

*待脚本首次运行后自动填充*

| 项目 | Stars | 语言 | 简介 |
|--------|-------|------|---------|
| *Waiting for first update...* | | | |

---

## 💡 如何推荐项目？

欢迎提 Issue 或 PR，告诉我你发现的好项目！

- 🐛 发现 Bug → [提 Issue](https://github.com/vinson-lee01/ops-engineering-roadmap/issues)
- 💡 有好项目推荐 → [提 PR](https://github.com/vinson-lee01/ops-engineering-roadmap/pulls)
- 📬 联系我 → GitHub @vinson-lee01

---

<details>
<summary>📖 脚本工作原理（点击展开）</summary>

每日 UTC 00:05，GitHub Actions 自动运行 `scripts/update_trending.py`：

1. 搜索 GitHub 上 `topic:devops` `topic:sre` `topic:kubernetes` 等关键词
2. 按 Star 增长速度和总 Star 数排序
3. 过滤掉 archived 和 12 个月未更新的仓库
4. 生成中文版和英文版两个文件
5. 自动提交到 main 分支

你可以随时在 [Actions 页面](https://github.com/vinson-lee01/ops-engineering-roadmap/actions) 查看运行记录。

</details>
