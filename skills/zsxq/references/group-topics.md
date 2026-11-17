# group +topics（主题时间线与精华列表）

对应操作：`group +topics`；MCP 调用见下方命令块。

按时间倒序浏览指定星球的主题，支持时间窗、内容范围筛选和分页；也可单独读取精华列表。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 列出星球最新 20 条主题（表格显示）
zsxq-cli group +topics --group-id 123456789

# 返回更多（最多 30），或按游标翻页
zsxq-cli group +topics --group-id 123456789 --limit 30
zsxq-cli group +topics --group-id 123456789 --end-time "2025-12-01T00:00:00.000+0800"

# MCP 等效调用：限定时间下界并裁剪列表
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/groups/123456789/topics","query":{"scope":"all","begin_time":"2026-01-01T00:00:00.000+0800","count":30},"shape":"topic.excerpt"}'

# 精华列表：count 必传
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/groups/123456789/topics/digests","query":{"sort":"by_create_time","direction":"desc","count":30}}'
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/groups/123456789/topics", "query": {"scope": "all", "begin_time": "2026-01-01T00:00:00.000+0800", "count": 30}, "shape": "topic.excerpt"}
```

精华列表：

```json
{"method": "GET", "path": "/v2/groups/123456789/topics/digests", "query": {"sort": "by_create_time", "direction": "desc", "count": 30}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `group_id` | **是** | 星球 ID（从 `group +list` 获取） |
| `scope` | 否 | `all`（默认）、`digests` 精华、`by_owner` 星主和合伙人发布的主题（不含他们的回答）、`questions` 问答、`unanswered_questions` 未回答提问、`tasks` 作业 |
| `begin_time` | 否 | 时间窗下界，格式 `2026-01-01T00:00:00.000+0800` |
| `end_time` | 否 | 时间窗上界；翻页时取本页末条 `create_time` |
| `count` | 否 | 每页条数，默认 20，最大 30 |
| `shape` | 否 | 列表筛选建议 `topic.excerpt`，保留摘要、作者、互动和精华/置顶状态，附件只留数量 |

精华列表：

| 参数 | 必填 | 说明 |
|------|------|------|
| `sort` | 否 | 使用 `by_create_time` |
| `count` | **是** | 1–30；缺失会返回 `14001 无效的count` |
| `direction` | 否 | `desc`（默认）或 `asc` |
| `hashtag_id` | 否 | 只读指定标签下的精华 |
| `index` | 否 | 翻页时传上一页返回的 `resp_data.index` |

### 通道映射

| CLI flag / 形式 | HTTP 字段 |
|-----------------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/topics` |
| `--limit` / `query.count` | `query.count` |
| `--end-time` / `query.end_time` | `query.end_time` |
| `--scope` / `query.scope` | `query.scope` |
| `query.begin_time` | `query.begin_time` |
| `shape` | `call_zsxq_api` 顶层裁剪参数，不放入 query |

## 输出

MCP 时间线返回 `body.resp_data.topics[]`。`topic.excerpt` 包含主题 ID、作者、时间、互动数、精华/置顶状态和正文摘要，图片与文件只保留数量；精读使用 [topic-detail](topic-detail.md)。

精华列表返回 `body.resp_data.topics[]` 和 `index`，条目本身以标题、作者、时间和互动数为主，不传 `shape`。

<!-- cli-only:start -->

CLI shortcut 默认表格输出：

| TOPIC ID | TYPE | TITLE / DIGEST | CREATED AT |
|----------|------|----------------|------------|
| 111222333444 | talk | 示例主题标题 | 2025-12-31T09:19:28.239+0800 |

<!-- cli-only:end -->

## 说明

- `begin_time` 是时间下界，`end_time` 是上界和翻页游标；窗口终点不传时由服务端处理。相对日期以可靠的东八区当前日期计算，缺少当前日期时先确认。
- 默认从新到旧。下一页保持 `begin_time` 和其他筛选条件不变，把本页末条 `create_time` 传给 `end_time`，按 `topic_id` 去重；返回少于 `count`、越过起点或已足够回答时停止。
- 用于摘要或问答时默认最多 5 页；未覆盖完整时间窗必须说明实际截止时间。用户明确要求完整枚举时继续翻页，并披露任何截断。
- 列表预览用于筛选，精读后再下结论或引用。数量、占比只限实际读取范围，不估算全量。
- 打卡主题默认不进入普通时间线；查询打卡内容用 [group-checkins](group-checkins.md) 先定位任务，再读任务主题。
- 精华列表与普通时间线的 `scope=digests` 不是同一返回结构；需要精华专用字段和 `index` 分页时使用精华列表。

<!-- cli-only:start -->

CLI shortcut 的 `--json` 输出含 `has_more` 和 `next_end_time` 时，可直接把 `next_end_time` 用于下一页。

<!-- cli-only:end -->

## 错误说明

| 症状 | 处理 |
|------|------|
| 精华列表返回 `14001 无效的count` | 补传 1–30 的 `count` 后重试 |
| 时间窗为空 | 只表示该范围无匹配主题，不扩大权限或改用未授权入口 |

通用错误（401、参数缺失、404、游标时间格式错误等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 查看主题详情
- [topic-search](topic-search.md) — 搜索主题
- [group-checkins](group-checkins.md) — 查询打卡任务与打卡主题
- [group-hashtags](group-hashtags.md) — 按标签筛选主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
