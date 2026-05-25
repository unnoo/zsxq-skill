# topic +create（发布主题）

本 skill 对应 shortcut：`zsxq-cli topic +create`。

在指定星球内发布一条新主题（帖子）。

> [!IMPORTANT]
> 仅支持发布 `talk`（普通帖子）类型主题。`q&a`、`task`、`solution` 类型暂不支持通过 CLI 创建。

> [!CAUTION]
> 这是**公开写入操作** —— 发布后对星球成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 发布的内容

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

```bash
# 第一步：确认目标星球
zsxq-cli group +list

# 第二步：确认内容无误后执行
zsxq-cli topic +create --group-id <id> --text "内容"

# 第三步：验证发布结果
zsxq-cli topic +detail --topic-id <新建的 topic_id>
```

## 失败语义

写入失败即原子回滚 —— 不会留下空主题或半成品 topic_id。重试前请先确认参数是否合法。

## 错误说明

通用错误（401、`--group-id is required`、星球无权限发帖等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。本命令无特有错误。

## 参考

- [zsxq-topic-reply](zsxq-topic-reply.md) — 对已发主题评论
- [zsxq-group-list](../../zsxq-group/references/zsxq-group-list.md) — 获取 group_id
- [zsxq-shared](../../zsxq-shared/SKILL.md)
