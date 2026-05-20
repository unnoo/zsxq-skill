---
name: zsxq-shared
version: 1.3.0
description: "知识星球 CLI 共享基础：认证登录（auth login/logout/status）、配置诊断（doctor/config show）、通用 API 调用规范（api list/api call/api raw 调用底层接口或原始 HTTP 接口）、星球与主题分享链接拼接（电脑端 / 手机端）、写入与删除操作的安全规则、常见错误码处理（401 token 过期、缺参数等）。当用户首次登录、退出登录、查看认证状态、调用 zsxq-cli api raw / api call、需要拼接知识星球分享链接，或遇到认证或 HTTP 错误时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli auth --help"
---

# zsxq-cli 共享规则

本技能指导你如何通过 zsxq-cli 操作知识星球资源，以及有哪些注意事项。

## 索引

- [Commands](#commands) — 认证、诊断、底层 API 调用命令一览
- [认证](#认证) — OAuth 设备授权码流程
- [直接调用 API](#直接调用-api) — `api call` / `api raw` 详细用法与示例
- [链接拼接](#链接拼接) — 主题/星球分享链接（电脑端 / 手机端）
- [安全规则](#安全规则) — Token、写入确认、ID 查询前置
- [常见错误处理](#常见错误处理) — 通用错误（401/403/404/参数缺失/分页时间格式）

## Commands

| 命令 | 说明 |
|------|------|
| `zsxq-cli auth login` | OAuth 设备授权码登录（首次使用、token 过期或切换账户时） |
| `zsxq-cli auth status` | 查看当前登录账户（默认表格，加 `--json` 输出 JSON） |
| `zsxq-cli auth logout` | 清除本地凭据 |
| `zsxq-cli doctor` | 诊断 CLI 配置与 keychain 认证状态 |
| `zsxq-cli config show` | 显示版本信息与当前配置（加 `--json` 输出 JSON） |
| `zsxq-cli api list` | 列出所有可用底层接口工具及参数 |
| `zsxq-cli api call <tool>` | 调用底层接口工具，需配 `--params '<json>'` |
| `zsxq-cli api raw` | 直接调用原始 HTTP 接口（需 `--method` `--path`） |

详细用法见下面各小节。

## 认证

zsxq-cli 使用 **OAuth 2.0 设备授权码流程（RFC 8628）** 认证，token 存储在系统 Keychain 中，永久有效。

### OAuth 登录流程

`zsxq-cli auth login` 启动后：
1. 命令输出一个 `verification_uri` 链接和 `user_code`
2. 用户在手机或浏览器中打开链接，完成授权
3. CLI 自动轮询，授权完成后自动保存 token

> 当你作为 AI Agent 帮用户登录时，在后台运行 `zsxq-cli auth login`，读取输出后将授权链接提供给用户，等待用户完成授权。

## 直接调用 API

当 Shortcut 无法满足需求时，可以直接调用底层接口（参数与方法见上面 Commands 表）。

`api call` 示例：

```bash
zsxq-cli api call get_self_info --params '{}'
zsxq-cli api call search_groups --params '{"keyword":"Go语言"}'

# 跨星球查询当前用户主题足迹（不传 group_id 即查所有星球）
zsxq-cli api call get_user_footprints --params '{"user_id":"123456"}'
# 限定单个星球
zsxq-cli api call get_user_footprints --params '{"user_id":"123456","group_id":"123456789"}'
```

`api raw` 示例：

```bash
zsxq-cli api raw --method GET --path /v3/users/self

# --body 支持简写，自动包装 req_data
zsxq-cli api raw --method PUT --path /v2/topics/123 --body '{"text":"新内容"}'
```

> 列表/查询类操作请优先使用 `api call`（如 `get_group_topics`），`api raw` 主要用于 `api call` 尚未覆盖的写入接口。
>
> `api raw` 响应已去除三层嵌套，直接返回数据内容。

## 链接拼接

当用户需要分享链接时，使用以下模板拼接。输出时同时提供电脑端和手机端两个版本。

### 主题链接

- 电脑端：`https://wx.zsxq.com/group/{group_id}/topic/{topic_id}`
- 手机端：`https://wx.zsxq.com/mweb/views/topicdetail/topicdetail.html?topic_id={topic_id}&group_id={group_id}`

### 星球链接

- 电脑端：`https://wx.zsxq.com/group/{group_id}`
- 手机端：`https://wx.zsxq.com/mweb/views/topic/topic.html?group_id={group_id}`

## 安全规则

- **Token 是登录凭证**，禁止在终端明文输出或分享给他人
- **写入/删除操作前必须确认用户意图**（发帖、编辑、评论、回答、创建笔记、删除主题或笔记、提交 NPS 反馈等）
- 不确定 group_id / topic_id / note_id 时，先用查询命令确认，再执行写入或删除

## 常见错误处理

下表覆盖所有 zsxq-cli 命令通用的错误。各命令的 reference 文档只列出与该命令直接相关的特殊错误（如 `--score must be 0–10`、`code: 100262 无权限删除`），通用错误一律回到这里。

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `authentication failed (HTTP 401)` / `not logged in` | Token 无效、过期或未登录 | 运行 `zsxq-cli auth login` 重新登录 |
| 403 / 无权限 / 不可访问 | 当前账户无访问目标资源的权限 | 切换到正确账户，或加入对应星球后重试 |
| 404 / 资源不存在 | group_id / topic_id / note_id 等无效或对应资源已被删除 | 重新核对 ID；可用 `group +list`、`topic +search`、`note +list` 等查询 |
| `--<flag> is required` | 缺少必填参数 | 用对应查询命令获取后再填，例如 group_id 用 `group +list`、topic_id 用 `topic +search` |
| `--end-time` 解析失败 | 分页时间格式错误 | 使用上一页 JSON 中返回的 `next_end_time` / `create_time` 原值 |
