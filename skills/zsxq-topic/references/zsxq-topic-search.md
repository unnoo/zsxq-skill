# topic +search（搜索主题）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli topic +search`。

在指定星球内进行全文搜索，返回匹配的主题列表。搜索使用 RAG 服务，结果按相关性排序。

## 命令

```bash
# 在星球内搜索关键词（表格显示）
zsxq-cli topic +search --group-id 123456789 --query "Go 语言"

# 搜索中文内容
zsxq-cli topic +search --group-id 123456789 --query "产品设计"

# JSON 格式输出（含完整 topic 字段）
zsxq-cli topic +search --group-id 123456789 --query "AI" --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--query <text>` | **是** | 搜索关键词，支持中英文 |
| `--json` | 否 | 输出原始 JSON |

## 输出（表格模式）

| TOPIC ID | TYPE | TITLE / DIGEST | CREATED AT |
|----------|------|----------------|------------|
| 111222333444 | talk | 示例主题标题 | 2025-12-31T09:19:28.239+0800 |

## 说明

- 搜索范围限定在单个星球内，不支持跨星球搜索
- 结果数量由服务端决定，不支持 `--limit` 参数
- 若需要按时间浏览（而非搜索），改用 `group +topics`
- 获得 `topic_id` 后，用 `topic +detail` 查看完整内容

## 参考

- [zsxq-topic-detail](zsxq-topic-detail.md) — 查看主题完整详情
- [zsxq-group-topics](../../zsxq-group/references/zsxq-group-topics.md) — 按时间浏览主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
