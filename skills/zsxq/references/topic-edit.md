# topic +edit（编辑主题）

对应命令：`zsxq-cli topic +edit`。

编辑自己发布的主题内容或附件。未修改的字段自动保留。

> [!CAUTION]
> 这是**公开写入操作** —— 编辑后内容立即更新，对星球成员可见。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其当前内容
> 2. 修改后的内容
> 3. 若修改 AI 声明（`--ai` / `--ai-mode`）或关联投票（`--vote-id`）：改动后的状态

> [!IMPORTANT]
> - 只能编辑自己发布的主题，无法编辑他人的主题
> - 问答（`q&a`）主题不支持编辑，需修改请删除后重新发布（`topic +create --ask`）
> - **AI 声明一经设置不可修改**（实测）：对已有声明（aigc / personal_perspective）的主题，`--ai` / `--ai-mode` 修改会被服务端静默忽略 —— 命令返回成功但声明保持原值。仅在主题**尚无** AI 声明时可首次设置

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

# 声明为 AI 生成（等同 --ai-mode aigc）
zsxq-cli topic +edit --topic-id 111222333444 --ai

# 修改 AI 声明模式
zsxq-cli topic +edit --topic-id 111222333444 --ai-mode none

# 更换关联投票
zsxq-cli topic +edit --topic-id 111222333444 --vote-id 7483647214
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--text <text>` | 否 | 新正文（不传则保留原内容） |
| `--files <paths>` | 否 | 新附件，多个用逗号分隔（替换原有附件） |
| `--clear-files` | 否 | 清除所有附件（与 `--files` 互斥） |
| `--ai` | 否 | 将 AI 声明设为 aigc（与 `--ai-mode` 互斥；仅对尚无 AI 声明的主题生效） |
| `--ai-mode <mode>` | 否 | 将 AI 声明设为 `aigc` / `personal_perspective` / `none`；不传则保留原声明（仅对尚无 AI 声明的主题生效） |
| `--vote-id <id>` | 否 | 更换主题关联的投票（vote uid，仅 talk）；不传则保留原投票 |
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

| 错误 | 原因 |
|------|------|
| `问答主题不支持编辑，如需修改请重新发布（topic +create --ask）` | 编辑了 `q&a` 主题 |
| `--clear-files 和 --files 不能同时使用` | 两个附件参数同传 |
| `请提供 --text、--files、--clear-files、--ai/--ai-mode 或 --vote-id` | 没有提供任何修改项 |
| `--ai 和 --ai-mode 不能同时使用` | 两个 AI 声明参数同传 |
| `--ai-mode 取值必须是 aigc、personal_perspective 或 none` | `--ai-mode` 值非法 |

通用错误（401、`--topic-id is required`、主题不存在、403 无权限编辑他人主题等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 编辑前确认主题内容
- [topic-create](topic-create.md) — 发布新主题
- [topic-delete](topic-delete.md) — 删除主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
