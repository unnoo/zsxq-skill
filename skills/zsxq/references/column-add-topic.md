# 收录主题到专栏（通过 api raw）

把一条已有主题收录进指定专栏。CLI 未封装该能力，通过 `api raw` 调用原始 HTTP 接口（action `group/addcolumntopic`）。**一次请求只收录一条主题**；批量收录多条见 [批量收录主题到专栏](scenarios/archive-topics-to-column.md)。

> [!CAUTION]
> 这是**写入操作** —— 会改变专栏内容。执行前必须向用户确认：
> 1. 目标专栏（`column_id` 及专栏名称，用 [group-columns](group-columns.md) 核对）
> 2. 要收录的主题（`topic_id`，批量时为完整的 `topic_id` 列表及对应标题）
> 3. 操作身份具备权限（星主、合伙人或管理员）

> [!IMPORTANT]
> 每个专栏**最多 100 条主题**，超过上限接口会返回错误 code、收录失败。批量收录前先看目标专栏当前 `statistics.topics_count`（见 [group-columns](group-columns.md)），预估「现有数量 + 本次数量」是否超过 100。

## 命令

```bash
# 收录一条主题到专栏（--body 会自动包装 req_data）
zsxq-cli api raw --method POST \
  --path /v2/groups/<group_id>/columns/<column_id>/topics \
  --body '{"topic_id": <topic_id>}'

# 示例
zsxq-cli api raw --method POST \
  --path /v2/groups/758421284/columns/5585254544/topics \
  --body '{"topic_id": 146808189}'
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<group_id>` | **是** | 星球 ID（路径参数，从 `group +list` 获取） |
| `<column_id>` | **是** | 目标专栏 ID（路径参数，从 [group-columns](group-columns.md) 按专栏名找到） |
| `topic_id` | **是** | 要收录的主题 ID（请求体，单个值，从 `group +topics` / `topic +search` 获取） |

## 输出

成功后返回成功封套（`succeeded` / `success` 为 `true`）。本操作为写入类，文档未实执行，具体返回字段以实际调用为准。

## 推荐工作流

```bash
# 第一步：拿到 group_id（按星球名搜索或列出星球）
zsxq-cli group +list

# 第二步：查专栏列表，按专栏名找到 column_id，并看现有 topics_count 是否接近 100
zsxq-cli api raw --method GET --path /v2/groups/758421284/columns

# 第三步：确认待收录主题的 topic_id 与内容
zsxq-cli topic +detail --topic-id 146808189

# 第四步：与用户确认「目标专栏 + 主题」后执行收录
zsxq-cli api raw --method POST \
  --path /v2/groups/758421284/columns/5585254544/topics \
  --body '{"topic_id": 146808189}'
```

## 失败语义

单条收录是独立请求，失败即该条不被收录、不产生半收录状态；不影响其他主题的收录结果。达到 100 上限后，后续主题会持续返回上限错误。

## 错误说明

| 错误 | 原因 |
|------|------|
| 上限错误 code | 专栏主题数已达 100 上限，无法再收录（见 IMPORTANT） |
| 无权限 / `code` 类权限错误 | 当前账户非星主 / 合伙人 / 管理员，无权收录 |

通用错误（401、404 星球或专栏不存在、`--body` / 参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-columns](group-columns.md) — 收录前查专栏列表、找 `column_id`、看 `topics_count`
- [group-topics](group-topics.md) — 获取待收录主题的 `topic_id`
- [批量收录主题到专栏](scenarios/archive-topics-to-column.md) — 批量逐条收录的场景编排
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
