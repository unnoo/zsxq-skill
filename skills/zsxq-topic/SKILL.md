---
name: zsxq-topic
version: 1.3.1
description: "知识星球主题管理：搜索主题、查看主题详情、发布帖子、编辑主题、发表评论、回复某条评论（楼中楼）、回答提问、删除主题；通过 api call 查看主题评论列表、设置精华、设置标签、查看自己提的问题与已回答记录。当用户需要查找内容、发帖、编辑主题、评论、回复评论、回答问题、删除主题、查看主题评论、查看自己的提问记录、或管理主题精华和标签时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli topic --help"
---

# topic

> 首次使用或遇到认证错误（401 / token 过期 / `not logged in`）时，先读 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md) 了解登录与 API 调用约定。日常调用已登录账户时无需每次重读。

## Core Concepts

- **主题（Topic）**：星球内的内容单元，由 `topic_id` 唯一标识。类型：
  - `talk`：普通帖子（图文）
  - `q&a`：提问，可被星主回答
  - `task`：作业题目
  - `solution`：作业答案
- **评论（Comment）**：主题下的回复，由 `comment_id` 标识，支持楼中楼（`replied_comment_id`）。
- **精华（Digested）**：星主可将优质主题设为精华，在星球内突出展示。

## Resource Relationships

```
Group (group_id)
└── Topic (topic_id) — talk / q&a / task / solution
    ├── Comment (comment_id)
    │   └── 楼中楼 Reply (replied_comment_id)
    ├── Answer（q&a 类型专属）
    └── Hashtag 标签列表
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`zsxq-cli topic +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+search`](references/zsxq-topic-search.md) | 在星球内全文搜索主题，返回 topic_id / 类型 / 标题 / 时间表格 |
| [`+detail`](references/zsxq-topic-detail.md) | 获取单条主题的完整详情（内容、评论数、点赞数、标签等） |
| [`+create`](references/zsxq-topic-create.md) | 在指定星球发布新主题（仅支持 talk 类型），需确认内容后执行 |
| [`+edit`](references/zsxq-topic-edit.md) | 编辑自己发布的主题（正文、附件），需确认内容后执行 |
| [`+reply`](references/zsxq-topic-reply.md) | 对主题发表评论，支持楼中楼回复，需确认内容后执行 |
| [`+answer`](references/zsxq-topic-answer.md) | 对提问类主题（q&a）发布官方回答，需确认内容后执行 |

## API（通过 `zsxq-cli api call` 直接调用）

Shortcut 未覆盖的高级操作：

| 工具 | 参数 | 说明 |
|------|------|------|
| `get_topic_comments` | `topic_id`, `limit`, `index` | 获取主题评论列表（分页） |
| `set_topic_digested` | `topic_id`, `digested` | 设置/取消精华（星主权限） |
| `set_topic_tags` | `topic_id`, `titles` | 为主题设置标签（标签名数组） |
| `get_self_question_topics` | `topic_filter`, `count`, `end_time` | 查看自己发起的提问（`unanswered`/`answered`） |
| `get_self_answer_topics` | `topic_filter`, `count`, `end_time` | 查看别人向我发起的提问（`unanswered`/`answered`） |

## 原始 HTTP 调用（`zsxq-cli api raw`）

| 操作 | 命令模板 | 说明 |
|------|----------|------|
| [删除主题](references/zsxq-topic-delete.md) | `api raw --method DELETE --path /v2/topics/<topic_id>` | 删除主题，不可恢复 |
