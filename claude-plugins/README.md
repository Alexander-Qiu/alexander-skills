# Claude Plugins 集合

Alexander Skills 的 Claude Code Plugins 集合，包含 **22 个精选插件**，提升你的 Claude Code 开发体验。

## 一键安装

如果你想安装 Alexander shared skills 和 Claude Code plugins，优先使用仓库根目录的统一安装器：

```bash
cd /mnt/data/qrz-dev/mem/alexander-skills
./install.sh --agent claude-code
```

本目录下的 `install.sh` 只负责 Claude Code plugins。

```bash
cd /mnt/data/qrz-dev/mem/alexander-skills/claude-plugins
./install.sh
```

脚本会自动：
1. 注册 4 个 marketplaces（claude-plugins-official, pua-skills, openai-codex, thedotmack）
2. 通过 `claude plugin install` 安装全部 22 个插件
3. 验证安装结果

安装完成后**重启 Claude Code** 生效。

## 包含的 Plugins

### 官方 Plugins (13个)

| Plugin | 描述 |
|--------|------|
| **agent-sdk-dev** | Agent SDK 开发工具包，用于创建和验证 Agent SDK 项目 |
| **claude-opus-4-5-migration** | 模型迁移工具，从 Sonnet 4.x/Opus 4.1 迁移到 Opus 4.5 |
| **code-review** | 自动化代码审查，多代理并行分析 PR |
| **commit-commands** | Git 工作流自动化，简化 commit、push 和 PR 创建 |
| **explanatory-output-style** | 教育性输出风格，解释实现选择和代码库模式 |
| **feature-dev** | 功能开发工作流，7阶段结构化开发流程 |
| **frontend-design** | 前端设计工具，创建生产级前端界面 |
| **hookify** | 自定义 Hooks 创建工具，防止不期望的行为 |
| **learning-output-style** | 学习模式输出风格，鼓励有意义的代码贡献 |
| **plugin-dev** | Plugin 开发工具包，7个专家技能辅助开发 |
| **pr-review-toolkit** | PR 审查工具集，专业评论、测试、错误处理分析 |
| **ralph-wiggum** | 自引用 AI 循环，迭代开发直到完成 |
| **security-guidance** | 安全提醒 Hook，监控 9 种安全模式 |

### Marketplace Plugins (1个)

| Plugin | 版本 | 描述 | 位置 |
|--------|------|------|------|
| **claude-mem** | 10.0.7 | 持久化内存系统，跨会话保留上下文 | `marketplace/claude-mem/` (完整项目) |

### 外部维护 Plugins

以下插件不再由本仓库 vendored / 维护，请直接使用上游仓库：

| Plugin | 维护方 | 安装方式 |
|--------|--------|----------|
| **codex** | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | `/plugin marketplace add openai/codex-plugin-cc` 然后 `/plugin install codex@openai-codex` |

## 快速安装

### 方法一：使用安装脚本（推荐）

```bash
cd /mnt/data/qrz-dev/mem/alexander-skills/claude-plugins
./install.sh
```

然后选择安装模式：
- **全局安装**：安装到 `~/.claude/plugins/`，所有项目可用
- **项目安装**：安装到当前目录的 `.claude/plugins/`，仅当前项目可用

### 方法二：手动复制

```bash
# 全局安装
mkdir -p ~/.claude/plugins/alexander-skills
cp -r /mnt/data/qrz-dev/mem/alexander-skills/claude-plugins/plugins/* ~/.claude/plugins/alexander-skills/

# 项目安装
mkdir -p ./.claude/plugins/alexander-skills
cp -r /mnt/data/qrz-dev/mem/alexander-skills/claude-plugins/plugins/* ./.claude/plugins/alexander-skills/
```

## 使用方法

安装完成后，Claude Code 会自动加载这些 plugins。你可以：

1. **查看所有 plugins**：在 Claude Code 中使用 `/plugin` 命令
2. **使用 plugin 命令**：例如 `/feature-dev` 启动功能开发工作流
3. **享受增强功能**：某些 plugins（如 security-guidance）会自动运行

## 更新 Plugins

要更新到最新版本：

```bash
cd /mnt/data/qrz-dev/mem/alexander-skills
git pull  # 如果有更新
./claude-plugins/install.sh  # 重新运行安装脚本
```

## 目录结构

```
claude-plugins/
├── README.md           # 本文件
├── install.sh          # 安装脚本
├── registry.json       # Plugin 注册表
├── plugins/            # 标准 plugins 目录 (13个)
│   ├── agent-sdk-dev/
│   ├── code-review/
│   └── ...
└── marketplace/        # 第三方完整插件项目
    └── claude-mem/     # 含源码、测试、文档的完整项目
        ├── plugin/     # 编译后的插件
        └── plugin/skills/mem-search/
```

## 每个 Plugin 的详细说明

### agent-sdk-dev
Agent SDK 开发工具包，提供：
- `/new-sdk-app` 命令：交互式创建新的 Agent SDK 项目
- `agent-sdk-verifier-py` 代理：验证 Python SDK 应用
- `agent-sdk-verifier-ts` 代理：验证 TypeScript SDK 应用

### claude-opus-4-5-migration
帮助迁移代码和提示：
- 自动迁移模型字符串
- 更新 beta headers
- 调整提示以适应 Opus 4.5

### code-review
自动化 PR 代码审查：
- 5个并行 Sonnet 代理分析
- CLAUDE.md 合规性检查
- Bug 检测
- 历史上下文分析
- 基于置信度的评分过滤误报

### commit-commands
Git 工作流自动化：
- `/commit`：简化 git commit
- `/commit-push-pr`：commit、push 并创建 PR
- `/clean_gone`：清理已删除的远程分支

### feature-dev
功能开发工作流：
- `/feature-dev`：7阶段引导式开发流程
- `code-explorer` 代理：代码库分析
- `code-architect` 代理：架构设计
- `code-reviewer` 代理：质量审查

### hookify
自定义 Hooks 创建工具：
- `/hookify`：从对话模式创建 hooks
- `/hookify:list`：列出配置的 hooks
- Python 核心规则引擎
- 多个实用示例

### plugin-dev
Plugin 开发工具包：
- `/plugin-dev:create-plugin`：8阶段引导式 plugin 创建
- 7个专家技能模块：
  - agent-development
  - command-development
  - hook-development
  - mcp-integration
  - plugin-settings
  - plugin-structure
  - skill-development

### pr-review-toolkit
PR 审查工具集：
- `/pr-review-toolkit:review-pr`：运行审查
- 6个专业代理：评论分析、测试分析、错误处理、类型设计、代码质量、代码简化

### ralph-wiggum
自引用 AI 循环：
- `/ralph-loop`：启动自主迭代循环
- `/cancel-ralph`：停止循环
- 适合复杂任务的迭代开发

### security-guidance
安全提醒 Hook：
- 自动监控 9 种安全模式
- 命令注入检测
- XSS 检测
- Eval 使用警告
- 危险 HTML 检测
- Pickle 反序列化警告
- OS.system 调用检测

### claude-mem
持久化内存系统：
- 跨会话保留上下文
- MCP 工具集成：`search`, `timeline`, `get_observations`
- 自动会话上下文捕获
- 后台工作服务

## 兼容性

- **Claude Code**: 所有 plugins 均兼容
- **平台**: Linux, macOS, Windows (WSL)
- **版本要求**: Claude Code 最新版本

## 许可证

各 plugin 保留其原始许可证：
- 官方 Plugins: 遵循各自 LICENSE 文件
- claude-mem: AGPL-3.0

## 贡献

欢迎提交 Issue 或 PR 来改进这些 plugins。

## 相关链接

- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Plugins](https://github.com/anthropics/claude-plugins)
- [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc)
- [alexander-skills](https://github.com/yourname/alexander-skills)
