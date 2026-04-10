# topic +create（发布主题）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

本 skill 对应 shortcut：`zsxq-cli topic +create`。

在指定星球内发布一条新主题（帖子）。

> [!CAUTION]
> 这是**公开写入操作** —— 发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 标题和内容

## 命令

```bash
# 发布一条主题
zsxq-cli topic +create \
  --group-id 123456789 \
  --title "示例主题标题" \
  --content "示例主题正文内容"

# 多行内容（使用 \n 换行）
zsxq-cli topic +create \
  --group-id 123456789 \
  --title "示例主题标题" \
  --content "第一段内容\n第二段内容"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID（从 `group +list` 获取） |
| `--title <text>` | **是** | 主题标题 |
| `--content <text>` | **是** | 主题正文内容，支持换行符 `\n` |
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

```bash
# 第一步：确认目标星球
zsxq-cli group +list

# 第二步：（可选）确认内容无误后执行
zsxq-cli topic +create --group-id <id> --title "标题" --content "内容"

# 第三步：验证发布结果
zsxq-cli topic +detail --topic-id <新建的 topic_id>
```

## 参考

- [zsxq-topic-reply](zsxq-topic-reply.md) — 对已发主题评论
- [zsxq-group-list](../../zsxq-group/references/zsxq-group-list.md) — 获取 group_id
- [zsxq-shared](../../zsxq-shared/SKILL.md)
