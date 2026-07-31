# 设置主题标签（api call set_topic_tags）

通过 `zsxq-cli api call set_topic_tags` 为某主题设置标签（hashtag），返回更新后的主题简要信息。

> [!CAUTION]
> 这是**写入操作** —— 会改变主题的标签。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 完整的标签列表（`titles`）—— 见下方 IMPORTANT

> [!IMPORTANT]
> `titles` 是本次要设置的**完整标签集合**，不是「追加一个标签」。为避免误删原有标签，先用 `topic +detail` 查看该主题当前标签，把需要保留的一并放进 `titles` 再提交。

## 命令

```bash
# 为主题设置标签（数组形式，可多个）
zsxq-cli api call set_topic_tags --params '{"topic_id":"123","titles":["标签1","标签2"]}'
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `topic_id` | **是** | 主题 ID（字符串，从 `topic +search` / `group +topics` 获取） |
| `titles` | **是** | 标签标题的**字符串数组**（如 `["产品","增长"]`）；无需带 `#`，为本次设置的完整标签集合 |

## 输出

成功后返回更新后的主题简要信息（含新的标签）；具体字段以 `api call` 实际输出为准。

## 推荐工作流

```bash
# 第一步：查看主题现有标签，避免覆盖时误删
zsxq-cli topic +detail --topic-id 123

# 第二步：与用户确认「最终完整标签集合」后执行
zsxq-cli api call set_topic_tags --params '{"topic_id":"123","titles":["产品","增长"]}'
```

> 查看星球已有哪些标签可用 `group +hashtags`（见 [group-hashtags](group-hashtags.md)）。

## 失败语义

设置失败即不改变原标签，不会产生半更新状态。

## 错误说明

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 无权限 / `code` 类权限错误 | 当前账户无权修改该主题标签（非作者/星主） | 用有权限的账户操作 |

通用错误（401、`topic_id` / `titles` 缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 操作前查看主题当前标签
- [group-hashtags](group-hashtags.md) — 查看星球已有标签
- [topic-digest](topic-digest.md) — 设置/取消精华（同为写入类 api call）
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
