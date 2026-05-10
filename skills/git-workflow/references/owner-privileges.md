# Owner Privileges

**Alexander Qiu** (`ruizhi_qiu@foxmail.com`, 仓库所有者) 有以下特权：

| 特权 | 说明 |
|------|------|
| 直接 push 到 main | 无需创建 PR，可直接 `git push origin main` |
| 本地批量合并 | 可在本地合并多个已验证的 feature 分支后统一推送 |
| 默认推送行为 | 推送时默认直接向 main 分支推送 |

**前提条件：**
- 每个 feature 分支都**已通过所有验证**（测试通过、功能正常）
- 合并前在本地再次验证 main 分支功能正常
- 合并后确保 `git status` 显示 working tree clean

**推荐流程：**
```bash
# 1. 确保本地 main 最新
git checkout main
git pull origin main

# 2. 依次合并已验证的 feature 分支
git merge feature/skill-a  # 已验证的分支 A
git merge fix/skill-b      # 已验证的分支 B

# 3. 最终验证
npm run build  # 如有构建步骤
npm test       # 如有测试

# 4. 直接推送到 remote main
git push origin main

# 5. 清理本地已合并的分支
git branch -d feature/skill-a
git branch -d feature/skill-b
```

详见 [CONTRIBUTING.md](../../CONTRIBUTING.md) 获取完整规则。
