# 验证报告：compose-operations-report

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/compose-operations-report.md` |
| 分类 | 写 · 场景（主写入 = `topic +create` 发布报告帖） |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284）；一次性主题 B `55522441481241154`（测完已删） |
| 原始日志 | [`logs/compose-operations-report.log`](logs/compose-operations-report.log) |
| 授权 | 用户 2026-07-28 一次性授权「研发测试 758421284 可发布/POST/PUT」，仅限本星球；写策略=仅自建一次性主题，测完 DELETE 清理（群级净零） |

## 测试用例

> 主干：拉真实数据 → 聚合 → `topic +create` 发布报告帖 → 校验发布成功。「实际」列摘录真实输出。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 数据采集：拉主题供聚合 | `group +topics --group-id 758421284 --limit 10 --json` | 返回主题 + counts 供统计 | 10 条，talk/q&a 分布、counts 可聚合（「文件」7 评为活跃项） | ✅ |
| 2 | 主干写入：发布运营日报帖 | `topic +create --group-id 758421284 --text "<运营日报正文>" --json` | 发帖成功，返回 topic_id | `✓ Topic created`；`topic.topic_id=55522441481241154`，text/create_time 回显 | ✅ |
| 3 | 校验：报告帖已入库 | `group +topics --limit 10 --json`（发布后） | 新帖出现在列表首位 | 主题 B 出现在列表首位，content 与发布一致 | ✅ |
| 4 | 清理：删除报告帖（净零） | `api raw DELETE /v2/topics/55522441481241154` | 删除成功 | `resp_data:{}, succeeded:true`，200 | ✅ |
| 5 | 复原验证：确认帖已消失 | `group +topics --limit 5 --json` | B 不在列表 | `B(55522441481241154) 存在? False` | ✅ |

## 实测校准了哪些文档假设

- **`topic +create --json` 输出结构**：成功返回 `{success:true, topic:{create_time, text, title, topic_id}}` —— topic_id **嵌套在 topic 对象内**（与首版理解"顶层 topic_id"不同）。已确认 topic-create.md 的「输出」示例应体现嵌套结构。
- **只能创建 talk 类主题**：`topic +create` 仅支持 talk（帖子），运营报告帖正属 talk，与场景用途契合，无需其它类型。
- 数据聚合（主题数、类型分布、活跃度）均来自 group +topics 真实字段，非估算，符合场景「数量/互动数来自真实拉取」的完成标准。

## 安全测试策略

- **策略**：测试星球 + 自建一次性主题 + net-zero 自复原。
- **如何保证净零变更**：报告帖是本账户新建的 talk（主题 B），不触碰任何真实成员内容；发布→校验→`api raw DELETE` 删除，群内主题集恢复到发布前。
- **复原验证**：删除后重拉主题列表，确认 B 已消失（`存在? False`），「文件」帖回到列表首位（= 发布前状态）。见日志「复原验证」段。

## 未覆盖 / 已知风险

- 本次报告正文由真实数据手工聚合示例，未测超长正文/富文本/图文混排的发布（场景不要求）。
- 未测发布失败回滚语义（发布是单次原子操作，CLI 返回 success 才算成功，无部分写入）。

## 结论

**通过（主干写入 + 净零清理全链路实测）。**

"拉真实数据 → 发布报告帖 → 校验"主干按文档工作，`topic +create` 发布成功且 topic_id 结构已校准；测试帖发布后即删、群级净零已复原验证。写入严格限定在用户授权的 758421284 内、仅操作自建主题。
