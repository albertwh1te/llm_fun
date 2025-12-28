---
name: journal-recorder
description: 记录想法、观点和感受到journal日志。当用户说"记录"、"记"后跟内容时触发。支持记录类型：想法(THOUGHT)、感受(FEELING)、灵感(IDEA)、学习(LEARNING)、笔记(NOTE)。注意：如果用户只是说"记录"或"记"而没有具体内容，则不需要使用此skill。
---

# Journal Recorder

记录想法和观点到 journal 当天文件。

## 记录格式

```
YYYY-MM-DD HH:MM 记录内容
TYPE

```

示例：
```
2025-12-26 03:23 今天确定了问题是手续费的问题
THOUGHT

2025-12-29 08:00 今天锻炼的效果很不错
FEELING
```

## 记录类型

| 类型 | 适用场景 |
|------|----------|
| THOUGHT | 思考、分析、总结 |
| FEELING | 情绪、感受、心情 |
| IDEA | 灵感、创意 |
| LEARNING | 学习心得、新知识 |
| NOTE | 普通笔记 |

## 使用方法

```bash
python3 scripts/record.py --journal-dir ./journal "记录内容" --type TYPE
```

## 响应风格

记录后给用户简短的鼓励或认可：
- 学习类：恭喜学到新知识！
- 反思类：失败是成功之母，继续加油！
- 灵感类：好想法！
- 感受类：记录心情很重要 💪

## 类型判断规则

- 提到"学习"、"学到"、"了解" → LEARNING
- 提到"感觉"、"觉得"、情绪词 → FEELING  
- 提到"想法"、"灵感"、"点子" → IDEA
- 默认 → THOUGHT
