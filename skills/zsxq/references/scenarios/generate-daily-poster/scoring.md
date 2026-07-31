# 主题综合打分（模型四维 + 公式兜底）

> 由场景入口 [`../generate-daily-poster.md`](../generate-daily-poster.md) 的「执行流程 · 打分」步骤引用。

对候选池中每条主题计算 `final_score ∈ [0, 100]`，**值越高越靠前**。打分由两部分加权：模型四维主观分（70%）+ 公式客观分（30%）。

## 1. 模型四维打分（批量评估）

**输入**：候选池中所有主题（content 全文 + 每条主题的全部评论）。如某条主题评论数较多，截取前 50 条。

**任务**：让模型一次性输出 JSON 数组，每条主题给出 4 个维度分（每维 0–25，整数），并写一行 ≤ 20 字的入选理由。提示词大意：

> 你是星球内容编辑。请阅读下列主题与评论，对每条按 4 个维度评分（每维 0–25，整数）：
> 1. **信息密度** insight：是否有独到观点、数据、可执行结论
> 2. **讨论热度** discussion：评论是否有质量交锋（不是凑数评论）
> 3. **行业相关性** relevance：对该星球主理人/读者群体的价值
> 4. **传播潜力** virality：标题/角度是否值得二次分享
>
> 仅输出 JSON 数组：`[{"topic_id":"...", "insight":18, "discussion":12, "relevance":20, "virality":15, "reason":"..."}, ...]`。不要任何其他文字。

**模型分**：`model_score = insight + discussion + relevance + virality`（满分 100）

**批量上限**：单批最多 30 条，超过则分批调用并合并结果。

## 2. 公式客观分（兜底）

```
raw = (digested ? 50 : 0)        # 精华加 50
    + likes * 3                   # 点赞:每个 +3
    + comments * 2                # 评论:每条 +2
    + log10(readers + 1) * 5      # 阅读:对数防大星球碾压
    + (type == 'q&a' ? 5 : 0)     # 问答类:+5

formula_score = min(100, raw)     # 归一到 0-100
```

字段来源：`digested`、`counts.likes`、`counts.comments`、`counts.readers`、`type`（主题类型只有 `talk` / `q&a` / `task` / `solution` 四种）。

## 3. 加权合成与排序

```
final_score = model_score * 0.7 + formula_score * 0.3
```

排序与截取：

1. 按 `final_score` 降序排列；相同分数时按 `formula_score` → `create_time` 依次 tiebreaker
2. **数量限制**：每个星球默认保留 **final_score 排名前 5** 的主题（可通过参数自定义上限）
3. 候选池 ≤ 5 条时全部保留；为 0 条时该星球区块整块省略

## 4. 模型不可用时的降级

若模型批量评分调用失败（网络、超时、JSON 解析错误等），**不阻塞日报**：

- 自动降级为「纯公式分」排序（即 `final_score = formula_score`）
- 在文字报告末尾追加一行提示：「⚠️ 本次主题评分降级为公式打分（模型评估失败）」

> 加权比例、单维权重可以在用户明确给出新偏好时按调整后的值执行，但不要主动改默认值。

## 参考

- 场景入口：[`../generate-daily-poster.md`](../generate-daily-poster.md)
- 主题字段来源：[`../../group-topics.md`](../../group-topics.md)（`counts` / `type` / `digested` 等）
