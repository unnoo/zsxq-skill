# group 专栏列表（通过 api raw）

列出指定星球的全部专栏，用于按专栏名称找到 `column_id`（收录主题、浏览专栏主题都要用到）。CLI 未封装该能力，通过 `api raw` 调用原始 HTTP 接口获取。

## 命令

```bash
# 获取星球的专栏列表
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/columns

# 示例
zsxq-cli api raw --method GET --path /v2/groups/888888888/columns
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<group_id>` | **是** | 星球 ID（拼接到 URL 路径中，从 `group +list` 获取） |

## 输出

`api raw` 返回完整响应封套，专栏列表位于 `body.resp_data.columns`：

```json
{
  "body": {
    "resp_data": {
      "columns": [
        {
          "column_id": 888888888001,
          "name": "精华归档",
          "cover_url": "https://file.zsxq.com/column_cover.png",
          "statistics": { "topics_count": 10 },
          "create_time": "2025-01-01T00:00:00.000+0800",
          "last_topic_attach_time": "2025-06-01T00:00:00.000+0800"
        }
      ]
    },
    "succeeded": true
  },
  "status_code": 200,
  "success": true
}
```

`columns[]` 每项字段：

| 字段 | 说明 |
|------|------|
| `column_id` | 专栏 ID，设置主题所属专栏（[topic-attached-columns](topic-attached-columns.md)）、浏览专栏主题时使用 |
| `name` | 专栏名称，用于按名字定位目标专栏 |
| `statistics.topics_count` | 专栏内主题数，判断是否接近每栏 100 条上限 |
| `create_time` | 专栏创建时间 |
| `last_topic_attach_time` | 最近一次添加主题到专栏的时间（可选，仅在部署 v2.25.0 后添加过主题时返回） |
| `cover_url` | 专栏封面图链接 |

## 说明

- 该接口未封装为 shortcut 或 `api call`，只能用 `api raw --method GET` 调用；成员（含已过期成员）可读。
- **按专栏名找 `column_id`**：遍历 `columns[]`，把 `name` 与用户给出的专栏名称比对，取匹配项的 `column_id`。命中**多个同名**或**一个都没匹配到**时，列出候选（`column_id` + `name`）让用户确认，不要默认取第一个。
- `columns[]` 为空数组表示该星球未开通专栏或暂无专栏，属正常返回、不是错误。需要创建专栏时见 [group-column-create](group-column-create.md)。
- `columns[]` 已按服务端排好的展示顺序返回，无需再排序。

## 错误说明

本接口无特有错误。通用错误（401、403 无权限、404 星球不存在、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-column-create](group-column-create.md) — 创建新专栏
- [topic-attached-columns](topic-attached-columns.md) — 拿到 `column_id` 后读取/设置主题所属专栏
- [group-list](group-list.md) — 获取 `group_id`
- [批量收录主题到专栏](scenarios/archive-topics-to-column.md) — 组合本操作的场景
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
