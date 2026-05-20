# topic +answer（回答提问）

本 skill 对应 shortcut：`zsxq-cli topic +answer`。

对 `q&a` 类型的主题发布**官方回答**。仅适用于问答类主题，且每个问题只能回答一次。

> [!CAUTION]
> 这是**公开写入操作**，且**每个问题只能回答一次**，回答后无法修改。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其问题内容
> 2. 回答的完整内容

> [!IMPORTANT]
> `+answer` 与 `+reply` 的区别：
> - `+answer`：发布"官方回答"，附加在问题下方，标记为已回答（`q&a` 专用，只能用一次）
> - `+reply`：发表普通评论，适用于所有类型主题，可发多条

## 命令

```bash
# 回答一个提问
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "示例回答内容"

# JSON 格式输出
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "示例回答内容" \
  --json

# 带附件的回答
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "示例回答内容" \
  --files diagram.png
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID（必须是 `q&a` 类型） |
| `--text <text>` | **是** | 回答正文 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔 |
| `--json` | 否 | 输出原始 JSON |

## 推荐工作流

先确认主题类型，再发布：

```bash
# 第一步：确认目标主题是 q&a 类型并核对问题内容
zsxq-cli topic +detail --topic-id 111222333466 --json
# 查看返回 JSON 中的 "type" 是否为 "q&a"

# 第二步：确认无误后发布回答
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "示例回答内容"
```

如果不知道有哪些待回答的提问，先列一下：

```bash
# 自己发起的未回答提问
zsxq-cli api call get_self_question_topics --params '{"topic_filter":"unanswered","count":20}'

# 别人向我发起的未回答提问
zsxq-cli api call get_self_answer_topics --params '{"topic_filter":"unanswered","count":20}'
```

> `get_self_question_topics` / `get_self_answer_topics` 还支持 `topic_filter:"answered"` 查看已回答记录。

## 失败语义

写入失败即原子回滚 —— 失败不会消耗"每题只能回答一次"的额度，确认参数后可重试。

## 错误说明

| 错误 | 原因 |
|------|------|
| `问题已回答` | 该主题已有官方回答，每题只能回答一次 |
| `topic is not q&a` | 主题类型不是提问，应使用 `+reply` 发评论 |

通用错误（401、`--topic-id is required`、主题不存在等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-topic-reply](zsxq-topic-reply.md) — 发表普通评论（适用于所有类型）
- [zsxq-topic-detail](zsxq-topic-detail.md) — 查看主题详情和类型
- [zsxq-shared](../../zsxq-shared/SKILL.md)
