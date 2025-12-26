# Journal Skill - Quick Start Guide

## 🚀 快速开始

### 方式1：使用Gemini命令（推荐）

```bash
# 记录一个想法
gemini journal "我想到了一个关于RAG优化的方案"

# 记录完成的工作
gemini journal "完成了PostgreSQL查询优化"

# 记录一个链接
gemini journal "发现了这篇paper: https://arxiv.org/abs/... 讲述LLM优化"

# 生成每日时间线
gemini journal-timeline
```

### 方式2：使用Python脚本

```bash
# 首先设置别名（添加到 .bashrc 或 .zshrc）
alias jlog='python3 /path/to/scripts/journal_logger.py log'

# 然后使用
jlog thought "我的新想法"
jlog work "完成了什么任务"
jlog link "https://..." "链接描述"

# 查看今日entries
python3 scripts/journal_logger.py list

# 查看统计
python3 scripts/journal_logger.py stats
```

### 方式3：使用Shell包装脚本

```bash
# 添加到path或使用完整路径
source scripts/jlog.sh

jlog thought "My idea"
jlog work "Completed task"
jlog link "https://..." "Description"
jlog list
```

---

## 📁 文件结构

创建后会生成这些文件：

```
journal/
├── journal_2025-12-26.md      # 原始日志（所有entries）
├── journal_2025-12-25.md      
├── timeline_2025-12-26.md     # 每日时间线（整理后）
└── timeline_2025-12-25.md
```

### journal_YYYY-MM-DD.md 示例
```markdown
# Daily Journal - 2025-12-26

## [08:30] 💡 THOUGHT: LLM Memory Management
- Ideas about handling context length
- Potential sliding window compression approach

## [10:45] ✅ WORK: Completed journal skill setup
- Created Gemini command config
- Set up file structure

## [14:20] 🔗 LINK: Andrej Karpathy's scaling post
- Source: https://twitter.com/karpathy/status/...

## [16:00] ✅ WORK: Code review and bug fixes
- Merged 2 PRs
- Fixed critical issue
```

### timeline_YYYY-MM-DD.md 示例
```markdown
# Daily Timeline - 2025-12-26
**Generated:** 2025-12-26 17:45:00

## 📊 Summary
- **Total entries:** 4
- **Breakdown:** 💡 Thoughts: 1 | ✅ Work: 2 | 🔗 Links: 1
- **Time span:** 08:30 - 16:00

## 💡 Thoughts & Ideas
- **08:30** LLM Memory Management - Ideas about context length handling

## ✅ Completed Work
- **10:45** Journal skill setup completed
- **16:00** Code review and bug fixes

## 🔗 Shared Resources & Links
- **14:20** Andrej Karpathy's scaling insights
  - [Twitter](https://twitter.com/karpathy/status/...)

## 🎯 Key Insights
Today focused on improving personal knowledge management infrastructure while staying current with LLM research trends. Made solid progress on tooling.
```

---

## 🎯 使用模式

### 模式1：随时快速记录
```bash
# 想到一个想法时立即记录
jlog thought "新的函数式编程方法"

# 完成一个任务时立即记录
jlog work "修复了内存泄漏bug"

# 看到有趣的链接时立即记录
jlog link "https://github.com/..." "Amazing new framework"
```

### 模式2：批量整理
```bash
# 黄昏时整理一天的entries，生成时间线
gemini journal-timeline

# 查看生成的时间线
cat journal/timeline_2025-12-26.md

# 或在编辑器中打开
code journal/timeline_2025-12-26.md
```

### 模式3：跨平台记录
可以从不同的来源记录：
- **Twitter/X**: "看到了XXX的推文，链接+要点"
- **Telegram**: "频道里的想法或资源"
- **YouTube**: "视频内容或灵感"
- **GitHub**: "有趣的项目或代码审查"

---

## ⚙️ 高级配置

### 添加bash别名（推荐）

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
# Journal shortcuts
alias jlog='python3 /Users/matianjun/Dropbox/code/llm_fun/scripts/journal_logger.py log'
alias jlist='python3 /Users/matianjun/Dropbox/code/llm_fun/scripts/journal_logger.py list'
alias jstats='python3 /Users/matianjun/Dropbox/code/llm_fun/scripts/journal_logger.py stats'
```

### 自动生成每日时间线（可选）

使用 `crontab` 每天18:00自动生成：

```bash
crontab -e
```

添加：
```
0 18 * * * cd /Users/matianjun/Dropbox/code/llm_fun && gemini journal-timeline
```

### 集成MkDocs导航

编辑 `mkdocs.yml`：

```yaml
nav:
  - Home: index.md
  - Documentation: docs/
  - Journal: journal/
  - Papers: papers/
```

然后在MkDocs中浏览journal文件。

---

## 💾 备份和同步

### 自动Git备份
```bash
# 每次提交journal文件自动保存
git add journal/
git commit -m "Journal: Daily entries - $(date +%Y-%m-%d)"
```

### 与Obsidian同步
如果使用Obsidian，在vault中包含journal文件夹，可以：
- 使用Obsidian编辑日志
- 创建到docs/的双向链接
- 使用标签和高级查询

---

## 🔍 查询和分析

### 查找特定主题
```bash
# 搜索所有包含"LLM"的entries
grep -i "llm" journal/*.md

# 搜索特定日期
grep -h "💡" journal/journal_2025-12-*.md
```

### 统计entries
```bash
# 计算总entries数
grep -c "##" journal/*.md

# 按类型统计
echo "Thoughts:"; grep -c "💡" journal/*.md
echo "Work:"; grep -c "✅" journal/*.md
echo "Links:"; grep -c "🔗" journal/*.md
```

---

## 📚 文件说明

| 文件 | 说明 | 何时使用 |
|------|------|---------|
| `journal_YYYY-MM-DD.md` | 原始日志，包含所有当天entries | 快速记录时 |
| `timeline_YYYY-MM-DD.md` | 整理后的时间线，分类显示 | 回顾一天时 |
| `scripts/journal_logger.py` | Python核心脚本 | 直接调用或别名 |
| `scripts/jlog.sh` | Shell包装脚本 | 额外的便利层 |
| `.gemini/commands/journal.toml` | Gemini命令配置 | Gemini CLI集成 |
| `.gemini/commands/journal-timeline.toml` | 时间线生成配置 | Gemini CLI集成 |

---

## 🚨 故障排除

### 问题：Gemini命令找不到
**解决**: 确保 `.gemini/commands/journal.toml` 文件存在且格式正确

### 问题：Python脚本权限错误
**解决**: 运行 `chmod +x scripts/journal_logger.py`

### 问题：Journal文件夹不存在
**解决**: 脚本会自动创建，但也可以手动 `mkdir -p journal`

### 问题：时间线生成失败
**解决**: 确保journal文件存在且有entries；检查Gemini配置

---

## 📝 最佳实践

1. **及时记录**: 不要延迟记录，立即捕捉想法
2. **简洁清晰**: entries应该简短但有意义
3. **分类使用**: 使用正确的entry类型（thought/work/link）
4. **定期回顾**: 每晚或周末查看时间线
5. **跨链接**: 在docs/中引用journal insights
6. **归档历史**: 旧的journal文件可归档，保留timeline用于回顾

---

## 🔮 未来扩展

潜在的功能增强：
- [ ] 按标签过滤entries (#productivity #learning #idea)
- [ ] 自动生成周/月总结
- [ ] 与Notion/Roam Research集成
- [ ] AI摘要和insight生成
- [ ] 搜索和全文索引
- [ ] 数据可视化（entries趋势）

