# topic +scheduled（查看定时任务）

对应命令：`zsxq-cli topic +scheduled`。

列出星球内**待执行的定时任务**（定时发布主题与定时回答），并显示配额统计（每星球上限 10 个）。

## 命令

```bash
zsxq-cli topic +scheduled --group-id 123456789
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID |
| `--json` | 否 | 输出原始 JSON（不含配额统计） |

## 输出（表格模式）

```
JOB ID   SCHEDULED TIME                  TYPE    DIGEST
888      2026-08-20T10:00:00.000+0800    topic   定时发布的内容
889      2026-08-21T09:00:00.000+0800    answer  定时回答摘要

待执行定时任务：2 个（每星球上限 10）
```

## 说明

- `TYPE` 列：`topic` = 定时发布主题，`answer` = 定时回答（问答主题附带的定时回答任务）
- 已执行或已删除的任务不在列表内
- 配额统计来自独立接口，统计失败时仅不显示配额行，不影响任务列表
- 定时发布任务用 `topic +schedule --job-id` 修改；定时回答任务不支持经 `+schedule` 修改，需删除后重建（见 [topic-schedule](topic-schedule.md)）

## 错误说明

通用错误（401、`--group-id is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。本命令无特有错误。

## 参考

- [topic-schedule](topic-schedule.md) — 创建 / 修改定时发布任务
- [topic-unschedule](topic-unschedule.md) — 取消定时任务
- [topic-answer](topic-answer.md) — 定时回答（`topic +answer --scheduled-time`）
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
