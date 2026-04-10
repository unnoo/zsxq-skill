---
name: zsxq-topic
version: 1.0.0
description: "知识星球主题管理：搜索主题、查看详情、发布帖子、发表评论、回答提问、设置精华和标签。当用户需要查找内容、发帖、评论、回答问题、或管理主题时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli topic --help"
---

# topic (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md)，其中包含认证、错误处理规则。**

## Core Concepts

- **主题（Topic）**：星球内的内容单元，由 `topic_id` 唯一标识。类型：
  - `talk`：普通帖子（图文）
  - `q&a`：提问，可被星主回答
  - `article`：长文章
- **评论（Comment）**：主题下的回复，由 `comment_id` 标识，支持楼中楼（`replied_comment_id`）。
- **精华（Digested）**：星主可将优质主题设为精华，在星球内突出展示。

## Resource Relationships

```
Group (group_id)
└── Topic (topic_id) — talk / q&a / article
    ├── Comment (comment_id)
    │   └── 楼中楼 Reply (replied_comment_id)
    ├── Answer（q&a 类型专属）
    └── Hashtag 标签列表
```

## Important Notes

### 写入操作前必须确认

发帖、评论、回答均为**不可撤销的公开操作**，执行前必须向用户确认：
1. 目标星球 / 主题（group_id / topic_id）
2. 发布的内容（title / content / text）

### topic_id 的获取

不确定 topic_id 时，先查询再操作：
- 关键词搜索：`topic +search --group-id xxx --query "关键词"`
- 浏览最新：`group +topics --group-id xxx`
- 查看详情：`topic +detail --topic-id xxx`

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`zsxq-cli topic +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+search`](references/zsxq-topic-search.md) | 在星球内全文搜索主题，返回 topic_id / 类型 / 标题 / 时间表格 |
| [`+detail`](references/zsxq-topic-detail.md) | 获取单条主题的完整详情（内容、评论数、点赞数、标签等） |
| [`+create`](references/zsxq-topic-create.md) | 在指定星球发布新主题（帖子），需确认内容后执行 |
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
