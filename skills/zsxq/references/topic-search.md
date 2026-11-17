# topic +search（语义与关键词搜索）

在指定星球内检索主题。话题、观点和“某成员谈过什么”优先语义检索；确切名称、术语、筛选和时间排序使用关键词检索。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 增强语义检索
zsxq-cli topic +search --group-id 123456789 --query "Go 语言" --json

# MCP 等效语义检索：可按成员别名和时间窗过滤
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/rag/topics/search","query":{"group_id":"123456789","query":"产品设计","alias":"示例成员","size":20}}'

# 关键词检索：按时间排序并使用 index 翻页
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/search/groups/123456789/topics","query":{"keyword":"产品设计","filter_types":"talk","order_by":"time","index":0,"count":20},"shape":"topic.excerpt"}'
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

语义检索，不传 `shape`：

```json
{"method": "GET", "path": "/v2/rag/topics/search", "query": {"group_id": "123456789", "query": "产品设计", "size": 20}}
```

关键词检索：

```json
{"method": "GET", "path": "/v2/search/groups/123456789/topics", "query": {"keyword": "产品设计", "count": 20, "index": 0}, "shape": "topic.excerpt"}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `group_id` | **是** | 单个星球 ID |
| `query` | **是** | 词、短语或完整问题，去掉首尾空白后不能为空 |
| `size` | 否 | 返回条数，默认 20，不超过 30；环境上限可能更低，按错误修正一次 |
| `alias` | 否 | 成员在星球内的别名或昵称；先匹配别名再匹配昵称，匹配不到返回空，不降级为全星球搜索 |
| `start_time` / `end_time` | 否 | 主题创建时间窗，格式 `2026-01-01T00:00:00.000+0800` |
| `shape` | 不使用 | 该伪接口不支持响应裁剪 |

关键词检索 `/v2/search/groups/{group_id}/topics`：

| 参数 | 必填 | 说明 |
|------|------|------|
| `keyword` | **是** | 1–128 字；多个名称分别查询，不拼成一个关键词 |
| `filter_roles` | 否 | 逗号分隔：`owner`、`partner`、`guest`、`admin`、`member` |
| `filter_types` | 否 | 逗号分隔：`digests`、`talk`、`qa`、`task`、`solution`、`checkin` |
| `order_by` | 否 | `default` 综合排序；`time` 按时间从新到旧 |
| `index` | 翻页必填 | 第一页为 0，之后传上一页返回的 `resp_data.index` |
| `count` | 否 | 每页条数，建议 20 |
| `shape` | 否 | 列表筛选建议 `topic.excerpt`，精读再取完整详情 |

### 通道映射

| CLI flag / 形式 | HTTP 字段 |
|-----------------|-----------|
| `--group-id` / `query.group_id` | 语义检索的 `query.group_id`；关键词检索的 path `group_id` |
| `--query` | 语义检索的 `query.query`；关键词检索的 `query.keyword` |
| `query` JSON | 同名 query 参数 |
| `shape` | `call_zsxq_api` 顶层裁剪参数，不放入 query；语义检索禁用 |

## 输出

语义检索返回 `body.topics[]` 和 `body.rag_response`，不是普通的 `body.resp_data` 列表；主题包含正文和来源信息，按相关度排列，无翻页。`rag_response.results[]` 是检索证据，最终引用以实际返回主题为准。

关键词检索返回 `body.resp_data.topics[]` 和下一页 `index`。`topic.excerpt` 用于筛选，获得 `topic_id` 后用 [topic-detail](topic-detail.md) 精读。

<!-- cli-only:start -->

CLI shortcut 默认表格输出；`--json` 返回完整主题。CLI 通道无条数参数，需要增强检索的排序质量时使用 shortcut，不与 MCP 结果混排。

<!-- cli-only:end -->

## 说明

- 单星球检索；跨星球按 [search-across-groups](scenarios/search-across-groups.md) 组合，不拼多个 `group_id`。
- 语义检索无分页，可用关键词检索补充；关键词支持筛选和翻页，但都不是全星球完整枚举。
- 多个名称分别查。`alias` 无结果时先用 [group-members](group-members.md) 确认名字再修正一次，不自动搜全星球。
- 精读后再下结论。零命中不等于没有相关内容；图片 URL 不等于模型已经看过图片。

## 推荐工作流

1. 用 [group-list](group-list.md) 确认 `group_id`，按意图选择语义或关键词路径。
2. 多次查询按 `topic_id` 去重并保留来源；入选主题用 [topic-detail](topic-detail.md) 精读后再总结。
3. 输出查询范围和零命中/截断情况；需要链接时按 [share-links](share-links.md) 拼接。

## 错误说明

| 症状 | 处理 |
|------|------|
| 语义检索 `size` 超过环境上限 | 按错误提示缩小一次，不循环尝试 |
| `alias` 无结果 | 确认成员别名/昵称后修正一次，不自动搜全星球 |
| 关键词返回空列表 | 换用语义检索或相关词；不得表述为星球没有该内容 |

通用错误（401、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 查看主题完整详情
- [search-across-groups](scenarios/search-across-groups.md) — 跨星球检索
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
