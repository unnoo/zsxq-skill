# group +list（列出星球）

本 skill 对应 shortcut：`zsxq-cli group +list`。

列出当前登录用户**加入或创建**的所有知识星球。常用于获取 `group_id` 供后续操作使用。

## 命令

```bash
# 列出星球（默认最多 10 个，表格显示）
zsxq-cli group +list

# 返回更多结果
zsxq-cli group +list --limit 50

# JSON 格式输出（含完整字段）
zsxq-cli group +list --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 最多返回数量，默认 10，最大 200 |
| `--json` | 否 | 输出原始 JSON（含 owner、statistics 等完整字段） |

## 输出（表格模式）

| GROUP ID | NAME |
|----------|------|
| 123456789 | 示例星球 |

## 说明

- 返回结果同时包含用户**加入**和**创建**的星球
- `group_id` 是纯数字字符串，后续 `+topics`、`+hashtags` 等命令均需要此值
- 如需在结果中区分"加入 / 创建"，使用 `--json` 查看完整字段

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 当前账户尚未加入或创建任何星球 | 确认登录账户：`zsxq-cli user +info` |

通用错误（401 等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-group-topics](zsxq-group-topics.md) — 查看星球内主题
- [zsxq-group-hashtags](zsxq-group-hashtags.md) — 查看星球标签
- [zsxq-shared](../../zsxq-shared/SKILL.md)
