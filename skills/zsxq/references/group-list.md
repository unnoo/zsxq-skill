# group +list（列出星球）

对应操作：`group +list`；MCP 调用见下方命令块。

列出当前登录用户**加入或创建**的所有知识星球。常用于获取 `group_id` 供后续操作使用。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 列出星球（默认最多 10 个，表格显示）
zsxq-cli group +list

# 返回更多结果
zsxq-cli group +list --limit 50

# JSON 格式输出（含完整字段）
zsxq-cli group +list --json
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/groups"}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 最多返回数量，默认 10，最大 200 |
| `--json` | 否 | 输出原始 JSON（含 owner、statistics 等完整字段） |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--limit` | 不上送（由工具在本地校验与截断；MCP 通道由 agent 自行截断返回列表） |
| `--scope` | 不上送（同上） |
| — | `user_id` 不需要（CLI 取本地 config，MCP 通道无需） |

## 输出

<!-- cli-only:start -->

CLI 通道默认表格输出（`--json` 为 JSON）：

| GROUP ID | NAME |
|----------|------|
| 123456789 | 示例星球 |

<!-- cli-only:end -->

MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

MCP 通道返回 `body.resp_data.groups[]`（含 owner、statistics 等完整字段），无条数参数，截断由 agent 自行处理。

## 说明

- 返回结果同时包含用户**加入**和**创建**的星球
- `group_id` 是纯数字字符串，后续 `+topics`、`+hashtags` 等命令均需要此值
- 用户只给星球名称时按名称匹配：命中多个相似星球要列出候选（`group_id` + 名称）让用户确认，**不默认取第一个**；一个都没命中则请用户核对名称或直接给 `group_id`
<!-- cli-only:start -->
- 如需在结果中区分"加入 / 创建"，使用 `--json` 查看完整字段
<!-- cli-only:end -->

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 当前账户尚未加入或创建任何星球 | 确认登录账户：`user +info` |

通用错误（401 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-topics](group-topics.md) — 查看星球内主题
- [group-hashtags](group-hashtags.md) — 查看星球标签
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
