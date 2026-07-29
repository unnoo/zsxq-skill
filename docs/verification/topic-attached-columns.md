# 验证报告：topic-attached-columns

| 项 | 值 |
|----|----|
| 被测文档 | `references/topic-attached-columns.md`（读取 / 设置主题所属专栏） |
| 分类 | 读 + 写 · 操作 |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284）· 测试主题 topic_id=14422151554128522 |
| 原始日志 | [`logs/topic-attached-columns.log`](logs/topic-attached-columns.log) |
| 授权 | 用户经 AskUserQuestion 选择「执行自复原方案」，一次性授权在测试主题上做净零变更的写入测试；授权仅限本次专栏验证 |

## 测试用例

> 逐命令覆盖读取、设置（加入 / 清空 / 替换）、特有错误（429）、复原。「实际」列摘录真实输出关键片段，完整原文见 [`logs/topic-attached-columns.log`](logs/topic-attached-columns.log) 对应用例段。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 读取星球专栏列表（基线） | `api raw GET /v2/groups/758421284/columns` | 返回专栏数组含 column_id/name/topics_count | 哈哈哈(5585254544) topics_count=4；嘿嘿嘿(2212524241) topics_count=1 | ✅ |
| 2 | 读取主题所属专栏（无归属） | `api raw GET /v2/topics/14422151554128522/attached_columns` | `resp_data.columns` 为空数组 | `"columns": []`, `succeeded: true` | ✅ |
| 3 | 设置：加入哈哈哈 + 复核 | `api raw POST .../attached_columns --body '{"column_ids":[5585254544]}'` 后再 GET | 设置成功；复读含哈哈哈且带 last_topic_attach_time；计数 4→5 | POST `resp_data:{}` succeeded=true；复读含哈哈哈 `last_topic_attach_time:2026-07-29T11:02:29`；topics_count=5 | ✅ |
| 4 | 设置：空数组清空 + 复核 | `api raw POST .../attached_columns --body '{"column_ids":[]}'` 后再 GET | 归属清空；计数 5→4 | POST `resp_data:{}`；复读 `columns:[]`；哈哈哈 topics_count=4 | ✅ |
| 5 | 替换语义（首试，遇限流） | 连续 POST 哈哈哈→嘿嘿嘿→复读（脚本用 `&& echo ok`） | 若替换则只剩嘿嘿嘿 | step2 无 `ok` 输出、step3 仍显示哈哈哈 → **失败被 `&& echo ok` 静默**，触发隔离重跑 | ⚠️→见 6/7 |
| 6 | 隔离重跑暴露 429 | 单独 `api raw POST .../attached_columns --body '{"column_ids":[2212524241]}'` | 打印完整响应 | `{"ok":false,"error":{...\"code\":429,\"info\":\"操作过于频繁， 请稍后重试\"}}` `[exit 1]` | ✅（证实 429 + 整条失败不重试） |
| 7 | 替换语义（放慢重验） | 复原→POST 哈哈哈→(sleep)→POST 嘿嘿嘿→复读，各步间隔 2~3s | 复读只剩嘿嘿嘿（全量替换） | `当前归属: [(2212524241, '嘿嘿嘿')]` | ✅ |
| 8 | 自复原复核（净零） | 清空后 GET 主题归属 + GET 星球计数 | 归属 `[]`、计数回到基线(4/1) | `归属: []`；哈哈哈=4、嘿嘿嘿=1，与基线一致 | ✅ |

## 实测校准了哪些文档假设

- **设置成功返回体**：初稿「输出」节把 set 也写成读取式的 `columns[]` 封套；实测 POST 成功时 `body.resp_data` 为**空对象 `{}`**、以 `succeeded/success` 为 `true` 表示成功，不回显专栏列表 → 校准 `topic-attached-columns.md`「输出」节，拆成「读取 / 设置」两个真实示例，并注明设置后需另发一次读取复核。
- **替换语义**：实测 POST 是**全量替换**而非追加（先设 A、再单独设 B → 只剩 B）→ 「IMPORTANT」与「推荐工作流」明确「先 GET 现有→合并去重→再 POST 全量」，避免把主题踢出其它专栏。
- **429 限流真实存在**：短时间密集 POST 触发 `429「操作过于频繁，请稍后重试」`，且 CLI **整条命令失败、退出码 1、不自动重试** → 「错误说明」补 429 行，场景 [archive-topics-to-column](../../skills/zsxq/references/scenarios/archive-topics-to-column.md) 写入间隔约 2 秒。

## 安全测试策略（写操作）

- **策略**：自复原（net-zero）。
- **如何保证净零变更**：写入前先 `GET attached_columns` 读取该主题原始专栏归属并记录；测试过程中的所有 POST 均为临时值；测试结束后 POST 回原始 `column_ids`（原本无归属则 POST 空数组 `[]`）复原。
- **复原验证**：复原后再发一次 `GET attached_columns`，确认专栏归属与测试前一致（见日志「复原验证」段）。

## 未覆盖 / 已知风险

- **每专栏 100 条上限**的超限失败分支未实测（测试专栏内容量远低于上限，无法自然触发）。
- 429 退避后**自动重试成功**的完整链路未逐次实测（仅确认单条命令失败、需人工放慢重试）。

## 结论

**通过。** 读取（GET）、设置（POST 全量替换、空数组清空）、替换语义、429 限流、自复原复原均按预期工作；文档「输出 / 错误说明 / IMPORTANT / 推荐工作流」已按实测校准，与真实行为一致。写路径已在测试主题上完成净零验证，未触碰生产内容。
