# topic +detail（查看主题详情）

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
    "type": "talk",
    "title": "示例主题标题",
    "content": "示例主题正文内容...",
    "create_time": "2025-12-31T09:19:28.239+0800",
    "digested": false,
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

字段含义：

- `type`：主题类型，`talk`（普通帖子）/ `q&a`（提问）/ `task`（作业题目）/ `solution`（作业答案）
- `digested`：是否被设为精华
- `counts`：评论数 / 点赞数 / 阅读数
- `owner` / `group`：主题作者与所属星球的精简信息

## 说明

- `+detail` 不含评论内容；如需评论列表，调用 `get_topic_comments`（见 zsxq-topic SKILL.md 的 API 表）

## 错误说明

通用错误（401、`--topic-id is required`、主题不存在、无权限访问等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-topic-reply](zsxq-topic-reply.md) — 对主题发表评论
- [zsxq-topic-answer](zsxq-topic-answer.md) — 回答提问类主题
- [zsxq-topic-search](zsxq-topic-search.md) — 搜索主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
