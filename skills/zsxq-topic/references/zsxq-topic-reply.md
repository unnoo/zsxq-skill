# topic +reply（发表评论）

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

# 带附件的评论
zsxq-cli topic +reply \
  --topic-id 111222333444 \
  --text "示例评论内容" \
  --files screenshot.png
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--text <text>` | **是** | 评论内容 |
| `--reply-to <id>` | 否 | 被回复的评论 ID（楼中楼，即对评论的回复而非对主题的评论）；省略则为顶层评论 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔（如 `screenshot.png,log.txt`） |
| `--json` | 否 | 输出原始 JSON（含 comment_id、create_time 等） |

## 输出

```
✓ Comment posted
{
  "comment_id": "222333444555",
  "create_time": "2026-04-01T15:45:07.961+0800",
  "text": "示例评论内容"
}
```

## 推荐工作流

顶层评论：

```bash
# 第一步：确认目标主题
zsxq-cli topic +detail --topic-id 111222333444

# 第二步：发表评论
zsxq-cli topic +reply --topic-id 111222333444 --text "评论内容"
```

楼中楼回复（先拿到要回复的 `comment_id`）：

```bash
# 第一步：列出主题评论，找到目标 comment_id
zsxq-cli api call get_topic_comments --params '{"topic_id":"111222333444","limit":30}'

# 第二步：用 --reply-to 指向那条评论
zsxq-cli topic +reply --topic-id 111222333444 --text "回复内容" --reply-to 222333444555
```

## 失败语义

写入失败即原子回滚 —— 不会留下空评论或半成品 comment_id。重试前请先确认参数是否合法。

## 错误说明

通用错误（401、`--topic-id is required`、主题不存在、`--reply-to` 对应的评论不存在等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-topic-detail](zsxq-topic-detail.md) — 查看主题详情（获取 topic_id）
- [zsxq-topic-answer](zsxq-topic-answer.md) — 回答提问类主题（q&a 专用）
- [zsxq-shared](../../zsxq-shared/SKILL.md)
