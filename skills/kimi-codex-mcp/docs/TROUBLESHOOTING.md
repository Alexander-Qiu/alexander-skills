# Kimi Codex MCP 故障排查指南

## 常见问题

### 1. MCP 调用超时 / 网络连接失败

#### 症状
- 调用 `codex()` 工具时返回错误：`call-codex.sh timed out after 30s`
- 或看到错误：`failed to refresh available models: timeout waiting for child process to exit`
- Codex CLI 单独执行也卡住或超时

#### 诊断步骤

**Step 1: 检查代理环境变量**
```bash
echo "HTTP_PROXY: $HTTP_PROXY"
echo "HTTPS_PROXY: $HTTPS_PROXY"
```

如果输出为空，说明代理未设置。

**Step 2: 检查 Clash 是否运行**
```bash
pgrep -x clash
# 或
pgrep -a clash
```

**Step 3: 测试 API 连通性**
```bash
# 无代理测试（应该失败或超时）
timeout 5 curl https://api.openai.com/v1/models

# 有代理测试（应该返回 401，说明网络通但需认证）
export HTTPS_PROXY=http://127.0.0.1:7890
timeout 5 curl -s -o /dev/null -w "%{http_code}" https://api.openai.com/v1/models
```

#### 根本原因
Codex 需要连接 OpenAI API (`api.openai.com`)，如果网络不通或代理未设置，会导致连接超时。

#### 解决方案

**方案 A: 临时设置环境变量（当前终端）**
```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export ALL_PROXY=socks5://127.0.0.1:7891

# 然后重启 Kimi CLI
```

**方案 B: 修改启动脚本（永久）**

编辑 `scripts/start-native-codex-mcp.sh`，在文件开头添加：

```bash
#!/bin/bash
set -euo pipefail

# 自动检测并设置代理（如果 clash 在运行）
if pgrep -x clash > /dev/null 2>&1; then
    export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
    export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"
    export ALL_PROXY="${ALL_PROXY:-socks5://127.0.0.1:7891}"
    export http_proxy="${http_proxy:-http://127.0.0.1:7890}"
    export https_proxy="${https_proxy:-http://127.0.0.1:7890}"
    export all_proxy="${all_proxy:-socks5://127.0.0.1:7891}"
fi

# ... 原有代码
```

**方案 C: 使用环境文件**

创建 `~/.codex/codex-mcp.env`：
```bash
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=socks5://127.0.0.1:7891
```

#### 验证修复

```bash
# 测试 Codex CLI 直连
codex exec --skip-git-repo-check "Say hello"

# 测试 MCP 调用
kimi -yp "Use codex tool to say hello"
```

---

### 2. 其他常见问题

#### 认证失败
```
401 Unauthorized
```
- 检查 `~/.codex/auth.json` 是否存在
- 运行 `codex login` 重新登录

#### 模型配额超限
```
quota exceeded
subscription quota limit
```
- 配置 fallback provider（见 SKILL.md）
- 或使用 `route=ondemand-gemini`

---

## 调试模式

启用详细日志：
```bash
export KIMI_CODEX_DEBUG=1
```

这将输出更多诊断信息到 stderr。

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/start-native-codex-mcp.sh` | MCP server 启动脚本 |
| `scripts/call-codex.sh` | 底层调用脚本 |
| `~/.codex/codex-mcp.env` | 环境变量配置 |
| `~/.codex/config.toml` | Codex 配置 |
| `~/.codex/auth.json` | 认证信息 |
