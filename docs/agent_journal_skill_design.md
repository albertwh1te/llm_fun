****# Agent Journal Skill 设计方案

## 概述
这个skill用于记录用户的随时想法、社交媒体信息（Twitter/Telegram/YouTube）和完成的工作，最终生成每日时间线。

---

## 1. Skill触发方式

### 方式 A：Gemini命令（推荐）
```bash
gemini journal "我刚完成了XYZ项目"
gemini journal-thought "我想到了一个关于LLM的想法"
gemini journal-link "分享了这个YouTube视频：[链接] 关于强化学习"
```

### 方式 B：Gemini命令配置
创建 `.gemini/commands/journal.toml` - 用于快速记录
创建 `.gemini/commands/journal-timeline.toml` - 用于生成每日时间线

### 方式 C：脚本快捷键（可选）
如果使用shell/Python脚本，可以设置别名：
```bash
alias jlog='python3 scripts/journal_logger.py'
```

---

## 2. Agent Skill Prompt设计

### 2.1 Journal记录命令 (.gemini/commands/journal.toml)

```toml
description = "Log thoughts, links, and work completion to daily journal"

prompt = """
You are a Personal Journal Assistant. Your task is to capture and organize the user's daily activities, thoughts, and findings.

User input: {{args}}

Task:
1. Parse the input to identify the type of entry:
   - THOUGHT: Personal reflection or idea
   - WORK: Completed work/task
   - LINK: Social media link (Twitter/Telegram/YouTube/etc)
   - OTHER: General note

2. Extract key information:
   - Type of entry
   - Content/description
   - Source (if applicable - URL, platform)
   - Current timestamp

3. Format as JSON structure and append to today's journal file in folder: `journal/`

4. File naming: `journal_YYYY-MM-DD.md` (e.g., `journal_2025-12-26.md`)

5. Journal entry format:
```
## [HH:MM] TYPE: Description
- Details about the entry
- Source/Link (if applicable)
```

6. Ensure:
   - Entries are timestamped
   - Multiple entries same day are appended in chronological order
   - File is valid Markdown
   - Clear separation between different types (use emoji: 💡 for thoughts, ✅ for work, 🔗 for links)

Output the formatted entry and confirm it was saved.
"""
```

### 2.2 每日时间线生成命令 (.gemini/commands/journal-timeline.toml)

```toml
description = "Generate daily timeline from journal entries"

prompt = """
You are a Daily Timeline Synthesizer. Your task is to create a comprehensive timeline from journal entries.

Task:
1. Read today's journal file: `journal/journal_YYYY-MM-DD.md` (use current date)

2. Create a structured timeline:
   - Group entries by type (Thoughts, Work, Links)
   - Include timestamps
   - Add brief summaries for longer entries
   
3. Generate output file: `journal/timeline_YYYY-MM-DD.md`

4. Timeline format:
```markdown
# Daily Timeline - YYYY-MM-DD

## 📊 Summary
- Total entries: X
- Thoughts: X | Work items: X | Links: X

## 💡 Thoughts & Ideas
[Chronological list]

## ✅ Completed Work
[Chronological list]

## 🔗 Shared Resources
[Chronological list with links]

## 🎯 Key Insights
[Synthesized learnings from the day]
```

5. Save to `journal/timeline_YYYY-MM-DD.md`

6. Output the generated timeline for user review.
"""
```

---

## 3. 脚本支持

### 3.1 可选Python脚本 (scripts/journal_logger.py)

如果想要更高级的功能，可以创建辅助脚本：

```python
#!/usr/bin/env python3
"""
Journal Logger - Standalone CLI for quick journal entries
"""

import json
import os
from datetime import datetime
from pathlib import Path

class JournalLogger:
    def __init__(self, journal_dir="journal"):
        self.journal_dir = Path(journal_dir)
        self.journal_dir.mkdir(exist_ok=True)
    
    def get_today_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.journal_dir / f"journal_{today}.md"
    
    def log_entry(self, entry_type, content, source=None):
        """Log an entry to today's journal"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create entry
        emoji_map = {
            "thought": "💡",
            "work": "✅",
            "link": "🔗",
            "other": "📝"
        }
        emoji = emoji_map.get(entry_type, "📝")
        
        entry = f"## [{timestamp}] {emoji} {entry_type.upper()}: {content}\n"
        if source:
            entry += f"- Source: {source}\n"
        entry += "\n"
        
        # Append to file
        file_path = self.get_today_file()
        with open(file_path, "a") as f:
            f.write(entry)
        
        return f"✓ Logged to {file_path.name}"
    
    def generate_timeline(self):
        """Generate timeline for today"""
        # Implementation here
        pass

if __name__ == "__main__":
    import sys
    logger = JournalLogger()
    
    if len(sys.argv) < 3:
        print("Usage: journal_logger.py <type> <content> [source]")
        sys.exit(1)
    
    entry_type = sys.argv[1]
    content = sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(logger.log_entry(entry_type, content, source))
```

### 3.2 可选Shell脚本包装 (scripts/jlog.sh)

```bash
#!/bin/bash
# Quick journal logger wrapper

# Usage: jlog thought "my idea"
#        jlog work "completed task"
#        jlog link "https://..." "description"

TYPE=$1
shift
CONTENT="$@"

python3 scripts/journal_logger.py "$TYPE" "$CONTENT"
```

---

## 4. 文件存储结构

### 4.1 创建journal文件夹

```
journal/
├── journal_2025-12-26.md      # 当日日志（全部entries）
├── journal_2025-12-25.md      # 历史日志
├── timeline_2025-12-26.md     # 当日时间线（综合版）
├── timeline_2025-12-25.md     # 历史时间线
├── weekly_digest_W52.md       # 周汇总（可选）
└── monthly_digest_2025-12.md  # 月汇总（可选）
```

### 4.2 存储的文件说明

#### **核心文件（必需）**

| 文件 | 说明 | 何时创建 |
|------|------|--------|
| `journal_YYYY-MM-DD.md` | 原始日志文件，包含所有entries（想法、工作、链接） | 首次记录时自动创建 |
| `timeline_YYYY-MM-DD.md` | 每日时间线，经过综合整理和分类 | 用户手动生成或定时生成 |

#### **扩展文件（可选）**

| 文件 | 说明 | 何时创建 |
|------|------|--------|
| `weekly_digest_W{week}.md` | 周汇总，统计该周的insights | 每周末或周一生成 |
| `monthly_digest_{YYYY-MM}.md` | 月度报告，关键learnings | 月末或月初生成 |

#### **索引文件（可选）**

| 文件 | 说明 | 何时创建 |
|------|------|--------|
| `journal_index.md` | 所有journal文件的导航索引 | 定期更新 |

### 4.3 单个文件示例

#### journal_2025-12-26.md
```markdown
# Daily Journal - 2025-12-26

## [08:30] 💡 THOUGHT: LLM agents的内存管理
- 思考about how to handle context length for long-running agents
- 可能需要implement sliding window compression

## [10:15] ✅ WORK: Completed the journal skill design
- Finished prompt engineering for journal entries
- Set up file structure in docs/

## [11:45] 🔗 LINK: Twitter - Andrej Karpathy's latest post about scaling
- https://twitter.com/karpathy/status/...
- Insights about model training optimization

## [14:20] ✅ WORK: Code review for project X
- Merged 3 pull requests
- Fixed 2 critical bugs

## [16:30] 💡 THOUGHT: Potential integration with Obsidian
- Could use Obsidian plugins to auto-sync journal entries
- Create bidirectional links between journal and docs/
```

#### timeline_2025-12-26.md
```markdown
# Daily Timeline - 2025-12-26

## 📊 Summary
- **Total entries:** 5
- **Thoughts:** 2 | **Work items:** 2 | **Links:** 1
- **Time span:** 08:30 - 16:30 (8 hours of logged activity)

## 💡 Thoughts & Ideas
1. **08:30** - LLM agents的内存管理
   - Context length handling for long-running agents
   - Potential: sliding window compression

2. **16:30** - Potential integration with Obsidian
   - Auto-sync capability with Obsidian plugins
   - Bidirectional linking between journal and docs

## ✅ Completed Work
1. **10:15** - Journal skill design completion
2. **14:20** - Code review & bug fixes (3 PRs merged, 2 bugs fixed)

## 🔗 Shared Resources
- Andrej Karpathy's post on model training optimization
  - [Twitter link] - Insights about scaling

## 🎯 Key Insights
- Memory management in LLM agents remains a critical challenge
- Obsidian integration could enhance knowledge management workflow
- Productive day: 5 major entries across multiple categories
```

---

## 5. 完整使用流程

### 步骤1：初始化
```bash
# 创建journal文件夹（如果不存在）
mkdir -p journal
```

### 步骤2：配置Gemini命令
```bash
# 将journal.toml放入 .gemini/commands/
# 将journal-timeline.toml放入 .gemini/commands/
```

### 步骤3：记录日志
```bash
# 记录想法
gemini journal "我想到了一个关于RAG的优化方案"

# 记录工作完成
gemini journal "完成了API endpoint的实现"

# 记录链接
gemini journal "发现了一篇论文：https://arxiv.org/abs/..."
```

### 步骤4：生成时间线
```bash
# 生成今日时间线
gemini journal-timeline
```

### 步骤5：查看结果
```bash
# 查看原始日志
cat journal/journal_2025-12-26.md

# 查看时间线
cat journal/timeline_2025-12-26.md

# 或在MkDocs中浏览
mkdocs serve
```

---

## 6. 集成建议

### 6.1 与mkdocs集成
在 `mkdocs.yml` 中添加journal导航：
```yaml
nav:
  - Home: index.md
  - Docs: docs/
  - Journal: journal/
```

### 6.2 与Obsidian集成
在 `.obsidian/` 中配置vault识别journal文件夹，支持：
- 链接到docs/中的概念
- 标签系统 (#thought, #work, #link)
- 双向链接

### 6.3 自动化建议
可添加 GitHub Actions 或 cron job：
```bash
# 每天18:00自动生成时间线
0 18 * * * cd /path/to/repo && gemini journal-timeline
```

---

## 7. 技术考虑

### 数据安全
- Journal文件应包含在git中（可选通过.gitignore排除敏感信息）
- 使用git commit自动备份每日更新

### 扩展性
- 支持标签系统（#productivity, #learning, #idea）
- 支持搜索和过滤
- 支持按主题统计

### 隐私
- 可选加密敏感journal条目
- 选择性地在公开知识库中分享insights

---

## 总结表

| 问题 | 答案 |
|------|------|
| **如何触发** | Gemini命令: `gemini journal` 和 `gemini journal-timeline` |
| **Prompt写法** | 见第2节，分为两个command配置 |
| **需要脚本** | 可选：Python脚本用于更高级功能，Shell脚本作为CLI包装 |
| **存储文件数量** | 最少2个（journal + timeline）；扩展可有4-5个（周/月汇总） |
| **文件位置** | `journal/` 文件夹 |
| **文件名规则** | `journal_YYYY-MM-DD.md` / `timeline_YYYY-MM-DD.md` |
