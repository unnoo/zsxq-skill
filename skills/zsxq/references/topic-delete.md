# topic 删除（通过 api raw）

通过 `zsxq-cli api raw` 删除指定主题。删除后**不可恢复**。

对应命令：CLI 通道 `zsxq-cli api raw --method DELETE --path /v2/topics/<topic_id>`；MCP 通道见下方命令块。

> [!CAUTION]
> 这是**不可逆的破坏性操作** —— 删除后主题及其所有评论、回答将永久消失，无法恢复。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 明确用户确实要删除（而非取消精华、删除评论等其他操作）

## 命令

**CLI 通道：**

```bash
# 删除主题
zsxq-cli api raw --method DELETE --path /v2/topics/<topic_id>

# 示例
zsxq-cli api raw --method DELETE --path /v2/topics/88888888888888
```

**MCP 通道（`call_zsxq_api`）：**

```json
{"method": "DELETE", "path": "/v2/topics/111222333444"}
```

CLI 通道的 `api raw` 与 MCP 通道**仅外壳不同** —— 都是同一次 `DELETE /v2/topics/{topic_id}` 请求，删除后同样**不可恢复**。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<topic_id>` | **是** | 主题 ID（拼接到 URL 路径中） |

### 通道映射

| CLI 形式 | HTTP 字段 |
|----------|-----------|
| `<topic_id>`（路径） | path `/v2/topics/{topic_id}`（两通道同一路径） |

## 推荐工作流

**两通道步骤相同，仅调用形式不同**：确认主题用 CLI `topic +detail` / MCP `GET /v2/topics/{topic_id}/info`；删除用上方对应通道的命令。

```bash
# 第一步：确认主题内容，确保删对目标
zsxq-cli topic +detail --topic-id 88888888888888

# 第二步：向用户确认后执行删除
zsxq-cli api raw --method DELETE --path /v2/topics/88888888888888
```

## 失败语义

删除失败即原子回滚 —— 主题保持原状不会被部分删除。

## 错误说明

| 错误             | 原因 |
|----------------|------|
| `code: 100262` | 无权限删除该主题（非主题作者或星主） |
| `code: 100002` | 主题不存在或已被删除 |

通用错误（401、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-edit](topic-edit.md) — 删除前若只是想改内容，优先考虑编辑
- [topic-detail](topic-detail.md) — 删除前确认主题内容
- [topic-search](topic-search.md) — 搜索主题获取 topic_id
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
