# topic +detail（查看主题详情）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli topic +detail`。

获取单条主题的完整详情，包括内容正文、发布者、点赞数、评论数、标签等。

## 命令

```bash
# 查看主题详情（JSON 输出）
zsxq-cli topic +detail --topic-id 111222333444

# 使用 --json 标志（效果相同，detail 命令始终输出 JSON）
zsxq-cli topic +detail --topic-id 111222333444 --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID（从 `topic +search` 或 `group +topics` 获取） |
| `--json` | 否 | 输出原始 JSON（detail 命令默认即 JSON 输出） |

## 输出字段说明

```json
{
  "topic": {
    "topic_id": "111222333444",
    "type": "talk",               // talk / q&a / article
    "title": "示例主题标题",
    "content": "示例主题正文内容...",
    "create_time": "2025-12-31T09:19:28.239+0800",
    "digested": false,            // 是否精华
    "counts": {
      "comments": 3,
      "likes": 10,
      "readers": 200
    },
    "owner": {
      "name": "示例用户",
      "user_id": "123456"
    },
    "group": {
      "group_id": "123456789",
      "name": "示例星球"
    }
  }
}
```

## 获取评论列表

`+detail` 不含评论内容，如需获取评论，使用 API 调用：

```bash
zsxq-cli api call get_topic_comments \
  --params '{"topic_id":"111222333444","limit":30}'

# 翻页（使用返回的 index 值）
zsxq-cli api call get_topic_comments \
  --params '{"topic_id":"111222333444","limit":30,"index":"<上一页返回的 index>"}'
```

## 参考

- [zsxq-topic-reply](zsxq-topic-reply.md) — 对主题发表评论
- [zsxq-topic-answer](zsxq-topic-answer.md) — 回答提问类主题
- [zsxq-topic-search](zsxq-topic-search.md) — 搜索主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
