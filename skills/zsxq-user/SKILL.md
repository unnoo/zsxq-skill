---
name: zsxq-user
version: 1.3.0
description: "知识星球用户信息与反馈：查看当前登录用户的个人资料、查询跨星球的最近发主题足迹、提交 NPS 反馈（推荐分数 + 建议）。当用户需要查看自己的用户 ID、昵称、头像、认证状态，查看自己最近在各星球发过的主题，或向知识星球官方提交 NPS 评分/产品建议时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli user --help"
---

# user

> 首次使用或遇到认证错误（401 / token 过期 / `not logged in`）时，先读 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md) 了解登录与 API 调用约定。日常调用已登录账户时无需每次重读。

## Core Concepts

- **用户（User）**：当前已登录的知识星球账户，由 `user_id`（纯数字）唯一标识。`user_id` 在 `group +list`、搜索成员等操作中被用作参数。

## Shortcuts（推荐优先使用）

| Shortcut | 说明 |
|----------|------|
| [`+info`](references/zsxq-user-info.md) | 查看当前登录用户的完整个人资料，含 user_id、昵称、认证状态 |
| [`+footprints`](references/zsxq-user-footprints.md) | 查看自己在所有星球发过的主题（跨星球足迹），支持分页 |
| [`+nps`](references/zsxq-user-nps.md) | 提交 NPS 反馈（0–10 分推荐分数 + 必填文字建议，500 字以内），需确认内容后执行 |

## 相关操作

- 在某个星球内按昵称搜索成员、获取 user_id：见 [zsxq-group](../zsxq-group/SKILL.md) 的 `search_group_members`
