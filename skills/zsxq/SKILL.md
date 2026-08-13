---
name: zsxq
description: "知识星球 CLI（zsxq-cli）完整操作指南，涵盖星球与内容管理的全部场景。当用户提到知识星球、zsxq、小密圈、星球、登录/认证、发帖、评论、回答、编辑、删除主题、定时发布/定时任务/定时回答、投票、问答主题、markdown 正文、AI 声明（aigc/personal_perspective）、置顶、精华、标签/hashtag、成员、足迹、提问记录、分享链接、NPS 反馈、group_id、topic_id，需要登录/查看认证状态、查看/搜索/发布/编辑/管理知识星球内容、修改星球名称/简介/背景图/亮点图（星球设置）、做每日巡场 / 评论区运营 / 提问管理 / 精华与标签整理 / 运营日报周报复盘 / 生成星球日报海报图片 / 生成竖版动画视频 / 负面内容监控 / 批量打标签 / 到期成员续费关怀 / 收录主题到专栏等运营场景、拼接分享链接、直接调用底层接口（api call / api raw）、查成员列表 / 成员到期时间 / 专栏 column 列表，或需要检查/迁移/清理旧版知识星球 skill（zsxq-shared、zsxq-group 等升级到单一 zsxq）时，必须使用本 Skill。即使只涉及单一操作（如获取 group_id、查看帖子详情、回复评论），也应触发。"
metadata:
  version: 2.1.0
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
| 每日巡场：查今天需要关注/处理的新内容 | → [`scenarios/daily-patrol.md`](references/scenarios/daily-patrol.md) |
| 整理评论区、找未回复评论并起草回复 | → [`scenarios/triage-comments.md`](references/scenarios/triage-comments.md) |
| 处理别人向我提的、还没回答的问题 | → [`scenarios/manage-inbound-questions.md`](references/scenarios/manage-inbound-questions.md) |
| 整理精华与标签（加精 / 打标签建议） | → [`scenarios/curate-digest-and-tags.md`](references/scenarios/curate-digest-and-tags.md) |
| 生成运营日报 / 周报 / 复盘 | → [`scenarios/compose-operations-report.md`](references/scenarios/compose-operations-report.md) |
| 把星球内容做成日报海报图片（PNG） | → [`scenarios/generate-daily-poster.md`](references/scenarios/generate-daily-poster.md) |
| 把星球帖子做成竖版动画视频（MP4） | → [`scenarios/generate-video.md`](references/scenarios/generate-video.md) |
| 巡查监控负面 / 风险内容 | → [`scenarios/monitor-risky-content.md`](references/scenarios/monitor-risky-content.md) |
| 按给定标签批量给主题打标 | → [`scenarios/batch-tag-topics.md`](references/scenarios/batch-tag-topics.md) |
| 到期成员续费关怀（识别即将到期成员、分层写话术） | → [`scenarios/care-expiring-members.md`](references/scenarios/care-expiring-members.md) |
| 把最新主题批量收录进专栏 | → [`scenarios/archive-topics-to-column.md`](references/scenarios/archive-topics-to-column.md) |
| 检查/迁移/清理旧版 zsxq skill | → [`references/scenarios/migrate-legacy-skills.md`](references/scenarios/migrate-legacy-skills.md) |
| 直接调底层 API / 探索未封装能力 | → [`references/cli-exploration.md`](references/cli-exploration.md) |
| 拼接知识星球分享链接 | → [`references/share-links.md`](references/share-links.md) |
| 了解安全规则（写入/删除确认） | → [安全规则](#安全规则) |
| 列出我加入的星球 / 获取 group_id | → [`references/group-list.md`](references/group-list.md) |
| 修改星球名称 / 简介 / 背景图 / 亮点图 | → [`references/group-settings.md`](references/group-settings.md) |
| 浏览星球内最新主题 | → [`references/group-topics.md`](references/group-topics.md) |
| 查看星球标签 | → [`references/group-hashtags.md`](references/group-hashtags.md) |
| 在星球内搜索内容 | → [`references/topic-search.md`](references/topic-search.md) |
| 查看帖子详情 | → [`references/topic-detail.md`](references/topic-detail.md) |
| 发帖（普通 / 投票 / 提问 / markdown / AI 声明） | → [`references/topic-create.md`](references/topic-create.md) |
| 编辑帖子 | → [`references/topic-edit.md`](references/topic-edit.md) |
| 评论 / 楼中楼回复 | → [`references/topic-reply.md`](references/topic-reply.md) |
| 回答提问（立即 / 定时 / 静默） | → [`references/topic-answer.md`](references/topic-answer.md) |
| 删除主题 | → [`references/topic-delete.md`](references/topic-delete.md) |
| 定时发布主题 / 修改或取消定时任务 | → [`references/topic-schedule.md`](references/topic-schedule.md) |
| 查看待执行的定时任务与配额 | → [`references/topic-scheduled.md`](references/topic-scheduled.md) |
| 设为精华 / 置顶（星主） | → [`references/topic-set.md`](references/topic-set.md) |
| 取消精华（底层接口 api call） | → [`references/topic-digest.md`](references/topic-digest.md) |
| 给主题设置标签 | → [`references/topic-tags.md`](references/topic-tags.md) |
| 读取 / 设置主题所属专栏（收录到专栏） | → [`references/topic-attached-columns.md`](references/topic-attached-columns.md) |
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
│   ├── Scheduled Job (job_id) — 定时发布主题/回答，每星球上限 10
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
- **精华（Digested）/ 置顶（Sticky）**：有管理权限（星主 / 管理员 / 合伙人）可将主题设为精华或置顶，改变其在星球内的展示。
- **定时任务（Scheduled Job）**：主题或回答可以定时在未来某个时间点自动发布（14 天窗口内），每星球上限 10 个。

## 安全规则

- **禁止输出或传播认证 token** —— token 是登录凭证，不在终端明文输出，不分享给他人
- **写入/删除操作前必须确认用户意图**（发帖、编辑、评论、回答、定时发布、设置精华/置顶、修改星球资料、创建笔记、删除主题或笔记、取消定时任务、提交 NPS 反馈等）
- 不确定 `group_id` / `topic_id` / `comment_id` / `note_id` 时，先用查询命令确认，再执行写入或删除
- **笔记是公开内容**，任何持有链接的人均可访问 —— 涉及隐私或敏感信息不要写进笔记
- `api raw` 写入不得绕过原子操作的安全约束；探索模式发现的写入接口同样需要用户确认
- 各写入/删除 reference 的 `> [!CAUTION]` 块列出该操作特有的确认项

## 场景（Scenarios）

场景表达业务目标，由多个原子操作编排而成。SKILL.md 只链接场景入口，流程细节见入口文档。

| 场景 | 触发语 | 入口 |
|------|--------|------|
| 每日巡场 | 「每日巡场 / 巡检星球」「看看今天有什么要处理的」 | [`scenarios/daily-patrol.md`](references/scenarios/daily-patrol.md) |
| 评论区运营 | 「整理评论区问题给我回复」「找出没回复的评论、起草回复」 | [`scenarios/triage-comments.md`](references/scenarios/triage-comments.md) |
| 提问管理 | 「找出别人向我提问但我还没回答的」「按优先级整理待回答提问」 | [`scenarios/manage-inbound-questions.md`](references/scenarios/manage-inbound-questions.md) |
| 精华与标签整理 | 「整理最近主题，该加精加精、该打标签打标签」「哪些帖子值得设精华」 | [`scenarios/curate-digest-and-tags.md`](references/scenarios/curate-digest-and-tags.md) |
| 运营日报 / 周报 / 复盘 | 「做今天的运营日报」「做本周运营周报」「复盘过去 7 天运营」 | [`scenarios/compose-operations-report.md`](references/scenarios/compose-operations-report.md) |
| 生成星球日报海报 | 「生成星球日报海报 / 做张日报图」「把最近内容做成一张海报发群里」 | [`scenarios/generate-daily-poster.md`](references/scenarios/generate-daily-poster.md) |
| 生成竖版动画视频 | 「帮我把这篇帖子做成视频」「找最近适合做视频的帖子」「生成本周视频」「把星球内容做成视频」 | [`scenarios/generate-video.md`](references/scenarios/generate-video.md) |
| 负面内容监控 | 「巡查 / 监控星球风险内容」「每小时查辱骂 / 广告 / 投诉」 | [`scenarios/monitor-risky-content.md`](references/scenarios/monitor-risky-content.md) |
| 自动打标签 | 「用给定标签给最近主题批量打标」「批量回标历史内容」 | [`scenarios/batch-tag-topics.md`](references/scenarios/batch-tag-topics.md) |
| 到期成员续费关怀 | 「查即将到期的成员」「做续费关怀 / 续费提醒」「按活跃度给到期成员写话术」 | [`scenarios/care-expiring-members.md`](references/scenarios/care-expiring-members.md) |
| 收录主题到专栏 | 「把最新 N 条主题收录进专栏 XX」「批量把主题归档到专栏 / 整理专题合集」 | [`scenarios/archive-topics-to-column.md`](references/scenarios/archive-topics-to-column.md) |
| 迁移旧版 skill | 「检查/清理/迁移旧版知识星球 skill」「升级 zsxq skill」 | [`scenarios/migrate-legacy-skills.md`](references/scenarios/migrate-legacy-skills.md) |

## 星球管理（group）

| Shortcut | 说明 | Reference |
|----------|------|-----------|
| `zsxq-cli group +list` | 列出加入/创建的星球，获取 group_id | [`group-list.md`](references/group-list.md) |
| `zsxq-cli group +topics` | 浏览星球最新主题（分页） | [`group-topics.md`](references/group-topics.md) |
| `zsxq-cli group +hashtags` | 列出星球标签及主题数 | [`group-hashtags.md`](references/group-hashtags.md) |
| `zsxq-cli group +settings` | 修改星球名称 / 简介 / 背景图 / 亮点图 ⚠️ | [`group-settings.md`](references/group-settings.md) |

**API（`zsxq-cli api call`）：**

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_groups` | `keyword` | 按关键词搜索星球 |
| `search_group_members` | `group_id`, `keyword`, `limit` | 搜索星球成员 |
| `get_hashtag_topics` | `hashtag_id`, `limit`, `end_time` | 列出某标签下的主题（分页） |

**原始 HTTP 调用：**

| 操作 | 命令模板 | Reference |
|------|----------|-----------|
| 成员列表 | `api raw --method GET --path /v2/groups/<group_id>/members --query '<json>'` | [`group-members.md`](references/group-members.md) |
| 专栏列表 | `api raw --method GET --path /v2/groups/<group_id>/columns` | [`group-columns.md`](references/group-columns.md) |
| 创建专栏 | `api raw --method POST --path /v2/groups/<group_id>/columns --body '{"name":"…"}'` ⚠️ | [`group-column-create.md`](references/group-column-create.md) |

> 成员列表的 `expired_time` 仅付费星球星主/管理员可见。主题的专栏归属为主题维度操作，见[主题管理](#主题管理topic)的原始 HTTP 调用。

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
| `zsxq-cli topic +create` | 发布新帖子（talk / q&a、投票、AI 声明、markdown）⚠️ | [`topic-create.md`](references/topic-create.md) |
| `zsxq-cli topic +edit` | 编辑自己的帖子（正文 / 附件 / AI 声明 / 投票）⚠️ | [`topic-edit.md`](references/topic-edit.md) |
| `zsxq-cli topic +reply` | 评论 / 楼中楼回复 ⚠️ | [`topic-reply.md`](references/topic-reply.md) |
| `zsxq-cli topic +answer` | 回答提问（支持定时 / 静默）⚠️ | [`topic-answer.md`](references/topic-answer.md) |
| `zsxq-cli topic +set` | 设置精华 / 置顶 ⚠️ | [`topic-set.md`](references/topic-set.md) |
| `zsxq-cli topic +schedule` | 定时发布主题（创建 / 修改）⚠️ | [`topic-schedule.md`](references/topic-schedule.md) |
| `zsxq-cli topic +scheduled` | 查看待执行定时任务与配额 | [`topic-scheduled.md`](references/topic-scheduled.md) |
| `zsxq-cli topic +unschedule` | 取消定时任务 ⚠️ | [`topic-unschedule.md`](references/topic-unschedule.md) |

> ⚠️ = 写入操作，执行前必须向用户确认内容。

**API（`zsxq-cli api call`）：**

| 工具 | 参数 | 说明 | Reference |
|------|------|------|-----------|
| `get_topic_comments` | `topic_id`, `limit`, `index` | 获取主题评论列表（分页） | — |
| `set_topic_digested` | `topic_id`, `digested` | 设置/取消精华（星主权限）⚠️ | [`topic-digest.md`](references/topic-digest.md) |
| `set_topic_tags` | `topic_id`, `titles` | 为主题设置标签（titles 为完整标签集合）⚠️ | [`topic-tags.md`](references/topic-tags.md) |
| `get_self_question_topics` | `topic_filter`, `count`, `end_time` | 查看自己发起的提问 | — |
| `get_self_answer_topics` | `topic_filter`（`unanswered`/`answered`）, `count`, `end_time` | 查看别人向我发起的提问（账号级，返回项带 `group` 字段，需按星球过滤） | — |

> ⚠️ = 写入操作（`set_topic_digested` / `set_topic_tags` 会修改星球内容），执行前必须向用户确认，并遵守[安全规则](#安全规则)与对应 reference 的 `> [!CAUTION]` 块。

**原始 HTTP 调用：**

| 操作 | 命令模板 | Reference |
|------|----------|-----------|
| 删除主题 | `api raw --method DELETE --path /v2/topics/<topic_id>` ⚠️ | [`topic-delete.md`](references/topic-delete.md) |
| 读取主题所属专栏 | `api raw --method GET --path /v2/topics/<topic_id>/attached_columns` | [`topic-attached-columns.md`](references/topic-attached-columns.md) |
| 设置主题所属专栏 | `api raw --method POST --path /v2/topics/<topic_id>/attached_columns --body '{"column_ids":[...]}'` ⚠️ | [`topic-attached-columns.md`](references/topic-attached-columns.md) |

> ⚠️ = 写入操作，执行前必须向用户确认。设置主题所属专栏为**全量替换**：`column_ids` 会覆盖该主题原有专栏归属，「加入某专栏」须先读现有集合再并入回设，详见 [`topic-attached-columns.md`](references/topic-attached-columns.md)。

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
