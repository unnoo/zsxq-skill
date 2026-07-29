# 验证报告：generate-daily-poster

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/generate-daily-poster.md` + 子文档 `scoring.md` / `render-poster.md` / `layout-multi.md` / `layout-single.md` |
| 分类 | 只读（对星球）· 场景（由旧 `zsxq-report` skill 迁移而来） |
| zsxq-cli 版本 | v0.4.9 |
| 环境 | node v23.9.0 / npx 10.9.2 / python3 3.12.4 / http-server 未全局安装 / **Playwright MCP 不可用（无 browser_* 工具）** |
| 测试日期 | 2026-07-29 |
| 测试对象 | 研发测试（group_id=758421284），只读 |
| 原始日志 | [`logs/generate-daily-poster.log`](logs/generate-daily-poster.log) |
| 授权 | **无需写入授权**：本场景对星球只读、产物为本地图片，不向星球发布任何内容；与用户「不要测试发布/写入类功能」约束一致。二维码/HTTP 服务均为本地操作。 |

## 测试用例

> 覆盖：只读数据链路（星球列表、主题 JSON + 字段校准）、打分公式核算、渲染前置（二维码、本地 HTTP 服务）、**HTML 海报生成 + 布局规则断言、降级兜底**。仅 Playwright 截图本身因环境无 MCP 未实测（用例8）。「实际」列摘录真实输出，完整原文见 [`logs/generate-daily-poster.log`](logs/generate-daily-poster.log) 对应用例段。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 拉星球列表（第 2 步选星球） | `zsxq-cli group +list` | 返回星球表，含 group_id + 名称 | 表头 `GROUP ID / NAME`，87 个星球含 758421284 研发测试 | ✅ |
| 2 | 拉主题 JSON + 校准打分字段（第 3 步） | `group +topics --group-id 758421284 --limit 5 --json` | 每条主题含 counts/digested/type/create_time/owner | `counts.{comments,likes,readers}`、`digested`、`type:talk`、`owner` 齐全；`has_more`+`next_end_time` 存在 | ✅ |
| 3 | 打分公式核算（第 4 步） | `python3 verify_scoring.py`（内嵌用例2 真实字段） | formula_score 按 scoring.md 公式算出、降序正确 | 「文件」=19.40 居首；comments=1 的排在 comments=0 之上；同分稳定序 | ✅ |
| 4 | 二维码生成（render-poster「二维码」） | `npx --yes qrcode "https://m.zsxq.com/groups/758421284/join.html" -o … -w 300` | 生成 300px PNG | `saved qrcode to: …`；`PNG image data, 300 x 300` | ✅ |
| 5 | 本地 HTTP 服务兜底（render-poster「截图」步骤1） | `python3 -m http.server 8199 --directory .` + curl | 同源静态服务可访问 | `HTTP 200` | ✅ |
| 6 | **HTML 海报生成 + 布局规则断言**（render-poster「渲染 HTML」+ layout-single） | `python3 gen_poster.py`（layout-single 规格 + 用例2 真实数据） | 结构良好；数据绑定；0 值省略逐行+汇总生效 | 7 断言全 PASS：标签平衡、5 主题行、likes 全 0 无 👍、主题#3 无 💬、绑定 💬7👀11、汇总 💬20👀56 | ✅ |
| 7 | **降级兜底**：浏览器不可用时保留 HTML 到用户目录（render-poster「截图失败兜底」） | `cp … 日报-<ts>.html` 到模拟用户目录 + 校验可读 | HTML 按 `日报-<ts>.html` 落盘、可读、内容完整 | 落盘 2944 字节、首行 `<!doctype html>`、`.topic` 行数=5；清理成功 | ✅ |
| 8 | Playwright 截图（正常路径最后一环） | 预检 `browser_navigate` / `page.screenshot` / `browser_close` | 出 PNG | **本环境无 Playwright MCP 工具，未实测** | ⚠️ 未实测 |

## 实测校准了哪些文档假设

- **`owner.alias` 可为 null**：实测第 1 条主题 `owner.alias=null, name="明明"`，其余条 alias 有值。→ 证实场景第 3 步「发布者取 `owner.alias`/`owner.name`」的回退逻辑必要且正确，文档无需改。
- **打分依赖字段与 JSON 结构一致**：`counts.{likes,comments,readers}`、`digested`、`type`、`create_time` 均在 `topics_brief[]` 内直接可取，无需逐条 `topic +detail`。→ 与 scoring.md 字段来源、场景第 3 步「JSON 的 counts 直接喂打分」一致。
- **公式算术正确**：手工复核「文件」`raw=0+0*3+7*2+log10(12)*5=19.3959`，与脚本逐位一致；tiebreaker（comments 高者先、同分按 create_time）符合 scoring.md「3. 排序」。
- **迁移适配无回归**：源 4 文件的跨 skill 引用（`../zsxq-group/...`、`zsxq-shared`）已全部改为项目内路径（`../../group-topics.md`、`../auth-errors.md`）；顶部「前置条件读 zsxq-shared」行已删（认证归 auth-errors）；主题链接改引 `share-links.md`。check-docs.py 死链检查为最终把关。

## 安全测试策略

- 本场景**对星球零写入**（只 `group +list` / `group +topics`），无 create/edit/reply/delete/digest/tags 等写操作，**不触发写入授权门**。
- 二维码（`npx qrcode`）与本地 HTTP 服务（`python3 -m http.server`）均为**本地无害操作**：仅在临时目录生成/服务文件，测试后已 `rm` 清理，不碰生产内容、不联网写。
- 打分核算脚本 `verify_scoring.py` 内嵌用例2 的真实字段离线运算，无副作用。

## 未覆盖 / 已知风险

> 边界厘清：首版报告把「整条渲染路径」标为未实测，掩盖了其中可测的部分。本次补测后拆分如下——

- **HTML 生成（用例6）、降级兜底（用例7）：已测通过**。二者是本地文件操作、不碰星球、不需 Playwright，本环境完全可测。
- **Playwright 截图本身（用例8）：真不可测**。本环境无 Playwright MCP（无 `browser_*` 工具），故「浏览器预检 → 2x zoom → page.screenshot 出 PNG → browser_close」无法执行。该段文档系从原 `zsxq-report` skill 原样迁移、未改命令语义。**待在配有 Playwright MCP 的环境补测截图与 PNG 视觉效果。**
- 多星球布局的实际视觉渲染同样依赖截图能力，未做像素级验证（结构规则已由用例6 的 layout-single 断言间接覆盖）。
- 模型四维打分为主观评估，本次只核算了公式兜底分（客观、可复现的部分）；模型分质量不在静态验证范围。

## 结论

**有条件通过（仅 Playwright 截图未实测；渲染前置 + HTML 生成 + 降级兜底均已实测通过）。**

- 只读数据链路（`group +list` / `group +topics --json`）、打分公式、二维码生成、本地 HTTP 服务、**HTML 海报生成（含 0 值省略等布局规则断言）、降级兜底（HTML 落盘到用户目录）** 均按预期工作，真实输出与文档一致；迁移中的字段回退、跨引用改写已按实测校准。
- 唯一未覆盖的是 Playwright 截图这一环——因本环境缺 MCP 能力，非文档缺陷；该路径命令由旧 skill 原样迁移，且其失败时的降级兜底已验证可用（用例7），风险低。补测条件明确（需 Playwright MCP 环境）。
