# topic +unschedule（取消定时任务）

对应命令：CLI 通道 `zsxq-cli topic +unschedule`；MCP 通道见下方命令块。

删除一条待执行的定时任务（定时发布主题或定时回答），删除后到点**不会**发布。

> [!CAUTION]
> 这是**删除操作** —— 任务删除后其内容不会发布，且不可恢复。执行前必须向用户确认：
> 1. 目标星球（group_id）
> 2. 要删除的任务（job_id）及其对应内容 / 发布时间（先 `topic +scheduled` 核对）

> [!IMPORTANT]
> 仅能删除**自己创建**的定时任务。

## 命令

**CLI 通道：**

```bash
zsxq-cli topic +unschedule --group-id 123456789 --job-id 888
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "DELETE", "path": "/v2/groups/123456789/scheduled_jobs/777888999"}
```

`--group-id` 与 `--job-id` 都拼进 path；DELETE 请求无 body。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID |
| `--job-id <id>` | **是** | 要删除的定时任务 ID（从 `topic +scheduled` 获取） |
| `--json` | 否 | 输出原始 JSON |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/scheduled_jobs/{job_id}` |
| `--job-id` | path `/v2/groups/{group_id}/scheduled_jobs/{job_id}` |

## 输出

成功后输出 `✓ Scheduled job deleted`；`--json` 模式仅输出服务端返回的 JSON。MCP 通道恒为 `{success, status_code, body}` 信封（DELETE 无业务 body）。

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：核对任务用 CLI `topic +scheduled` / MCP `GET /v2/groups/{group_id}/scheduled_jobs`；删除用上方对应通道的命令。

```bash
# 第一步：列出待执行任务，核对要删的 job_id 与内容
zsxq-cli topic +scheduled --group-id 123456789

# 第二步：向用户确认后删除
zsxq-cli topic +unschedule --group-id 123456789 --job-id 888

# 第三步：确认已从列表消失
zsxq-cli topic +scheduled --group-id 123456789
```

## 失败语义

删除失败任务仍在列表中，到点仍会执行；确认参数后可重试。

## 错误说明

| 错误 | 原因 |
|------|------|
| `API 错误(52201): 未找到待发布的定时任务` | job_id 不存在或已执行/已删除 |
| `API 错误(<code>): <msg>` | 服务端拒绝（非本人创建的任务等） |

通用错误（401、`--group-id is required`、`--job-id is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-scheduled](topic-scheduled.md) — 查看待执行任务
- [topic-schedule](topic-schedule.md) — 创建 / 修改定时发布任务
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
