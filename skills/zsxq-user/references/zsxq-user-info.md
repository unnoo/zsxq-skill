# user +info（查看个人资料）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

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
    "user_id": "123456",          // 用户 ID（其他命令的 user_id 参数）
    "name": "示例用户",            // 昵称
    "unique_id": "demo_user",     // 唯一标识（类似用户名）
    "location": "示例城市",        // 地区
    "avatar_url": "https://..."   // 头像 URL
  },
  "identity_status": "authenticated",  // 实名认证状态
  "subscribed_wechat": true,           // 是否关注公众号
  "accounts": {
    "wechat": {
      "name": "示例微信昵称"
    }
  }
}
```

## 常见用途

- **获取 user_id**：`user_id` 字段用于 `get_user_footprints`、`get_user_groups` 等 API 的参数
- **确认登录账户**：验证当前 CLI 是否使用了正确的账户
- **检查认证状态**：`identity_status` 为 `authenticated` 表示已实名认证

## 参考

- [zsxq-shared](../../zsxq-shared/SKILL.md) — 认证与登录
- [zsxq-group-list](../../zsxq-group/references/zsxq-group-list.md) — 查看星球列表
