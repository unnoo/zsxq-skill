# group 成员列表（通过 api raw）

列出指定星球的成员，支持按到期时间、加入时间等排序与筛选。CLI 未封装此工具，通过 `zsxq-cli api raw --method GET --path /v2/groups/<group_id>/members` 调用；查询条件用 `--query`（JSON 对象）传入。

## 命令

```bash
# 列出星球成员（默认所有成员，按加入时间倒序，取 20 条）
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/members --query '{"count":20}'

# 即将到期：普通成员按到期时间正序（最先到期在前），限定未来 14 天窗口
zsxq-cli api raw --method GET --path /v2/groups/888888888/members \
  --query '{"scope":"regular","sort":"expired_time","order":"asc","begin_time":"2026-07-28T00:00:00.000+0800","end_time":"2026-08-11T23:59:59.999+0800","count":200}'

# 已过期成员：按编号翻页
zsxq-cli api raw --method GET --path /v2/groups/888888888/members \
  --query '{"scope":"expired","sort":"number","count":200}'
```

## 参数

`--query` 内的 JSON 字段：

| 参数 | 必填 | 说明 |
|------|------|------|
| `scope` | 否 | 成员范围。`all`（默认）/ `privileged`（星主、合伙人、管理员、嘉宾）/ `privileged_and_volunteer`（特权成员和志愿者）/ `expired`（已过期）/ `trial`（免费体验）/ `regular`（普通成员，不含特权与体验） |
| `sort` | 否 | 排序字段。`join_time`（默认，按加入时间）/ `expired_time`（按到期时间，**仅当 `scope` 为 `regular` 或 `expired` 时有效**，否则返回空数组）/ `update_time`（按变更时间）/ `number`（按成员编号，**仅当 `scope` 为 `expired` 时有效**，否则返回空数组）。`login_time` 已废弃 |
| `order` | 否 | 排序顺序。`asc`（正序）/ `desc`（默认，倒序）。筛选数据的方向与排序顺序一致 |
| `begin_time` | 否 | 限定 `sort` 所指时间字段的下界，默认 `1970-01-01T00:00:00.000+0800` |
| `end_time` | 否 | 限定 `sort` 所指时间字段的上界，默认服务器处理请求的时刻 |
| `filter` | 否 | 按 `member.status` 过滤，默认 `joined,exited`（全部）。可取 `joined`（已加入）/ `exited`（已退出）或其组合 |
| `count` | **是** | 返回数量，取值范围 `[1,200]` |
| `page_tag` | 否 | 分页标记，**仅当 `sort` 为 `number` 时有效**；不传表示第一页 |

`<group_id>` 拼接在 URL 路径中，从 [group-list](group-list.md) 获取。

## 输出

`api raw` 返回 JSON 信封，成员在 `body.resp_data.members[]`（按 `sort` 字段和 `order` 顺序排列）：

```json
{
  "body": {
    "resp_data": {
      "members": [
        {
          "group_id": 888888888,
          "user_id": 999999999,
          "name": "测试成员",
          "join_time": "2025-01-01T00:00:00.000+0800",
          "expired_time": "2026-01-01T00:00:00.000+0800",
          "update_time": "2025-06-01T00:00:00.000+0800",
          "login_time": "2025-12-01T00:00:00.000+0800",
          "status": "joined",
          "location": "北京",
          "isolated": false
        }
      ]
    },
    "succeeded": true
  },
  "status_code": 200,
  "success": true
}
```

成员对象常见字段：

| 字段 | 说明 |
|------|------|
| `user_id` | 用户 ID |
| `name` | 昵称 |
| `number` | 成员编号（可选，仅当星球启用「成员编号」且已分配时提供） |
| `alias` | 别名 / 星球名片（可选） |
| `join_time` | 最近一次加入星球的时刻（付费星球为最近一次付费加入的时刻） |
| `expired_time` | 服务到期时刻（可选，见下方「说明」的可见性条件） |
| `update_time` | 变更时刻 |
| `login_time` | 最近一次登录时刻（可用作活跃度信号） |
| `status` | `joined`（已加入）/ `exited`（已退出） |
| `location` | IP 属地 |
| `isolated` | 是否被拉黑 |
| `description` | 成员描述（可选） |
| `user_specific.remark` | 当前请求者为该成员设置的备注（可选） |

## 说明

- **`expired_time` 的可见性**：仅当请求发起者是该付费星球的**星主或管理员**，或查询的是**付费星球中自己的信息**时才返回。免费星球、以及以普通成员身份查询他人时，`expired_time` 不返回（字段缺失或为 `null`）。查「即将到期」必须以星主/管理员身份操作。
- **查即将到期成员**：用 `scope=regular` + `sort=expired_time` + `order=asc`（最先到期在前），配合 `begin_time`（设为当前时刻）和 `end_time`（设为窗口末端，如 14 天后）圈定时间窗；或直接用 `scope=expired` 拉取已过期成员。
- **排序字段的适用范围**：`sort=expired_time` 只在 `scope=regular` 或 `scope=expired` 下有效，`sort=number` 只在 `scope=expired` 下有效，其他组合会返回空数组（已实测验证：`scope=all` + `sort=expired_time` 返回空）。
- **翻页**：响应体不含 `has_more` / 游标字段，需自行判断。
  - 时间排序（`join_time` / `expired_time` / `update_time`）：当返回条数等于 `count` 时可能还有更多，用最后一条的对应时间推进游标继续拉——`order=asc` 时把 `begin_time` 设为该时间，`order=desc` 时把 `end_time` 设为该时间，直到返回不足 `count` 或为空。
  - `sort=number`（仅 `scope=expired`）：用上一页返回中最后一条的 `number` 作为下一次的 `page_tag`。
- `number` 仅当星球启用「成员编号」并已分配时才有；未启用的星球该字段缺失（实测多数星球不返回）。
- 定位**单个**成员用关键词搜索更直接：`zsxq-cli api call search_group_members --params '{"group_id":<id>,"keyword":"昵称","limit":10}'`；本接口用于**成批**拉取成员列表。

## 错误说明

| 错误 | 原因 |
|------|------|
| `expired_time` 字段缺失 | 非该付费星球星主/管理员，或星球为免费星球——无权查看到期时间 |
| `members` 为空数组 | 该 `scope` 下无成员，或 `sort` 与 `scope` 组合非法（如 `scope=all` 配 `sort=expired_time`） |

通用错误（401、403、404、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-list](group-list.md) — 获取 group_id
- [group-topics](group-topics.md) — 浏览星球主题
- [scenarios/care-expiring-members](scenarios/care-expiring-members.md) — 到期成员续费关怀场景
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
