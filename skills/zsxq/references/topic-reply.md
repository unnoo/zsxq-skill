# topic +reply（发表评论）

对应命令：CLI 通道 `zsxq-cli topic +reply`；MCP 通道见下方命令块。

对指定主题发表评论，支持楼中楼（回复某条评论）。

> [!CAUTION]
> 这是**公开写入操作** —— 评论发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标主题（topic_id）
> 2. 评论内容

## 命令

**CLI 通道：**

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

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "POST", "path": "/v2/topics/111222333444/comments", "body": {"req_data": {"text": "评论内容", "image_ids": [], "mentioned_user_ids": []}}}
```

楼中楼加 `"replied_comment_id": "888999"`（对应 CLI 通道的 `--reply-to`）。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--text <text>` | **是** | 评论内容 |
| `--reply-to <id>` | 否 | 被回复的评论 ID（楼中楼，即对评论的回复而非对主题的评论）；省略则为顶层评论 |
| `--files <path>` | 否 | 单个附件路径（仅支持上传 1 个文件：一张图片或一个文件） |
| `--json` | 否 | 输出原始 JSON（含 comment_id、create_time 等） |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--topic-id` | path `/v2/topics/{topic_id}/comments` |
| `--text` | `req_data.text` |
| `--reply-to` | `req_data.replied_comment_id` |
| `--files`（仅 1 个） | **仅 CLI 通道**（附件上传缺口，见 [endpoint-catalog](endpoint-catalog.md) 的「通道缺口」） |

## 输出

```
✓ Comment posted
{
  "comment_id": "222333444555",
  "create_time": "2026-04-01T15:45:07.961+0800",
  "text": "示例评论内容"
}
```

MCP 通道恒为 `{success, status_code, body}` 信封，新评论信息（`comment_id`、`create_time`）在 `body.resp_data`。

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：读主题用 CLI `topic +detail` / MCP `GET /v2/topics/{topic_id}/info`；读评论列表用 CLI `api call get_topic_comments` / MCP `GET /v2/topics/{topic_id}/comments`（分页游标用返回的 `index`）；发评论用上方对应通道的命令（MCP 通道不能带附件）。

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

| 错误 | 原因 |
|------|------|
| `评论内容不能为空，请提供 --text 或 --files` | 内容与附件都为空 |
| `评论仅支持上传 1 个文件` | `--files` 传了多个路径（逗号分隔） |

通用错误（401、`--topic-id is required`、主题不存在、`--reply-to` 对应的评论不存在等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 查看主题详情（获取 topic_id）
- [topic-answer](topic-answer.md) — 回答提问类主题（q&a 专用）
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
