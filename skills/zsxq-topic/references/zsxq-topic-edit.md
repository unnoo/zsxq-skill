# topic +edit（编辑主题）

本 skill 对应 shortcut：`zsxq-cli topic +edit`。

编辑自己发布的主题内容或附件。未修改的字段自动保留。

> [!CAUTION]
> 这是**公开写入操作** —— 编辑后内容立即更新，对星球成员可见。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其当前内容
> 2. 修改后的内容

> [!IMPORTANT]
> 只能编辑自己发布的主题，无法编辑他人的主题。

## 命令

```bash
# 修改正文
zsxq-cli topic +edit \
  --topic-id 111222333444 \
  --text "新的正文内容"

# 替换附件
zsxq-cli topic +edit \
  --topic-id 111222333444 \
  --files new-photo.jpg,new-doc.pdf

# 清除所有附件
zsxq-cli topic +edit \
  --topic-id 111222333444 \
  --clear-files

# 同时修改正文和附件
zsxq-cli topic +edit \
  --topic-id 111222333444 \
  --text "新的正文内容" \
  --files new-photo.jpg
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--text <text>` | 否 | 新正文（不传则保留原内容） |
| `--files <paths>` | 否 | 新附件，多个用逗号分隔（替换原有附件） |
| `--clear-files` | 否 | 清除所有附件 |
| `--json` | 否 | 输出原始 JSON |

## 推荐工作流

```bash
# 第一步：确认当前主题内容
zsxq-cli topic +detail --topic-id 111222333444

# 第二步：确认无误后执行编辑
zsxq-cli topic +edit \
  --topic-id 111222333444 \
  --text "新的正文内容"

# 第三步：验证编辑结果
zsxq-cli topic +detail --topic-id 111222333444
```

## 失败语义

编辑失败即原子回滚 —— 原内容保留不变，不会出现"改一半"的状态。重试前请先确认参数是否合法。

## 错误说明

通用错误（401、`--topic-id is required`、主题不存在、403 无权限编辑他人主题等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-topic-detail](zsxq-topic-detail.md) — 编辑前确认主题内容
- [zsxq-topic-create](zsxq-topic-create.md) — 发布新主题
- [zsxq-topic-delete](zsxq-topic-delete.md) — 删除主题
- [zsxq-shared](../../zsxq-shared/SKILL.md)
