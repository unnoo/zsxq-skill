# note +create（创建笔记）

本 skill 对应 shortcut：`zsxq-cli note +create`。

在知识星球创建一条公开笔记，支持文本和图片附件。任何人通过笔记链接均可访问。

> [!CAUTION]
> 这是**写入操作**，且笔记是**公开内容** —— 不要把它当作私密备忘录使用。执行前必须向用户确认：
> 1. 笔记内容（text）
> 2. 附件列表（如有）

## 命令

```bash
# 创建一条笔记
zsxq-cli note +create --text "示例笔记内容"

# 多行内容（使用 \n 换行）
zsxq-cli note +create --text "示例笔记第一行\n示例笔记第二行"

# JSON 格式输出（含新建 note_id）
zsxq-cli note +create --text "示例笔记内容" --json

# 带图片的笔记
zsxq-cli note +create --text "记录" --files idea.jpg
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--text <text>` | **是** | 笔记内容 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔（仅图片） |
| `--json` | 否 | 输出原始 JSON（含 note_id、create_time） |

## 输出

```
✓ Note created
{
  "note_id": "444555666777",
  "create_time": "2026-04-01T15:45:31.007+0800",
  "text": "示例笔记内容"
}
```

## 推荐工作流

```bash
# 第一步：与用户确认笔记内容（公开可访问，避免写入隐私）
# 第二步：执行创建
zsxq-cli note +create --text "笔记内容"

# 第三步：（可选）拿到 note_id 后立即查看，确认内容正确
zsxq-cli note +detail --note-id <新建的 note_id>
```

## 失败语义

写入失败即原子回滚 —— 不会留下空笔记或半成品 note_id。重试前请先确认参数是否合法。

## 错误说明

通用错误（401 等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-note-edit](zsxq-note-edit.md) — 编辑笔记
- [zsxq-note-delete](zsxq-note-delete.md) — 删除笔记
- [zsxq-topic-create](../../zsxq-topic/references/zsxq-topic-create.md) — 在星球内发布主题（帖子）
- [zsxq-shared](../../zsxq-shared/SKILL.md)
