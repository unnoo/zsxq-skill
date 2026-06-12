---
name: zsxq-group
version: 1.3.2
description: "知识星球（星球）管理：列出星球、浏览主题、查询标签、搜索成员。当用户需要查看自己加入或创建的星球、浏览星球内容、获取 group_id、查询星球标签或成员时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli group --help"
---

# group

> 首次使用或遇到认证错误（401 / token 过期 / `not logged in`）时，先读 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md) 了解登录与 API 调用约定。日常调用已登录账户时无需每次重读。

## Core Concepts

- **星球（Group）**：知识星球的社群单元，由 `group_id`（纯数字）唯一标识。用户可以是创建者（owner）或成员（member）。
- **主题（Topic）**：星球内的内容单元，包括帖子（talk）、提问（q&a）、作业（task）、作业答案（solution）等，由 `topic_id` 唯一标识。
- **标签（Hashtag）**：星球内的分类标签，由 `hashtag_id` 标识，可附加到主题上。

## Resource Relationships

```
Group (group_id)
├── Topic (topic_id) — talk / q&a / task / solution
│   ├── Comment (comment_id)
│   │   └── 楼中楼 Reply (replied_comment_id)
│   ├── Answer（q&a 类型专属）
│   └── Hashtag 标签
└── Hashtag (hashtag_id)
    └── Topic 列表
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`zsxq-cli group +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+list`](references/zsxq-group-list.md) | 列出当前用户加入或创建的所有星球，输出 group_id 和名称表格 |
| [`+topics`](references/zsxq-group-topics.md) | 列出星球内最新主题，支持分页游标，输出 topic_id / 类型 / 标题 / 时间表格 |
| [`+hashtags`](references/zsxq-group-hashtags.md) | 列出星球内所有标签及主题数量 |

## API（通过 `zsxq-cli api call` 直接调用）

Shortcut 未覆盖的高级操作：

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_groups` | `keyword` | 按关键词搜索星球 |
| `search_group_members` | `group_id`, `keyword`, `limit` | 搜索星球成员 |
| `get_hashtag_topics` | `hashtag_id`, `limit`, `end_time` | 列出某标签下的主题（分页） |

## 反例（不要做）

| ❌ 不要做 | ✅ 应该做 |
|----------|----------|
| 按关键词找内容时用 `+topics` 翻页逐条人工筛选 | 用 [zsxq-topic](../zsxq-topic/SKILL.md) 的 `+search` 全文搜索 |
| 查「自己最近发过什么」时逐个星球跑 `+topics` | 用 [zsxq-user](../zsxq-user/SKILL.md) 的 `+footprints` 一次拿到跨星球足迹 |
| 用户只给星球名称时，让用户自己提供 group_id 或凭记忆猜 ID | 先 `group +list`（自己加入的）或 `search_groups`（公开搜索）查到 ID 再继续 |
| 名称命中多个相似星球时默认取第一个 | 列出候选（group_id + 名称）让用户确认 |
| 把 `search_group_members` 当成员列表接口、调大 `limit` 遍历全员 | 它是关键词搜索，只用于按昵称定位具体成员 |
