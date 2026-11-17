# group 官方运营大盘

读取星主或管理员可访问的官方运营指标，包括昨日、近 30 日日均和今日累计；用于运营数据日报，不用主题扫描冒充官方指标。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 先取当前用户和星球角色字段
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/users/self","fields":"user.user_id"}'
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/groups/123456789","fields":"group.group_id,group.name,group.owner.user_id,group.admin_ids,group.partner_ids"}'

# 星主或管理员读取活跃指标；管理员不请求 income_count
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/dashboard/groups/123456789/overview","fields":"daily.member_active_count,daily.member_increase_count,statistics.yesterday.member_active_count,statistics.within_30days_average.member_active_count"}'
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/dashboard/groups/123456789/overview", "fields": "daily.member_active_count,daily.member_increase_count,statistics.yesterday.member_active_count,statistics.within_30days_average.member_active_count"}
```

身份核对使用 `GET /v2/users/self` 和 `GET /v2/groups/{group_id}`，字段与 CLI 示例相同。本接口不传 `shape`，只按所需指标传 `fields`。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `group_id` | **是** | 目标星球 ID；调用前确认当前用户是其星主或管理员 |
| `fields` | **是** | 相对 `resp_data` 的逗号分隔字段路径；只请求报告所需叶子字段 |
| `shape` | 不使用 | 大盘没有命名 shape；不要自行添加 |

### 通道映射

| CLI 形式 | HTTP / 工具字段 |
|----------|-----------------|
| `path` | `/v2/dashboard/groups/{group_id}/overview` |
| `fields` | `call_zsxq_api` 顶层字段投影，不放入 query |

可请求的报告项：

| 报告项 | `statistics.yesterday` / `statistics.within_30days_average` 下的字段 |
|--------|---------------------------------------------------------------------|
| 加入人数 | `member_increase_count` |
| 续期人数 | `member_renew_count` |
| 活跃用户数 | `member_active_count` |
| 评论数 | `member_comment_count` |
| 阅读量 | `member_read_count` |
| 点赞数 | `member_like_count` |
| 作业主题数 | `member_task_count` |
| 打卡主题数 | `member_checkin_count` |
| 收入，仅星主按需读取 | `income_count` |

`daily` 只请求 `member_active_count`、`member_increase_count`。完整昨日/日均报告按需把上表字段分别展开为 `statistics.yesterday.<字段>` 和 `statistics.within_30days_average.<字段>`；只有确认当前用户是星主且用户需要收入时，才添加两个 `income_count` 路径。

## 输出

`resp_data.daily` 与 `resp_data.statistics` 同级；`statistics.yesterday` 与 `statistics.within_30days_average` 中的指标同名。HTTP 200 仍须检查 `body.succeeded`，失败信封不能当作指标数据。

## 说明

- 身份只依据接口或可信宿主数据：`owner.user_id` 是星主，`admin_ids` 是管理员；合伙人不算大盘管理员。字段缺失时身份未知，不开放收入读取。
- 昨日按东八区自然日；近 30 日是**日均**而非累计。`daily` 是今日截至当前的累计，不与完整昨日或日均直接计算涨跌；今日重置时刻未复验时须披露。
- 缺省、`null`、空对象不是 0。活跃用户与发帖作者人数口径不同，不相加或替换。
- 收入原值单位为分，展示元时除以 100；包括加入、续期、礼品卡、付费提问和赞赏，不含退款。非零量级仍需按环境复验，不作财务对账结论。
- 大盘不可用时说明原因，不用主题扫描估算官方指标。另做内容盘点时使用相同星球和时间窗，分别标明“官方指标”和“主题观察”。

## 错误说明

| 错误码 / 症状 | 处理 |
|---------------|------|
| `17208` | 星球不存在或不是付费星球；说明大盘不可用，不把空载荷写成全零 |
| `1030` | 无权读取；停止并说明原因，不换路径或参数重试 |
| HTTP 200 但 `succeeded=false` | 按业务失败处理，不读取空 `resp_data` 作为指标 |

通用错误（401、403、404、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-list](group-list.md) — 定位目标星球
- [user-info](user-info.md) — 获取当前用户 ID
- [compose-operations-report](scenarios/compose-operations-report.md) — 组合官方指标与内容盘点
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
