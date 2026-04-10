# zsxq-skill

[![npm version](https://img.shields.io/npm/v/zsxq-cli.svg)](https://www.npmjs.com/package/zsxq-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

知识星球官方出品，由知识星球团队开发和维护 — 让人类和 AI Agent 都能在终端中操作知识星球。

[安装](#安装与快速开始) · [能做什么](#能做什么) · [Skills](#agent-skills) · [认证](#认证) · [命令](#功能详情) · [安全](#安全与风险提示使用前必读)

## 为什么选 zsxq-skill？

- **知识星球官方出品** — 由知识星球团队直接开发和维护，与平台同步更新
- **权限范围清晰** — 以你自己的账号身份运行，只能访问你有权限查看的内容（你加入或创建的星球），不越权
- **为 Agent 原生设计** — Skills 开箱即用，适配 Claude、Cursor 等主流 AI 工具
- **三分钟上手** — 三步完成安装，从安装到第一次操作只需几分钟
- **安全可控** — OAuth 2.0 授权，Token 存储在系统 Keychain，写入操作前必须用户确认

## 能做什么

安装并登录后，你可以直接用自然语言让 AI 帮你：

| 场景 | 示例 |
|------|------|
| 浏览星球 | "列出我加入的所有星球" |
| 搜索主题 | "在 XX 星球搜索关于 Python 的主题" |
| 查看主题 | "查看 XX 星球最新的 20 条主题" |
| 管理标签 | "列出 XX 星球的所有标签" |
| 发布主题 | "在 XX 星球发一条主题，内容是……" |
| 评论回答 | "回答 XX 星球里这条提问……" |
| 记录笔记 | "在我的知识星球笔记里记录……" |
| 查看足迹 | "查看我最近在各星球发过的主题" |
| 查看账号 | "查看我的知识星球账号信息" |

## 适合谁用

- 知识星球的**星主**：用 AI 快速回复提问、整理精华、管理主题标签
- 知识星球的**普通成员**：用 AI 搜索和整理星球内容，提升信息获取效率
- **开发者**：基于 zsxq-cli 和 MCP 工具构建自定义自动化流程

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

命令会输出一个链接和验证码，用手机或浏览器打开链接完成授权，CLI 自动检测并保存登录状态。

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

本工具可供 AI Agent 调用以自动化操作知识星球，存在模型幻觉、执行不可控、提示词注入等固有风险；授权登录后，AI Agent 将以你的账号身份在授权范围内执行操作，可能导致非预期的内容发布等后果，请谨慎使用。

工具已在多个层面启用默认安全保护（写入/删除操作前必须确认用户意图、Token 存储于系统 Keychain 不在终端明文输出），但上述风险仍然存在。

请充分知悉全部使用风险，使用本工具即视为你自愿承担相关责任。

---

## License

MIT
