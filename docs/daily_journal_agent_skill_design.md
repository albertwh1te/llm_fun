****# 🗓️ Daily Journal Agent Skill 设计方案

## 概述

基于你的需求，设计一套完整的每日记录系统，包含两个核心 Agent Skill：
1. **Journal Logger** - 随时记录想法、工作状态
2. **Timeline Generator** - 生成每日时间线流水账

---

## 📁 数据结构设计

### 文件组织

```
llm_fun/
├── journal/
│   ├── journal_2025-12-26.md      # 每日随机记录 (Obsidian Daily Note)
│   └── journal_2025-12-27.md
├── timeline/
│   ├── timeline_2025-12-26.md     # 每日时间线 (结构化流水账)
│   └── timeline_2025-12-27.md
└── .github/skills/
    ├── journal-logger/
    │   └── SKILL.md
    └── timeline-manager/
        └── SKILL.md
```

### Journal 文件格式 (`journal/journal_YYYY-MM-DD.md`)

```markdown
# Daily Journal - 2025-12-26

## [09:15] 💡 THOUGHT: 想到一个优化方案
- 可以用向量数据库加速搜索

## [10:00] 🎯 WORK: 开始写代码
- 任务: 实现用户认证模块

## [12:30] ☕ BREAK: 午餐

## [14:00] 📚 LEARN: 读了一篇论文
- Link: https://arxiv.org/xxx
- 关键点: Transformer优化技巧
```

### Timeline 文件格式 (`timeline/timeline_YYYY-MM-DD.md`)

```markdown
# Timeline - 2025-12-26

| 开始时间 | 结束时间 | 类型 | 活动 | 时长 |
|---------|---------|------|------|------|
| 09:00 | 10:00 | WORK | 代码review | 1h |
| 10:00 | 12:00 | WORK | 写用户认证模块 | 2h |
| 12:00 | 13:00 | BREAK | 午餐 | 1h |
| 13:00 | 15:30 | WORK | 调试bug | 2.5h |
| 15:30 | 16:00 | LEARN | 看技术文档 | 0.5h |

## 今日统计
- 📊 工作时间: 5.5h
- 📚 学习时间: 0.5h
- ☕ 休息时间: 1h
```

---

## 🔑 触发词设计

### 自然语言触发 (推荐)

| 触发场景 | 示例用语 | 动作 |
|---------|---------|------|
| 快速记录想法 | "记录一下", "记一下", "note", "想到了" | 追加到 journal |
| 开始任务 | "开始工作", "开始xxx", "doing xxx" | 记录开始时间 + 任务 |
| 结束任务 | "做完了", "结束", "done", "换个事情" | 询问是完成/暂停/并行，更新 timeline |
| 生成时间线 | "生成今日总结", "timeline", "今天做了什么" | 汇总 journal → timeline |
| 查看状态 | "现在在做什么", "当前任务" | 显示当前活动任务 |

### 状态机设计

```
[空闲] --"开始xxx"--> [工作中: xxx]
[工作中: xxx] --"做完了"--> [空闲] (记录完成)
[工作中: xxx] --"换个事情"--> [询问状态] --"完成了"--> [空闲]
                                        --"暂停了"--> [暂停: xxx]
                                        --"并行"--> [工作中: xxx + yyy]
```

---

## 🛠️ Agent Skill 实现

### Skill 1: Journal Logger

**路径**: `.github/skills/journal-logger/SKILL.md`

```markdown
---
name: Journal Logger
description: 快速记录想法、工作状态、学习笔记。触发词：记录、记一下、note、想到了
version: 1.0.0
---

# Journal Logger 指令

你是一个个人日志助手，帮助用户快速记录日常想法和工作状态。

## 触发条件
当用户说以下关键词时激活：
- "记录"、"记一下"、"note"
- "想到了"、"有个想法"
- "开始"、"做完了"、"换个事情"

## 记录类型
根据内容自动分类：
- 💡 THOUGHT: 想法、灵感
- 🎯 WORK: 工作任务
- 📚 LEARN: 学习笔记
- 🔗 LINK: 链接/资源
- ☕ BREAK: 休息

## 操作流程

### 快速记录
1. 获取当前时间 (`date +"%H:%M"`)
2. 判断记录类型
3. 追加到 `journal/journal_YYYY-MM-DD.md`
4. 回复确认（简短温馨）

### 开始任务
1. 记录开始时间和任务名称
2. 更新 `.current_task` 状态
3. 回复鼓励语

### 结束任务
1. 询问：完成/暂停/并行？
2. 计算时长
3. 写入 timeline
4. 清除/更新当前任务状态

## 回复风格
- 简短温馨，1-2句话
- 使用 emoji
- 开始工作时："加油！💪"
- 完成任务时："辛苦了！✅"
- 记录想法时："已记录 📝"

## 文件路径
- Journal: `journal/journal_$(date +%Y-%m-%d).md`
- Timeline: `timeline/timeline_$(date +%Y-%m-%d).md`
- 状态文件: `journal/.current_task.json` (可选)
```

### Skill 2: Timeline Manager

**路径**: `.github/skills/timeline-manager/SKILL.md`

```markdown
---
name: Timeline Manager
description: 管理每日时间线，生成工作流水账和统计。触发词：timeline、今天做了什么、每日总结
version: 1.0.0
---

# Timeline Manager 指令

你是时间管理助手，帮助用户追踪和分析每日时间分配。

## 触发条件
- "timeline"、"时间线"
- "今天做了什么"、"每日总结"
- "统计"、"分析今天"

## 核心功能

### 生成时间线
1. 读取当日 `journal/journal_YYYY-MM-DD.md`
2. 提取所有 WORK 类型记录
3. 计算时间区间和时长
4. 生成 markdown 表格
5. 输出到 `timeline/timeline_YYYY-MM-DD.md`

### 统计分析
按类型汇总时间：
- 工作时间
- 学习时间
- 休息时间
- 其他

### 周/月报表 (高级功能)
- 分析 `timeline/` 目录下所有文件
- 生成趋势图表数据
```

---

## 💡 最佳实践建议

### 1. 最小摩擦原则

| 方式 | 摩擦度 | 推荐场景 |
|------|--------|---------|
| 直接在 Copilot Chat 说"记录：xxx" | ⭐ 低 | 日常快速记录 |
| 终端 alias: `jl "想法"` | ⭐⭐ 更低 | 重度用户 |
| Obsidian 快捷键 | ⭐⭐⭐ 最低 | 已在 Obsidian 中 |

### 2. 状态追踪方案

**方案 A: 无状态 (推荐开始用)**
- 每次说"开始xxx"单独记录
- 说"做完了"时手动说明是哪个任务
- 优点：简单，无需维护状态

**方案 B: 有状态**
- 维护 `journal/.current_task.json`
```json
{
  "task": "写认证模块",
  "start_time": "2025-12-26T10:00:00",
  "type": "WORK"
}
```
- 说"做完了"自动知道是哪个任务
- 优点：更智能；缺点：需要额外逻辑

### 3. 回复示例

```
用户: 记录一下，刚想到可以用Redis缓存加速
助手: 📝 已记录 [09:15] 💡 THOUGHT

用户: 开始写代码了
助手: 💪 加油！已记录开始时间 09:20

用户: 做完了
助手: ✅ 辛苦了！09:20-11:45 (2h25m) 已写入时间线

用户: 今天做了什么
助手: 📊 今日统计:
- 工作: 5.5h
- 学习: 1h  
- 休息: 1h
详见 timeline/timeline_2025-12-26.md
```

---

## 🚀 实施步骤

### Phase 1: 基础版 (1-2小时)
1. 创建 `.github/skills/journal-logger/SKILL.md`
2. 测试基本记录功能
3. 手动生成 timeline

### Phase 2: 自动化 (2-3小时)
1. 创建 `.github/skills/timeline-manager/SKILL.md`
2. 实现自动时间线生成
3. 添加统计功能

### Phase 3: 优化 (可选)
1. 添加状态追踪 (current_task.json)
2. 创建 shell alias 快捷方式
3. 集成 Obsidian 快捷键
4. 添加周报/月报生成

---

## 📋 文件模板

### 新建 Journal 模板

```markdown
# Daily Journal - {{date}}

> 今日主题/目标: 

---

<!-- 记录会自动追加在下方 -->
```

### Timeline 模板

```markdown
# Timeline - {{date}}

| 开始时间 | 结束时间 | 类型 | 活动 | 时长 |
|---------|---------|------|------|------|

## 今日统计
- 📊 工作时间: 0h
- 📚 学习时间: 0h
- ☕ 休息时间: 0h

## 备注

```

---

## 🔧 辅助工具 (可选)

### Shell Alias

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias jl='echo "## [$(date +%H:%M)] 💡 THOUGHT: $1" >> ~/Dropbox/code/llm_fun/journal/journal_$(date +%Y-%m-%d).md && echo "📝 已记录"'
alias jw='echo "## [$(date +%H:%M)] 🎯 WORK: $1" >> ~/Dropbox/code/llm_fun/journal/journal_$(date +%Y-%m-%d).md && echo "💪 加油"'
```

使用: `jl "想到一个好点子"` 或 `jw "开始写代码"`

---

## 总结

这套设计的核心理念：
1. **最小摩擦** - 用自然语言触发，无需记忆复杂命令
2. **渐进式复杂度** - 从简单开始，按需添加功能
3. **双文件分离** - Journal 存原始记录，Timeline 存结构化数据
4. **Obsidian 友好** - 完全兼容 Daily Notes 插件

建议从 Phase 1 开始，用几天后再根据实际需求迭代优化。
