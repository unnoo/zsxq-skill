# note +delete（删除笔记）

对应命令：`zsxq-cli note +delete`。

删除指定笔记。删除后**不可恢复**。

> [!CAUTION]
> 这是**不可逆的破坏性操作** —— 删除后笔记将永久消失，无法恢复。执行前必须向用户确认：
> 1. 目标笔记（note_id）及其内容
> 2. 明确用户确实要删除

## 命令

```bash
# 删除笔记
zsxq-cli note +delete --note-id 444555666777
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--note-id <id>` | **是** | 笔记 ID（从 `note +list` 获取） |

## 推荐工作流

```bash
# 第一步：确认笔记内容
zsxq-cli note +detail --note-id 444555666777

# 第二步：向用户确认后执行删除
zsxq-cli note +delete --note-id 444555666777
```

## 失败语义

删除失败即原子回滚 —— 笔记保持原状不会被部分删除。

## 错误说明

通用错误（401、`--note-id is required`、笔记不存在、无权限等）见 [auth-errors](auth-errors.md#常见错误处理)。本命令无特有错误。

## 参考

- [note-detail](note-detail.md) — 删除前确认笔记内容
- [note-list](note-list.md) — 查看笔记列表获取 note_id
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
