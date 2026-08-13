# topic +create（发布主题）

对应命令：`zsxq-cli topic +create`。

在指定星球内发布一条新主题（帖子）。

> [!IMPORTANT]
> - 支持 `talk`（普通帖子，默认）与 `q&a`（提问，需 `--ask`）两种类型；`task`、`solution` 类型暂不支持通过 CLI 创建。
> - 投票（`--vote-title`）仅支持 `talk` 类型，不能与 `--ask` 提问同用。
> - 提问（`--ask`）不能问自己；在配置了**提问费用**的星球（星主设置了最低提问金额）会创建失败 —— CLI 无法传提问金额参数，实测返回 `code 80105/80106`。

> [!CAUTION]
> 这是**公开写入操作** —— 发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 发布的内容与类型（普通帖子 / 投票 / 提问）
> 3. 投票主题：投票标题与全部选项；提问主题：向谁提问（对方 user_id）、是否匿名
> 4. 是否声明 AI 生成（`--ai` / `--ai-mode`）
> 5. 若对草稿做了排版或改写：把**完整确认稿**（标题、正文、标签、附件清单）交用户核对，待其明确表示”确认发布”后再执行

## 命令

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

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID（从 `group +list` 获取） |
| `--text <text>` | 否* | 主题正文内容，支持 `\n` 换行（提问时必填；与 `--markdown-file` 互斥） |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔（图片/文件）；提问主题不支持 |
| `--ai` | 否 | 声明内容为 AI 生成（等同 `--ai-mode aigc`），与 `--ai-mode` 互斥 |
| `--ai-mode <mode>` | 否 | AI 声明模式：`aigc`（AI 生成）/ `personal_perspective`（个人观点）/ `none`（不声明） |
| `--ask <user_id>` | 否 | 向指定成员提问，创建 `q&a` 主题；值为对方 user_id |
| `--anonymous` | 否 | 匿名提问（仅与 `--ask` 同用） |
| `--vote-title <title>` | 否 | 投票标题；提供时内联创建投票并关联主题（仅 talk，与 `--ask` 互斥） |
| `--vote-options <list>` | 否 | 投票选项，逗号分隔、至少 2 个（选项内不能含逗号）；须与 `--vote-title` 同时提供 |
| `--markdown` | 否 | 正文按 markdown 渲染 |
| `--markdown-file <path>` | 否 | 读取本地 .md 文件作为正文发布（按 markdown，非附件上传）；与 `--text` 互斥 |
| `--json` | 否 | 输出原始 JSON（含新建 topic_id） |

\* `--text`、`--files`、`--vote-title` 至少提供其一。

## 输出

成功后输出：

```
✓ Topic created
{
  "success": true,
  "topic": {
    "topic_id": "45544144118151518",
    "create_time": "2026-08-13T19:20:50.565+0800",
    "text": "示例主题正文内容",
    "title": "示例主题标题"
  }
}
```

主题状态（类型、`creation_statement`、关联投票等）以 `topic +detail` 的返回为准。

## 推荐工作流

把草稿整理成规范帖子再发布的内容运营流程：

**① 明确主题类型与目标**

确认主题类型（见上方 IMPORTANT）：`talk` 普通帖子（默认）/ 带投票的帖子（`--vote-title`）/ `q&a` 提问（`--ask`），并明确本篇目标（分享观点 / 通知 / 引导讨论 / 收集意见 / 向成员提问等）。同时确认目标星球：

```bash
zsxq-cli group +list
```

**② 准备正文（排版 / 标签 / 附件）**

按本文件 `## 参数` 支持的能力整理内容，不臆造参数：

- **排版**：标题、分段、换行都写进 `--text`（支持 `\n`）。常见要求——标题简洁、正文分段、结尾加一句引导互动的话；若用户要求“只排版，不改写”，则保留原文观点与立场、仅调整格式。
- **话题标签**：标签**内嵌在正文 content 里**，形如 `<e type="hashtag" .../>`（与 [topic-detail](topic-detail.md) 的说明一致）。给标签建议时先看星球现有标签体系、尽量对齐以免造重复标签：`zsxq-cli group +hashtags --group-id <id>`（见 [group-hashtags](group-hashtags.md)）。
- **图片 / 文件**：用 `--files`（逗号分隔）。@成员等富文本同样内嵌在正文中；能力边界一律以 `## 参数` 为准。

**③ 发布前把完整确认稿交用户确认（写入意图确认）**

把整理后的**完整确认稿**——标题、正文、标签、附件清单、目标星球——一并展示给用户，待其明确表示“确认发布”后再执行；默认不直接发帖。此步对应上方 `> [!CAUTION]`。

**④ 发布**

用户确认后调用本文件 `## 命令`：

```bash
zsxq-cli topic +create --group-id <id> --text "确认后的正文"
```

**⑤ 发布后校验（可选）**

用返回的 `topic_id` 拉详情，核对正文与标签是否按预期落地（标签的解析方式见 [topic-detail](topic-detail.md)）：

```bash
zsxq-cli topic +detail --topic-id <新建的 topic_id>
```

## 失败语义

写入失败即原子回滚 —— 不会留下空主题或半成品 topic_id。重试前请先确认参数是否合法。

## 错误说明

| 错误 | 原因 |
|------|------|
| `--ai 和 --ai-mode 不能同时使用` | 两个 AI 声明参数同传 |
| `--ai-mode 取值必须是 aigc、personal_perspective 或 none` | `--ai-mode` 值非法 |
| `投票仅支持普通主题（talk），不能与 --ask 问答主题同时使用` | 投票与提问同用 |
| `--vote-title 和 --vote-options 必须同时提供` | 投票只给了标题或只给了选项 |
| `投票至少需要 2 个选项` / `投票选项不能为空` | 选项不足 2 个或含空项 |
| `--anonymous 仅支持与 --ask 一起使用` | 没指定提问对象却要求匿名 |
| `问答主题不支持上传附件，请仅提供 --text` | 提问带了 `--files` |
| `问答主题必须提供 --text` | 提问没写内容 |
| `问答内容不能超过 1000 字符` | 提问内容超长 |
| `主题内容不能为空，请提供 --text、--files 或 --vote-title` | 内容、附件、投票全部为空 |
| `--text 和 --markdown-file 不能同时使用` | 两种正文来源同传 |
| `读取 markdown 文件失败: ...` | .md 文件读取失败 |
| `MCP tool error: {"code":80105,...}` | 向自己提问（`--ask` 传了自己的 user_id） |
| `MCP tool error: {"code":80106,...}` | 服务端拒绝创建提问（实测于配置提问费用的星球；CLI 无法传提问金额） |

通用错误（401、`--group-id is required`、星球无权限发帖等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-reply](topic-reply.md) — 对已发主题评论
- [group-list](group-list.md) — 获取 group_id
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
