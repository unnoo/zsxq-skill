# note +list（查看笔记列表）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli note +list`。

查看当前登录用户的个人笔记列表，按创建时间倒序排列。

## 命令

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

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 返回条数，默认 20，最大 30 |
| `--end-time <time>` | 否 | 分页游标，传入上一页最后一条的 `create_time` |
| `--json` | 否 | 输出原始 JSON |

## 输出（表格模式）

| NOTE ID | CONTENT | CREATED AT |
|---------|---------|------------|
| 444555666777 | 示例笔记内容… | 2026-04-10T09:00:00.000+0800 |

## 参考

- [zsxq-note-create](zsxq-note-create.md) — 创建笔记
- [zsxq-shared](../../zsxq-shared/SKILL.md)
