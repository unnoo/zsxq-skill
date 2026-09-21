# note +edit（编辑笔记）

对应命令：CLI 通道 `zsxq-cli note +edit`；MCP 通道见下方命令块。

编辑已有笔记的内容。未修改的字段自动保留。

> [!CAUTION]
> 这是**写入操作** —— 编辑后内容立即更新，原内容不可恢复。执行前必须向用户确认：
> 1. 目标笔记（note_id）及其当前内容
> 2. 修改后的内容（含附件变更，如有）

> [!IMPORTANT]
> 只能编辑自己创建的笔记，无法编辑他人的笔记。

## 命令

**CLI 通道：**

```bash
# 修改笔记内容
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容"

# JSON 格式输出
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容" --json
```

**MCP 通道（`call_zsxq_api`）：**

先读当前笔记（`image_ids` 无变动且当前为空时，第二步不发送该字段）：

```json
{"method": "GET", "path": "/v2/notes/555666777"}
```

再写入新内容：

```json
{"method": "PUT", "path": "/v2/notes/555666777", "body": {"req_data": {"text": "新内容"}}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--note-id <id>` | **是** | 笔记 ID（从 `note +list` 获取） |
| `--text <text>` | 否 | 新内容（不传则保留原内容） |
| `--files <paths>` | 否 | 新附件，多个用逗号分隔（仅图片，替换原有附件） |
| `--clear-files` | 否 | 清除所有附件 |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--note-id` | path `/v2/notes/{note_id}`（GET 读当前值、PUT 写入同一路径） |
| `--text` | `req_data.text` |
| `--files` | `req_data.image_ids`（整体替换；**图片上传仅 CLI 通道**） |
| `--clear-files` | `req_data.image_ids: []`（置空） |
| `--json` | 无对应字段 —— MCP 通道恒为 `{success, status_code, body}` 信封，无格式开关 |

MCP 通道的 `image_ids` 须先 `GET /v2/notes/{note_id}` 读出当前值后原样回传（先读后写，避免误清空附件）；当前值为空且本次不改附件时**不要发送** `image_ids`。

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：先读当前内容确认，再写入。

```bash
# 第一步：确认当前笔记内容
zsxq-cli note +detail --note-id 444555666777

# 第二步：确认无误后执行编辑
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容"
```

MCP 通道：

```json
{"method": "GET", "path": "/v2/notes/555666777"}
```

```json
{"method": "PUT", "path": "/v2/notes/555666777", "body": {"req_data": {"text": "新的笔记内容"}}}
```

## 失败语义

编辑失败即原子回滚 —— 原内容保留不变。重试前请先确认参数是否合法。

## 错误说明

通用错误（401、`--note-id is required`、笔记不存在、403 无权限编辑他人笔记等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [note-detail](note-detail.md) — 编辑前查看笔记内容
- [note-create](note-create.md) — 创建笔记
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
