# topic +create（发布主题）

对应命令：`zsxq-cli topic +create`。

在指定星球内发布一条新主题（帖子）。

> [!IMPORTANT]
> 仅支持发布 `talk`（普通帖子）类型主题。`q&a`、`task`、`solution` 类型暂不支持通过 CLI 创建。

> [!CAUTION]
> 这是**公开写入操作** —— 发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 发布的内容
> 3. 若对草稿做了排版或改写：把**完整确认稿**（标题、正文、标签、附件清单）交用户核对，待其明确表示“确认发布”后再执行

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
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID（从 `group +list` 获取） |
| `--text <text>` | **是** | 主题正文内容，支持 `\n` 换行 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔（图片/文件） |
| `--json` | 否 | 输出原始 JSON（含新建 topic_id） |

## 输出

成功后输出：

```
✓ Topic created
{
  "topic_id": "111222333455",
  "title": "示例主题标题",
  "create_time": "2026-04-01T15:44:23.555+0800"
}
```

## 推荐工作流

把草稿整理成规范帖子再发布的内容运营流程：

**① 明确主题类型与目标**

确认要发的是 `talk` 普通帖子（本命令仅支持 talk，见上方 IMPORTANT），并明确本篇目标（分享观点 / 通知 / 引导讨论等）。同时确认目标星球：

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

通用错误（401、`--group-id is required`、星球无权限发帖等）见 [auth-errors](auth-errors.md#常见错误处理)。本命令无特有错误。

## 参考

- [topic-reply](topic-reply.md) — 对已发主题评论
- [group-list](group-list.md) — 获取 group_id
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
