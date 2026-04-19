# topic delete（删除主题）

> **前置条件：** 先阅读 [`../zsxq-shared/SKILL.md`](../../zsxq-shared/SKILL.md) 了解认证和安全规则。

通过 `zsxq-cli api raw` 删除指定主题。删除后**不可恢复**。

> [!CAUTION]
> 这是**不可逆的破坏性操作** —— 删除后主题及其所有评论、回答将永久消失，无法恢复。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 明确用户确实要删除（而非取消精华、删除评论等其他操作）

## 命令

```bash
# 删除主题
zsxq-cli api raw --method DELETE --path /v2/topics/<topic_id>

# 示例
zsxq-cli api raw --method DELETE --path /v2/topics/15522482218442
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<topic_id>` | **是** | 主题 ID（拼接到 URL 路径中） |

## 推荐工作流

```bash
# 第一步：确认主题内容，确保删对目标
zsxq-cli topic +detail --topic-id 15522482218442

# 第二步：向用户确认后执行删除
zsxq-cli api raw --method DELETE --path /v2/topics/15522482218442
```

## 错误说明

| 错误             | 原因 |
|----------------|------|
| `code: 100262` | 无权限删除该主题（非主题作者或星主） |
| `code: 100002` | 主题不存在或已被删除 |

## 参考

- [zsxq-topic-detail](zsxq-topic-detail.md) — 删除前确认主题内容
- [zsxq-topic-search](zsxq-topic-search.md) — 搜索主题获取 topic_id
- [zsxq-shared](../../zsxq-shared/SKILL.md)
