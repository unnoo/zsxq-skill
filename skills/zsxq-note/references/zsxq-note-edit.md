# note +edit（编辑笔记）

本 skill 对应 shortcut：`zsxq-cli note +edit`。

编辑已有笔记的内容。未修改的字段自动保留。

> [!CAUTION]
> 这是**写入操作** —— 编辑后内容立即更新，原内容不可恢复。执行前必须向用户确认：
> 1. 目标笔记（note_id）及其当前内容
> 2. 修改后的内容（含附件变更，如有）

> [!IMPORTANT]
> 只能编辑自己创建的笔记，无法编辑他人的笔记。

## 命令

```bash
# 修改笔记内容
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容"

# JSON 格式输出
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容" --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--note-id <id>` | **是** | 笔记 ID（从 `note +list` 获取） |
| `--text <text>` | 否 | 新内容（不传则保留原内容） |
| `--files <paths>` | 否 | 新附件，多个用逗号分隔（仅图片，替换原有附件） |
| `--clear-files` | 否 | 清除所有附件 |
| `--json` | 否 | 输出原始 JSON |

## 推荐工作流

```bash
# 第一步：确认当前笔记内容
zsxq-cli note +detail --note-id 444555666777

# 第二步：确认无误后执行编辑
zsxq-cli note +edit --note-id 444555666777 --text "新的笔记内容"
```

## 失败语义

编辑失败即原子回滚 —— 原内容保留不变。重试前请先确认参数是否合法。

## 错误说明

通用错误（401、`--note-id is required`、笔记不存在、403 无权限编辑他人笔记等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-note-detail](zsxq-note-detail.md) — 编辑前查看笔记内容
- [zsxq-note-create](zsxq-note-create.md) — 创建笔记
- [zsxq-shared](../../zsxq-shared/SKILL.md)
