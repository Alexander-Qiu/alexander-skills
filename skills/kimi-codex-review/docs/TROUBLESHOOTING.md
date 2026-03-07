# Kimi Codex Review - 故障排查

## 常见问题

### 1. Codex CLI 未安装

**症状：**
```
Codex CLI not found
```

**解决：**
```bash
npm install -g @openai/codex
codex login
```

---

### 2. 网络连接超时

**症状：**
```
Codex review timed out after 120s
failed to refresh available models: timeout
```

**诊断：**
```bash
# 检查代理
echo $HTTPS_PROXY

# 测试连通性
curl -x http://127.0.0.1:7890 https://api.openai.com/v1/models
```

**解决：**
- 确保 clash 在运行，或手动设置代理：
```bash
export HTTPS_PROXY=http://127.0.0.1:7890
```

- 脚本会自动检测 clash 并设置代理

---

### 3. 认证失败

**症状：**
```
401 Unauthorized
Not authenticated
```

**解决：**
```bash
codex login
# 或
codex auth
```

---

### 4. 配额超限

**症状：**
```
quota exceeded
subscription quota limit
```

**解决：**
脚本会自动回退到 zenmux provider。确保设置了：
```bash
export ZENMUX_ONDEMAND_API_KEY="sk-ai-v1-..."
```

或强制使用 fallback：
```bash
./scripts/kimi-codex-review.sh --provider zenmux --model google/gemini-3-flash-preview --uncommitted
```

---

### 5. 不在 git 仓库中

**症状：**
```
Not in a git repository
```

**解决：**
必须在 git 仓库中运行 review 命令：
```bash
cd /your/git/repo
./scripts/kimi-codex-review.sh --uncommitted
```

---

## 调试模式

启用详细日志：
```bash
KIMI_CODEX_DEBUG=1 ./scripts/kimi-codex-review.sh --uncommitted
```

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/kimi-codex-review.sh` | 主脚本 |
| `scripts/select-codex-target.sh` | Fallback 选择逻辑 |
| `~/.codex/config.toml` | Codex 配置 |
| `~/.codex/auth.json` | 认证信息 |
