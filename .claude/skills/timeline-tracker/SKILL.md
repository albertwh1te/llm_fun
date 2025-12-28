---
name: timeline-tracker
description: 时间记录与时间线生成工具。当用户提到以下场景时使用：(1) 开始/完成任务并追踪时间 (2) 记录睡眠和休息 (3) 查询今天做了什么。触发词：开始、做完了、timeline、今天做了什么、这周做了什么、睡眠记录。注意：如果用户只是说"记录"或"记"，则不需要添加timeline记录。
---

# Timeline Tracker

时间记录与流水账生成助手。自动追踪工作任务时长，直接写入timeline表格。

## 目录结构

```
timeline/
  timeline_YYYY-MM-DD.md   # 每日时间线流水账（表格格式）
  .current_task.json       # 当前任务状态
```

## 快速响应指南

| 用户说 | 动作 | 响应示例 |
|--------|------|----------|
| 记录：想到一个好点子 | **不添加timeline记录** | 好的，记住了 |
| 记：XXX | **不添加timeline记录** | 好的，记住了 |
| 开始写代码 | 调用 start 命令 | 💪 加油！已记录开始时间 09:30 |
| 做完了 | 调用 finish 命令 | ✅ 辛苦了！09:30-11:45 (2h15m) |
| 换个事情 | 先询问上个任务状态 | 上个任务是完成还是暂停？ |
| 我从7点睡到12点 | 调用 sleep 命令 | 😴 睡了5小时，注意休息！ |
| 今天做了什么 | 调用 today 命令 | 显示统计摘要 |
| 这周做了什么 | 调用 weekly 命令 | 📊 显示周报 |

## 记录类型

| Emoji | 类型 | 场景 |
|-------|------|------|
| 🎯 | work | 工作任务 |
| ✅ | done | 完成 |
| 📚 | learn | 学习笔记 |
| ☕ | break | 休息 |
| 😴 | sleep | 睡眠 |

## 脚本使用

### 开始任务

```bash
python3 scripts/timeline_logger.py --base-dir ./timeline start "<task_name>"
```

### 完成任务

```bash
python3 scripts/timeline_logger.py --base-dir ./timeline finish [--status done|pause]
```

### 记录睡眠

```bash
python3 scripts/timeline_logger.py --base-dir ./timeline sleep "7:00" "12:00"
```

### 今日摘要

```bash
python3 scripts/timeline_logger.py --base-dir ./timeline today
```

### 周报

```bash
python3 scripts/timeline_logger.py --base-dir ./timeline weekly
```

## 智能提醒

- 工作超过4小时：提醒休息
- 睡眠不足6小时：提醒注意休息
- 有未完成任务时开始新任务：提示先处理
