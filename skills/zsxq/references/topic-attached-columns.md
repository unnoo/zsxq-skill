# 主题所属专栏（读取 / 设置，通过 api raw）

读取一条主题当前所属的专栏列表，或覆盖式设置它所属的专栏集合。CLI 未封装为 shortcut，通过 `api raw` 调用原始 HTTP 接口（action `group_topic/attachedcolumns` 读取、`group_topic/attachtopicstocolumn` 设置）。**「把主题加入某专栏」= 先读现有专栏 → 并入目标 → 整表回设**。

> [!CAUTION]
> 设置操作是**替换性写入** —— 会改变主题的专栏归属。执行前必须向用户确认：
> 1. 目标主题（`topic_id`）
> 2. 设置后该主题应所属的**完整**专栏集合（`column_ids`，用 [group-columns](group-columns.md) 核对每个 `column_id` 与名称）
> 3. 「加入」场景务必已**并入原有专栏**（见下方 IMPORTANT），避免把主题踢出其他专栏
> 4. 操作身份具备权限（星主、合伙人或管理员）

> [!IMPORTANT]
> - **替换语义**：`POST` 的 `column_ids` 是**全量替换**，不在列表中的原有专栏会被取消；传空数组 `[]` = 把该主题移出**所有**专栏。要「新增」而非「替换」，必须先 `GET` 读出现有 `column_ids`、并入目标、去重后再整表 `POST`。
> - **每专栏 100 主题上限**：`column_ids` 中未超限的专栏会设置成功，已超限的专栏设置失败；若结果里存在超限专栏，接口返回错误 code。

## 命令

```bash
# ① 读取主题当前所属的专栏列表
zsxq-cli api raw --method GET --path /v2/topics/<topic_id>/attached_columns

# ② 覆盖式设置主题所属的专栏集合（--body 会自动包装 req_data）
zsxq-cli api raw --method POST \
  --path /v2/topics/<topic_id>/attached_columns \
  --body '{"column_ids": [888888888001, 888888888002]}'

# 移出所有专栏：传空数组
zsxq-cli api raw --method POST \
  --path /v2/topics/<topic_id>/attached_columns \
  --body '{"column_ids": []}'
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<topic_id>` | **是** | 主题 ID（路径参数，从 `group +topics` / `topic +search` 获取） |
| `column_ids` | **是** | 设置后该主题应所属的**完整**专栏 ID 列表（请求体，全量替换）。`column_id` 从 [group-columns](group-columns.md) 获取；空数组表示移出所有专栏 |

## 输出

**读取**：`body.resp_data.columns[]`，每项为专栏对象（`column_id` / `name` / `statistics.topics_count` 等，格式同 [group-columns](group-columns.md)）；已归入主题的专栏项会多带一个 `last_topic_attach_time`。无归属时 `columns` 为空数组 `[]`。

```json
{
  "body": {
    "resp_data": {
      "columns": [
        {
          "column_id": 888888888001,
          "name": "精华归档",
          "last_topic_attach_time": "2025-06-01T00:00:00.000+0800",
          "statistics": { "topics_count": 5 }
        }
      ]
    },
    "succeeded": true
  },
  "status_code": 200,
  "success": true
}
```

**设置**：成功时 `resp_data` 为空对象、以 `succeeded` / `success` 为 `true` 表示成功（不回显专栏列表，需另发一次读取复核）；若存在超限专栏则返回错误 code。

```json
{
  "body": { "resp_data": {}, "succeeded": true },
  "status_code": 200,
  "success": true
}
```

## 推荐工作流

把主题加入目标专栏（保留原有归属）：

```bash
# 第一步：拿到 group_id，查专栏列表找到目标 column_id、并看现有 topics_count 是否接近 100
zsxq-cli group +list
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/columns

# 第二步：读出该主题现有所属专栏，收集其 column_id
zsxq-cli api raw --method GET --path /v2/topics/<topic_id>/attached_columns

# 第三步：把目标 column_id 并入现有集合、去重，与用户确认最终完整列表

# 第四步：整表回设（现有 + 目标，去重后的完整 column_ids）
zsxq-cli api raw --method POST \
  --path /v2/topics/<topic_id>/attached_columns \
  --body '{"column_ids": [<现有...>, <目标>]}'
```

移出某专栏：同样先读现有集合，从中**剔除**该专栏后整表回设。

## 失败语义

设置为单次整表替换：请求成功即该主题专栏归属被设为所给集合；失败即维持原状、不产生部分变更。当 `column_ids` 含已达 100 上限的专栏时，未超限专栏仍会设置成功、超限专栏失败，并返回错误 code —— 属**部分成功**，需读取复核实际结果。

## 错误说明

| 错误 | 原因 |
|------|------|
| 上限错误 code | `column_ids` 中某专栏已达 100 主题上限，该专栏设置失败 |
| 无权限 / `code` 类权限错误 | 当前账户非星主 / 合伙人 / 管理员，无权设置 |
| `429`「操作过于频繁，请稍后重试」 | 短时间内密集写入触发限流。放慢节奏、每次写入间隔约 2 秒后重试；批量场景见 [archive-topics-to-column](scenarios/archive-topics-to-column.md) |
| `接口 ... 不存在，请检查路径是否正确` | 当前 zsxq-cli 版本的底层接口工具尚未登记该路径，需升级 zsxq-cli（该接口为主题维度 `attached_columns`，替代已废弃的 column 维度收录接口） |

通用错误（401、404 主题不存在、`--body` / 参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-columns](group-columns.md) — 查专栏列表、找 `column_id`、看 `topics_count`
- [group-topics](group-topics.md) — 获取待设置主题的 `topic_id`
- [topic-tags](topic-tags.md) — 同为覆盖式写入的近义操作（标签），注意同类「先读后并」陷阱
- [批量收录主题到专栏](scenarios/archive-topics-to-column.md) — 批量把主题归入专栏的场景编排
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
