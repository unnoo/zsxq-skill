# topic +create（发布主题）

对应操作：`topic +create`；MCP 调用见下方命令块。

在指定星球内发布一条新主题（帖子）。

> [!IMPORTANT]
> - 支持 `talk`（普通帖子，默认）与 `q&a`（提问）两种类型；`task`、`solution` 类型暂不支持通过本操作创建。
> - 投票仅支持 `talk` 类型，不能与提问（`q&a`）同用。
> - 关联打卡任务仅支持 `talk` 类型，不能与提问（`q&a`）同用；`checkin_id` 从 [group-checkins](group-checkins.md) 查询。
> - 提问不能问自己；在配置了**提问费用**的星球（星主设置了最低提问金额）会创建失败 —— 本操作无法传提问金额参数，实测返回 `code 80105/80106`。

> [!CAUTION]
> 这是**公开写入操作** —— 发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 发布的内容与类型（普通帖子，可选投票或关联打卡任务 / 提问）
> 3. 投票主题：投票标题与全部选项；提问主题：向谁提问（对方 user_id）、是否匿名；关联打卡任务时：目标任务的名称与 checkin_id
> 4. 是否声明 AI 生成（AI 声明模式）
> 5. 若对草稿做了排版或改写：把**完整确认稿**（标题、正文、标签、附件清单）交用户核对，待其明确表示”确认发布”后再执行

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 发布一条主题
zsxq-cli topic +create \
  --group-id 123456789 \
  --text "示例主题正文内容"

# 带附件（图片/文件，逗号分隔）
zsxq-cli topic +create \
  --group-id 123456789 \
  --text "示例内容" \
  --files photo.jpg,report.pdf

# 声明内容为 AI 生成（等同 --ai-mode aigc）
zsxq-cli topic +create --group-id 123456789 --text "AI 生成的内容" --ai

# AI 声明模式：aigc / personal_perspective / none
zsxq-cli topic +create --group-id 123456789 --text "内容" --ai-mode personal_perspective

# 创建带投票的主题
zsxq-cli topic +create \
  --group-id 123456789 \
  --text "大家来投票" \
  --vote-title "你支持哪个方案？" \
  --vote-options "方案A,方案B,方案C"

# 关联打卡任务（仅 talk，需 zsxq-cli ≥ 0.5.1；checkin_id 从 group-checkins 查询）
zsxq-cli topic +create \
  --group-id 123456789 \
  --text "今日打卡" \
  --checkin-id 88888

# 向指定成员提问（q&a 主题）
zsxq-cli topic +create \
  --group-id 123456789 \
  --ask 77777 \
  --text "请问这个问题怎么解决？"

# 匿名提问
zsxq-cli topic +create --group-id 123456789 --ask 77777 --text "问题内容" --anonymous

# 正文按 markdown 渲染
zsxq-cli topic +create --group-id 123456789 --text "# 标题" --markdown

# 读取本地 .md 文件作为正文（按 markdown 发布，非附件上传）
zsxq-cli topic +create --group-id 123456789 --markdown-file article.md
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

发布普通帖子（`talk`）：

```json
{"method": "POST", "path": "/v2/groups/123456789/topics", "body": {"req_data": {"type": "talk", "text": "示例主题正文内容"}}}
```

发布提问（`q&a` 类型）：

```json
{"method": "POST", "path": "/v2/groups/123456789/topics", "body": {"req_data": {"type": "q&a", "text": "请问这个问题怎么解决？", "questionee_id": "77777"}}}
```

关联打卡任务（`talk` 类型；`checkin_id` 为数字）：

```json
{"method": "POST", "path": "/v2/groups/123456789/topics", "body": {"req_data": {"type": "talk", "text": "今日打卡", "checkin_id": 88888}}}
```

带投票的帖子需两步 —— 先创建投票：

```json
{"method": "POST", "path": "/v3/votes", "body": {"req_data": {"title": "你支持哪个方案？", "options": [{"title": "方案A"}, {"title": "方案B"}]}}}
```

取响应中的 `vote.uid` 作为发帖 `req_data.vote_uid`。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID（从 `group +list` 获取） |
| `--text <text>` | 否* | 主题正文内容，支持 `\n` 换行（提问时必填；与本地文件发布互斥） |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔（图片/文件）；提问主题不支持 |
| `--ai` / `--ai-mode <mode>` | 否 | AI 声明：取值 `aigc`（AI 生成）/ `personal_perspective`（个人观点）/ `none`（不声明）；简写开关等同 `aigc` |
| `--ask <user_id>` | 否 | 向指定成员提问，创建 `q&a` 主题；值为对方 user_id |
| `--anonymous` | 否 | 匿名提问（仅提问主题可用） |
| `--vote-title <title>` | 否 | 投票标题；提供时内联创建投票并关联主题（仅 talk，与提问互斥） |
| `--vote-options <list>` | 否 | 投票选项，逗号分隔、至少 2 个（选项内不能含逗号）；须与投票标题同时提供 |
| `--checkin-id <id>` | 否 | 关联打卡任务（仅 talk，与提问互斥）；任务 ID 从 [group-checkins](group-checkins.md) 查询 |
| `--markdown` | 否 | 正文按 markdown 渲染 |
| `--markdown-file <path>` | 否 | 读取本地 .md 文件作为正文发布（按 markdown，非附件上传）；与正文文本参数互斥 |
| `--json` | 否 | 输出原始 JSON（含新建 topic_id） |

\* 正文、附件、投票标题至少提供其一。

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/topics` |
| `--text` | `req_data.text` |
| `--title`（hidden） | `req_data.title`（q&a 不传） |
| `--markdown` | `req_data.text_type: "markdown"` |
| `--markdown-file` | 无对应字段 —— MCP 通道由 agent 自读文件内容作为 `req_data.text` 传入 |
| `--ai` / `--ai-mode` | `req_data.creation_statement` |
| `--ask` | `type: "q&a"` + `req_data.questionee_id` |
| `--anonymous` | `req_data.anonymous: true` |
| `--vote-title` / `--vote-options` | 先 `POST /v3/votes` 再带 `vote_uid` |
| `--checkin-id` | `req_data.checkin_id`（数字） |
| `--files` | **仅 CLI 通道**（附件上传缺口，见 [endpoint-catalog](endpoint-catalog.md) 的「通道缺口」） |

## 输出

成功后输出：

```
✓ Topic created
{
  "success": true,
  "topic": {
    "topic_id": "111222333444",
    "create_time": "2026-08-13T19:20:50.565+0800",
    "text": "示例主题正文内容",
    "title": "示例主题标题"
  }
}
```

主题状态（类型、`creation_statement`、关联投票等）以 `topic +detail` 的返回为准。关联打卡任务时，响应与 `topic +detail` 中均含 `checkin` 对象（`checkin_id` / `title` / `min_words_count`），可据此核对关联是否生效。

MCP 通道恒为 `{success, status_code, body}` 信封，新建主题信息在 `body.resp_data`；正文是否按 markdown 落地、标签是否解析成功，以 `GET /v2/topics/{topic_id}/info` 的返回为准。

<!-- cli-only:start -->
CLI 通道下以 `topic +detail` 的返回为准（JSON 结构与 `body.resp_data` 相同）。
<!-- cli-only:end -->

## 推荐工作流

把草稿整理成规范帖子再发布的内容运营流程。下面每一步给出 MCP 通道的调用形式：底层接口工具 `call_zsxq_api` 的调用体（`{method, path, body}`）。

<!-- cli-only:start -->
下面每一步同时给出 CLI 通道的命令形式：bash 命令。
<!-- cli-only:end -->

**① 明确主题类型与目标**

确认主题类型（见上方 IMPORTANT）：`talk` 普通帖子（默认）/ 带投票的帖子 / `q&a` 提问，并明确本篇目标（分享观点 / 通知 / 引导讨论 / 收集意见 / 向成员提问等）。同时确认目标星球：

<!-- cli-only:start -->

```bash
zsxq-cli group +list
```

<!-- cli-only:end -->

```json
{"method": "GET", "path": "/v2/groups"}
```

**② 准备正文（排版 / 标签 / 附件）**

按本文件 `## 参数` 支持的能力整理内容，不臆造参数：

- **排版**：标题、分段、换行都写进正文内容字段（支持 `\n`；MCP 通道为 `req_data.text`）。常见要求——标题简洁、正文分段、结尾加一句引导互动的话；若用户要求“只排版，不改写”，则保留原文观点与立场、仅调整格式。
- **话题标签**：标签**内嵌在正文 content 里**，形如 `<e type="hashtag" .../>`（与 [topic-detail](topic-detail.md) 的说明一致）。给标签建议时先看星球现有标签体系、尽量对齐以免造重复标签（见 [group-hashtags](group-hashtags.md)；MCP 通道 `{"method": "GET", "path": "/v2/groups/123456789/hashtags"}`）。
- **图片 / 文件**：MCP 通道无法上传附件，附件需由宿主侧完成上传后把 `image_ids` / `file_ids` 带入（见 [endpoint-catalog](endpoint-catalog.md) 的「通道缺口」）。@成员等富文本同样内嵌在正文中；能力边界一律以 `## 参数` 为准。

<!-- cli-only:start -->
- **图片 / 文件**：附件上传仅 CLI 通道支持，用 `--files` 直接传本地路径。
<!-- cli-only:end -->

**③ 发布前把完整确认稿交用户确认（写入意图确认）**

把整理后的**完整确认稿**——标题、正文、标签、附件清单、目标星球——一并展示给用户，待其明确表示“确认发布”后再执行；默认不直接发帖。此步对应上方 `> [!CAUTION]`。

**④ 发布**

用户确认后调用本文件 `## 命令`：

<!-- cli-only:start -->

CLI 通道：

```bash
zsxq-cli topic +create --group-id <id> --text "确认后的正文"
```

<!-- cli-only:end -->

MCP 通道（对应上方 MCP 命令块的发布主题调用；提问用 `type:"q&a"` + `questionee_id`）：

```json
{"method": "POST", "path": "/v2/groups/<group_id>/topics", "body": {"req_data": {"type": "talk", "text": "确认后的正文"}}}
```

**⑤ 发布后校验（可选）**

用返回的 `topic_id` 拉详情，核对正文与标签是否按预期落地（标签的解析方式见 [topic-detail](topic-detail.md)）：

<!-- cli-only:start -->

```bash
zsxq-cli topic +detail --topic-id <新建的 topic_id>
```

<!-- cli-only:end -->

```json
{"method": "GET", "path": "/v2/topics/<新建的 topic_id>/info"}
```

## 失败语义

写入失败即原子回滚 —— 不会留下空主题或半成品 topic_id。重试前请先确认参数是否合法。

## 错误说明

服务端返回的错误：

| 错误 | 原因 |
|------|------|
| `投票至少需要 2 个选项` / `投票选项不能为空` | 选项不足 2 个或含空项 |
| `问答内容不能超过 1000 字符` | 提问内容超长 |
| `code 80105`（MCP 通道看 `body.succeeded` / `body.code`） | 向自己提问（提问对象传了自己的 user_id） |
| `code 80106`（MCP 通道看 `body.succeeded` / `body.code`） | 服务端拒绝创建提问（实测于配置提问费用的星球；本操作无法传提问金额） |

<!-- cli-only:start -->
CLI 通道下 `80105` / `80106` 显示为 `MCP tool error`。
<!-- cli-only:end -->

<!-- cli-only:start -->

CLI 通道的本地参数校验提示：

| 错误 | 原因 |
|------|------|
| `--ai 和 --ai-mode 不能同时使用` | 两个 AI 声明参数同传 |
| `--ai-mode 取值必须是 aigc、personal_perspective 或 none` | `--ai-mode` 值非法 |
| `投票仅支持普通主题（talk），不能与 --ask 问答主题同时使用` | 投票与提问同用 |
| `--vote-title 和 --vote-options 必须同时提供` | 投票只给了标题或只给了选项 |
| `--anonymous 仅支持与 --ask 一起使用` | 没指定提问对象却要求匿名 |
| `问答主题不支持上传附件，请仅提供 --text` | 提问带了 `--files` |
| `问答主题必须提供 --text` | 提问没写内容 |
| `主题内容不能为空，请提供 --text、--files 或 --vote-title` | 内容、附件、投票全部为空 |
| `--text 和 --markdown-file 不能同时使用` | 两种正文来源同传 |
| `读取 markdown 文件失败: ...` | .md 文件读取失败 |

<!-- cli-only:end -->

通用错误（401、参数缺失、星球无权限发帖等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-checkins](group-checkins.md) — 查询打卡任务、获取 checkin_id
- [topic-reply](topic-reply.md) — 对已发主题评论
- [group-list](group-list.md) — 获取 group_id
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
