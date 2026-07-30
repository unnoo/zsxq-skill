# 生成竖版动画视频（generate-video）

把知识星球的帖子/文章内容转为**竖版动画视频**（2160×3840，9:16，~17-21s），适合发布到抖音、视频号、小红书。AI 提炼内容为结构化脚本，通过内置渲染脚本生成动画 HTML，可选录制 4K MP4。

> **依赖**：本场景需 Node.js ≥ 18；MP4 录制另需 ffmpeg + puppeteer（`scripts/scenarios/generate-video/` 目录下 `npm install`）。详见「所需输入」环境依赖。

> [!CAUTION]
> - **视频生成涉及 LLM 对内容的提炼和改写**：AI 提炼后的脚本可能改变原文语气或强调方向，生成前必须向用户展示脚本预览并等待确认
> - **输出文件在本机，不向星球发布任何内容**：动画 HTML 和 MP4 保存在本地 `~/Desktop/内容雷达/` 目录，不会写回知识星球
> - **确保有转载/改编原文内容的权利**：视频素材来源于星球成员帖子，星主应确认帖子授权范围再制作视频

## 适用意图

- 「帮我把这篇帖子做成视频」「生成这个帖子的竖版视频」
- 「帮我找最近适合做视频的帖子」「本周有哪些帖子能做视频」
- 「帮我提炼星球精华，做几条视频」
- 「生成本周视频合集」「做几条爆款视频」

## 不适用情况

- 只需要**文字**运营报告（无需视频）→ 用 [compose-operations-report](compose-operations-report.md)
- 只需要**静态海报图片**（PNG）→ 用 [generate-daily-poster](generate-daily-poster.md)
- 只需要查看/搜索帖子，不做视频 → 直接用 [group-topics](../group-topics.md) / [topic-search](../topic-search.md)
- 帖子是纯图片帖（无文字）或 Q&A 类型 → 视频需要文字内容支撑，不适用
- 帖子正文不足 200 字 → 内容过短，不适合结构化视频
- 只在星球内部传播、不发布到站外平台 → 视频是站外传播介质，如不需站外传播则无需本场景
- 环境未满足依赖且用户不接受「纯 JSON 交付」降级 → 停止，先安装依赖

## 所需输入

| 输入 | 必填 | 说明 |
|------|------|------|
| 内容来源 | **是** | 用户提供一条具体的星球帖子（topic_id / 链接 / 标题）或直接粘贴文字。如说「帮我找」，则用 `group +topics` 浏览候选 |
| 星球（group_id 或星球名） | 内容来源是帖子时**是** | 帖子所属的星球。只给名称时先用 `group +list` 解析 group_id |
| 作者名 | 否 | 显示在视频封面上的作者昵称（取自 `topic +detail` 的 `owner` 字段，用户也可覆盖） |
| 品牌色 | 否 | 视频主题色（十六进制，取自 topic +detail 的 `brand` 信息。用户不指定时用默认品牌色） |
| 保存目录 | 否 | 默认 `~/Desktop/内容雷达/`；用户可指定其它路径 |

**环境依赖（本场景专属，非全 skill 必需）**：

| 依赖 | 必须？ | 安装方式 | 说明 |
|------|--------|---------|------|
| Node.js ≥ 18 | **是** | `node --version` 确认 | 运行渲染脚本 |
| npm install（脚本依赖） | 否（仅 MP4） | `cd ~/.claude/skills/zsxq/scripts/scenarios/generate-video && npm install` | 安装 puppeteer（~200MB）。首次安装可用 `PUPPETEER_SKIP_DOWNLOAD=true npm install` 跳过 Chromium 下载，然后用系统已装的 Chrome（见录制步骤）|
| ffmpeg | 否（仅 MP4） | `brew install ffmpeg` | 视频编码 |

## 使用的原子操作

| 操作 | reference | 在本场景中的作用 |
|------|-----------|-----------------|
| `group +list` | [../group-list.md](../group-list.md) | 过渡步骤：按星球名定位 group_id |
| `group +topics --json` | [../group-topics.md](../group-topics.md) | 拉取候选帖子列表，通过 `counts`（likes/comments）辅助评分选帖 |
| `topic +detail` | [../topic-detail.md](../topic-detail.md) | 取选定帖子的完整正文（`article.text` / `talk.text`）、作者、标题 |
| `topic +search` | [../topic-search.md](../topic-search.md) | 按关键词搜索特定内容 |

场景专属处理（非 CLI 操作）：AI 内容提炼与 JSON 结构化（规则见下文「提炼铁律」）；渲染动画 HTML 与录制 MP4 由 `scripts/scenarios/generate-video/` 下内置脚本完成。

## 执行流程

### 第 0 步：环境预检

先确认渲染环境可用，避免跑完数据才发现无法渲染：

```bash
node --version  # 应 ≥ v18
ls ~/.claude/skills/zsxq/scripts/scenarios/generate-video/render.js
```

- **成功**：继续
- **Node.js 版本不足**：提示升级
- **render.js 不存在**：说明 skill 安装不完整，提示检查仓库文件

如果用户后续要录制 MP4，再检查：

```bash
ls ~/.claude/skills/zsxq/scripts/scenarios/generate-video/node_modules/puppeteer  # puppeteer 是否已安装
which ffmpeg  # ffmpeg 是否可用
```

### 第 1 步：确定内容来源

**场景 A — 用户指定了具体帖子**：
- 用户给了 topic_id → 直接进入第 2 步拉详情
- 用户给了帖子链接 → 按 [share-links](../share-links.md) 解析出 topic_id
- 用户粘贴了文字 → 直接用用户提供的文字（跳过第 2 步），星球名/作者名/品牌色让用户提供或用默认值

**场景 B — 用户说「帮我找适合做视频的帖子」**：
1. `group +list` 确定目标星球（名称命中多个时列候选让用户确认）
2. `group +topics --group-id <ID> --limit 30 --json` 拉最近帖子
3. **按爆款潜力评分**，优先选择：有冲突/争议/反常识的 > 有具体数字/金额的 > 有个人故事/情绪的 > 有明确方法论/步骤的
4. **排除**：纯数据分析、纯链接分享、Q&A 问答、文字 < 200 字、文字 > 1500 字
5. 列出 2–3 篇推荐，附理由和爆款潜力评分，让用户选择
6. 用户说「找更早的」或「找关于 XX 的」→ `topic +search --group-id <ID> --query "关键词"`
7. 选定后进入第 2 步

### 第 2 步：取帖子正文

```bash
zsxq-cli topic +detail --topic-id <TOPIC_ID> --json
```

提取字段：
- `owner.name` 或 `owner.alias` → 作者昵称
- `content` → 正文（无论 `talk`/`article` 类型，文本均在此字段）
- `title` → 标题（可选，仅文章类型有关联标题）

用户粘贴文字时本步跳过。

### 第 3 步：AI 提炼内容为结构化脚本

**AI 独立完成提炼，不调外部 API。**

按以下流程执行：

1. **确定模板**：根据内容特点自动选择
   - 长文（> 400 字）、多要点、有论证过程 → **结构化模板**（4 页 × 封面 2s + 内容 5s = 17s）
   - 金句、短观点（≤ 400 字）、情绪共鸣 → **金句模板**（6 页 × 3.5s = 21s）

2. **提炼为结构化 JSON**，schema 如下：

```json
{
  "planet": "星球名称",
  "author": "作者名（留空则不显示分隔符）",
  "brand_color": "#品牌色十六进制",
  "topic": "视频主题（≤8字）",
  "topic_highlight": "topic中需高亮的关键词（1-3字）",

  "cover": {
    "chip": "星球名 · 第X期",
    "h1": ["封面标题第1行（≤8字）", "封面标题第2行（≤8字）"],
    "h1_accent": 1,
    "sub": "封面副标题（≤20字）",
    "trio": [
      { "label": "关键词（2字）", "desc": "解释（≤5字）", "color": "orange" },
      { "label": "关键词（2字）", "desc": "解释（≤5字）", "color": "orange" },
      { "label": "关键词（2字）", "desc": "解释（≤5字）", "color": "cream" }
    ]
  },

  "scenes": [
    {
      "chip": "场景标签（2-6字）",
      "h1": ["标题第1行（≤8字）", "标题第2行（≤8字）"],
      "h1_accent": 1,
      "sub": "补充说明（≤25字）",
      "items": ["要点1（≤18字）", "要点2（≤18字）", "要点3（≤18字）"]
    }
  ],

  "finale": {
    "chip": "结语标签",
    "h1": ["结论第1行（≤8字）", "结论第2行（≤8字）"],
    "sub": "结论展开（≤30字）",
    "items": [],
    "finale_text": "金句（≤15字×2行，用\\n换行）"
  },

  "cta": null
}
```

3. **遵守提炼铁律**（违反任何一条 → 重写）：

   - 结论先行 — 封面第一页就说核心观点，不要先铺垫再总结
   - 主谓宾完整 — 每行标题必须独立成句，不省略主语（"我选择放弃"而非"选择放弃"）
   - 不用符号代替语义 — 禁止 ≠、→、& 等符号，用文字表达
   - 金句两行对仗或递进 — "做完不算 / 做通才算"、"五百万很多 / 一个事故更贵"
   - trio 描述 ≤ 5 字 — 绝对不允许换行
   - topic ≤ 8 字 — 超过必缩短
   - items 单条 ≤ 18 字 — 超过必拆分或缩短
   - 结语页不要 items — 只用大字金句（finale_text），清晰有力
   - 数字具体 — "500 万"比"很多钱"好，"3 年"比"很久"好
   - 系列编号 — chip 里带"第 X 期"，建立连续性

4. **黑名单**（绝对不能出现）：

   - ❌ 一个字单独掉到下一行
   - ❌ "≠"、"→"、"&" 等符号做标题
   - ❌ 没有主语的句子做标题
   - ❌ 结语页带边框的居中文字
   - ❌ "扫码加入"（视频里放不了码）
   - ❌ trio 描述超过 5 个字
   - ❌ 两行标题必须连起来才能理解的写法

5. **质量自查**：生成 JSON 后逐项检查以下 7 项，任何一项不通过则修改后再输出：

   | # | 检查项 | 标准 |
   |---|--------|------|
   | 1 | 每行主谓宾完整 | 遮住其他行，这一行单独能看懂 |
   | 2 | trio 描述 ≤ 5 字 | 数字数 |
   | 3 | topic ≤ 8 字 | 数字数 |
   | 4 | 无禁用符号 | 无 ≠ → & |
   | 5 | items 单条 ≤ 18 字 | 数字数 |
   | 6 | 金句两行对仗 | 读出来有节奏感 |
   | 7 | 封面结论先行 | 第一页就能抓住人 |

### 第 4 步：展示脚本预览，等待用户确认

生成脚本摘要向用户展示：

```
📋 视频脚本预览 · 第N期

封面：「[标题第1行] / [标题第2行]」
场景1：[标签] — [标题第1行] [标题第2行]
场景2：[标签] — [标题第1行] [标题第2行]
场景3：[标签] — [标题第1行] [标题第2行]（如有）
结语：[金句]

确认生成视频？还是需要调整？
```

- 用户说「确认」→ 进入第 5 步
- 用户说「第 X 场景改成 XX」→ 修改后重新展示预览
- 用户说「换个模板 / 用金句模板」→ 改用金句模板（6 页 × 3.5s）

### 第 5 步：渲染动画 HTML

用户确认脚本后：

```bash
# 1. 将 JSON 写入文件
# （Write 工具写入 ~/Desktop/内容雷达/<slug>.json）

# 2. 渲染动画 HTML（结构化模板）
node ~/.claude/skills/zsxq/scripts/scenarios/generate-video/render.js \
  ~/Desktop/内容雷达/<slug>.json \
  ~/Desktop/内容雷达/<slug>.html

# 3. 浏览器预览
open ~/Desktop/内容雷达/<slug>.html
```

- `render.js` 为结构化模板（4 页）；金句模板用 `render-minimal.js`
- render.js 成功 → 打开浏览器让用户预览动画效果
- 用户不满意动画 → 返回第 3 步修改 JSON 后重新渲染
- 用户满意 → 问是否要录制 MP4

### 第 6 步（可选）：录制 4K MP4

用户想要最终视频文件时：

> 需已安装 puppeteer + ffmpeg（见环境依赖）。如果系统已装有 Google Chrome，可跳过 Chromium 下载，用系统 Chrome 录制：
> ```bash
> PUPPETEER_SKIP_DOWNLOAD=true npm install  # 首次安装，跳过 Chromium 下载
> PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
>   node ~/.claude/skills/zsxq/scripts/scenarios/generate-video/record.js ...
> ```

```bash
# 1. 封面截图
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  node ~/.claude/skills/zsxq/scripts/scenarios/generate-video/record.js \
  ~/Desktop/内容雷达/<slug>.html \
  ~/Desktop/内容雷达/<slug>-cover.png --cover

# 2. 录制完整视频
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  node ~/.claude/skills/zsxq/scripts/scenarios/generate-video/record.js \
  ~/Desktop/内容雷达/<slug>.html \
  ~/Desktop/内容雷达/<slug>-4k.mp4 \
  17   # 时长：2 + (页数-1) × 5
```

录制使用虚拟时钟（确定性帧同步），约需 1–2 分钟。

**模板与时长对照**：

| 模板 | 脚本 | 适用内容 | 页数 | 总时长 |
|------|------|----------|------|--------|
| 结构化 | `render.js` | 长文、多要点、有论证过程 | 4 页 | 封面 2s + 内容 5s/page = 17s |
| 金句型 | `render-minimal.js` | 金句、短观点、情绪共鸣 | 6 页 | 3.5s/page = 21s |

## 分支与停止条件

- **Node.js 版本不足**：提示升级，停止
- **render.js 不存在**：说明 skill 安装不完整，停止
- **无适合做视频的帖子**（场景 B 浏览后）：如实报告「当前无适合内容」，不强行选
- **帖子过短（< 200 字）**：告知用户，建议选其他帖子或用金句模板
- **帖子过长（> 1500 字）**：AI 只取核心论点，不试图覆盖全文
- **内容来源为纯链接分享/纯数据/无文字**：告知不适合做视频
- **AI 提炼被用户多次退回**（超过 3 轮修改）：建议换帖子或手动写脚本
- **record.js 缺失依赖**（puppeteer/ffmpeg 未装）：告知用户缺少什么，问是安装依赖还是只要 HTML。如果 puppeteer 已装但找不到 Chromium，提示设置 `PUPPETEER_EXECUTABLE_PATH` 指向系统 Chrome
- **录制失败**：保留 HTML 文件，不阻塞
- **限流（API 调用的 429 / frequently）**：退避几秒重试，不循环猛刷
- **用户只要预览、不要视频**：停在 HTML 预览阶段结束

## 用户确认点

1. **选帖确认**（场景 B）：列出候选帖子后，用户明确选择要处理哪一篇
2. **脚本预览确认**：AI 提炼后的 JSON 脚本展示给用户，确认或修改后才渲染（核心确认点——提炼可能改变原文语气）
3. **录制 MP4 前**：告知 MP4 录制需 1–2 分钟，询问是否确认（较大资源消耗）
4. **降级确认**：环境不满足录制条件时，确认是否接受仅 HTML 输出

## 完成标准

- AI 已按提炼铁律完成内容提炼，输出符合 schema 的结构化 JSON
- 脚本预览已经用户确认（至少一轮确认通过）
- `render.js` / `render-minimal.js` 成功输出动画 HTML 至用户目录（含 open 预览）
- （可选）`record.js` 成功录制 4K MP4 至用户目录
- 用户不满意渲染结果时，已支持返回修改脚本重试

## 失败与回退

- **只读阶段（第 0–2 步）**完全无副作用，可安全重跑
- **提炼阶段（第 3 步）**不产生外部文件，修改 JSON 重新展示即可
- **渲染阶段（第 5 步）**：render.js 报错先检查 JSON 格式（常见：引号未闭合、字段缺失），修正后重跑
- **录制阶段（第 6 步）**：若失败则保留 HTML 供用户手动操作；puppeteer 未安装则 `cd ~/.claude/skills/zsxq/scripts/scenarios/generate-video && npm install`；Chromium 缺失（报 `ERR_BROWSER_NOT_FOUND`）则设 `PUPPETEER_EXECUTABLE_PATH` 指向系统 Chrome
- 通用错误（404、参数缺失、解析失败等）见 [auth-errors](../auth-errors.md#常见错误处理)

## 附加资源

- 渲染脚本路径：`scripts/scenarios/generate-video/render.js`（结构化模板）/ `render-minimal.js`（金句模板）/ `record.js`（录制）
- 脚本依赖安装：`cd ~/.claude/skills/zsxq/scripts/scenarios/generate-video && npm install`（仅录制 MP4 需要 puppeteer）；跳过 Chromium 下载用 `PUPPETEER_SKIP_DOWNLOAD=true npm install`
- 拉帖子列表：[group-topics](../group-topics.md)；帖子详情：[topic-detail](../topic-detail.md)
- 星球列表：[group-list](../group-list.md)；主题搜索：[topic-search](../topic-search.md)
- 分享链接解析：[share-links](../share-links.md)
- 常见品牌色参考：星球创业笔记 `#2B5EA7`、生财有术 `#2FA98A`、鹿野 `#1A6B52`、刘容发现了 `#2B5EA7`、默认 `#C84B1F`
- 认证与常见错误：[auth-errors](../auth-errors.md)
