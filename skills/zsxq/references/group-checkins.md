# group 打卡任务列表（通过 api raw）

查询指定星球的打卡任务，用于查看当前可用的打卡任务、筛选进行中或已结束的任务，以及在发布关联打卡的主题前获取 `checkin_id`（见 [topic-create](topic-create.md)）。CLI 未封装该能力，通过 `api raw` 调用原始 HTTP 接口获取。

对应操作：`GET /v2/groups/<group_id>/checkins`；MCP 调用见下方命令块。

## 命令

<!-- cli-only:start -->

**CLI 通道：**

```bash
# 查询星球全部打卡任务
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/checkins \
  --query '{"scope":"all","count":100}'

# 只查询进行中的打卡任务
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/checkins \
  --query '{"scope":"ongoing","count":100}'

# 按创建时间向前翻页
zsxq-cli api raw --method GET --path /v2/groups/<group_id>/checkins \
  --query '{"scope":"all","end_time":"2026-01-01T00:00:00.000+0800","count":100}'
```

<!-- cli-only:end -->

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/groups/123456789/checkins", "query": {"scope": "all", "count": 100}}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<group_id>` | **是** | 星球 ID（拼接到 URL 路径中，从 `group +list` 获取） |
| `scope` | 否 | 打卡任务范围：`all`（全部，默认）、`ongoing`（进行中）、`over`（已结束）、`closed`（已关闭） |
| `end_time` | 否 | 按 `checkin.create_time` 限定查询上界；缺省为服务端处理请求的时刻。翻页时填入上一页最后一条任务的 `create_time` |
| `count` | **是** | 返回数量，范围 `[1,100]`；查询全部任务时用 `100` |

### 通道映射

| CLI 形式 | HTTP 字段 |
|----------|-----------|
| `<group_id>`（路径） | path `/v2/groups/{group_id}/checkins` |
| `query` JSON | 同名 query 参数（`scope` / `end_time` / `count`） |

## 输出

返回完整响应封套，打卡任务列表位于 `body.resp_data.checkins[]`：

```json
{
  "body": {
    "resp_data": {
      "checkins": [
        {
          "checkin_id": "1148218242",
          "title": "2026运动打卡",
          "status": "ongoing",
          "create_time": "2026-01-04T15:38:06.040+0800",
          "validity": { "expiration_time": "2026-12-27T23:59:59.000+0800", "long_period": false },
          "statistics": { "completed_count": 2, "joined_count": 48, "today_checkined_count": 0 }
        }
      ]
    },
    "succeeded": true
  },
  "status_code": 200,
  "success": true
}
```

`checkins[]` 每项的关键字段（其余字段如 `owner`、`group`、`joined_users` 等与任务定位无关，按需读取）：

| 字段 | 说明 |
|------|------|
| `checkin_id` | 打卡任务 ID；发布关联打卡主题时作为发帖的打卡任务 ID 传入（MCP 通道为发帖 `req_data.checkin_id`，数字） |
| `title` | 打卡任务名称，用于与用户确认目标任务（**不是 `name`**，该字段恒为 null） |
| `status` | 任务状态：`ongoing`（进行中）/ `over`（已结束）/ `closed`（已关闭），与 `scope` 筛选项对应 |
| `create_time` | 任务创建时间，翻页时作为下一次请求的 `end_time` |
| `validity.expiration_time` | 任务截止时间 |
| `statistics.joined_count` / `completed_count` / `today_checkined_count` | 参与人数 / 完成人数 / 今日打卡人数 |

MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`（结构与上方一致）。

## 说明

- 这是查询打卡任务的专用接口。需要列出星球有哪些打卡任务时，优先调用本接口，不要通过 `group +topics` 的普通主题分页结果反推。
- 用户要发布关联打卡的主题时，先用本接口按 `scope` 查询，按 `title` 或 `status` 筛选并核对 `checkin_id`，再执行 [topic-create](topic-create.md)；不要把 `topic_id` 当作 `checkin_id`。命中多个同名任务时，列出候选（`checkin_id` + `title` + `status`）让用户确认，不要默认取第一个。
- 翻页：响应不含显式游标。当返回数量达到 `count` 时，取本页最后一条的 `create_time` 填入下一次请求的 `end_time`，直到返回不足 `count` 或为空；按 `checkin_id` 去重。
- 如果 `scope=ongoing` 为空，不代表星球没有历史打卡任务；查看全部任务改用 `scope=all`。
- 已结束（`over`）或已关闭（`closed`）的任务能否继续关联发帖未经实测；发布打卡主题默认选择 `ongoing` 任务。

## 错误说明

本接口无特有错误。通用错误（401、403 无权限、404 星球不存在、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-create](topic-create.md) — 发布关联打卡任务的主题
- [group-topics](group-topics.md) — 浏览普通主题流（不用于查询打卡任务清单）
- [group-list](group-list.md) — 获取 `group_id`
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
