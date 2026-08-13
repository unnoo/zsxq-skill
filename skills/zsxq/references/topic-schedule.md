# topic +schedule（定时发布主题）

对应命令：`zsxq-cli topic +schedule`。

创建或修改一条**定时发布任务**，让主题在未来指定时间自动发布到星球。带 `--job-id` 时为修改已有任务（未提供的字段保持原值），不带则创建新任务。

> [!CAUTION]
> 这是**写入操作** —— 任务到点会自动发布，内容对星球成员公开，且**发布时无需再次确认**。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 要发布的完整内容（修改任务时：要改动的字段）
> 3. 定时发布时间

> [!IMPORTANT]
> - 定时任务**每星球上限 10 个**（用 `topic +scheduled` 查看待执行数量）
> - 定时时间必须**晚于当前时间**且在**未来 14 天以内**（服务端窗口），时区为中国标准时间（+0800）
> - 定时发布仅支持 `talk` 普通主题；定时**回答**用 `topic +answer --scheduled-time`（见 [topic-answer](topic-answer.md)）

## 命令

```bash
# 创建定时发布任务
zsxq-cli topic +schedule \
  --group-id 123456789 \
  --text "定时发布的内容" \
  --scheduled-time "2026-08-20 10:00"

# 带附件
zsxq-cli topic +schedule \
  --group-id 123456789 \
  --text "内容" \
  --files photo.jpg \
  --scheduled-time "2026-08-20T10:00:00"

# 修改已有任务（只改发布时间）
zsxq-cli topic +schedule \
  --group-id 123456789 \
  --job-id 888 \
  --scheduled-time "2026-08-21 09:00"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID |
| `--job-id <id>` | 否 | 定时任务 ID（从 `topic +scheduled` 获取）；提供时为修改模式 |
| `--text <text>` | 创建时**是** | 正文内容；修改模式省略则保留原内容 |
| `--files <paths>` | 否 | 附件路径，多个用逗号分隔；修改模式省略则保留原附件 |
| `--scheduled-time <time>` | 创建时**是** | 发布时间，如 `"2026-08-20 10:00"` 或 `"2026-08-20T10:00:00"` |
| `--json` | 否 | 输出原始 JSON |

## 输出

成功后输出 `✓ Scheduled job saved` 及服务端返回的 JSON（`resp_data` 为空，**不含 job_id** —— 用 `topic +scheduled` 查看新任务的 job_id）；`--json` 模式仅输出 JSON。

## 推荐工作流

```bash
# 第一步：查看现有定时任务与配额
zsxq-cli topic +scheduled --group-id 123456789

# 第二步：把完整确认稿（内容 + 发布时间）交用户核对后执行
zsxq-cli topic +schedule \
  --group-id 123456789 \
  --text "确认后的内容" \
  --scheduled-time "2026-08-20 10:00"

# 第三步：验证任务已入队
zsxq-cli topic +scheduled --group-id 123456789
```

## 失败语义

参数校验（内容 / 时间格式 / 14 天窗口）与附件上传失败不会创建任务；创建或修改失败不改变已有任务列表。

## 错误说明

| 错误 | 原因 |
|------|------|
| `请至少提供 --text 或 --files` | 创建模式没给内容 |
| `请提供 --scheduled-time（定时发布时间）` | 创建模式没给发布时间 |
| `修改时请至少提供 --scheduled-time、--text 或 --files 之一` | 修改模式三个都没给 |
| `无法解析时间 "..."，请使用 "2026-08-14 10:00" 或 "2026-08-14T10:00:00" 格式` | 时间格式不对 |
| `定时时间必须晚于当前时间（当前: ...）` | 时间已过（服务端会立即发布，CLI 拦截） |
| `定时时间必须在未来 14 天以内` | 超过服务端允许的 14 天窗口 |
| `未找到 job_id=... 的定时任务（可能已执行或不存在）` | 修改模式的任务 ID 不存在或已执行 |
| `定时回答任务暂不支持通过 +schedule 修改，请删除后重新创建（topic +answer --scheduled-time）` | 用 +schedule 修改了定时回答任务 |
| `API 错误(<code>): <msg>` | 服务端拒绝（如配额已满） |

通用错误（401、`--group-id is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-scheduled](topic-scheduled.md) — 查看待执行定时任务与配额
- [topic-unschedule](topic-unschedule.md) — 取消定时任务
- [topic-answer](topic-answer.md) — 定时回答（`topic +answer --scheduled-time`）
- [topic-create](topic-create.md) — 立即发布主题
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
