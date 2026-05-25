# group +topics（浏览星球主题）

本 skill 对应 shortcut：`zsxq-cli group +topics`。

列出指定星球内最新发布的主题，按时间倒序排列，支持分页。

## 命令

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

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--limit <n>` | 否 | 返回数量，默认 20，最大 30 |
| `--end-time <t>` | 否 | 分页游标，格式：`2025-12-01T00:00:00.000+0800`（上一页返回的 `next_end_time`） |
| `--json` | 否 | 输出原始 JSON |

## 输出（表格模式）

| TOPIC ID | TYPE | TITLE / DIGEST | CREATED AT |
|----------|------|----------------|------------|
| 111222333444 | talk | 示例主题标题 | 2025-12-31T09:19:28.239+0800 |

- `TYPE`：`talk`（帖子）、`q&a`（提问）、`task`（作业题目）、`solution`（作业答案）
- `TITLE / DIGEST`：优先显示标题，无标题时显示内容摘要（截断至 50 字符）

## 说明

按时间倒序返回最新主题。当 `--json` 输出中 `has_more: true` 时，使用返回的 `next_end_time` 值作为 `--end-time` 参数继续翻页：

```bash
# 第一页
zsxq-cli group +topics --group-id 123456789 --json
# → 得到 next_end_time: "2025-11-01T10:00:00.000+0800"

# 第二页
zsxq-cli group +topics --group-id 123456789 \
  --end-time "2025-11-01T10:00:00.000+0800" --json
```

## 错误说明

通用错误（401、参数缺失、404、`--end-time` 格式错误等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-topic-detail](../../zsxq-topic/references/zsxq-topic-detail.md) — 查看主题详情
- [zsxq-topic-search](../../zsxq-topic/references/zsxq-topic-search.md) — 按关键词搜索主题
- [zsxq-group-hashtags](zsxq-group-hashtags.md) — 按标签筛选主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
