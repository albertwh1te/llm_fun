[]()# 🚀 部署实战：将国产大模型 Doubao-Seed-Code 接入 Claude Code

本指南将带你一步步在本地环境中部署 Claude Code，并将其底层模型替换为字节跳动的 **Doubao-Seed-Code**。通过这种方式，你可以以极低的成本享受顶级的 AI 编程体验。

---

## 📋 准备工作

在开始之前，请确保你满足以下条件：
1.  **Node.js 环境**：已安装 Node.js (推荐 v18 或更高版本)。
2.  **豆包 API Key**：前往 [火山引擎](https://www.volcengine.com/) 申请 `doubao-seed-code-preview-latest` 模型的 API Key。
3.  **终端工具**：Mac/Linux 终端或 Windows WSL。

---

## 🛠️ 详细部署步骤

### 第一步：创建项目并安装 Claude Code 📦

我们需要在一个独立的目录中安装 Claude Code，以免污染全局环境。

```bash
# 1. 创建并进入项目目录
mkdir ~/claude-model
cd ~/claude-model

# 2. 初始化 npm 项目 (一路回车即可)
npm init -y

# 3. 安装 Claude Code 官方包
npm install @anthropic-ai/claude-code
```

### 第二步：创建专属配置目录 📂

为了区分官方 Claude 和我们魔改的豆包版配置，我们创建一个独立的配置文件夹。

```bash
# 在项目根目录下创建配置文件夹
mkdir .claude-doubao
```

### 第三步：编写启动脚本 (核心步骤) 📝

我们将创建一个 Shell 脚本来“劫持” Claude Code 的配置，使其连接到豆包的服务器。

1.  **创建存放脚本的目录：**

    ```bash
    mkdir ~/claude-model/bin
	    ```

2.  **创建并编辑脚本文件：**

    使用你喜欢的编辑器 (如 `vim` 或 `nano`) 创建 `~/claude-model/bin/claude-doubao` 文件。

    ```bash
    nano ~/claude-model/bin/claude-doubao
    ```

3.  **写入以下内容 (直接复制粘贴)：**

    ⚠️ **注意**：请将 `YOUR_DOUBAO_API_KEY` 替换为你真实的 API Key。

    ```bash
    #!/usr/bin/env bash
    # Wrapper for Claude Code CLI using Doubao API
    
    # 指向我们刚刚安装的 claude 可执行文件
    CLAUDE_BIN="$HOME/claude-model/node_modules/.bin/claude"
    
    # --- 核心配置区 ---
    # 注入豆包的 API Key (填写你的 Key)
    export ANTHROPIC_AUTH_TOKEN="YOUR_DOUBAO_API_KEY"
    
    # 强制将 Base URL 指向火山引擎的兼容接口
    export ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/api/compatible"
    
    # 指定使用的模型名称
    export ANTHROPIC_MODEL="doubao-seed-code-preview-latest"
    
    # 设置超长超时时间 (防止生成长代码时断开，单位毫秒)
    export API_TIMEOUT_MS=3000000
    
    # 指定配置文件目录 (避免与官方配置冲突)
    export CLAUDE_CONFIG_DIR="$HOME/claude-model/.claude-doubao"
    
    # --- 启动 ---
    exec "$CLAUDE_BIN" "$@"
    ```

4.  **保存并退出编辑器。**

5.  **赋予脚本执行权限：**

    ```bash
    chmod +x ~/claude-model/bin/claude-doubao
    ```

### 第四步：配置环境变量 🌐

为了让你在任何目录下都能直接输入 `claude-doubao` 来启动，我们需要将脚本目录加入到系统 PATH 中。

1.  **编辑你的 Shell 配置文件** (通常是 `~/.bashrc` 或 `~/.zshrc`)：

    ```bash
    # 如果你是 macOS 用户 (使用 Zsh)
    nano ~/.zshrc
    
    # 如果你是 Linux 用户 (使用 Bash)
    nano ~/.bashrc
    ```

2.  **在文件末尾添加以下一行：**

    ```bash
    export PATH="$HOME/claude-model/bin:$PATH"
    ```

3.  **使配置立即生效：**

    ```bash
    source ~/.zshrc  # 或 source ~/.bashrc
    ```

---

## ✅ 验证与使用

现在，部署已经完成！让我们来测试一下。

### 1. 检查版本
在终端输入以下命令，如果能看到 Claude Code 的版本号，说明安装成功。

```bash
claude-doubao --version
```

### 2. 开始使用
找一个你想写代码的目录（或者新建一个），然后直接运行：

```bash
# 新建测试目录
mkdir ~/space-invaders
cd ~/space-invaders

# 召唤 AI 程序员
claude-doubao
```

现在，你应该能看到 Claude Code 的交互界面，你可以对它说：
> "请帮我用 Python 写一个简单的贪吃蛇游戏。"

它会开始思考（Chain of Thought），然后为你生成代码。所有的 API 请求都会走火山引擎的通道，价格实惠且稳定！

---

## 🧩 进阶技巧：双开模式

通过这种方式部署，你其实拥有了“双系统”：

*   输入 **`claude-doubao`** ➡️ 使用 **豆包模型** (便宜、稳定、中文友好)。
*   输入 **`claude`** ➡️ 使用 **官方 Claude 模型** (如果你在全局安装过，且有官方 Key 的话)。

两者互不干扰，配置隔离。祝你在 AI 编程的世界里玩得开心！🚀
