# group +hashtags（查看星球标签）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli group +hashtags`。

列出指定星球内所有的话题标签（Hashtag）及其主题数量。常用于获取 `hashtag_id` 以便按分类浏览内容。

## 命令

```bash
# 列出星球所有标签（表格显示）
zsxq-cli group +hashtags --group-id 123456789

# JSON 格式（含 hashtag_id、owner 等完整字段）
zsxq-cli group +hashtags --group-id 123456789 --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID（从 `group +list` 获取） |
| `--json` | 否 | 输出原始 JSON |

## 输出（表格模式）

| HASHTAG ID | TITLE | TOPIC COUNT |
|------------|-------|-------------|
| 333444555666 | #示例标签# | 12 |
| 333444555677 | #示例标签二# | 5 |

## 按标签浏览主题

获得 `hashtag_id` 后，可通过 API 列出该标签下的所有主题：

```bash
zsxq-cli api call get_hashtag_topics \
  --params '{"hashtag_id":"333444555666","limit":20}'

# 翻页
zsxq-cli api call get_hashtag_topics \
  --params '{"hashtag_id":"333444555666","limit":20,"end_time":"2025-11-01T00:00:00.000+0800"}'
```

## 参考

- [zsxq-group-topics](zsxq-group-topics.md) — 浏览星球全部主题
- [zsxq-topic-search](../../zsxq-topic/references/zsxq-topic-search.md) — 关键词搜索主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
