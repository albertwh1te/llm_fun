# 📚 Claude Agent Skills 完整参考指南

## 什么是 Agent Skills？

**Agent Skills** 是模块化的功能扩展，用来增强 Claude 的能力。它们是有组织的文件夹，包含说明文档（SKILL.md）和辅助文件（脚本、模板等）。

### 核心特性：模型自动调用

Skills 最重要的特点是**模型自动调用**——Claude 会根据你的请求和 Skill 的描述自动决定是否使用某个 Skill，而不需要你显式调用（不像 Slash Commands 需要你输入 `/command`）。

---

## 三个 Skill 存储位置

### 1. 个人 Skills（Personal Skills）
```
~/.claude/skills/my-skill-name/
```
- 在你所有项目中都可用
- 用于个人工作流和实验
- 适合跨项目通用的能力

### 2. 项目 Skills（Project Skills） ⭐
```
.claude/skills/my-skill-name/
```
- 存在项目根目录中，可以提交到 git
- 团队成员拉取项目后自动可用
- **推荐用于团队合作和项目特定功能**

### 3. 插件 Skills（Plugin Skills）
```
Claude Code 插件目录
```
- 随 Claude Code 插件一起打包
- 安装插件后自动可用

---

## 创建 Skill 的完整步骤

### 步骤 1：创建文件夹结构

项目 Skill 示例：
```
.claude/skills/skill-name/
├── SKILL.md              # 必需 - 主说明文件
├── reference.md          # 可选 - 参考资料
├── examples.md           # 可选 - 使用示例
├── scripts/
│   └── helper.py         # 可选 - 辅助脚本
└── templates/
    └── template.txt      # 可选 - 模板文件
```

### 步骤 2：编写 SKILL.md

这是 Skill 的核心文件，必须包含 YAML 前置信息：

```yaml
---
name: skill-name
description: 这个 Skill 做什么，什么时候使用它
allowed-tools: Read, Grep, Glob  # 可选 - 限制工具
---

# Skill 标题

## 说明
清晰的步骤和指导...

## 使用示例
具体的使用案例...

## 最佳实践
相关的建议和技巧...
```

### 必需字段

| 字段 | 说明 | 限制 |
|------|------|------|
| `name` | 小写字母、数字、连字符 | 最多 64 个字符 |
| `description` | 明确说明做什么 + 何时使用 | 最多 1024 个字符 |

### 可选字段

| 字段 | 说明 |
|------|------|
| `allowed-tools` | 限制 Skill 能使用的工具（仅 Claude Code） |
| `version` | Skill 版本号 |

---

## Description 写法最佳实践

Description 是最关键的部分——它决定了 Claude 什么时候会识别和使用你的 Skill。

### ❌ 不好的写法

```
处理文档
帮助管理文件
通用助手
```

**问题**：太模糊，Claude 无法识别使用场景。

### ✅ 好的写法

```
从 PDF 文件提取文本和表格、填充表单、合并文档。当你处理 PDF 文件、需要表单填充或文档合并时使用。
```

**优点**：
- 明确说明能力
- 包含触发关键词
- 描述使用时机

### 写 Description 的公式

```
[具体动作] [输入类型] [输出类型]。当 [触发场景] 时使用。
```

**示例**：
> 从 Markdown 文件中提取代码块并创建可运行的脚本。当需要从文档中提取代码或自动化文档处理时使用。

---

## 限制工具访问（allowed-tools）

用 `allowed-tools` 限制 Skill 能使用的工具，这对安全性和范围控制很重要：

```yaml
---
name: safe-reader
description: 安全地读取文件。当需要查看代码或文档内容时使用。
allowed-tools: Read, Grep, Glob
---
```

### 常用工具组合

**只读操作**：
```
allowed-tools: Read, Grep, Glob
```

**文件修改**：
```
allowed-tools: Read, Write, Edit, Bash
```

**网络操作**：
```
allowed-tools: WebFetch, WebSearch
```

**完整工具列表**：
- `Read` - 读取文件
- `Write` - 创建文件
- `Edit` - 编辑文件
- `Glob` - 查找文件
- `Grep` - 搜索文本
- `Bash` - 执行命令
- `WebFetch` - 获取网页
- `WebSearch` - 搜索网络

### ⚠️ 重要限制

`allowed-tools` 仅在 **Claude Code** 中有效，Agent SDK 不支持此功能。

---

## 实际例子：完整的 Skill

### 例子：Commit 信息生成器

```
.claude/skills/commit-helper/
└── SKILL.md
```

**SKILL.md 内容**：

```yaml
---
name: generating-commit-messages
description: 根据 git diff 生成清晰的 commit 信息和详细说明。当你准备提交代码或需要写 commit 信息时使用。
allowed-tools: Bash, Read
---

# 生成 Commit 信息

## 使用说明

1. 运行 `git diff --staged` 查看暂存区的变化
2. 分析变化的类型和影响
3. 生成 commit 信息：
   - **摘要行**：< 50 个字符，说明是什么改变了
   - **详细描述**：解释为什么做这个改变
   - **Footer**：关闭相关 issue

## 使用示例

### 示例 1：功能添加

用户：「我添加了新的错误处理。」

输出：
```
feat: Add error handling for network timeouts

- Implement retry logic with exponential backoff
- Log detailed error messages for debugging
- Update error boundaries in React components

Closes #123
```

### 示例 2：Bug 修复

用户：「修复了登录页面的样式问题。」

输出：
```
fix: Correct login form layout on mobile devices

- Adjust flexbox properties for responsive design
- Fix padding inconsistencies in form inputs
- Test on iOS Safari

Fixes #456
```

## 最佳实践

- ✅ 使用现在时态："Add feature" 而不是 "Added feature"
- ✅ 说明"是什么"和"为什么"，不说"怎么做"
- ✅ 保持摘要行简洁（< 50 字符）
- ✅ 在详细说明中使用 bullet points
- ❌ 避免过长或过于技术性的说明
- ❌ 不要在摘要中包含代码

## 版本历史
- v1.0.0 (2025-12-25): 初始版本
```

---

## Skills vs Slash Commands 对比

这两者是不同的工具，用于不同场景：

| 特性 | Skills | Slash Commands |
|------|--------|-----------------|
| **调用方式** | 模型自动调用 | 用户显式调用 (`/command`) |
| **发现方式** | Claude 基于描述判断 | 必须记住命令名称 |
| **使用场景** | 扩展 Claude 的能力 | 快速工具/快捷方式 |
| **复杂度** | 大型多步操作 | 简单快速操作 |
| **示例** | 生成 commit 信息、处理 PDF、连接知识库 | 打开文件、显示帮助、快速转换 |

**何时选择**：
- **用 Skill**：当操作需要 Claude 的智能判断和上下文理解
- **用 Command**：当操作是固定的、用户会主动触发的

---

## 调试：Skill 没有被触发

如果你的 Skill 没有被识别和使用，按顺序检查：

### 检查清单

```
□ Description 是否足够具体？
  → 太模糊或太通用会导致无法被识别
  → 应该包含"什么时候使用"的信息

□ 文件路径是否正确？
  - 个人 Skill: ~/.claude/skills/skill-name/SKILL.md
  - 项目 Skill: .claude/skills/skill-name/SKILL.md

□ YAML 前置信息语法是否正确？
  → 检查冒号、缩进、引号

□ 文件名是否正确？
  → 必须是 SKILL.md（大写）

□ 重启 Claude Code
  → 有时新 Skill 需要重新启动才会加载
```

### 运行调试命令

```bash
# 查看加载错误
claude --debug

# 检查 Skill 是否被识别
ls -la .claude/skills/
```

### 常见问题排查

**问题**：Claude 识别到 Skill 但没有使用
- **原因**：description 太模糊
- **解决**：添加更多具体的触发关键词和使用场景

**问题**：Skill 文件存在但无法加载
- **原因**：YAML 语法错误或路径问题
- **解决**：检查缩进、冒号、引号

**问题**：Tool restriction 没有生效
- **原因**：你在 Agent SDK 中使用（不支持）
- **解决**：`allowed-tools` 仅在 Claude Code 中有效

---

## 项目中现有的 Skills

这个项目已经有以下 Skill：

### knowledge-connector
```
.claude/skills/knowledge-connector/
```
- **用途**：发现和链接知识库中的相关概念
- **何时使用**：当你想找到文档之间的关系、改进交叉引用、构建知识地图时
- **关键特性**：
  - 发现隐含的概念连接
  - 建议缺失的交叉引用
  - 改进知识库导航

---

## 创建自己的 Skill：快速指南

### 5 分钟快速创建

1. **创建目录**：
   ```bash
   mkdir -p .claude/skills/my-skill
   ```

2. **写 SKILL.md**：
   ```yaml
   ---
   name: my-skill
   description: 清晰的描述 + 使用场景
   ---

   # My Skill

   ## 说明
   步骤和指导...
   ```

3. **测试**：
   - 在 Claude Code 中描述你的需求
   - Claude 会自动识别并使用 Skill

4. **改进**：
   - 如果没被识别，改进 description
   - 添加具体的 examples
   - 迭代优化

---

## 最佳实践总结

✅ **做这些**
- 写清晰具体的 description
- 包含 trigger keywords（关键词）
- 提供具体的使用示例
- 添加版本历史
- 保持 Skill 专注（一个能力 = 一个 Skill）

❌ **避免这些**
- 过于通用的描述
- 缺少"何时使用"信息
- 一个 Skill 做太多事
- 忘记文件夹结构

---

## 更多资源

- **官方 Claude Code Skills 文档**：https://code.claude.com/docs/en/skills
- **Agent Skills 概览**：https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Agent SDK 中的 Skills**：https://docs.claude.com/en/docs/agent-sdk/skills
- **公开 Skills 仓库**：https://github.com/anthropics/skills
- **Agent Skills 深度分析**：https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- **第一原理深度解析**：https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

## 版本历史
- v1.0.0 (2025-12-25): 初始发布 - 完整的 Agent Skills 参考指南
