# user +info（查看个人资料）

对应命令：CLI 通道 `zsxq-cli user +info`；MCP 通道见下方命令块。

获取当前登录账户的完整个人资料，包括 user_id、昵称、地区、认证状态、订阅信息等。

## 命令

**CLI 通道：**

```bash
# 查看个人资料（JSON 输出）
zsxq-cli user +info

# 使用 --json 标志（效果相同，+info 始终输出 JSON）
zsxq-cli user +info --json
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "GET", "path": "/v2/users/self"}
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--json` | 否 | 输出原始 JSON（+info 默认即 JSON 输出） |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--json` | 无对应字段 —— MCP 通道恒为 `{success, status_code, body}` 信封，无格式开关 |

## 输出字段说明

CLI 通道直接输出业务数据（`+info` 始终为 JSON）；MCP 通道恒为 `{success, status_code, body}` 信封，业务数据在 `body.resp_data`，`user_id` 位于 `body.resp_data.user.user_id`。

```json
{
  "user": {
    "user_id": "123456",
    "name": "示例用户",
    "unique_id": "demo_user",
    "location": "示例城市",
    "avatar_url": "https://..."
  },
  "identity_status": "authenticated",
  "subscribed_wechat": true,
  "accounts": {
    "wechat": {
      "name": "示例微信昵称"
    }
  }
}
```

字段含义：

- `user.user_id`：用户 ID，是 `get_user_footprints`、`get_user_groups` 等 API 的参数
- `user.unique_id`：唯一标识（类似用户名）
- `identity_status`：实名认证状态，`authenticated` 表示已实名
- `subscribed_wechat`：是否关注公众号
- `accounts`：第三方账户绑定信息

## 说明

- 常用于获取 `user_id` 给其他命令使用，或在切换账户后核对当前登录身份
- MCP 通道下凡是需要 `user_id` 的操作（`user +footprints`、`note +list` 等）先调本接口（`GET /v2/users/self`）取得，CLI 通道则由工具自己读本地 config，无需显式传

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 输出账户与预期不符 | 当前 keychain 中保存的是其他账户 | `zsxq-cli auth logout` 后重新登录 |

通用错误（401 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [auth-errors](auth-errors.md) — 认证与登录
- [group-list](group-list.md) — 查看星球列表
