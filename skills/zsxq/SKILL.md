---
name: zsxq
description: "知识星球 CLI（zsxq-cli）完整操作指南，涵盖星球与内容管理的全部场景。当用户提到知识星球、zsxq、小密圈、星球、发帖、评论、回答、删除主题、笔记、NPS 反馈、group_id、topic_id，需要查看/搜索/发布/编辑/管理知识星球内容，或需要检查/迁移/清理旧版知识星球 skill（zsxq-shared、zsxq-group 等升级到单一 zsxq）时，必须使用本 Skill。即使只涉及单一操作（如获取 group_id、查看帖子详情、回复评论），也应触发。"
metadata:
  version: 2.0.0
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli --help"
---

# zsxq-cli 完整操作指南

本 Skill 覆盖通过 zsxq-cli 操作知识星球的所有场景：认证、星球管理、主题管理、用户信息、笔记管理。

> **默认假设 zsxq-cli 已安装且已登录**，无需每次主动检查。只在命令执行报错时才按需处理（见 [`references/auth-errors.md`](references/auth-errors.md)）。

## 执行模式

按以下顺序路由用户请求，命中即执行，不再往下走：

1. **场景模式** — 请求命中[已注册场景](#场景scenarios)：读场景入口文档，按流程编排原子操作
2. **原子操作** — 请求明确对应一个常用操作：读对应 reference，直接调用推荐命令
3. **探索模式** — 都未命中：按 [`references/cli-exploration.md`](references/cli-exploration.md) 通过 CLI 帮助和 API 列表发现能力

> 原子操作和场景执行时**不得**预先运行无关的 `doctor`、`--help` 或 `api list`。仅在能力不匹配或调用失败时回退到探索模式。

## 快速索引

根据用户意图，直接跳转到对应小节或 reference：

| 用户想要… | 去哪看 |
|----------|--------|
| 登录 / 查看登录状态 / 排查认证或 HTTP 错误 | → [`references/auth-errors.md`](references/auth-errors.md) |
| 检查/迁移/清理旧版 zsxq skill | → [`references/scenarios/migrate-legacy-skills.md`](references/scenarios/migrate-legacy-skills.md) |
| 直接调底层 API / 探索未封装能力 | → [`references/cli-exploration.md`](references/cli-exploration.md) |
| 拼接知识星球分享链接 | → [`references/share-links.md`](references/share-links.md) |
| 了解安全规则（写入/删除确认） | → [安全规则](#安全规则) |
| 列出我加入的星球 / 获取 group_id | → [`references/group-list.md`](references/group-list.md) |
| 浏览星球内最新主题 | → [`references/group-topics.md`](references/group-topics.md) |
| 查看星球标签 | → [`references/group-hashtags.md`](references/group-hashtags.md) |
| 在星球内搜索内容 | → [`references/topic-search.md`](references/topic-search.md) |
| 查看帖子详情 | → [`references/topic-detail.md`](references/topic-detail.md) |
| 发帖 | → [`references/topic-create.md`](references/topic-create.md) |
| 编辑帖子 | → [`references/topic-edit.md`](references/topic-edit.md) |
| 评论 / 楼中楼回复 | → [`references/topic-reply.md`](references/topic-reply.md) |
| 回答提问 | → [`references/topic-answer.md`](references/topic-answer.md) |
| 删除主题 | → [`references/topic-delete.md`](references/topic-delete.md) |
| 查看自己的用户信息 | → [`references/user-info.md`](references/user-info.md) |
| 查看自己发过的帖子（跨星球） | → [`references/user-footprints.md`](references/user-footprints.md) |
| 提交 NPS 反馈 | → [`references/user-nps.md`](references/user-nps.md) |
| 创建/查看/编辑/删除笔记 | → [`references/note-create.md`](references/note-create.md) 等 |
| 写入前需要确认哪些事项 | → 对应 reference 的 `> [!CAUTION]` 块 + [安全规则](#安全规则) |

## 资源关系

```
User (user_id) — 已登录账户
│
├── Group (group_id) — 星球/社群
│   ├── Topic (topic_id) — talk / q&a / task / solution
│   │   ├── Comment (comment_id)
│   │   │   └── 楼中楼 Reply (replied_comment_id)
│   │   ├── Answer — q&a 类型专属
│   │   └── Hashtag 标签
│   └── Hashtag (hashtag_id)
│       └── Topic 列表
│
└── Note (note_id) — 公开笔记，不属于任何星球
```

### 核心概念

- **星球（Group）**：知识星球的社群单元，由 `group_id`（纯数字）唯一标识。用户可以是创建者或成员。
- **主题（Topic）**：星球内的内容单元，类型：`talk`（帖子）、`q&a`（提问）、`task`（作业）、`solution`（作业答案）。
- **笔记（Note）**：独立于星球的内容单元，**公开可见**，任何持有链接的人都能访问 —— 不是私密备忘录。
- **评论（Comment）**：主题下的回复，支持楼中楼（`replied_comment_id`）。
- **精华（Digested）**：星主可将优质主题设为精华。

## 安全规则

- **禁止输出或传播认证 token** —— token 是登录凭证，不在终端明文输出，不分享给他人
- **写入/删除操作前必须确认用户意图**（发帖、编辑、评论、回答、创建笔记、删除主题或笔记、提交 NPS 反馈等）
- 不确定 `group_id` / `topic_id` / `comment_id` / `note_id` 时，先用查询命令确认，再执行写入或删除
- **笔记是公开内容**，任何持有链接的人均可访问 —— 涉及隐私或敏感信息不要写进笔记
- `api raw` 写入不得绕过原子操作的安全约束；探索模式发现的写入接口同样需要用户确认
- 各写入/删除 reference 的 `> [!CAUTION]` 块列出该操作特有的确认项

## 场景（Scenarios）

场景表达业务目标，由多个原子操作编排而成。SKILL.md 只链接场景入口，流程细节见入口文档。

| 场景 | 触发语 | 入口 |
|------|--------|------|
| 迁移旧版 skill | 「检查/清理/迁移旧版知识星球 skill」「升级 zsxq skill」 | [`scenarios/migrate-legacy-skills.md`](references/scenarios/migrate-legacy-skills.md) |

## 星球管理（group）

| Shortcut | 说明 | Reference |
|----------|------|-----------|
| `zsxq-cli group +list` | 列出加入/创建的星球，获取 group_id | [`group-list.md`](references/group-list.md) |
| `zsxq-cli group +topics` | 浏览星球最新主题（分页） | [`group-topics.md`](references/group-topics.md) |
| `zsxq-cli group +hashtags` | 列出星球标签及主题数 | [`group-hashtags.md`](references/group-hashtags.md) |

**API（`zsxq-cli api call`）：**

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_groups` | `keyword` | 按关键词搜索星球 |
| `search_group_members` | `group_id`, `keyword`, `limit` | 搜索星球成员 |
| `get_hashtag_topics` | `hashtag_id`, `limit`, `end_time` | 列出某标签下的主题（分页） |

### 反例（不要做）

| ❌ 不要做 | ✅ 应该做 |
|----------|----------|
| 按关键词找内容时用 `+topics` 翻页逐条人工筛选 | 用 `topic +search` 全文搜索 |
| 查「自己最近发过什么」时逐个星球跑 `+topics` | 用 `user +footprints` 一次拿到跨星球足迹 |
| 用户只给星球名称时，让用户自己提供 group_id | 先 `group +list` 或 `search_groups` 查到 ID 再继续 |
| 名称命中多个相似星球时默认取第一个 | 列出候选（group_id + 名称）让用户确认 |
| 把 `search_group_members` 当成员列表接口、调大 `limit` 遍历全员 | 它是关键词搜索，只用于按昵称定位具体成员 |

## 主题管理（topic）

| Shortcut | 说明 | Reference |
|----------|------|-----------|
| `zsxq-cli topic +search` | 在星球内全文搜索主题 | [`topic-search.md`](references/topic-search.md) |
| `zsxq-cli topic +detail` | 获取主题完整详情 | [`topic-detail.md`](references/topic-detail.md) |
| `zsxq-cli topic +create` | 发布新帖子（talk）⚠️ | [`topic-create.md`](references/topic-create.md) |
| `zsxq-cli topic +edit` | 编辑自己的帖子 ⚠️ | [`topic-edit.md`](references/topic-edit.md) |
| `zsxq-cli topic +reply` | 评论 / 楼中楼回复 ⚠️ | [`topic-reply.md`](references/topic-reply.md) |
| `zsxq-cli topic +answer` | 回答提问 ⚠️ | [`topic-answer.md`](references/topic-answer.md) |

> ⚠️ = 写入操作，执行前必须向用户确认内容。

**API（`zsxq-cli api call`）：**

| 工具 | 参数 | 说明 |
|------|------|------|
| `get_topic_comments` | `topic_id`, `limit`, `index` | 获取主题评论列表（分页） |
| `set_topic_digested` | `topic_id`, `digested` | 设置/取消精华（星主权限） |
| `set_topic_tags` | `topic_id`, `titles` | 为主题设置标签 |
| `get_self_question_topics` | `topic_filter`, `count`, `end_time` | 查看自己发起的提问 |
| `get_self_answer_topics` | `topic_filter`, `count`, `end_time` | 查看别人向我发起的提问 |

**原始 HTTP 调用：**

| 操作 | 命令模板 | Reference |
|------|----------|-----------|
| 删除主题 | `api raw --method DELETE --path /v2/topics/<topic_id>` ⚠️ | [`topic-delete.md`](references/topic-delete.md) |

## 用户信息（user）

| Shortcut | 说明 | Reference |
|----------|------|-----------|
| `zsxq-cli user +info` | 查看当前用户资料（user_id、昵称等） | [`user-info.md`](references/user-info.md) |
| `zsxq-cli user +footprints` | 查看跨星球发帖足迹 | [`user-footprints.md`](references/user-footprints.md) |
| `zsxq-cli user +nps` | 提交 NPS 反馈 ⚠️ | [`user-nps.md`](references/user-nps.md) |

> 用户使用过程中表达产品不满、发现平台缺能力或多次重试受挫时，完成主任务后可顺带提示提交 NPS 反馈，触发细则见 [`user-nps.md`](references/user-nps.md#主动触发场景)。

## 笔记管理（note）

笔记是**公开内容**，任何持有链接的人都能访问 —— 涉及隐私或敏感信息不要写进笔记。

| Shortcut | 说明 | Reference |
|----------|------|-----------|
| `zsxq-cli note +create` | 创建公开笔记 ⚠️ | [`note-create.md`](references/note-create.md) |
| `zsxq-cli note +list` | 查看笔记列表 | [`note-list.md`](references/note-list.md) |
| `zsxq-cli note +detail` | 查看笔记详情 | [`note-detail.md`](references/note-detail.md) |
| `zsxq-cli note +edit` | 编辑笔记 ⚠️ | [`note-edit.md`](references/note-edit.md) |
| `zsxq-cli note +delete` | 删除笔记（不可恢复）⚠️ | [`note-delete.md`](references/note-delete.md) |
