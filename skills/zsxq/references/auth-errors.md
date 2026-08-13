# 认证与常见错误

zsxq-cli 的登录认证、错误排查与 CLI 未安装恢复流程。首次使用、遇到 401 / token 过期 / `not logged in`、或命令报错时读本文档。

## 认证命令

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

## 常见错误处理

下表覆盖所有 zsxq-cli 命令通用的错误。各命令 reference 只列出与该命令直接相关的特有错误。

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `command not found: zsxq-cli` / `zsxq-cli: command not found` | CLI 工具未安装 | 见下方 [CLI 未安装恢复流程](#cli-未安装恢复流程) |
| `authentication failed (HTTP 401)` / `not logged in` | Token 无效、过期或未登录 | 运行 `zsxq-cli auth login` |
| 403 / 无权限 / 不可访问 | 当前账户无访问权限 | 切换账户，或加入对应星球 |
| 404 / 资源不存在 | group_id / topic_id / note_id 无效或已删除 | 用 `group +list`、`topic +search`、`note +list` 等核对 ID |
| `MCP tool error: {"code":429,...}` / 操作过于频繁 | 短时间内写入/调用过密触发限流 | 等待几秒到几十秒后重试；批量操作时在命令间留间隔 |
| `--<flag> is required` | 缺少必填参数 | 用对应查询命令获取后再填 |
| `--end-time` 解析失败 | 分页时间格式错误 | 使用上一页 JSON 中返回的 `next_end_time` / `create_time` 原值 |

## CLI 未安装恢复流程

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
