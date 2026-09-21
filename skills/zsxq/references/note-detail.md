# note +detail（查看笔记详情）

对应命令：CLI 通道 `zsxq-cli note +detail`；MCP 通道见下方命令块。

获取单条笔记的完整详情，包括内容正文、创建时间等。

## 命令

**CLI 通道：**

```bash
# 查看笔记详情
zsxq-cli note +detail --note-id 444555666777

# JSON 格式输出
zsxq-cli note +detail --note-id 444555666777 --json
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/notes/555666777"}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--note-id <id>` | **是** | 笔记 ID（从 `note +list` 获取） |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--note-id` | path `/v2/notes/{note_id}` |
| `--json` | 无对应字段 —— MCP 通道恒为 `{success, status_code, body}` 信封，无格式开关 |

## 输出字段说明

```json
{
  "note": {
    "note_id": "444555666777",
    "text": "笔记正文…",
    "create_time": "2026-04-10T09:00:00.000+0800"
  }
}
```

完整字段以 `--json` 实际输出为准。

CLI 通道输出的是上述提取好的 `note` 子对象；MCP 通道恒为 `{success, status_code, body}` 信封，取 `body.resp_data.note`。

## 错误说明

通用错误（401、`--note-id is required`、笔记不存在等）见 [auth-errors](auth-errors.md#常见错误处理)。本命令无特有错误。

## 参考

- [note-list](note-list.md) — 查看笔记列表获取 note_id
- [note-edit](note-edit.md) — 编辑笔记
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
