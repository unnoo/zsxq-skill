---
name: zsxq-group
version: 1.0.0
description: "知识星球（星球）管理：列出星球、浏览主题、查询标签、搜索成员。当用户需要查看自己加入或创建的星球、浏览星球内容、获取 group_id、查询星球标签或成员时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli group --help"
---

# group (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md)，其中包含认证、错误处理规则。**

## Core Concepts

- **星球（Group）**：知识星球的社群单元，由 `group_id`（纯数字）唯一标识。用户可以是创建者（owner）或成员（member）。
- **主题（Topic）**：星球内的内容单元，包括帖子（talk）、提问（q&a）、文章（article）等，由 `topic_id` 唯一标识。
- **标签（Hashtag）**：星球内的分类标签，由 `hashtag_id` 标识，可附加到主题上。

## Resource Relationships

```
Group (group_id)
├── Topic (topic_id) — talk / q&a / article
│   ├── Comment (comment_id)
│   └── Hashtag 标签
└── Hashtag (hashtag_id)
    └── Topic 列表
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`zsxq-cli group +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+list`](references/zsxq-group-list.md) | 列出当前用户加入的所有星球，支持分页，输出 group_id 和名称表格 |
| [`+topics`](references/zsxq-group-topics.md) | 列出星球内最新主题，支持分页游标，输出 topic_id / 类型 / 标题 / 时间表格 |
| [`+hashtags`](references/zsxq-group-hashtags.md) | 列出星球内所有标签及主题数量 |

## API（通过 `zsxq-cli api call` 直接调用）

```bash
zsxq-cli api list                           # 查看所有可用工具
zsxq-cli api call <tool> --params '<json>'  # 调用工具
```

Shortcut 未覆盖的高级操作：

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_groups` | `keyword` | 按关键词搜索星球 |
| `search_group_members` | `group_id`, `keyword`, `limit` | 搜索星球成员 |
| `get_hashtag_topics` | `hashtag_id`, `limit`, `end_time` | 列出某标签下的主题（分页） |
