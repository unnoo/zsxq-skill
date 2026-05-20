# note +detail（查看笔记详情）

本 skill 对应 shortcut：`zsxq-cli note +detail`。

获取单条笔记的完整详情，包括内容正文、创建时间等。

## 命令

```bash
# 查看笔记详情
zsxq-cli note +detail --note-id 444555666777

# JSON 格式输出
zsxq-cli note +detail --note-id 444555666777 --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--note-id <id>` | **是** | 笔记 ID（从 `note +list` 获取） |
| `--json` | 否 | 输出原始 JSON |

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

## 错误说明

通用错误（401、`--note-id is required`、笔记不存在等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-note-list](zsxq-note-list.md) — 查看笔记列表获取 note_id
- [zsxq-note-edit](zsxq-note-edit.md) — 编辑笔记
- [zsxq-shared](../../zsxq-shared/SKILL.md)
