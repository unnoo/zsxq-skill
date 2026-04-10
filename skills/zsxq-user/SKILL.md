---
name: zsxq-user
version: 1.1.0
description: "知识星球用户信息：查看当前登录用户的个人资料、查询跨星球的最近发主题足迹。当用户需要查看自己的用户 ID、昵称、头像、认证状态，或查看自己最近在各星球发过的主题时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli user --help"
---

# user (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md)，其中包含认证、错误处理规则。**

## Core Concepts

- **用户（User）**：当前已登录的知识星球账户，由 `user_id`（纯数字）唯一标识。`user_id` 在 `group +list`、搜索成员等操作中被用作参数。

## Shortcuts（推荐优先使用）

| Shortcut | 说明 |
|----------|------|
| [`+info`](references/zsxq-user-info.md) | 查看当前登录用户的完整个人资料，含 user_id、昵称、认证状态 |
| [`+footprints`](references/zsxq-user-footprints.md) | 查看自己在所有星球发过的主题（跨星球足迹），支持分页 |

## API（通过 `zsxq-cli api call` 直接调用）

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_group_members` | `group_id`, `keyword`, `limit` | 在星球内按昵称搜索成员，获取其 user_id |
