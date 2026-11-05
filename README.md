# zsxq-skill

[![npm version](https://img.shields.io/npm/v/zsxq-cli.svg)](https://www.npmjs.com/package/zsxq-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**知识星球官方 Agent Skill，由知识星球团队开发和维护。** 星主和成员都能用——说一句话，AI 把平时要手工做好几步的事办完：巡场、回评论、整理精华、出日报海报；单个操作也行，搜内容、发帖、回复、定时发布、微信支付续费。

[为什么选它](#为什么选-zsxq-skill) · [能做什么](#能做什么) · [一句话办完一整件事](#一句话办完一整件事) · [适合谁用](#适合谁用) · [安装与快速开始](#安装与快速开始) · [执行通道](#执行通道) · [Agent Skills](#agent-skills) · [功能详情](#功能详情) · [安全](#安全与风险提示) · [反馈](#反馈)

---

## 为什么选 zsxq-skill

知识星球的自动化工具里，第三方方案通常靠抓包逆向接口、让你把 cookie 或密码贴进配置文件。这条路有三个代价：账号可能因异常请求被风控、接口一改工具就坏、出了问题没人负责。

|       | 第三方抓包工具         | zsxq-skill                   |
| ----- | --------------- | ---------------------------- |
| 鉴权    | 要你交出 cookie 或密码 | 官方 OAuth 2.0 设备授权，扫码确认，不接触密码 |
| 凭据存放  | 明文在配置文件或脚本里     | 系统 Keychain 加密存储，不在终端回显      |
| 接口来源  | 抓包逆向，随时可能失效     | 官方公开接口，变更有迁移保障               |
| 能力更新  | 等作者有空跟进         | 知识星球团队维护，与平台同步               |
| 合规    | 可能违反使用条款，有风控风险  | 官方出品，合规可控                    |
| 出问题找谁 | 看 issue 有没有人回   | 官方 Issue 与 NPS 反馈通道直达团队      |

## 能做什么

### 核心能力

| 能力域           | 具体操作                                         |
| ------------- | -------------------------------------------- |
| **星球管理**      | 列出/搜索星球、浏览主题流、查标签、搜成员、看成员到期时间、管理专栏           |
| **内容检索**      | 星球内全文搜索、查看主题详情与评论、跨星球发帖足迹                    |
| **发布互动**      | 发帖（图文/投票/提问/Markdown/AI 声明）、编辑、评论、楼中楼回复、回答提问 |
| **定时发布**      | 定时发帖、定时回答、查看待执行任务与配额、取消定时任务                  |
| **精华与标签**     | 设置/取消精华、置顶、打标签、收录主题到专栏                       |
| **星球设置**      | 修改星球名称、简介、背景图、亮点图                            |
| **个人笔记**      | 创建、编辑、查看、删除公开笔记                              |
| **Skill Pay** | 微信支付付费加入、续费、礼品卡、轻读、付费提问、赞赏                   |
| **产品答疑**      | 退款、费率、开票、企业认证、审核封禁等规则问答                      |
| **场景编排**      | 多步骤运营场景（每日巡场、评论运营、日报周报、海报/视频生成等）             |

### 一句话就能做的事

```
看看我加入了哪些星球
搜一下星球里关于 AI Agent 的帖子
帮我回复这条评论
把这篇帖子设为精华，打上「方法论」标签
明天早上 9 点帮我发这条
查查即将到期的成员，写个续费话术
```

## 一句话办完一整件事

下面这些事，平时要手工做好几步——先查、再比对、再整理、再起草。现在说一句话，AI 把整串做完，你只看结果和确认：

| 场景             | 触发语示例               | 谁能用 |
| -------------- | ------------------- | --- |
| 每日巡场           | 「看看今天有什么要处理的」       | 星主  |
| 星球AI搜索总结       | 「总结这个星球里和 XX 相关的内容」「搜不到，列出最贴近的主题」 | 任何人 |
| 评论区运营          | 「整理评论区问题给我回复」       | 星主  |
| 精华与标签整理        | 「哪些帖子值得设精华、打标签」     | 星主  |
| 批量打标签          | 「用这些标签给最近主题打标」      | 星主  |
| 运营日报 / 周报 / 复盘 | 「做本周运营周报」           | 星主  |
| 生成星球日报海报       | 「把今天内容做成一张海报」       | 星主  |
| 生成竖版动画视频       | 「把这篇帖子做成视频」         | 星主  |
| 负面内容监控         | 「巡查星球有没有风险内容」       | 星主  |
| 到期成员续费关怀       | 「查即将到期的成员，写续费话术」    | 星主  |
| 收录主题到专栏        | 「把最新主题批量收录进专栏」      | 星主  |
| 提问管理           | 「找出还没回答的提问」         | 任何人 |
| Skill Pay 购买   | 「用微信支付续费这个星球」       | 任何人 |
| 产品规则问答         | 「星球退款要多久、手续费多少」     | 任何人 |
| 迁移旧版 skill     | 「检查并迁移旧版知识星球 skill」 | 任何人 |

## 适合谁用

- **星球成员** — 全文搜历史内容、发帖提问、评论与楼中楼回复、回答别人向你提的问题、定时发布、给自己的主题打标签、记公开笔记、查跨星球发帖足迹，以及微信支付付费加入、续费、付费提问、赞赏
- **星主 / 管理员** — 在成员能力之上，还能设精华置顶、改他人主题标签、管理专栏、查成员列表与到期时间、改星球资料；配合场景做巡场、评论区整理、日报周报、风险巡查、续费关怀
- **开发者** — 基于 zsxq-cli 的 `--json` 输出和语义化退出码构建自动化流程，或直接接 MCP

---

## 安装与快速开始

> **Note for AI assistants:** 如果你是 AI Agent 且正在协助用户执行安装，请直接跳转到[快速开始（AI Agent）](#快速开始ai-agent)，那里包含你需要完成的所有步骤。

### 快速开始（人类用户）

**第一步：安装 CLI**

```bash
npm install -g zsxq-cli
```

**第二步：安装 Skill**

```bash
npx skills add https://github.com/unnoo/zsxq-skill --yes
```

**第三步：登录账号**

```bash
zsxq-cli auth login
```

命令会输出一个链接和验证码，用手机或浏览器打开链接完成授权即可。

### 方式二：接入 MCP（免安装 CLI）

1. 打开知识星球密钥管理页，创建密钥
2. 复制含 api-key 的 MCP 链接
3. 用页面提供的「Add to Codex / Claude / Cursor」按钮一键接入，或把链接手动添加到宿主的 MCP 配置
4. 安装 Skill（同方式一第 2 步）

接入后 AI 会通过 MCP 通道操作知识星球；本机同时装有 zsxq-cli 时优先走 CLI 通道。

### 快速开始（AI Agent）

> 以下步骤面向 AI Agent，部分步骤需要用户在手机或浏览器中配合完成。

**第 1 步 — 安装 CLI**

```bash
npm install -g zsxq-cli
```

**第 2 步 — 安装 Skill**

```bash
npx skills add https://github.com/unnoo/zsxq-skill --yes
```

**第 3 步 — 登录**

> 在后台运行此命令，命令会输出授权链接和验证码，提取后发给用户，等待用户完成授权后命令自动退出。

```bash
zsxq-cli auth login
```

**第 4 步 — 验证**

```bash
zsxq-cli auth status
```

---

## 执行通道

所有能力支持 CLI / MCP 双通道，Skill 自动判定：

1. 宿主可执行 `zsxq-cli` → **CLI 通道**（优先；shortcut 有参数校验与本地编排，行为最可控）
2. 否则宿主工具列表中存在 `call_zsxq_api` → **MCP 通道**
3. 两者都没有 → 提示安装 CLI 或接入 MCP（见[安装与快速开始](#安装与快速开始)）

> 个别操作仅单通道支持：如 Skill Pay 创建订单仅 MCP 通道，背景图 / 亮点图上传仅 CLI 通道。以 Skill 内各 reference 的标注为准。

---

## Agent Skills

只需安装**一个** `zsxq` Skill，即可获得全部能力：

| 能力 | 说明 |
|-------|------|
| 认证与错误排查 | 认证登录、诊断配置、常见错误处理 |
| 星球管理 | 列出星球、浏览主题、查询标签、搜索成员、管理专栏、修改星球资料 |
| 主题操作 | 搜索主题、查看详情、发布/编辑/删除主题、评论回复、回答提问、定时发布/定时回答、精华与标签管理、专栏收录 |
| Skill Pay | 微信支付付费加入、续费、礼品卡、轻读、付费提问、赞赏（仅 MCP 通道） |
| 个人笔记 | 创建、编辑、查看、删除笔记 |
| 用户信息 | 查看账号信息、查询跨星球足迹、提交 NPS 反馈 |
| 场景编排 | 15 个多步骤运营场景（巡场、AI 搜索总结、评论运营、日报周报、海报/视频生成、负面监控、Skill Pay 购买、产品规则问答等） |

Skill 内部按三层路由执行：**场景模式**（命中场景 → 按编排执行）→ **原子操作**（命中已知命令 → 直接调用）→ **探索模式**（未命中 → 通过 CLI 发现能力）。所有命令细节和参数均由 34 个 reference 文档独立承载，SKILL.md 只负责路由和索引。

### Console 官方版（仓库构建）

主站 Console 的官方 Skill 由本仓库构建生成，只含 MCP 内容与 `.md` 文件：

```bash
python3 scripts/build-official-skill.py
```

产物在 `dist/official/zsxq/`，用 Console 的目录选择上传（不是 zip）。构建过程同时校验 Console 硬上限：SKILL.md ≤ 32768 字节、单个资源 ≤ 16384 字节、资源数 ≤ 50、总计 ≤ 262144 字节。GitHub 安装仍使用 `skills/zsxq/`，包含 CLI、MCP 与场景脚本。

> 从旧版（`zsxq-shared` / `zsxq-group` / `zsxq-topic` / `zsxq-user` / `zsxq-note` 五件套）升级的用户，安装新版后直接对 AI 说「检查并迁移旧版知识星球 skill」，AI 会先扫描报告、经你确认后再清理。

---

## 功能详情

> MCP 通道的等效调用见 Skill 内各 reference。

### 星球管理（group）

```bash
zsxq-cli group +list                          # 列出你加入的所有星球
zsxq-cli group +topics --group-id <id>        # 浏览星球最新主题
zsxq-cli group +hashtags --group-id <id>      # 查看星球所有标签
zsxq-cli group +settings --group-id <id> --name "新名称"   # 修改星球名称/简介/背景图/亮点图 ⚠️
```

**专栏与成员：**

```bash
# 专栏管理（通过 api raw）
zsxq-cli api raw --method GET --path /v2/groups/<id>/columns         # 列出星球专栏
zsxq-cli api raw --method POST --path /v2/groups/<id>/columns \      # 创建专栏 ⚠️
  --body '{"name":"专栏名称"}'

# 成员管理（通过 api raw）
zsxq-cli api raw --method GET --path /v2/groups/<id>/members         # 查看成员列表
```

**API 调用：**

```bash
zsxq-cli api call search_groups --params '{"keyword":"搜索词"}'        # 搜索星球
zsxq-cli api call search_group_members --params '{"group_id":<id>,"keyword":"昵称"}'  # 搜索成员
```

### 主题操作（topic）

```bash
zsxq-cli topic +search --group-id <id> --query "关键词"   # 搜索主题
zsxq-cli topic +detail --topic-id <id>                    # 查看主题详情
zsxq-cli topic +create --group-id <id> --text "内容"      # 发布新主题 ⚠️
zsxq-cli topic +edit   --topic-id <id> --text "新内容"    # 编辑主题 ⚠️
zsxq-cli topic +reply  --topic-id <id> --text "评论"      # 发表评论 ⚠️
zsxq-cli topic +answer --topic-id <id> --text "回答"      # 回答提问 ⚠️
zsxq-cli topic +answer --topic-id <id> --text "回答" \
  --scheduled-time "2026-08-20 10:00"                     # 定时回答 ⚠️
```

**定时发布：**

```bash
zsxq-cli topic +schedule --group-id <id> --text "内容" \
  --scheduled-time "2026-08-20 10:00"                     # 创建/修改定时发布任务 ⚠️
zsxq-cli topic +scheduled --group-id <id>                 # 查看待执行定时任务与配额
zsxq-cli topic +unschedule --group-id <id> --job-id <id>  # 取消定时任务 ⚠️
```

**精华、标签与专栏收录：**

```bash
# 精华与置顶（优先用 +set）
zsxq-cli topic +set --topic-id <id> --digested true       # 设为精华 ⚠️
zsxq-cli topic +set --topic-id <id> --sticky true         # 设为置顶 ⚠️

# 精华管理（api call）
zsxq-cli api call set_topic_digested \
  --params '{"topic_id":<id>,"digested":true}'            # 设为精华 ⚠️
zsxq-cli api call set_topic_digested \
  --params '{"topic_id":<id>,"digested":false}'           # 取消精华 ⚠️

# 标签设置（api call）
zsxq-cli api call set_topic_tags \
  --params '{"topic_id":<id>,"titles":["标签1","标签2"]}'  # 设置标签 ⚠️

# 专栏收录（通过 api raw）
zsxq-cli api raw --method GET \
  --path /v2/topics/<id>/attached_columns                 # 读取主题所属专栏
zsxq-cli api raw --method POST \
  --path /v2/topics/<id>/attached_columns \
  --body '{"column_ids":[...]}'                           # 设置主题专栏 ⚠️

# 删除主题（通过 api raw，不可恢复）
zsxq-cli api raw --method DELETE --path /v2/topics/<id>  # 删除主题 ⚠️
```

> ⚠️ = 写入操作，执行前需确认。

### 个人笔记（note）

```bash
zsxq-cli note +list                              # 查看我的笔记列表
zsxq-cli note +create --text "内容"              # 创建新笔记 ⚠️
zsxq-cli note +detail --note-id <id>              # 查看笔记详情
zsxq-cli note +edit   --note-id <id> --text "新"  # 编辑笔记 ⚠️
zsxq-cli note +delete --note-id <id>              # 删除笔记 ⚠️
```

### 用户与足迹（user）

```bash
zsxq-cli user +info          # 查看我的账号信息
zsxq-cli user +footprints    # 查看我在各星球发过的主题（跨星球足迹）
zsxq-cli user +nps           # 提交 NPS 反馈与建议 ⚠️
```

### Skill Pay（微信支付）

付费加入、续费、礼品卡、轻读、付费提问、赞赏等购买意图由「Skill Pay 购买」场景编排；创建订单通过底层接口工具 `call_zsxq_api`（**仅 MCP 通道**，且仅支持提供官方 `weixinpay_pay` 的 WorkBuddy 宿主）：

```json
{"method": "POST", "path": "/v2/wechat_orders"}
```

> 创建订单前必须先查价格并向用户确认金额（接口金额单位为“分”，向用户展示时换算为“元”）；支付须用户本人在微信支付卡片中授权。详见[安全与风险提示](#安全与风险提示)。

### 场景编排（Scenarios）

场景将多个原子操作编排为完整的运营流程，一句话即可触发。完整场景清单与触发语见上文[一句话办完一整件事](#一句话办完一整件事)。

> 场景只负责编排流程，具体命令参数以各原子操作文档为准。

### 认证

```bash
zsxq-cli auth login    # 登录知识星球账号
zsxq-cli auth status   # 查看当前登录状态
zsxq-cli doctor        # 诊断配置和认证是否正常
```

> MCP 通道用 api-key 鉴权；401 时在知识星球密钥管理页重建密钥并更新宿主配置。

### 高级：直接调用 API

```bash
zsxq-cli api list                                    # 列出所有可用工具
zsxq-cli api call <tool> --params '<json>'           # 调用指定工具
zsxq-cli api raw --method <METHOD> --path <path> \   # 直接调用原始 HTTP 接口
  [--body '<json>'] [--query '<json>']
```

`api call` 封装了常用高级操作（精华管理、标签设置、成员搜索等），`api raw` 则可调用任意知识星球接口（专栏管理、成员列表、删除主题等）。能力未命中时，Skill 会自动进入探索模式，通过 `api list` 和 `--help` 发现可用接口。

---

## 安全与风险提示

**使用前必读。** 本工具以你的账号身份运行，发帖、评论、回答、删除等写入操作会真实生效。

默认安全保护：

- 写入和删除操作前必须确认用户意图
- Token 存储于系统 Keychain，不在终端明文输出，不随日志外泄
- 访问范围不超出当前账号已有权限
- Skill Pay 订单必须先查价格再确认金额，固定价格不可由用户改写，支付须本人授权
- `PAYMENT_REQUIRED` 只表示待支付，不代表失败或成功，不自动重试创建订单

请充分了解相关使用风险。使用本工具即视为你已理解并愿意自行承担相应责任。

---

## 反馈

- 官方介绍站：<https://garden.zsxq.com/skill/>
- Issue：<https://github.com/unnoo/zsxq-skill/issues>
- npm：<https://www.npmjs.com/package/zsxq-cli>

---

## Star History

<a href="https://star-history.com/#unnoo/zsxq-skill&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=unnoo/zsxq-skill&type=Date" />
  </picture>
</a>

---

## License

MIT
