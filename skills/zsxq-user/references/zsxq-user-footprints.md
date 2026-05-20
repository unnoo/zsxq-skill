# user +footprints（查看主题足迹）

本 skill 对应 shortcut：`zsxq-cli user +footprints`。

查看当前用户在**所有星球**中最近发过的主题，按时间倒序排列。

## 命令

```bash
# 查看最近 20 条足迹（表格显示）
zsxq-cli user +footprints

# 指定数量
zsxq-cli user +footprints --limit 30

# JSON 格式（含完整字段）
zsxq-cli user +footprints --json

# 翻页（使用上一页返回的 create_time 作为游标）
zsxq-cli user +footprints --end-time "2025-11-01T00:00:00.000+0800"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 返回条数，默认 20，最大 30 |
| `--end-time <time>` | 否 | 分页游标，传入上一页最后一条的 `create_time` |
| `--json` | 否 | 输出原始 JSON |

## 输出（表格模式）

| TOPIC ID | TYPE | TITLE / DIGEST | GROUP | CREATED AT |
|----------|------|----------------|-------|------------|
| 111222333444 | talk | 示例主题标题 | 示例星球 | 2026-04-10T09:00:00.000+0800 |

## 说明

跨星球查询。与 `group +topics` 的区别：

| | `user +footprints` | `group +topics` |
|---|---|---|
| 范围 | **所有星球** | 单个星球 |
| 内容 | 用户在各星球发过的主题 | 星球内最新主题 |
| 必填参数 | 无 | `--group-id` |

## 错误说明

| 症状 | 可能原因 | 处理 |
|------|---------|------|
| 返回空列表 | 当前账户近期未在任何星球发主题 | 正常情况，无需处理 |

通用错误（401、`--end-time` 格式错误等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-user-info](zsxq-user-info.md) — 查看用户 ID 等基本信息
- [zsxq-group-topics](../../zsxq-group/references/zsxq-group-topics.md) — 查看单个星球的主题列表
- [zsxq-shared](../../zsxq-shared/SKILL.md)
