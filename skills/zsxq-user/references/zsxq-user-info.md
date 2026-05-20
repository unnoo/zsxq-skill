# user +info（查看个人资料）

本 skill 对应 shortcut：`zsxq-cli user +info`。

获取当前登录账户的完整个人资料，包括 user_id、昵称、地区、认证状态、订阅信息等。

## 命令

```bash
# 查看个人资料（JSON 输出）
zsxq-cli user +info

# 使用 --json 标志（效果相同，+info 始终输出 JSON）
zsxq-cli user +info --json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--json` | 否 | 输出原始 JSON（+info 默认即 JSON 输出） |

## 输出字段说明

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

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 输出账户与预期不符 | 当前 keychain 中保存的是其他账户 | `zsxq-cli auth logout` 后重新登录 |

通用错误（401 等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-shared](../../zsxq-shared/SKILL.md) — 认证与登录
- [zsxq-group-list](../../zsxq-group/references/zsxq-group-list.md) — 查看星球列表
