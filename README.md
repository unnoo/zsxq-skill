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

- **星球管理**：列出已加入的星球，搜索星球，查看标签、成员和专栏
- **内容搜索**：按关键词搜索星球里的帖子、文章和提问
- **主题查看**：查看主题详情、评论、点赞和标签信息
- **发布互动**：发布主题、编辑主题、评论回复、回答提问
- **精华与标签**：设置/取消精华，为主题打标签，管理专栏收录
- **个人笔记**：创建、编辑、查看、删除笔记
- **账号信息**：查看个人资料、发帖足迹、提交 NPS 反馈
- **场景编排**：多步骤运营场景（每日巡场、评论运营、日报周报、海报/视频生成等）

### 典型使用场景

- 看看我加入了哪些星球
- 搜索某个星球里的 AI / Python / 投资相关内容
- 查看某条主题的完整内容和评论互动
- 帮我发一条新主题，或回复这条评论
- 回答一个提问类主题
- 给主题设置标签、设为精华，或收录到专栏
- 记一条个人笔记，稍后再整理
- 查看我的账号信息和历史发帖足迹

**场景化运营**（一句话触发多步骤编排）：

- 「每日巡场」— 自动汇总今天新内容、待处理提问和评论
- 「整理评论区问题给我回复」— 找出未回复评论并起草回复
- 「做本周运营周报」— 统计新增/活跃/精华，生成结构化周报
- 「生成星球日报海报」— 把内容精选做成 PNG 海报图片
- 「把帖子做成视频」— 把星球内容转成竖版动画视频

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

只需安装**一个** `zsxq` Skill，即可获得全部能力：

| 能力 | 说明 |
|-------|------|
| 认证与错误排查 | 认证登录、诊断配置、常见错误处理 |
| 星球管理 | 列出星球、浏览主题、查询标签、搜索成员、管理专栏 |
| 主题操作 | 搜索主题、查看详情、发布/编辑/删除主题、评论回复、回答提问、精华与标签管理、专栏收录 |
| 个人笔记 | 创建、编辑、查看、删除笔记 |
| 用户信息 | 查看账号信息、查询跨星球足迹、提交 NPS 反馈 |
| 场景编排 | 12 个多步骤运营场景（巡场、评论运营、日报周报、海报/视频生成、负面监控等） |

Skill 内部按三层路由执行：**场景模式**（命中场景 → 按编排执行）→ **原子操作**（命中已知命令 → 直接调用）→ **探索模式**（未命中 → 通过 CLI 发现能力）。所有命令细节和参数均由 28 个 reference 文档独立承载，SKILL.md 只负责路由和索引。

> 从旧版（`zsxq-shared` / `zsxq-group` / `zsxq-topic` / `zsxq-user` / `zsxq-note` 五件套）升级的用户，安装新版后直接对 AI 说「检查并迁移旧版知识星球 skill」，AI 会先扫描报告、经你确认后再清理。

---

## 功能详情

### 星球管理（group）

```bash
zsxq-cli group +list                          # 列出你加入的所有星球
zsxq-cli group +topics --group-id <id>        # 浏览星球最新主题
zsxq-cli group +hashtags --group-id <id>      # 查看星球所有标签
```

**专栏与成员：**

```bash
# 专栏管理（通过 api raw）
zsxq-cli api raw --method GET --path /v2/groups/<id>/columns         # 列出星球专栏
zsxq-cli api raw --method POST --path /v2/groups/<id>/columns \      # 创建专栏 ⚠️
  --body '{"name":"专栏名称"}'

# 成员管理（通过 api raw）
zsxq-cli api raw --method GET --path /v2/groups/<id>/members         # 查看成员列表
```

**API 调用：**

```bash
zsxq-cli api call search_groups --params '{"keyword":"搜索词"}'        # 搜索星球
zsxq-cli api call search_group_members --params '{"group_id":<id>,"keyword":"昵称"}'  # 搜索成员
```

### 主题操作（topic）

```bash
zsxq-cli topic +search --group-id <id> --query "关键词"   # 搜索主题
zsxq-cli topic +detail --topic-id <id>                    # 查看主题详情
zsxq-cli topic +create --group-id <id> --text "内容"      # 发布新主题 ⚠️
zsxq-cli topic +edit   --topic-id <id> --text "新内容"    # 编辑主题 ⚠️
zsxq-cli topic +reply  --topic-id <id> --text "评论"      # 发表评论 ⚠️
zsxq-cli topic +answer --topic-id <id> --text "回答"      # 回答提问 ⚠️
```

**精华、标签与专栏收录：**

```bash
# 精华管理（api call）
zsxq-cli api call set_topic_digested \
  --params '{"topic_id":<id>,"digested":true}'            # 设为精华 ⚠️
zsxq-cli api call set_topic_digested \
  --params '{"topic_id":<id>,"digested":false}'           # 取消精华 ⚠️

# 标签设置（api call）
zsxq-cli api call set_topic_tags \
  --params '{"topic_id":<id>,"titles":["标签1","标签2"]}'  # 设置标签 ⚠️

# 专栏收录（通过 api raw）
zsxq-cli api raw --method GET \
  --path /v2/topics/<id>/attached_columns                 # 读取主题所属专栏
zsxq-cli api raw --method POST \
  --path /v2/topics/<id>/attached_columns \
  --body '{"column_ids":[...]}'                           # 设置主题专栏 ⚠️

# 删除主题（通过 api raw，不可恢复）
zsxq-cli api raw --method DELETE --path /v2/topics/<id>  # 删除主题 ⚠️
```

> ⚠️ = 写入操作，执行前需确认。

### 个人笔记（note）

```bash
zsxq-cli note +list                              # 查看我的笔记列表
zsxq-cli note +create --text "内容"              # 创建新笔记 ⚠️
zsxq-cli note +detail --note-id <id>              # 查看笔记详情
zsxq-cli note +edit   --note-id <id> --text "新"  # 编辑笔记 ⚠️
zsxq-cli note +delete --note-id <id>              # 删除笔记 ⚠️
```

### 用户与足迹（user）

```bash
zsxq-cli user +info          # 查看我的账号信息
zsxq-cli user +footprints    # 查看我在各星球发过的主题（跨星球足迹）
zsxq-cli user +nps           # 提交 NPS 反馈与建议 ⚠️
```

### 场景编排（Scenarios）

场景将多个原子操作编排为完整的运营流程，一句话即可触发：

| 场景 | 一句话触发 |
|------|-----------|
| 每日巡场 | 「看看今天有什么要处理的」 |
| 评论区运营 | 「整理评论区问题给我回复」 |
| 提问管理 | 「找出还没回答的提问」 |
| 精华与标签整理 | 「哪些帖子值得设精华、打标签」 |
| 运营日报 / 周报 / 复盘 | 「做本周运营周报」 |
| 生成星球日报海报 | 「把今天内容做成海报」 |
| 生成竖版动画视频 | 「把这篇帖子做成视频」 |
| 负面内容监控 | 「巡查星球有没有风险内容」 |
| 批量打标签 | 「用这些标签给最近主题打标」 |
| 到期成员续费关怀 | 「查即将到期的成员，写续费话术」 |
| 收录主题到专栏 | 「把最新主题批量收录进专栏」 |
| 迁移旧版 skill | 「检查并迁移旧版知识星球 skill」 |

> 场景只负责编排流程，具体命令参数以各原子操作文档为准。

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
zsxq-cli api raw --method <METHOD> --path <path> \   # 直接调用原始 HTTP 接口
  [--body '<json>'] [--query '<json>']
```

`api call` 封装了常用高级操作（精华管理、标签设置、成员搜索等），`api raw` 则可调用任意知识星球接口（专栏管理、成员列表、删除主题等）。能力未命中时，Skill 会自动进入探索模式，通过 `api list` 和 `--help` 发现可用接口。

---

## 安全与风险提示（使用前必读）

本工具以你的账号身份运行，因此在执行发帖、评论、回答提问等写入操作前，请务必确认内容。

工具已在多个层面提供默认安全保护，包括：

- 写入和删除操作前必须确认用户意图
- Token 存储于系统 Keychain，不在终端明文输出
- 访问范围不超出你当前账号已有权限

请充分了解相关使用风险。使用本工具，即视为你已理解并愿意自行承担相应责任。

---

## Star History

<a href="https://star-history.com/#unnoo/zsxq-skill&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date" />
  </picture>
</a>

---

## License

MIT
