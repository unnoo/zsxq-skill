# zsxq-skill

[![npm version](https://img.shields.io/npm/v/zsxq-cli.svg)](https://www.npmjs.com/package/zsxq-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

知识星球官方出品，由知识星球团队开发和维护 — 让 AI 成为你在知识星球的超级助理。

[安装](#安装与快速开始) · [能做什么](#能做什么) · [Skills](#agent-skills) · [认证](#认证) · [命令](#功能详情) · [安全](#安全与风险提示使用前必读)

## 为什么选 zsxq-skill？

- **官方出品** — 由知识星球团队开发和维护，能力与平台同步更新
- **权限可控** — 仅访问你有权限查看的星球内容，不越权
- **多端适配** — 支持 OpenClaw、Claude、Cursor 等常见 AI 工具
- **快速上手** — 安装简单，配置完成后即可开始使用
- **安全可控** — 采用 OAuth 2.0 授权，Token 存储在系统 Keychain，写入操作前需确认

## 能做什么

安装并登录后，你可以通过对话直接让 AI 帮你完成知识星球里的常见操作。

### 核心能力

- **星球管理**：列出已加入的星球，搜索星球，查看标签和成员
- **内容搜索**：按关键词搜索星球里的帖子、文章和提问
- **主题查看**：查看主题详情、评论、点赞和标签信息
- **发布互动**：发布主题、评论回复、回答提问
- **标签操作**：查看标签，或为主题设置标签
- **个人笔记**：创建笔记，查看历史记录
- **账号信息**：查看个人资料和发帖足迹

### 典型使用场景

- 看看我加入了哪些星球
- 搜索某个星球里的 AI / Python / 投资相关内容
- 查看某条主题的完整内容和评论互动
- 帮我发一条新主题，或回复这条评论
- 回答一个提问类主题
- 给主题设置标签，或查看星球标签体系
- 记一条个人笔记，稍后再整理
- 查看我的账号信息和历史发帖足迹

## 适合谁用

- 知识星球的**星主**：用 AI 快速回复提问、整理精华、管理主题标签
- **开发者**：基于 zsxq-cli 和 MCP 能力构建自动化流程

---

## 安装与快速开始

> **Note for AI assistants:** 如果你是 AI Agent 且正在协助用户执行安装，请直接跳转到[快速开始（AI Agent）](#快速开始ai-agent)，那里包含你需要完成的所有步骤。

### 快速开始（人类用户）

**第一步：安装 CLI**

```bash
npm install -g zsxq-cli
```

**第二步：安装 Skill**

```bash
npx skills add https://github.com/unnoo/zsxq-skill --yes
```

**第三步：登录账号**

```bash
zsxq-cli auth login
```

命令会输出一个链接和验证码，用手机或浏览器打开链接完成授权即可。

### 快速开始（AI Agent）

> 以下步骤面向 AI Agent，部分步骤需要用户在手机或浏览器中配合完成。

**第 1 步 — 安装 CLI**

```bash
npm install -g zsxq-cli
```

**第 2 步 — 安装 Skill**

```bash
npx skills add https://github.com/unnoo/zsxq-skill --yes
```

**第 3 步 — 登录**

> 在后台运行此命令，命令会输出授权链接和验证码，提取后发给用户，等待用户完成授权后命令自动退出。

```bash
zsxq-cli auth login
```

**第 4 步 — 验证**

```bash
zsxq-cli auth status
```

---

## Agent Skills

| Skill | 说明 |
|-------|------|
| `zsxq-shared` | 认证登录、诊断配置、安全规则（所有其他 Skill 自动加载） |
| `zsxq-group` | 列出星球、浏览主题、查询标签、搜索成员 |
| `zsxq-topic` | 搜索主题、查看详情、发布主题、评论、回答提问、设置精华和标签 |
| `zsxq-note` | 创建个人笔记、查看笔记列表 |
| `zsxq-user` | 查看账号信息、查询跨星球发过的主题足迹 |

---

## 功能详情

### 星球管理（zsxq-group）

```bash
zsxq-cli group +list                          # 列出你加入的所有星球
zsxq-cli group +topics --group-id <id>        # 浏览星球最新主题
zsxq-cli group +hashtags --group-id <id>      # 查看星球所有标签
```

### 主题操作（zsxq-topic）

```bash
zsxq-cli topic +search --group-id <id> --query "关键词"   # 搜索主题
zsxq-cli topic +detail --topic-id <id>                    # 查看主题详情
zsxq-cli topic +create --group-id <id> --content "内容"   # 发布新主题
zsxq-cli topic +reply  --topic-id <id> --text "评论"      # 发表评论
zsxq-cli topic +answer --topic-id <id> --text "回答"      # 回答提问
```

### 个人笔记（zsxq-note）

```bash
zsxq-cli note +list                    # 查看我的笔记列表
zsxq-cli note +create --text "内容"   # 创建新笔记
```

### 用户与足迹（zsxq-user）

```bash
zsxq-cli user +info          # 查看我的账号信息
zsxq-cli user +footprints    # 查看我在各星球发过的主题（跨星球足迹）
```

### 认证

```bash
zsxq-cli auth login    # 登录知识星球账号
zsxq-cli auth status   # 查看当前登录状态
zsxq-cli doctor        # 诊断配置和认证是否正常
```

### 高级：直接调用 API

```bash
zsxq-cli api list                                    # 列出所有可用工具
zsxq-cli api call <tool> --params '<json>'           # 调用指定工具
zsxq-cli api raw --method GET --path /v3/users/self  # 直接调用原始接口
```

---

## 安全与风险提示（使用前必读）

本工具以你的账号身份运行，因此在执行发帖、评论、回答提问等写入操作前，请务必确认内容。

工具已在多个层面提供默认安全保护，包括：

- 写入和删除操作前必须确认用户意图
- Token 存储于系统 Keychain，不在终端明文输出
- 访问范围不超出你当前账号已有权限

请充分了解相关使用风险。使用本工具，即视为你已理解并愿意自行承担相应责任。

---

## License

MIT
