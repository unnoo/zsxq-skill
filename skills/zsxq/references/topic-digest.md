# 设置/取消精华（api call set_topic_digested）

通过 `zsxq-cli api call set_topic_digested` 将某主题设为精华，或取消其精华状态。这是**管理权限（星主/管理员/合伙人）**的操作。

对应命令：CLI 通道 `zsxq-cli api call set_topic_digested`；MCP 通道见下方命令块。

> [!NOTE]
> 日常加精 / 取消精华优先用封装命令 `topic +set --digested`（见 [topic-set](topic-set.md)），它同时支持置顶（`--sticky`）。本文件记录底层接口工具 `set_topic_digested` 的原始用法。

> [!CAUTION]
> 这是**写入操作** —— 会改变主题在星球内的展示（精华会进入精华列表）。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 是**设为精华**（`digested: true`）还是**取消精华**（`digested: false`）

> [!IMPORTANT]
> 需要**管理权限**：星主、管理员或合伙人均可加精（经 admin+partner 账户实测确认，非仅星主）。无管理权限的普通成员调用会返回无权限错误。

## 命令

**CLI 通道：**

```bash
# 设为精华
zsxq-cli api call set_topic_digested --params '{"topic_id":"123","digested":true}'

# 取消精华
zsxq-cli api call set_topic_digested --params '{"topic_id":"123","digested":false}'
```

**MCP 通道（`call_zsxq_api`）：**

取消精华：

```json
{"method": "PUT", "path": "/v2/topics/111222333444", "body": {"req_data": {"digested": false}}}
```

设为精华把 `digested` 改为 `true` 即可 —— 与封装命令 [topic-set](topic-set.md) 的 `PUT /v2/topics/{topic_id}` 是**同一端点**，两个通道的权限要求也一致。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `topic_id` | **是** | 主题 ID（字符串，从 `topic +search` / `group +topics` 获取） |
| `digested` | **是** | 布尔值：`true` 设为精华，`false` 取消精华 |

### 通道映射

| CLI 形式 | HTTP 字段 |
|----------|-----------|
| `topic_id` | path `/v2/topics/{topic_id}` |
| `digested` | `body.req_data.digested` |

## 输出

成功后返回更新后的主题精华状态；具体字段以 `api call` 实际输出为准（可加 `--params` 外的默认 json 输出查看）。MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：确认主题用 CLI `topic +detail` / MCP `GET /v2/topics/{topic_id}/info`；设为 / 取消精华用上方对应通道的命令。

```bash
# 第一步：确认目标主题内容，确保操作对象正确
zsxq-cli topic +detail --topic-id 123

# 第二步：向用户确认「设为精华 / 取消精华」后执行
zsxq-cli api call set_topic_digested --params '{"topic_id":"123","digested":true}'
```

## 失败语义

设置为幂等操作，失败即不改变原精华状态，不会产生中间态。

## 错误说明

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 无权限 / `code` 类权限错误 | 当前账户无管理权限（非星主/管理员/合伙人） | 用有管理权限的账户操作，或确认账户角色 |

通用错误（401、`topic_id` 缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-set](topic-set.md) — 封装命令 `topic +set`（精华 + 置顶，日常优先用）
- [topic-detail](topic-detail.md) — 操作前确认主题内容
- [topic-tags](topic-tags.md) — 为主题设置标签（同为星主/作者写入类 api call）
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
