# 验证报告：triage-comments

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/triage-comments.md`（+ 原子操作 `references/topic-reply.md`） |
| 分类 | 写 · 场景（主写入 = `topic +reply`，含楼中楼 `--reply-to`） |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284）；一次性主题 A `55522441448144114`（测完已删，评论随之级联删除） |
| 原始日志 | [`logs/triage-comments.log`](logs/triage-comments.log) |
| 授权 | 用户 2026-07-28 一次性授权「研发测试 758421284 可发布/POST/PUT」；写策略=仅在自建一次性主题上回复，测完随主题 DELETE 清理 |

## 测试用例

> 主干：拉主题评论分诊 → 对需回复项 `topic +reply`（顶层）/ `--reply-to`（楼中楼）。「实际」列摘录真实输出。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 评论分诊（读）：拉主题评论 | `api call get_topic_comments {topic_id,limit}` | 返回评论供分类（需回复/风险/正常） | 见 monitor/daily-patrol：返回 text/create_time/owner，可分诊 | ✅ |
| 2 | 主干写入：发顶层回复 | `topic +reply --topic-id ...A --text "..." --json` | 回复成功，返回 comment_id | `✓ Comment posted`；`comment.comment_id=1521255452254812` | ✅ |
| 3 | 读回确认顶层评论入库 | `get_topic_comments {topic_id:...A,limit:30}` | 新评论出现 | 首条 `comment_id=1521255452254812` | ✅ |
| 4 | 楼中楼回复（--reply-to） | `topic +reply --topic-id ...A --text "..." --reply-to 1521255452254812 --json` | 回复挂在指定评论下 | `comment_id=4842488584482548`，含 `parent_comment_id:1521255452254812` + `repliee`（被回复人） | ✅ |
| 5 | q&a"待回复"判定（分诊信号） | `topic +detail` + `get_topic_comments`（q&a 55522511818555214） | 识别 q&a 是否已实质回答 | 1 评论"你好"非实质解答 → 分诊为**待回复** | ✅ |

## 实测校准了哪些文档假设

- **楼中楼回复字段结构**：`--reply-to <comment_id>` 成功后返回的 comment 对象带 `parent_comment_id`（= 被回复的顶层评论 id）+ `repliee`（被回复人 owner 信息）。→ 证实 topic-reply.md 的 `--reply-to` 用法；楼中楼与顶层回复的区别在这两个字段。
- **`topic +reply --json` 输出嵌套**：返回 `{success:true, comment:{comment_id, create_time, text, owner, ...}}` —— comment_id 在 comment 对象内。
- **回复即时可读**：发出后 `get_topic_comments` 立即可见，无延迟，分诊→回复→确认闭环成立。

## 安全测试策略

- **策略**：测试星球 + 自建一次性主题 + net-zero（回复随主题级联删除）。
- **如何保证净零变更**：所有回复只发在本账户新建的主题 A 上（顶层 + 楼中楼各一条），**不回复任何真实成员的主题/评论**。主题 A 最终整体 `api raw DELETE`，其下 2 条测试评论随主题级联删除（见 compose-operations-report 清理段）。
- **复原验证**：主题 A 删除后重拉列表确认消失（`A 存在? False`），评论随主题不复存在。

## 未覆盖 / 已知风险

- **未在真实成员评论下回复**：分诊场景真实用途是回复成员评论，但按用户约束 + 安全策略，只在自建主题上验证回复机制（顶层/楼中楼），未对真实成员内容产生可见回复。回复机制本身与目标主题归属无关，已完整验证。
- 评论删除的独立写操作（若分诊判定为需删除）不在本场景范围（转 topic-delete）。

## 结论

**通过（顶层 + 楼中楼回复机制、分诊判定实测；未在真实成员评论下回复）。**

`topic +reply` 顶层与 `--reply-to` 楼中楼均按文档工作（楼中楼带 parent_comment_id + repliee）；分诊读链路与"待回复"判定成立。回复仅发于自建主题，随主题删除净零。
