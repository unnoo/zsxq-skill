# 验证报告：generate-video

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/generate-video.md` |
| 分类 | 只读 + 本地文件生成场景（从知识星球取内容 → AI 提炼 → 本地渲染 HTML/MP4，**不写回星球**） |
| zsxq-cli 版本 | v0.4.9 |
| Node.js 版本 | v23.9.0 |
| 测试日期 | 2026-07-30 |
| 测试对象 | `scripts/scenarios/generate-video/render.js`（结构化模板）、`render-minimal.js`（金句模板）、`record.js`（录制）、CLI 数据流（group 758421284） |
| 原始日志 | [`logs/generate-video.log`](logs/generate-video.log) |

## 测试用例

| # | 用例（意图） | 执行的命令 | 预期 | 实际 | 结论 |
|---|------------|-----------|------|------|------|
| 1 | 环境预检 | `node --version` + `ls scripts/scenarios/generate-video/render.js` | Node ≥ 18 + 脚本存在 | v23.9.0 ✅；render.js/render-minimal.js/record.js 均存在 ✅ | ✅ |
| 2 | 结构化模板渲染 | `node render.js sample.json sample.html` | 输出 HTML，含多个场景 | ✅ HTML 已生成，5 场景（封面+3内容+结语），22s | ✅ |
| 3 | 金句模板渲染 | `node render-minimal.js minimal.json minimal.html` | 输出 HTML，大字流 | ✅ 金句模板 HTML 已生成，4 页，14s | ✅ |
| 4 | HTML 结构 | `wc -l sample.html` | 有效 HTML | 358 行，含 CSS 动画系统、响应式缩放、时间轴控制 ✅ | ✅ |
| 5 | CLI 数据流（group +list） | `zsxq-cli group +list --json` | 定位测试星球 | group_id=758421284 name=研发测试 ✅ | ✅ |
| 6 | CLI 数据流（group +topics） | `zsxq-cli group +topics --group-id 758421284 --limit 10 --json` | 返回主题列表 | 10 条主题，含 topic_id/type/counts ✅ | ✅ |
| 7 | CLI 数据流（topic +detail） | `zsxq-cli topic +detail --topic-id 82255242821881882 --json` | 提取正文 | `content` 字段含完整正文（实测正文在 `content` 而非 `article.text`/`talk.text` → 场景文档需校准） | ✅（有校准） |
| 8 | record.js 缺失依赖 | `node record.js sample.html out.mp4` | 提示 puppeteer 缺失 | `MODULE_NOT_FOUND` → 与场景文档描述一致 ✅ | ✅ |

## 实测校准了哪些文档假设

- **正文在 `content` 字段，非 `article.text`/`talk.text`**：实测 `topic +detail --json` 返回中，`talk` 类型的正文在 `topic.content`（字符串），而非 `topic.talk.text`。文档原假设 `article.text` / `talk.text` 与 v0.4.9 CLI 实际输出不一致→**已修正为 `content` 字段**。
- **render-minimal.js 的 JSON schema 不同**：金句模板使用 `pages[]` 数组（每页 `text` + `sub` + `highlight`），而非结构化模板的 `cover/scenes/finale` 结构。AI 需根据选择的模板生成对应格式。
- **ffmpeg 可用但 puppeteer 未安装**：录制路径需 `npm install` 安装 puppeteer 后才可走通，与场景文档「环境依赖」一致。

## 安全测试策略

- **策略**：纯只读 + 本地文件生成。zsxq-cli 调用仅限 `group +list` / `group +topics` / `topic +detail`（均为只读操作，已在测试星球 758421284 跑通的既有授权内）；渲染脚本在本地沙箱运行，输出 HTML 到临时目录，不接触网络。
- **零写入**：未向星球发布任何内容，未修改任何星球数据。
- **临时文件已清理**：测试生成的 HTML 文件位于 `~/.claude/jobs/dc7ff25f/tmp/`，随 job 清理。

## 未覆盖 / 已知风险

- **AI 提炼质量未验证**：提炼铁律（主谓宾完整、字数约束等）依赖 LLM 遵守规则，本次测试仅验证了渲染脚本和 CLI 数据流可工作，未实测 AI 提炼的 JSON 是否持续满足全部 10 条铁律。
- **record.js 录制路径未完整运行**：puppeteer 未安装；安装后需验证 `record.js` 在真实 Chromium 下能否正确截帧、编码 MP4。
- **HTML 浏览器端动画未人工预览**：输出的 HTML 文件需在浏览器中打开确认动画效果（CSS 时间轴、字体渲染、响应式缩放），自动测试仅验证了文件结构和脚本 exit code。
- **真实内容评分选帖未验证**：场景 B 的「爆款潜力评分」依赖 AI 判断，本次只验证了 `group +topics` 能返回数据供 AI 决策，未实测评分逻辑。
- **仅测试 `talk` 类型**：测试星球主题均为 `talk` 类型，`article`（文章）类型的 `content` 字段结构未实测。

## 结论

**主干通过。** 两项渲染脚本均按设计工作，CLI 数据流正常，环境依赖边界清晰（record.js 缺 puppeteer 时故障明确）。文档已根据实测校准正文 field 名。AI 提炼阶段的质量和录制路径受限于环境未完整验证。
