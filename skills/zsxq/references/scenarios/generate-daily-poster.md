# 生成星球日报海报（generate-daily-poster）

把知识星球一段时间（默认今日）的新增主题与互动数据，整理成**文字报告 + 高清海报图片（PNG）**，保存到用户指定目录。对星球**只读**，产物是本地图片，不向星球发布任何内容。可选在每个星球卡片附加加入二维码。

## 适用意图

- 「帮我生成「星球名」今天的日报海报」「做一张星球日报图」
- 「把最近的星球内容做成一张图 / 海报 / 日报卡片」
- 「生成内容摘要海报，我要发朋友圈 / 发群里」
- 需要**图片形式**的星球内容摘要（含点赞/评论/阅读互动数据）、可多星球合成一张

## 不适用情况

- 只要**文字**运营报告、且要**发布回星球**（发帖同步给成员）→ 用 [compose-operations-report](compose-operations-report.md)（写入类，方向相反）
- 只想看某段时间发了哪些主题、不需要整理成图 → 直接用 [group-topics](../group-topics.md)
- 无浏览器渲染环境（无 Playwright MCP）且用户不接受「保留 HTML 源文件」降级 → 停止，提示先配置环境（见「分支与停止条件」）

## 所需输入

| 输入 | 必填 | 说明 |
|------|------|------|
| 星球选择 | **是** | 只给星球名时先 `group +list` 定位 ID；支持单个或多个（序号或 group_id）；名称命中多个时列候选让用户确认 |
| 保存目录 | **是** | 海报 PNG 的保存路径，由用户指定（默认建议用户的 Downloads 目录，按运行环境 OS 解析） |
| 时间窗 | 否 | 默认「今日新增」；用户可指定其它窗口。判断日期以 `create_time` 为准 |
| 主题数上限 | 否 | 默认每星球取综合分前 5 条（见 [`generate-daily-poster/scoring.md`](generate-daily-poster/scoring.md)） |
| 加入二维码 | 否 | 默认**关闭**；用户明确要「带二维码 / 扫码入口」时开启 |

**环境依赖（本场景专属，非全 skill 必需）**：海报渲染需 **Node.js ≥ 18**（`node` / `npx` 可调用）+ **Playwright MCP**（浏览器渲染工具，`playwright-headless`）+ 本地 HTTP 服务（`npx http-server` 或 `python3 -m http.server`）。缺失时降级为保留 HTML，详见 [`generate-daily-poster/render-poster.md`](generate-daily-poster/render-poster.md)。

## 使用的原子操作

| 操作 | reference | 在本场景中的作用 |
|------|-----------|-----------------|
| `group +list` | [../group-list.md](../group-list.md) | 过渡步骤：按星球名定位 group_id、供用户选择 |
| `group +topics --json` | [../group-topics.md](../group-topics.md) | 拉时间窗内主题；JSON 的 `counts`（likes/comments/readers）、`digested`、`type` 直接喂打分 |
| 分享链接拼接 | [../share-links.md](../share-links.md) | 文字报告中每条主题附可点击的主题链接 |

场景专属处理（非 CLI 操作，见子文档）：主题综合打分 [`generate-daily-poster/scoring.md`](generate-daily-poster/scoring.md)；海报渲染与截图 [`generate-daily-poster/render-poster.md`](generate-daily-poster/render-poster.md)。

## 执行流程

### 第 1 步：浏览器可用性预检

海报依赖 Playwright MCP 渲染截图，**流程一开始就先探测浏览器**，避免跑完文字报告才发现无法出图。

```
browser_navigate → about:blank
```

- **成功**：继续完整海报流程
- **失败**（MCP 未配置 / Chromium 缺失 / 启动报错）：**立即暂停**，让用户选：① 降级模式（仍出文字报告 + 保留 HTML 源文件，用户自行截图/转 PDF）；② 取消，排查环境后再试。选降级则后续跳过截图，按 [render-poster](generate-daily-poster/render-poster.md) 的兜底逻辑保留 HTML。

### 第 2 步：定位并选择星球

`group +list` 拉星球列表，按「序号 / group_id / 星球名」表格呈现让用户选（单个或多个）。只给名称且命中多个相似星球时，列候选让用户确认，不默认取第一个。

### 第 3 步：拉时间窗内主题（每个选中星球）

`group +topics --group-id <id> --limit 30 --json` 取候选池，按 `create_time` 筛出落在时间窗（默认今日）的主题，全部纳入打分候选。`--limit` 越大候选越全，给打分留足空间。

字段提取：主题链接按 [share-links](../share-links.md) 拼接；`digested` 为 true 标 ⭐️；发布者取 `owner.alias`/`owner.name`；互动数取 `counts.likes`/`counts.comments`/`counts.readers`。**智能标题**：用模型据 content（+ 评论亮点）生成 ≤ 30 字吸睛标题；原文本身就短（≤ 30 字）则直接用原文。

### 第 4 步：综合打分与截取

按 [`generate-daily-poster/scoring.md`](generate-daily-poster/scoring.md)：`final_score = model_score*0.7 + formula_score*0.3`，降序取每星球前 5 条（可调）；模型评分不可用时自动降级为纯公式分并在报告末尾标注。

### 第 5 步：输出文字报告（先于海报）

先以 markdown 输出文字日报供快速浏览点击：按星球分组（今日无新增的星球整块省略）；每条一行含序号、⭐️、智能标题、发布者·时间、互动数据（**0 值项省略**，全 0 则整段省略）、可点击链接；每星球末尾附汇总（0 值项同样省略）。被跳过的星球不进正文，仅在报告末尾一行汇总提示。

### 第 6 步：询问二维码（可选）

渲染前主动问用户是否给每张星球卡片加「扫码加入」二维码（默认**关闭**，自留日报无需；邀请他人时开启）。用户初次请求已说明则不重复问。启用后的生成方式见 [render-poster](generate-daily-poster/render-poster.md)。

### 第 7 步：渲染海报并截图

按 [`generate-daily-poster/render-poster.md`](generate-daily-poster/render-poster.md)：入选星球数选布局（=1 单星球 / ≥2 多星球）→ 写 HTML 到临时目录 → 起本地 HTTP 服务 → Playwright 2x zoom 截 PNG → 复制改名到用户目录 `日报-<timestamp>.png` → 清理临时文件。

## 分支与停止条件

- **浏览器不可用**（预检失败）：让用户选降级（保留 HTML）或取消；用户要海报但拒绝降级 → 停止，提示配置 Playwright MCP
- **星球内容受限**（API 返回如「该星球内容仅限成员在星球内查看，暂不支持通过 API 访问」）：**立即暂停**告知该星球未开通 API 访问（星主需 APP → 实验室 → 开启 API 访问），让用户选跳过该星球或取消
- **名称命中多个星球**：列候选让用户确认，不猜
- **时间窗内无新增主题**：该星球区块整块省略；全部星球都无新增则如实告知，不虚构
- **模型打分失败**：降级为纯公式分，报告末尾标注，不阻塞
- **二维码生成失败**：该星球省略二维码，其余正常，报告末尾提示，不阻塞海报
- **截图失败**：不重试，保留 HTML 到用户目录并告知（见 render-poster 兜底）
- **限流（429 / frequently）**：退避几秒重试，不循环猛刷

## 用户确认点

1. **浏览器不可用时**：降级模式 / 取消，由用户选择后再继续
2. **星球选择**：用户明确选定单个或多个星球（名称命中多个时确认具体 ID）
3. **保存目录**：确认海报 PNG 落盘路径
4. **二维码开关**：默认关闭；仅用户明确要求才开启（初次已说明则无需再问）

> 本场景对星球只读、产物是本地图片，**不涉及向星球发布内容**，无写入类确认项。

## 完成标准

- 先输出符合格式的**文字报告**（含每条主题可点击链接、0 值省略、跳过星球仅末尾提示）
- 在用户指定目录生成一张**海报 PNG**（2x 高清无损）；降级模式下改为保留 `.html` 源文件到同目录
- 报告中的数量、互动数、类型均来自真实拉取的数据，非估算
- 临时文件（HTML、二维码 PNG、HTTP 服务）已清理

## 失败与回退

- **只读阶段（第 2–5 步）**部分失败（某页拉取出错、超时）：从最后成功的游标续拉即可，数据可重新累积，**无副作用**（不写星球）
- **渲染阶段（第 7 步）**：截图失败即保留 HTML 兜底，文字报告不受影响；临时文件在成功或兜底后均清理
- 本场景不产生星球侧写入，故无「已发布内容需回滚」问题
- 通用错误（401、404、参数缺失、`--end-time` 解析失败等）见 [auth-errors](../auth-errors.md#常见错误处理)

## 附加资源

- 打分规则：[`generate-daily-poster/scoring.md`](generate-daily-poster/scoring.md)
- 渲染与截图：[`generate-daily-poster/render-poster.md`](generate-daily-poster/render-poster.md)
- 布局规格：[`generate-daily-poster/layout-multi.md`](generate-daily-poster/layout-multi.md) / [`generate-daily-poster/layout-single.md`](generate-daily-poster/layout-single.md)
- 拉主题：[group-topics](../group-topics.md)；星球列表：[group-list](../group-list.md)；分享链接：[share-links](../share-links.md)
- 认证与常见错误：[auth-errors](../auth-errors.md)
