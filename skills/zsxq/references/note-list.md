# note +list（查看笔记列表）

对应命令：CLI 通道 `zsxq-cli note +list`；MCP 通道见下方命令块。

查看当前登录用户的个人笔记列表，按创建时间倒序排列。

## 命令

**CLI 通道：**

```bash
# 查看最新 20 条笔记（表格显示）
zsxq-cli note +list

# 指定数量
zsxq-cli note +list --limit 30

# JSON 格式（含完整字段）
zsxq-cli note +list --json

# 翻页（使用上一页返回的 create_time 作为游标）
zsxq-cli note +list --end-time "2025-11-01T00:00:00.000+0800"
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/users/123456/footprints", "query": {"count": 20, "filter": "note"}}
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
| — | path `/v2/users/{user_id}/footprints`；`user_id` CLI 取本地 config，MCP 通道先 `GET /v2/users/self`（见 [user-info](user-info.md)），并固定 `query.filter=note` |
| `--limit` | `query.count`（默认 20） |
| `--end-time` | `query.end_time` |
| `--json` | 无对应字段 —— MCP 通道恒为 `{success, status_code, body}` 信封，无格式开关 |

## 输出

CLI 通道默认表格输出（`--json` 为 JSON）；MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

| NOTE ID | CONTENT | CREATED AT |
|---------|---------|------------|
| 444555666777 | 示例笔记内容… | 2026-04-10T09:00:00.000+0800 |

CLI 通道从 `footprints[]` 中抽取 `note` 字段拼成上表；MCP 通道返回原始 footprints 结构，笔记数据在每条的 `note` 字段内（`body.resp_data.footprints[].note`）。

## 说明

按创建时间倒序返回。

**翻页（两通道一致）**：取上一页最后一条的 `create_time` 原值作为下一页游标。CLI 通道传 `--end-time`：

```bash
# 第一页
zsxq-cli note +list --json

# 第二页
zsxq-cli note +list --end-time "2025-11-01T00:00:00.000+0800" --json
```

MCP 通道取本页 `footprints[]` 末条的 `create_time` 原值作为下一页 `query.end_time`：

```json
{"method": "GET", "path": "/v2/users/123456/footprints", "query": {"count": 20, "filter": "note", "end_time": "2025-11-01T00:00:00.000+0800"}}
```

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 当前账户尚未创建任何笔记 | 正常情况，无需处理 |

通用错误（401、`--end-time` 格式错误等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [note-create](note-create.md) — 创建笔记
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
