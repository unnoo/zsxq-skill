---
name: zsxq-shared
version: 1.0.0
description: "知识星球 CLI 共享基础：认证登录（auth login/logout）、查看认证状态、诊断配置。当用户需要首次登录、退出登录、查看认证状态、或遇到认证错误时触发。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli auth --help"
---

# zsxq-cli 共享规则

本技能指导你如何通过 zsxq-cli 操作知识星球资源，以及有哪些注意事项。

## 认证

zsxq-cli 使用 **OAuth 2.0 设备授权码流程（RFC 8628）** 认证，token 存储在系统 Keychain 中，永久有效。

### 登录

```bash
# 发起登录（会输出一个授权链接，用户在手机/浏览器中打开并授权）
zsxq-cli auth login
```

登录流程：
1. 命令输出一个 `verification_uri` 链接和 `user_code`
2. 用户在手机或浏览器中打开链接，完成授权
3. CLI 自动轮询，授权完成后自动保存 token

> 当你作为 AI Agent 帮用户登录时，在后台运行 `zsxq-cli auth login`，读取输出后将授权链接提供给用户，等待用户完成授权。

### 查看认证状态

```bash
zsxq-cli auth status        # 表格显示当前登录账户
zsxq-cli auth status --json # JSON 格式输出
```

### 退出登录

```bash
zsxq-cli doctor             # 诊断配置和认证是否正常
```

### 配置诊断

```bash
zsxq-cli doctor             # 检查 CLI 配置和 keychain 认证状态
zsxq-cli config show        # 显示版本信息和当前配置
zsxq-cli config show --json # JSON 格式
```

## 直接调用 API

当 Shortcut 无法满足需求时，可以直接调用底层 MCP 工具：

```bash
zsxq-cli api list                           # 列出所有可用 MCP 工具及参数
zsxq-cli api call <tool> --params '<json>'  # 调用指定工具
zsxq-cli api raw --method GET --path /v3/users/self
```

示例：

```bash
zsxq-cli api call get_self_info --params '{}'
zsxq-cli api call search_groups --params '{"keyword":"Go语言"}'
zsxq-cli api call get_user_footprints --params '{"user_id":"123456","group_id":"123456789"}'

# 推荐：对通用 HTTP API 使用显式参数的 raw 子命令
zsxq-cli api raw --method GET --path /v2/groups/123456789/topics --query '{"count":10}'
```

## 安全规则

- **Token 是登录凭证**，禁止在终端明文输出或分享给他人
- **写入/删除操作前必须确认用户意图**（发帖、评论、创建笔记等）
- 不确定 group_id / topic_id 时，先用查询命令确认，再执行写入

## 常见错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `authentication failed (HTTP 401)` | Token 无效或过期 | 重新运行 `zsxq-cli auth login` |
| `not logged in` | 未完成登录 | 运行 `zsxq-cli auth login` |
| `--group-id is required` | 缺少必填参数 | 先用 `zsxq-cli group +list` 查询 group_id |
| `--topic-id is required` | 缺少必填参数 | 先用 `zsxq-cli group +topics` 或 `topic +search` 查询 topic_id |
