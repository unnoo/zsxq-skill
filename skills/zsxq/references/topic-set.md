# topic +set（设置精华/置顶）

对应命令：`zsxq-cli topic +set`。

设置或取消主题的**精华**（digested）和**置顶**（sticky）状态，直调官方「设置主题」接口。日常加精/取消精华优先用本命令，底层接口工具见 [topic-digest](topic-digest.md)。

> [!CAUTION]
> 这是**写入操作** —— 精华会进入星球精华列表，置顶会改变主题流顶部展示，对全体成员可见。执行前必须向用户确认：
> 1. 目标主题（topic_id）及其内容
> 2. 对精华 / 置顶各自是**设置**还是**取消**（`true` / `false`）；未提供的字段保持不变

> [!IMPORTANT]
> - 需要**管理权限**（星主 / 管理员 / 合伙人，同加精权限，见 [topic-digest](topic-digest.md)），无权限时服务端返回 `API 错误`
> - `--digested`、`--sticky` 至少提供一个；只传其一不影响另一个字段

## 命令

```bash
# 设为精华
zsxq-cli topic +set --topic-id 111222333444 --digested true

# 取消置顶
zsxq-cli topic +set --topic-id 111222333444 --sticky false

# 同时设置精华与置顶
zsxq-cli topic +set --topic-id 111222333444 --digested true --sticky true
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--digested true\|false` | 否 | 是否设为精华（`true` 设置 / `false` 取消）；不传则保持现状 |
| `--sticky true\|false` | 否 | 是否置顶（`true` 置顶 / `false` 取消）；不传则保持现状 |
| `--json` | 否 | 输出原始 JSON |

## 输出

成功后输出 `✓ Topic updated` 及服务端返回的 JSON；`--json` 模式仅输出 JSON。

## 推荐工作流

```bash
# 第一步：确认目标主题内容
zsxq-cli topic +detail --topic-id 111222333444

# 第二步：向用户确认「设 / 取消精华、设 / 取消置顶」后执行
zsxq-cli topic +set --topic-id 111222333444 --digested true

# 第三步：验证结果
zsxq-cli topic +detail --topic-id 111222333444
```

## 失败语义

失败即不改变原精华 / 置顶状态，不会产生中间态；确认参数后可重试。

## 错误说明

| 错误 | 原因 |
|------|------|
| `请至少提供 --digested 或 --sticky 之一` | 两个参数都没传 |
| `--digested 取值必须是 true 或 false` / `--sticky 取值必须是 true 或 false` | 值不是 `true` / `false` |
| `API 错误(<code>): <msg>` | 服务端拒绝（无管理权限、主题不存在等），`code` 与 `msg` 为服务端返回 |

通用错误（401、`--topic-id is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [topic-digest](topic-digest.md) — 底层接口工具 `set_topic_digested`（本命令精华能力的来源）
- [topic-detail](topic-detail.md) — 操作前后确认主题状态
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
