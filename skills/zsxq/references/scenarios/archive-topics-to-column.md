# 批量收录主题到专栏（archive-topics-to-column）

把某星球最新的 N 条主题批量收录进指定专栏，适合整理专题合集、活动精华归档、定期把优质新内容归入常设专栏。**主题的专栏归属是全量替换：每条主题都要「先读现有专栏 → 并入目标专栏 → 整表回设」，否则会把主题踢出其它专栏。先列出目标专栏与待收录主题清单供用户确认，确认后再逐条执行，每条写入请求间隔约 2 秒避免限速。**

## 适用意图

- 「把星球「XXX」最新的 20 条主题收录进专栏「YYY」」
- 「把最近这批活动帖归档到某个专栏」
- 「定期把优质新内容收录进常设专栏」

## 不适用情况

- 只收录单条主题 → 直接用 [topic-attached-columns](../topic-attached-columns.md) 原子操作，无需场景
- 从专栏移除主题、调整专栏内主题顺序 → 不属于本场景
- 目标星球尚未开通任何专栏且用户**拒绝创建** → 专栏为空时本场景会询问用户是否创建，用户拒绝则停止

## 所需输入

- 星球名称或 `group_id`
- 数量 N（收录最新的 N 条主题）
- 目标专栏名称（或直接给 `column_id`）

## 使用的原子操作

| 操作 | reference | 在本场景中的作用 |
|------|-----------|-----------------|
| 搜索星球 / 列出星球 | [group-list](../group-list.md)（或 `search_groups`） | 由星球名拿到 `group_id` |
| 浏览星球主题 | [group-topics](../group-topics.md) | 取最新 N 条主题的 `topic_id` |
| 专栏列表 | [group-columns](../group-columns.md) | 按专栏名找到 `column_id`，并看现有主题数 |
| 创建专栏 | [group-column-create](../group-column-create.md) | 专栏为空或找不到目标专栏时，按用户确认创建新专栏 |
| 读取 / 设置主题所属专栏 | [topic-attached-columns](../topic-attached-columns.md) | 逐条以「读现有→并入→整表回设」把主题并入目标专栏 |

## 执行流程

### 第一步：确定星球，拿到 group_id

按星球名搜索（`search_groups`）或 `group +list`（见 [group-list](../group-list.md)）。名称命中多个相似星球时，列出候选（`group_id` + 名称）让用户确认，不要默认取第一个。

### 第二步：取最新 N 条主题的 topic_id

用 `group +topics --group-id <id> --limit N`（见 [group-topics](../group-topics.md)），按时间倒序收集每条的 `topic_id` 与标题。`group +topics` 单次最多返回 30 条，N > 30 时用返回的 `next_end_time` 翻页累积到 N 条。

### 第三步：确定目标专栏（含创建）

**3a. 拉取专栏列表**：`api raw --method GET --path /v2/groups/<group_id>/columns`（见 [group-columns](../group-columns.md)）。

**3b. 专栏列表为空**（`columns[]` 为空数组）：

告知用户「该星球暂无专栏」。询问：

> 是否需要创建一个新专栏？提供专栏名称即可，创建后继续收录流程。

- 用户提供名称 → 按 [group-column-create](../group-column-create.md) 创建（`POST /v2/groups/<group_id>/columns --body '{"name":"…"}'`），拿到返回的 `column_id`（`topics_count` 为 0），跳至第四步
- 用户拒绝 → 停止（见「分支与停止条件」）

**3c. 专栏列表非空但找不到目标**：

遍历 `columns[]` 用 `name` 匹配用户指定的专栏名。匹配不到时：

> 未找到专栏「XXX」。是否需要创建？

- 用户同意 → 创建后继续
- 用户拒绝 → 停止

**3d. 命中多个同名专栏**：列出候选（`column_id` + `name` + `topics_count`）让用户确认唯一目标。

**3e. 正常命中**：取 `column_id`，记下 `statistics.topics_count`。

### 第四步：展示清单，等待确认

汇总给用户：目标专栏（名称 + `column_id`）、待收录的 N 条主题清单（`topic_id` + 标题）、以及容量预估「现有 `topics_count` + N 是否超过 100」。**这里是写入前的停止点，未获明确同意前不执行任何收录。**

### 第五步：逐条「读-并-回设」并报告

用户确认后，对每个 `topic_id` 按 [topic-attached-columns](../topic-attached-columns.md) 的模式收录：先 `GET /v2/topics/<topic_id>/attached_columns` 读出该主题现有专栏的 `column_id` 集合 → 把目标 `column_id` **并入并去重** → `POST` 回设**整表** `column_ids`。**每条主题的写入请求之间间隔约 2 秒**避免触发限速（读取不计）。逐条记录结果，全部完成后按顺序报告每条的 ✅ 成功 / ❌ 失败（失败附原因）。

> 切勿直接 `POST '{"column_ids":[<目标>]}'` —— 那会把主题从其它专栏移除。必须并入现有集合后整表回设。

## 分支与停止条件

- **主题为空**：`group +topics` 没返回任何主题 → 报告「无可收录主题」，结束
- **星球名命中多个**：列出候选让用户选定唯一星球
- **专栏列表为空**：询问用户是否创建新专栏。同意 → 创建后继续收录；拒绝 → 停止
- **专栏找不到**：列出已有专栏供参考，询问用户是选择已有专栏、创建新专栏还是放弃
- **专栏名命中多个**：列出候选让用户选定唯一目标
- **N > 30**：`group +topics` 需翻页累积，凑够 N 条再进入收录
- **容量超限**：现有 `topics_count` + N > 100 时，提前提示用户会触达每栏 100 条上限，请减少数量或更换专栏；收录过程中若某条返回上限错误，停止后续收录并报告已达上限
- **限流**（返回 429 / `frequently` 等）：退避几秒后重试当前这条，并保持 2 秒的请求间隔，不要循环猛刷

## 用户确认点

1. **批量收录前**（第四步）：列出目标专栏（名称 + `column_id`）与完整待收录主题清单（`topic_id` + 标题），取得明确同意后才开始写入
2. **创建专栏前**（第三步 3b/3c）：专栏为空或找不到时，向用户确认是否创建及专栏名称，取得同意后才调用创建接口
3. 若第一步命中多个星球、或第三步命中多个同名专栏：先确认唯一目标，再继续

## 完成标准

- N 条主题（或翻页累积到的实际条数）逐条尝试收录完毕，每条都有明确的 ✅ / ❌ 结果
- 成功收录的主题已进入目标专栏（可用 [group-columns](../group-columns.md) 复核 `topics_count` 增量确认）
- 向用户给出逐条结果汇总，失败项列出 `topic_id` 与失败原因

## 失败与回退

- 每条收录是独立的「读-并-回设」，单条失败不影响其他主题；记录失败的 `topic_id` 与原因，可对失败项单独重试
- 达到 100 上限后，目标专栏对应的回设会失败 → 停止收录并如实报告已收录数量与未收录清单
- 若主题已在目标专栏中，「读现有→并入去重→回设」得到的集合与原集合相同，回设为幂等、不会重复收录；无需额外判重
- 本场景为增量写入、无整体事务；中断后可从未收录清单续跑

## 附加资源

- [topic-attached-columns](../topic-attached-columns.md) — 读取/设置主题所属专栏的原子操作（含 CAUTION / 替换语义 / 100 条上限）
- [group-columns](../group-columns.md) — 专栏列表与按名找 `column_id`
- [group-column-create](../group-column-create.md) — 创建新专栏
- [group-topics](../group-topics.md) — 取最新主题的 `topic_id`
- [group-list](../group-list.md) — 获取 `group_id`
- [curate-digest-and-tags](curate-digest-and-tags.md) — 精华归档可与本场景搭配
- [auth-errors](../auth-errors.md) — 认证与常见错误
