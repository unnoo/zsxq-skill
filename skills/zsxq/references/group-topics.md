# group +topics（浏览星球主题）

对应命令：CLI 通道 `zsxq-cli group +topics`；MCP 通道见下方命令块。

列出指定星球内最新发布的主题，按时间倒序排列，支持分页。

## 命令

**CLI 通道：**

```bash
# 列出星球最新 20 条主题（表格显示）
zsxq-cli group +topics --group-id 123456789

# 返回更多（最多 30）
zsxq-cli group +topics --group-id 123456789 --limit 30

# 翻页：使用上一页返回的 next_end_time 作为游标
zsxq-cli group +topics --group-id 123456789 --end-time "2025-12-01T00:00:00.000+0800"

# JSON 格式（含完整 topic 字段、内容、点赞数等）
zsxq-cli group +topics --group-id 123456789 --json
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/groups/123456789/topics", "query": {"count": 20}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--limit <n>` | 否 | 返回数量，默认 20，最大 30 |
| `--end-time <t>` | 否 | 分页游标，格式：`2025-12-01T00:00:00.000+0800`（上一页返回的 `next_end_time`） |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/topics` |
| `--limit` | `query.count`（默认 20） |
| `--end-time` | `query.end_time` |
| `--scope` | `query.scope`（仅非 `all` 时传） |

## 输出

CLI 通道默认表格输出（`--json` 为 JSON）；MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

| TOPIC ID | TYPE | TITLE / DIGEST | CREATED AT |
|----------|------|----------------|------------|
| 111222333444 | talk | 示例主题标题 | 2025-12-31T09:19:28.239+0800 |

- `TYPE`：`talk`（帖子）、`q&a`（提问）、`task`（作业题目）、`solution`（作业答案）
- `TITLE / DIGEST`：优先显示标题，无标题时显示内容摘要（截断至 50 字符）

MCP 通道返回 `body.resp_data.topics[]`（完整 topic 字段，等同 CLI 的 `--json`）。

## 说明

按时间倒序返回最新主题。

**翻页（CLI 通道）**：当 `--json` 输出中 `has_more: true` 时，使用返回的 `next_end_time` 值作为 `--end-time` 参数继续翻页：

```bash
# 第一页
zsxq-cli group +topics --group-id 123456789 --json
# → 得到 next_end_time: "2025-11-01T10:00:00.000+0800"

# 第二页
zsxq-cli group +topics --group-id 123456789 \
  --end-time "2025-11-01T10:00:00.000+0800" --json
```

**翻页（MCP 通道）**：响应不含 `next_end_time` 字段，取本页**最后一条**主题的 `create_time` 原值作为下一页的 `query.end_time`：

```json
{"method": "GET", "path": "/v2/groups/123456789/topics", "query": {"count": 20, "end_time": "2025-11-01T10:00:00.000+0800"}}
```

> **翻页边界去重**：`next_end_time` 等于本页最后一条主题的 `create_time`，而 `--end-time` / `end_time` 是**含等于**的，因此下一页会把上一页最后一条主题**重复返回为首条**。翻页累积时须按 `topic_id` 去重（周期巡查同理按 `comment_id`），不要重复计数或重复处理边界主题。

## 错误说明

通用错误（401、参数缺失、404、`--end-time` 格式错误等）见 [auth-errors](auth-errors.md#常见错误处理)。本命令无特有错误。

## 参考

- [topic-detail](topic-detail.md) — 查看主题详情
- [topic-search](topic-search.md) — 按关键词搜索主题
- [group-hashtags](group-hashtags.md) — 按标签筛选主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
