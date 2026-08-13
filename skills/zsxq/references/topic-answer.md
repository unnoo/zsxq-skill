# topic +answer（回答提问）

对应命令：`zsxq-cli topic +answer`。

对 `q&a` 类型的主题发布**官方回答**。仅适用于问答类主题，且每个问题只能回答一次。

> [!CAUTION]
> 这是**公开写入操作**，且**每个问题只能回答一次**，回答后无法修改。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其问题内容
> 2. 回答的完整内容
> 3. 若为定时回答：发布时间（到点自动发布，无需再确认）与是否静默（仅提醒提问者）

> [!IMPORTANT]
> `+answer` 与 `+reply` 的区别：
> - `+answer`：发布"官方回答"，附加在问题下方，标记为已回答（`q&a` 专用，只能用一次）
> - `+reply`：发表普通评论，适用于所有类型主题，可发多条

> [!IMPORTANT]
> 定时回答（`--scheduled-time`）：
> - 时间必须**晚于当前时间**且在**未来 14 天以内**；任务同样占用星球定时任务配额（每星球上限 10，见 [topic-scheduled](topic-scheduled.md)）
> - 定时回答任务到点自动发布，可用 `topic +unschedule` 取消；不支持经 `topic +schedule --job-id` 修改

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

# 定时回答（到点自动发布）
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "定时回答内容" \
  --scheduled-time "2026-08-14 12:00"

# 定时静默回答（仅提醒提问者）
zsxq-cli topic +answer \
  --topic-id 111222333466 \
  --text "定时回答内容" \
  --scheduled-time "2026-08-14 12:00" \
  --silenced
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID（必须是 `q&a` 类型） |
| `--text <text>` | **是** | 回答正文 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔 |
| `--scheduled-time <time>` | 否 | 定时发布时间，如 `"2026-08-14 12:00"`；不传则立即回答 |
| `--silenced` | 否 | 静默回答：仅提醒提问者（仅与 `--scheduled-time` 同用） |
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

写入失败即原子回滚 —— 失败不会消耗"每题只能回答一次"的额度，也不会产生定时任务，确认参数后可重试。

## 错误说明

| 错误 | 原因 |
|------|------|
| `问题已回答` | 该主题已有官方回答，每题只能回答一次 |
| `topic is not q&a` | 主题类型不是提问，应使用 `+reply` 发评论 |
| `--silenced 仅支持与 --scheduled-time 一起使用` | 立即回答却要求静默 |
| `定时回答仅支持问答主题（当前: <type>），普通主题请使用 topic +reply 或 topic +schedule` | 定时回答只用于 `q&a` |
| `无法解析时间 "..."，请使用 "2026-08-14 10:00" 或 "2026-08-14T10:00:00" 格式` | 时间格式不对 |
| `定时时间必须晚于当前时间（当前: ...）` / `定时时间必须在未来 14 天以内` | 时间超出允许窗口 |

通用错误（401、`--topic-id is required`、主题不存在等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-reply](topic-reply.md) — 发表普通评论（适用于所有类型）
- [topic-detail](topic-detail.md) — 查看主题详情和类型
- [topic-schedule](topic-schedule.md) — 定时发布主题
- [topic-unschedule](topic-unschedule.md) — 取消定时回答任务
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
