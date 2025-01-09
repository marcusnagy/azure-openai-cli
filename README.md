# CLI for Azure Assistant

# Requirements / 要求

Environment Variables inside of `.env` file / 环境变量在 `.env` 文件中
```
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
```

To source the environment variables one can use the script as: / 要获取环境变量，可以使用以下脚本：
```bash
./local_env.sh
```

---

# Install Dependencies / 安装依赖

Install `uv` / 安装 `uv`

```bash
# With pip.
pip install uv
```

Install dependencies / 安装依赖
```bash
uv sync
```

Run linter / 运行代码检查工具
```bash
uv run --group lint ruff check
```

---

# Usage / 用法

Simple start use / 简单启动使用
```bash
uv run azure.py --start
```

To continue a conversation with a specific thread ID / 使用特定线程 ID 继续对话
```bash
uv run azure.py --start --thread <thread_id>
```

To specify a different assistant ID / 指定不同的助手 ID
```bash
uv run azure.py --start --assistant <assistant_id>
```

To get help / 获取帮助
```bash
uv run azure.py --help
```

To exit the conversation with the Assistant just type `exit` or `quit` / 要退出与助手的对话，只需输入 `exit` 或 `quit`

---

# Example / 示例

Start a new conversation and get the thread ID / 开始新对话并获取线程 ID
```bash
uv run azure.py --start
```

Continue a conversation with a specific thread ID / 使用特定线程 ID 继续对话
```bash
uv run azure.py --start --thread 1234567890
```

Start a conversation with a different assistant ID / 使用不同的助手 ID 开始对话
```bash
uv run azure.py --start --assistant asst_1234567890
```

---

# Development / 开发

To run the script locally, ensure you have the required environment variables set in a `.env` file. Then, you can run the script using the following command: / 要在本地运行脚本，请确保在 `.env` 文件中设置了所需的环境变量。然后，您可以使用以下命令运行脚本：
```bash
python azure.py --start
```

---