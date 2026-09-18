# 认证与常见错误

本文档覆盖两条通道的认证与错误排查：**CLI 通道**（zsxq-cli，OAuth 设备码登录）与 **MCP 通道**（api-key 接入，见 [SKILL.md](../SKILL.md#执行通道)）。

## CLI 通道认证

zsxq-cli 使用 **OAuth 2.0 设备授权码流程（RFC 8628）** 认证，token 存储在系统 Keychain 中。

| 命令 | 说明 |
|------|------|
| `zsxq-cli auth login` | OAuth 设备授权码登录（首次使用、token 过期或切换账户时） |
| `zsxq-cli auth status` | 查看当前登录账户（默认表格，加 `--json` 输出 JSON） |
| `zsxq-cli auth logout` | 清除本地凭据 |
| `zsxq-cli doctor` | 诊断 CLI 配置与 keychain 认证状态 |
| `zsxq-cli config show` | 显示版本信息与当前配置 |

## OAuth 登录流程

`zsxq-cli auth login` 启动后：

1. 命令输出一个 `verification_uri` 链接和 `user_code`
2. 用户在手机或浏览器中打开链接，完成授权
3. CLI 自动轮询，授权完成后自动保存 token

> 当你作为 AI Agent 帮用户登录时，在后台运行 `zsxq-cli auth login`，读取输出后将授权链接提供给用户，等待用户完成授权。

## MCP 通道认证

MCP 通道使用 api-key 鉴权（密钥管理页创建密钥后复制含 key 的链接接入宿主）。没有 `auth login` 等命令：

- 401 / 鉴权失败 → 提示用户到知识星球密钥管理页删除旧密钥、创建新密钥，并在宿主的 MCP 配置中更新链接后重连
- 宿主工具列表中没有 `call_zsxq_api` → 说明 MCP 未接入；按 [SKILL.md](../SKILL.md#执行通道)「执行通道」引导用户接入 MCP 或改装 CLI
- 不得要求用户把 api-key 贴到对话中；api-key 等同于登录凭证，按 token 同级保护

## 常见错误处理

下表覆盖两条通道通用的错误。各命令 reference 只列出与该命令直接相关的特有错误。

| 错误 | 通道 | 原因 | 解决方案 |
|------|------|------|---------|
| `command not found: zsxq-cli` / `zsxq-cli: command not found` | 仅 CLI 通道 | CLI 工具未安装 | 见下方 [CLI 通道：未安装恢复流程](#cli-通道未安装恢复流程) |
| `authentication failed (HTTP 401)` / `not logged in` | CLI 通道 | Token 无效、过期或未登录 | 运行 `zsxq-cli auth login` |
| 401 / 鉴权失败 | MCP 通道 | api-key 无效或已失效 | 到知识星球密钥管理页删除旧密钥、创建新密钥，在宿主的 MCP 配置中更新链接后重连 |
| 403 / 无权限 / 不可访问 | 两通道 | 当前账户无访问权限 | 切换账户，或加入对应星球 |
| 404 / 资源不存在 | 两通道 | group_id / topic_id / note_id 无效或已删除 | 用 `group +list`、`topic +search`、`note +list` 等核对 ID |
| `MCP tool error: {"code":429,...}` / 操作过于频繁 | 仅 CLI 通道（MCP 通道看响应 `body.succeeded` / `status_code`） | 短时间内写入/调用过密触发限流 | 等待几秒到几十秒后重试；批量操作时在命令间留间隔 |
| `--<flag> is required` | 仅 CLI 通道 | 缺少必填参数 | 用对应查询命令获取后再填 |
| `--end-time` 解析失败 | 仅 CLI 通道 | 分页时间格式错误 | 使用上一页 JSON 中返回的 `next_end_time` / `create_time` 原值 |

## CLI 通道：未安装恢复流程

MCP 通道无此流程；宿主缺 `call_zsxq_api` 时按 [SKILL.md](../SKILL.md#执行通道)「执行通道」引导接入。

当 zsxq-cli 命令报 `command not found` 时，不要中止任务，按以下流程恢复：

**1. 引导安装：**

```bash
# 确认 Node.js >= 18
node -v

# 全局安装
npm install -g zsxq-cli

# 验证
zsxq-cli --version
```

**2. 引导登录：**

```bash
zsxq-cli auth login
```

终端会输出授权链接，让用户在浏览器中打开并确认授权。

**3. 安装并登录成功后，自动重试用户原本要执行的操作。** 不需要用户再重复一遍指令。

> 这个流程只在命令真正报 `command not found` 时才触发。日常使用中绝大多数用户已安装，不应浪费 token 做预检查。

## 参考

- [cli-exploration](cli-exploration.md) — 探索模式与直接调用 API
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
