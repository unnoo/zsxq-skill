# group +hashtags（查看星球标签）

对应操作：`group +hashtags`；MCP 调用见下方命令块。

列出指定星球内所有的话题标签（Hashtag）及其主题数量。常用于获取 `hashtag_id` 以便按分类浏览内容。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 列出星球所有标签（表格显示）
zsxq-cli group +hashtags --group-id 123456789

# JSON 格式（含 hashtag_id、owner 等完整字段）
zsxq-cli group +hashtags --group-id 123456789 --json
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/groups/123456789/hashtags"}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/hashtags` |

## 输出

<!-- cli-only:start -->

CLI 通道默认表格输出（`--json` 为 JSON）：

| HASHTAG ID | TITLE | TOPIC COUNT |
|------------|-------|-------------|
| 333444555666 | #示例标签# | 12 |
| 333444555677 | #示例标签二# | 5 |

<!-- cli-only:end -->

MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

MCP 通道返回 `body.resp_data.hashtags[]`（含 hashtag_id、owner 等完整字段）。

## 说明

获得 `hashtag_id` 后，可通过 API 列出该标签下的所有主题：`GET /v2/hashtags/{hashtag_id}/topics`（query 参数见 [endpoint-catalog](endpoint-catalog.md)）。

<!-- cli-only:start -->
CLI 通道用底层接口工具 `get_hashtag_topics`。
<!-- cli-only:end -->

<!-- cli-only:start -->

```bash
zsxq-cli api call get_hashtag_topics \
  --params '{"hashtag_id":"333444555666","limit":20}'

# 翻页
zsxq-cli api call get_hashtag_topics \
  --params '{"hashtag_id":"333444555666","limit":20,"end_time":"2025-11-01T00:00:00.000+0800"}'
```

<!-- cli-only:end -->

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 该星球尚未创建任何标签 | 正常情况，无需处理 |

通用错误（401、参数缺失、星球不存在/无权限等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-topics](group-topics.md) — 浏览星球全部主题
- [topic-search](topic-search.md) — 关键词搜索主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
