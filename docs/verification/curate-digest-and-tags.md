# 验证报告：curate-digest-and-tags

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/curate-digest-and-tags.md`（+ `topic-digest.md` / `topic-tags.md`） |
| 分类 | 写 · 场景（主写入 = `set_topic_digested` + `set_topic_tags`） |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284）；一次性主题 A `55522441448144114`（测完已删） |
| 原始日志 | [`logs/curate-digest-and-tags.log`](logs/curate-digest-and-tags.log)；标签部分见 [`logs/batch-tag-topics.log`](logs/batch-tag-topics.log) |
| 授权 | 用户 2026-07-28 一次性授权「研发测试 758421284 可发布/POST/PUT」；写策略=仅自建一次性主题，测完 DELETE 清理 |

## 测试用例

> 主干：筛选优质主题 → 加精（set_topic_digested）+ 打标签（set_topic_tags）。「实际」列摘录真实输出。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 加精：digested=true | `api call set_topic_digested {topic_id:...A,digested:true}` | 主题标记为精华 | `digested:true, success:true`，topic.digested=true | ✅ |
| 2 | 取消加精（复原）：digested=false | `api call set_topic_digested {digested:false}` | 恢复非精华 | `digested: False success: True` | ✅ |
| 3 | 打标签（覆盖/并集语义） | `api call set_topic_tags {titles:[...]}` | 见 batch-tag-topics 用例 1–4 | annotation 反映标签集；覆盖式已证实 | ✅（详见 batch-tag-topics） |
| 4 | 权限：admin/partner（非 owner）能否加精 | 用例 1 以 admin+partner 账户执行 | 验证是否需星主权限 | **admin+partner 成功加精**（success:true），未返回无权限错误 | ✅ 见校准 |

## 实测校准了哪些文档假设

- **⚠️ `topic-digest.md` 权限说明不准确（已实测推翻）**：该文档称加精"需星主权限，非星主账户返回无权限错误"。实测本账户是 **admin + partner（非 owner）**，`set_topic_digested{digested:true}` **成功执行**（`success:true, digested:true`），并未返回无权限错误。→ **已据此校准 `topic-digest.md`**：管理员/合伙人（不止星主）即可加精，权限描述改为"需管理权限（星主/管理员/合伙人）"。
- **加精可逆**：digested true↔false 均成功，取消加精即复原，无副作用残留，适合 net-zero 测试。
- **标签覆盖式语义**（见 batch-tag-topics 校准）：curate 场景同时打标签时，必须先读现有 annotation 做并集再回写，否则清掉主题已有标签。

## 安全测试策略

- **策略**：测试星球 + 自建一次性主题 + net-zero 自复原（加精用即时 true→false 复原；标签随主题删除消失）。
- **如何保证净零变更**：digest/tags 只作用于本账户新建主题 A；加精后立即 `digested:false` 复原；主题 A 最终整体 DELETE（见 compose-operations-report 清理段）。全程不碰真实成员主题。
- **复原验证**：加精即时复原读回 `digested:False`；主题 A 删除后列表确认消失。

## 未覆盖 / 已知风险

- 批量筛选→加精的规模化流程未压测；单主题的加精/取消/打标签原子语义已验证。
- "优质内容筛选"依赖语义判断，不在静态验证范围。
- 未在真实优质成员主题上加精（可行且低风险，但测试策略选择只在自建主题上验证机制，避免对真实内容产生"已加精"的可见状态变更）。

## 结论

**通过（加精 + 取消 + 打标签机制实测；发现并修正 topic-digest.md 权限说明）。**

加精（可逆）与打标签（覆盖式）机制均按预期工作；**关键校准**：admin/partner 即可加精，`topic-digest.md`"仅星主"的说法被实测推翻并已修正。测试仅在自建主题、加精即时复原、主题删除净零。
