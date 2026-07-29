# 验证报告：daily-patrol

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/daily-patrol.md` |
| 分类 | 只读 · 场景 |
| zsxq-cli 版本 | v0.4.9 |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284），只读；操作者 Pigrun 748118287（admin+partner，非 owner） |
| 原始日志 | [`logs/daily-patrol.log`](logs/daily-patrol.log) |
| 授权 | 不涉及写入（全程只读） |

## 测试用例

> 主干：group +list 解析 → group +topics 拉候选 → topic +detail 逐条 → get_topic_comments 补判 ①④。分支各取一个用例。「实际」列摘录真实输出，完整原文见日志对应段。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 第 0 步：星球名→group_id | `zsxq-cli group +list` | 返回星球表，「研发测试」唯一命中 | 87 行星球表，`758421284 研发测试` 精确唯一命中 | ✅ |
| 2 | 第 1 步：拉候选主题 | `group +topics --group-id 758421284 --limit 10 --json` | 倒序返回，每条含 type/create_time/digested/counts | 10 条，字段齐全；`has_more:true`+`next_end_time` 存在 | ✅ |
| 3 | 第 2 步：逐条拉完整正文 | `topic +detail --topic-id 14422151554128522` | 返回 content/type/counts/owner/files | 「文件」帖正文 + 附件 `Go语言圣经.pdf`(4.3MB)、comments=7 | ✅ |
| 4 | ①类判定：q&a 是否已答（补拉评论） | `topic +detail 55522511818555214` + `get_topic_comments` | q&a 正文 + 评论供判定"已答/未答" | 正文"问题：测试回答下"；1 评论"你好"（非实质解答）→ 判为**待回复** | ✅ |
| 5 | ④类判定：风险信号在评论区 | `get_topic_comments 14422151554128522 --limit 30` | 拉全部评论供语义扫描 | 7 评论含 `[色][色][色]` 等表情 → 低风险，标注人工复核 | ✅ |
| 6 | ③类对齐：查星球已有标签体系 | `group +hashtags --group-id 758421284` | 返回标签表供建议对齐 | 200+ 标签（`#2#`104、`#google#`94…）→ 建议标签可对齐避免造重复 | ✅ |
| 7 | 分支：N>30 翻页（游标续拉） | `group +topics --limit 3 --json` 取 `next_end_time` → 作 `--end-time` 拉第 2 页 | 第 2 页续到更旧主题 | 页1 末条 `create_time`=页2 游标；页2 到达更旧的 `14422442228248252/45544554441458258` | ✅ |
| 8 | 分支：星球名命中多个 | （逻辑核对） | 列候选让用户选，不默认取第一个 | 本次「研发测试」唯一命中，多命中分支未触发（环境无重名星球） | ⚠️ 未触发 |

## 实测校准了哪些文档假设

- **翻页存在边界重叠**：`next_end_time` = 本页末条 `create_time`，`--end-time` 含等于 → 下一页把上页末条重复返回为首条（页1末条 `82255225551824582` 又出现在页2首）。场景第 92 行「翻页续拉」未提去重，但 monitor-risky-content.md:90 已要求按 topic_id 去重。**已据此校准 `group-topics.md`「说明」节补「翻页边界去重」注**；daily-patrol 依赖该原子操作，行为一致。
- **③类"无法确认现有标签"属实**：`topic +detail` 与 `group +topics` 的返回里，标签存于 `annotation` 字段（URL 编码的 `<e type="hashtag">` 实体），主题若无标签则 `annotation:""`。场景第 68 行"不返回主题现有标签字段"表述可更精确为"标签在 annotation 内联、非独立 tags[] 字段"，但结论（只能给建议标签）成立。
- 其余字段（type 四种、digested、counts、owner.alias 可为 null）与文档一致。

## 安全测试策略（写操作必填，只读写「不涉及写入」）

不涉及写入。本场景全程只读（group +list / group +topics / topic +detail / get_topic_comments / group +hashtags），对星球零副作用，可安全重跑。

## 未覆盖 / 已知风险

- 用例 8（星球名命中多个）：环境无重名星球，多命中分支未触发；判定逻辑（列候选不自选）是确定性的，属低风险。
- "今日无新内容"分支：测试星球有历史主题，未构造空窗口；逻辑为空返回即报告结束，低风险。
- 限流退避、个别 detail 失败跳过：本轮只读未触发（限流在 archive 写测试中真实命中并验证，见 archive-topics-to-column）。

## 结论

**通过（主干 + 可触发分支实测；2 个环境依赖分支未触发但逻辑确定）。**

只读四步链路（解析→拉列表→拉详情→补拉评论）与四类判定所需字段全部按文档工作；翻页边界重叠是本轮新发现，已校准到 `group-topics.md`。场景无写入、无副作用，可信度高。
