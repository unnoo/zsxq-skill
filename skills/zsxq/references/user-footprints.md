# user +footprints（查看主题足迹）

对应命令：CLI 通道 `zsxq-cli user +footprints`；MCP 通道见下方命令块。

查看当前用户在**所有星球**中最近发过的主题，按时间倒序排列。

## 命令

**CLI 通道：**

```bash
# 查看最近 20 条足迹（表格显示）
zsxq-cli user +footprints

# 指定数量
zsxq-cli user +footprints --limit 30

# JSON 格式（含完整字段）
zsxq-cli user +footprints --json

# 翻页（使用上一页返回的 create_time 作为游标）
zsxq-cli user +footprints --end-time "2025-11-01T00:00:00.000+0800"
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/users/123456/footprints", "query": {"count": 20, "filter": "all"}}
```

限定单个星球时（`filter` 改为 `group`，并带上星球 ID）：

```json
{"method": "GET", "path": "/v2/users/123456/footprints", "query": {"count": 20, "filter": "group", "group_id": "123456789", "filter_group_id": "123456789"}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 返回条数，默认 20，最大 30 |
| `--end-time <time>` | 否 | 分页游标，传入上一页最后一条的 `create_time` |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| — | path `/v2/users/{user_id}/footprints`；`user_id` CLI 取本地 config，MCP 通道先 `GET /v2/users/self`（见 [user-info](user-info.md)） |
| `--limit` | `query.count`（默认 20） |
| `--end-time` | `query.end_time` |
| `--json` | 无对应字段 —— MCP 通道恒为 `{success, status_code, body}` 信封，无格式开关 |

服务端限制：**仅可查本人**，两通道一致（`user_id` 传他人 ID 不会返回结果）。

## 输出

CLI 通道默认表格输出（`--json` 为 JSON）；MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

| TOPIC ID | TYPE | TITLE / DIGEST | GROUP | CREATED AT |
|----------|------|----------------|-------|------------|
| 111222333444 | talk | 示例主题标题 | 示例星球 | 2026-04-10T09:00:00.000+0800 |

MCP 通道返回 `body.resp_data.footprints[]`（完整足迹对象，等同 CLI 的 `--json`），CLI 表格中的各列由其中的 `topic` 与 `group` 字段抽取而来。

## 说明

跨星球查询。与 `group +topics` 的区别：

| | `user +footprints` | `group +topics` |
|---|---|---|
| 范围 | **所有星球** | 单个星球 |
| 内容 | 用户在各星球发过的主题 | 星球内最新主题 |
| 必填参数 | 无 | `--group-id` |

**翻页（两通道一致）**：用上一页最后一条的 `create_time` 原值作为下一页游标 —— CLI 通道传 `--end-time`，MCP 通道传 `query.end_time`（MCP 响应不含 `next_end_time` 字段，须自行从返回的 `footprints[]` 末条取 `create_time`）：

```json
{"method": "GET", "path": "/v2/users/123456/footprints", "query": {"count": 20, "filter": "all", "end_time": "2025-11-01T00:00:00.000+0800"}}
```

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 当前账户近期未在任何星球发主题 | 正常情况，无需处理 |

通用错误（401、`--end-time` 格式错误等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [user-info](user-info.md) — 查看用户 ID 等基本信息
- [group-topics](group-topics.md) — 查看单个星球的主题列表
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
