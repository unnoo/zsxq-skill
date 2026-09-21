# topic +search（搜索主题）

对应命令：CLI 通道 `zsxq-cli topic +search`；MCP 通道见下方命令块。

在指定星球内进行全文搜索，返回匹配的主题列表。搜索使用 RAG 服务，结果按相关性排序。

## 命令

**CLI 通道：**

```bash
# 在星球内搜索关键词（表格显示）
zsxq-cli topic +search --group-id 123456789 --query "Go 语言"

# 搜索中文内容
zsxq-cli topic +search --group-id 123456789 --query "产品设计"

# JSON 格式输出（含完整 topic 字段）
zsxq-cli topic +search --group-id 123456789 --query "AI" --json
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/search/groups/123456789/topics", "query": {"keyword": "关键词", "count": 20}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--query <text>` | **是** | 搜索关键词，支持中英文 |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/search/groups/{group_id}/topics` |
| `--query` | `query.keyword` |

## 输出

CLI 通道默认表格输出（`--json` 为 JSON）；MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

| TOPIC ID | TYPE | TITLE / DIGEST | CREATED AT |
|----------|------|----------------|------------|
| 111222333444 | talk | 示例主题标题 | 2025-12-31T09:19:28.239+0800 |

## 说明

- 搜索范围限定在单个星球内，不支持跨星球搜索
- 结果数量由服务端决定，CLI 通道不支持 `--limit` 参数（MCP 通道用 `count` 指定条数，见上方命令块）
- 若需要按时间浏览（而非搜索），改用 `group +topics`
- 获得 `topic_id` 后，用 `topic +detail` 查看完整内容
- 搜索为语义/模糊匹配（RAG 服务），可能漏召（相关内容没被命中）或误召（命中弱相关内容），检索结果需人工复核相关性后再采用
- 无翻页与游标机制：要扩大召回请用多个近义/相关关键词分别检索再合并，不要指望单次结果覆盖全部
- MCP 通道走官方搜索端点，排序语义与 CLI 通道的增强检索不同，结果顺序可能不一致；需要 CLI 的排序质量时改用 CLI 通道

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：`group +list` 对应 `GET /v2/groups`，本命令对应上方 MCP 块，`topic +detail` 对应 `GET /v2/topics/{topic_id}/info`。

**历史内容检索 / 资料合集**——围绕一个主题（如"如何做用户增长"）把星球里讲过的相关内容捞出来，去重归类后产出一份带分享链接的合集清单或要点摘要，用于避免重复回答、整理专题合集、旧内容二次发布、给新成员补历史资料。

1. **拿 group_id**：用 `group +list` 找到目标星球 ID（见 [group-list](group-list.md)）。
2. **按关键词检索**：用本命令 `topic +search --group-id <id> --query "<关键词>"` 检索；命中偏少时换近义/相关词多跑几次（如"用户增长""拉新""获客"），靠多关键词扩大召回（本命令无 `--limit`、无翻页）。
3. **去重归类**：合并多次检索结果，按 `topic_id` 去重；结果已按相关性排序，需要"最相关的前 N 条"时在结果侧自行截取（命令本身不限制条数），可再按 `CREATED AT` 发布时间归类。
4. **补齐内容**：对入选主题用 [topic-detail](topic-detail.md) 拉完整正文与作者信息，据此写 2–3 句摘要说明这条讲了什么。
5. **产出合集**：为每条主题拼接电脑端/手机端分享链接（见 [share-links](share-links.md)），输出"标题 + 发布时间 + 摘要 + 链接"的清单；若结果不足目标条数就把命中的全列出，若多条内容重合度高则提示可整合为一篇合集。

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 关键词未命中或星球内容较少 | 换近义词或改用 `group +topics` 时间序浏览 |

通用错误（401、`--group-id is required`、`--query is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 查看主题完整详情
- [group-topics](group-topics.md) — 按时间浏览主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
