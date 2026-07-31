# group 创建专栏（通过 api raw）

在指定星球中创建新专栏。CLI 未封装为 shortcut，通过 `api raw` 调用原始 HTTP 接口。

> [!CAUTION]
> 创建专栏是**写入操作**，执行前必须向用户确认：
> 1. 目标星球（`group_id` + 名称）
> 2. 专栏名称（`name`）
> 3. 操作身份具备权限（星主、合伙人或管理员）

## 命令

```bash
# 创建专栏
zsxq-cli api raw --method POST \
  --path /v2/groups/<group_id>/columns \
  --body '{"name":"专栏名称"}'

# 示例
zsxq-cli api raw --method POST \
  --path /v2/groups/888888888/columns \
  --body '{"name":"精华归档"}'
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<group_id>` | **是** | 星球 ID（拼接到 URL 路径中，从 `group +list` 获取） |
| `name` | **是** | 专栏名称（请求体字段） |

## 输出

成功时返回新创建的专栏对象（含 `column_id`）：

```json
{
  "body": {
    "resp_data": {
      "column": {
        "column_id": 888888888001,
        "name": "精华归档",
        "cover_url": "https://file.zsxq.com/column_cover.png",
        "create_time": "2025-01-01T00:00:00.000+0800",
        "statistics": {
          "topics_count": 0
        }
      }
    },
    "succeeded": true
  },
  "status_code": 200,
  "success": true
}
```

`column` 对象字段：

| 字段 | 说明 |
|------|------|
| `column_id` | 专栏 ID，后续收录主题、浏览专栏内容时使用 |
| `name` | 专栏名称 |
| `statistics.topics_count` | 专栏内主题数（新创建为 0） |
| `create_time` | 专栏创建时间 |
| `cover_url` | 专栏默认封面图链接 |

## 推荐工作流

```bash
# 1. 确定目标星球
zsxq-cli group +list

# 2. 创建专栏
zsxq-cli api raw --method POST \
  --path /v2/groups/<group_id>/columns \
  --body '{"name":"专栏名称"}'

# 3. 验证创建结果（查专栏列表确认新专栏在列）
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/columns
```

## 失败语义

创建为单次原子请求：请求成功即专栏已创建；失败即不产生任何变更。

## 错误说明

| 错误 | 原因 |
|------|------|
| 无权限 / `code` 类权限错误 | 当前账户非星主 / 合伙人 / 管理员，无权创建专栏 |
| 专栏名重复 | 星球内专栏名需唯一，同名创建可能返回错误 |
| `429`「操作过于频繁，请稍后重试」 | 短时间内密集请求触发限流，退避几秒后重试 |

通用错误（401、404 星球不存在、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-columns](group-columns.md) — 列出星球全部专栏
- [topic-attached-columns](topic-attached-columns.md) — 读取/设置主题所属专栏
- [批量收录主题到专栏](scenarios/archive-topics-to-column.md) — 组合本操作的场景
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
