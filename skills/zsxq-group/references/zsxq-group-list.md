# group +list（列出星球）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli group +list`。

列出当前登录用户**创建**的知识星球列表。常用于获取 `group_id` 供后续操作使用。

## 命令

```bash
# 列出创建的星球（默认最多 10 个，表格显示）
zsxq-cli group +list

# 返回更多结果
zsxq-cli group +list --limit 50

# 包含所有状态的星球（含已关闭等）
zsxq-cli group +list --scope all

# JSON 格式输出（含完整字段）
zsxq-cli group +list --json
```

## 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit <n>` | 否 | 10 | 最多返回数量（1–200） |
| `--scope <s>` | 否 | `normal` | `normal`：正常星球；`all`：所有状态 |
| `--json` | 否 | — | 输出原始 JSON（含 owner、statistics 等完整字段） |

## 输出（表格模式）

| GROUP ID | NAME |
|----------|------|
| 123456789 | 示例星球 |

## 说明

- 此命令只列出当前用户**创建**的星球，不含加入的他人星球
- 若需要查看加入的星球，使用 `--scope all` 或通过 `zsxq-cli api call get_user_groups` 配合参数调用
- `group_id` 是纯数字字符串，后续 `+topics`、`+hashtags` 等命令均需要此值

## 参考

- [zsxq-group-topics](zsxq-group-topics.md) — 查看星球内主题
- [zsxq-group-hashtags](zsxq-group-hashtags.md) — 查看星球标签
- [zsxq-shared](../../zsxq-shared/SKILL.md)
