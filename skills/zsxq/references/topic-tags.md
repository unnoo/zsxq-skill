# 设置主题标签（api call set_topic_tags）

通过 `zsxq-cli api call set_topic_tags` 为某主题设置标签（hashtag），返回更新后的主题简要信息。

对应命令：CLI 通道 `zsxq-cli api call set_topic_tags`；MCP 通道见下方命令块。

> [!CAUTION]
> 这是**写入操作** —— 会改变主题的标签。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 完整的标签列表（`titles`）—— 见下方 IMPORTANT

> [!IMPORTANT]
> `titles` 是本次要设置的**完整标签集合**，不是「追加一个标签」。为避免误删原有标签，先用 `topic +detail` 查看该主题当前标签，把需要保留的一并放进 `titles` 再提交。

## 命令

**CLI 通道：**

```bash
# 为主题设置标签（数组形式，可多个）
zsxq-cli api call set_topic_tags --params '{"topic_id":"123","titles":["标签1","标签2"]}'
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "PUT", "path": "/v2/topics/111222333444", "body": {"req_data": {"annotation": "<e type=\"hashtag\" hid=\"0\" title=\"%23%E6%8A%95%E8%B5%84%23\" /><e type=\"hashtag\" hid=\"0\" title=\"%23AI%23\" />"}}}
```

MCP 通道没有 `titles` 数组，需自行把标签构造为 `annotation`：

1. 每个标签**去首尾空白**
2. **补 `#` 前后缀**（`投资` → `#投资#`）
3. 做 **URL 编码**（`#投资#` → `%23%E6%8A%95%E8%B5%84%23`）
4. 套入 `<e type="hashtag" hid="0" title="编码值" />`
5. 全部**串联**为一个字符串（上例即 `["投资","AI"]`）

`titles` 的「完整标签集合、全量替换」语义在 MCP 通道同样适用 —— `annotation` 里没出现的标签会被移除。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `topic_id` | **是** | 主题 ID（字符串，从 `topic +search` / `group +topics` 获取） |
| `titles` | **是** | 标签标题的**字符串数组**（如 `["产品","增长"]`）；无需带 `#`，为本次设置的完整标签集合 |

### 通道映射

| CLI 形式 | HTTP 字段 |
|----------|-----------|
| `topic_id` | path `/v2/topics/{topic_id}` |
| `titles`（数组） | `body.req_data.annotation`（按上方规则构造的字符串，非数组） |

## 输出

成功后返回更新后的主题简要信息（含新的标签）；具体字段以 `api call` 实际输出为准。MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`。

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：查看现有标签用 CLI `topic +detail` / MCP `GET /v2/topics/{topic_id}/info`；设置标签用上方对应通道的命令（MCP 通道需先按规则构造 `annotation`）。

```bash
# 第一步：查看主题现有标签，避免覆盖时误删
zsxq-cli topic +detail --topic-id 123

# 第二步：与用户确认「最终完整标签集合」后执行
zsxq-cli api call set_topic_tags --params '{"topic_id":"123","titles":["产品","增长"]}'
```

> 查看星球已有哪些标签可用 `group +hashtags`（见 [group-hashtags](group-hashtags.md)）。

## 失败语义

设置失败即不改变原标签，不会产生半更新状态。

## 错误说明

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 无权限 / `code` 类权限错误 | 当前账户无权修改该主题标签（非作者/星主） | 用有权限的账户操作 |

通用错误（401、`topic_id` / `titles` 缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-detail](topic-detail.md) — 操作前查看主题当前标签
- [group-hashtags](group-hashtags.md) — 查看星球已有标签
- [topic-digest](topic-digest.md) — 设置/取消精华（同为写入类 api call）
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
