# user +nps（提交 NPS 反馈）

> **版本要求：** 需要 `zsxq-cli` ≥ **0.4.6**。低于该版本时 `+nps` 不存在，命令会被识别为未知 shortcut。

本 skill 对应 shortcut：`zsxq-cli user +nps`。

向知识星球官方提交 NPS（Net Promoter Score，净推荐值）反馈，包含 0–10 分的推荐分数和文字建议。

> [!CAUTION]
> 这是**写入操作** —— 反馈会发送给知识星球官方。执行前必须向用户确认：
> 1. 推荐分数（`--score`，0–10 的整数）
> 2. 文字建议内容（`--suggestion`，必填，500 字以内）

## 命令

```bash
# 提交分数 + 文字建议（两者均必填）
zsxq-cli user +nps \
  --score 9 \
  --suggestion "希望增加更多互动功能"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--score <n>` | **是** | NPS 推荐分数，整数 0–10（0 = 完全不推荐，10 = 极力推荐） |
| `--suggestion <text>` | **是** | 文字建议，最长 500 字 |
| `--json` | 否 | 输出原始 JSON |

## 输出

```
✓ NPS feedback submitted
```

## 说明

- 提交无频率限制，可多次提交。AI 在执行前仍应每次都向用户确认内容，避免误触发
- NPS 分数语义：
  - 推荐者（Promoters）9–10：忠实用户，会主动推荐
  - 中立者（Passives）7–8：满意但不会主动推荐
  - 贬损者（Detractors）0–6：不满意，可能有负面口碑

## 推荐工作流

```bash
# 第一步：与用户确认分数和建议
# AI 复述分数与建议内容，并核对建议字数 ≤ 500，等待用户确认

# 第二步：执行提交
zsxq-cli user +nps --score 9 --suggestion "希望增加更多互动功能"
```

## 失败语义

提交失败即原子回滚 —— 不会留下半成品反馈记录。重试前请先确认参数是否合法。

## 错误说明

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 提示仅列出 `+footprints` / `+info` 等 shortcut，未识别 `+nps` | 当前 zsxq-cli 版本低于 0.4.6 | 运行 `npm i -g zsxq-cli@latest` 升级，再用 `zsxq-cli config show` 确认版本 ≥ 0.4.6 |
| `--score must be 0–10` | 分数超出范围或非整数 | 改为 0–10 的整数 |
| `--suggestion exceeds 500 chars` | 建议超过 500 字 | 精简至 500 字以内 |

通用错误（401、`--score is required` / `--suggestion is required` 等参数缺失）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。

## 参考

- [zsxq-user-info](zsxq-user-info.md) — 查看当前登录账户
- [zsxq-shared](../../zsxq-shared/SKILL.md)
