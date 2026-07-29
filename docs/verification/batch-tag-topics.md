# 验证报告：batch-tag-topics

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/batch-tag-topics.md`（+ 原子操作 `references/topic-tags.md`） |
| 分类 | 写 · 场景（主写入 = `api call set_topic_tags`） |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284）；一次性主题 A `55522441448144114`（测完已删） |
| 原始日志 | [`logs/batch-tag-topics.log`](logs/batch-tag-topics.log) |
| 授权 | 用户 2026-07-28 一次性授权「研发测试 758421284 可发布/POST/PUT」；写策略=仅自建一次性主题，测完 DELETE 清理 |

## 测试用例

> 重点验证 set_topic_tags 的**覆盖式（overwrite）语义**——这是场景批量打标签必须先读后并的根因。「实际」列摘录真实输出。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 设置初始标签集 | `api call set_topic_tags {topic_id:...A,titles:["回归X","回归Y"]}` | 主题带 X、Y 两标签 | `annotation` 含 hashtag 实体 X(hid 28244225422421)、Y(hid 15411442144112) | ✅ |
| 2 | 读回确认 | `topic +detail --topic-id ...A --json` | annotation 反映 X、Y | detail 的 annotation 与 set 返回一致（X+Y） | ✅ |
| 3 | **覆盖验证**：只 set 一个新标签 | `api call set_topic_tags {titles:["回归Z"]}` | 若覆盖式→X、Y 被清，只剩 Z | `annotation` 只剩 Z(hid 15411442144852) → **证实覆盖式**：X、Y 被清除 | ✅ |
| 4 | 正确工作流：读原值→并集→回写 | `api call set_topic_tags {titles:["回归X","回归Y","回归Z"]}` | 三标签并存 | `annotation` 含 X+Y+Z 三实体 → 并集回写恢复全部 | ✅ |

## 实测校准了哪些文档假设

- **`titles` 是全量替换而非追加**（关键）：用例 3 实测——只传 `["回归Z"]`，原有 X、Y 被清除，主题只剩 Z。**证实 topic-tags.md「titles = 完整标签集（覆盖式）」的告警是真实且必要的**。批量打标签场景若不先读现有标签做并集，会误删主题已有标签 → 场景「读原 annotation → 解析现有 hashtag → 合并新标签 → 全量回写」的工作流是正确且强制的。
- **标签存储形态**：标签不是扁平 `tags[]`，而是内联在 `annotation` 字段的 URL 编码 hashtag 实体：`<e type="hashtag" hid="..." title="%23<urlencoded>%23" />`。读现有标签 = 解析 annotation 里的 hashtag 实体。
- `set_topic_tags` 成功返回完整 topic 对象（含更新后 annotation），可直接用于校验，无需再 detail 一次。

## 安全测试策略

- **策略**：测试星球 + 自建一次性主题 + net-zero（该主题最终整体删除）。
- **如何保证净零变更**：全部标签操作只作用于本账户新建的主题 A，从不碰真实成员主题（覆盖式语义会清掉他人已有标签，风险高，严禁在真实主题上试）。主题 A 在全部写测试后由 `api raw DELETE` 整体删除（见 compose-operations-report 日志清理段），标签随主题一并消失。
- **复原验证**：主题 A 删除后重拉列表确认已消失（`A 存在? False`），群内无本次标签残留。

## 未覆盖 / 已知风险

- 批量（多主题循环打标签）的规模化未压测；单主题的覆盖/并集语义是批量的原子基础，已验证。
- 标签数量上限、非法标签字符等边界未测（无接近上限样本）。
- 未在真实成员主题上验证（覆盖式语义会清他人标签，用户约束 + 安全考虑均禁止，属有意不测）。

## 结论

**通过（覆盖式语义 + 正确并集工作流实测；批量规模化未压测）。**

set_topic_tags 的全量替换语义被实测证实（只传 Z 清掉 X/Y），场景"先读后并全量回写"的核心工作流因此得到验证；测试仅在自建主题上进行，删除后群级净零。
