# topic +reply（发表评论）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli topic +reply`。

对指定主题发表评论，支持楼中楼（回复某条评论）。

> [!CAUTION]
> 这是**公开写入操作** —— 评论发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标主题（topic_id）
> 2. 评论内容

## 命令

```bash
# 对主题发表顶层评论
zsxq-cli topic +reply \
  --topic-id 111222333444 \
  --text "示例评论内容"

# 楼中楼：回复某条评论（--reply-to 指定 comment_id）
zsxq-cli topic +reply \
  --topic-id 111222333444 \
  --text "示例回复内容" \
  --reply-to 222333444555

# JSON 格式输出（含新建 comment_id）
zsxq-cli topic +reply \
  --topic-id 111222333444 \
  --text "示例评论内容" \
  --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--text <text>` | **是** | 评论内容 |
| `--reply-to <id>` | 否 | 被回复的评论 ID（楼中楼）；省略则为顶层评论 |
| `--json` | 否 | 输出原始 JSON（含 comment_id、create_time 等） |

## 获取 comment_id

如需回复某条评论（楼中楼），先获取评论列表：

```bash
zsxq-cli api call get_topic_comments \
  --params '{"topic_id":"111222333444","limit":30}'
```

从返回结果中找到目标评论的 `comment_id`，再传入 `--reply-to`。

## 输出

```
✓ Comment posted
{
  "comment_id": "222333444555",
  "create_time": "2026-04-01T15:45:07.961+0800",
  "text": "示例评论内容"
}
```

## 参考

- [zsxq-topic-detail](zsxq-topic-detail.md) — 查看主题详情（获取 topic_id）
- [zsxq-topic-answer](zsxq-topic-answer.md) — 回答提问类主题（q&a 专用）
- [zsxq-shared](../../zsxq-shared/SKILL.md)
