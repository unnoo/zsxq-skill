# 创建微信订单（底层接口工具 `call_zsxq_api`）

通过底层接口工具 `call_zsxq_api` 创建知识星球微信订单，并触发 Skill Pay。不要用 `zsxq-cli api raw` 代替本操作，CLI 无法保证把支付所需的 `_meta` 交给支付宿主。

> [!CAUTION]
> 创建订单会产生真实待支付订单，完成支付会发生真实资金交易。首先确认当前宿主是 WorkBuddy 且提供官方 `weixinpay_pay`；非 WorkBuddy（如 Claude Code / CC）必须说明不支持并停止，不得创建订单。通过宿主检查后，首次调用前还必须向用户确认：
> 1. 订单类型及中文含义
> 2. 购买/支付对象（相应的 `group_id`、`topic_id`、`comment_id`、`user_id` 或 `back_issue_id`；赞赏评论需同时确认 `topic_id` 和 `comment_id`，轻读查价需同时确认 `group_id` 和 `back_issue_id`）
> 3. 按[下单前查询价格](#下单前查询价格)取得的应付金额；接口金额单位为“分”，必须按 `金额 ÷ 100` 换算成“元”向用户展示，不得改写固定价格。`question_fee`、`reward_user`、`reward_topic`、`reward_comment` 由用户以“元”指定金额时，必须按 `amount = 元 × 100` 精确换算成整数分，并同时确认元值和将传入接口的 `amount`
> 4. 用户明确提供的优惠券或验证信息等可选字段
> 5. 用户在微信支付卡片中仍需再次确认支付；agent 不得代替用户授权支付

> [!IMPORTANT]
> - Skill Pay 仅支持 WorkBuddy；不能仅凭某个同名或非官方支付工具绕过宿主限制。
> - 本操作固定调用 `POST /v2/wechat_orders`。
> - 支持的订单类型为 `membership_fee`、`gift_card_fee`、`renewal_fee`、`question_fee`、`reward_user`、`reward_topic`、`reward_comment`、`group_invite_code`、`back_issue`。
> - 支付回调与履约由知识星球原支付链路处理。当前工具没有支付查单接口，不得把“已拉起支付”或“用户口头称已支付”当作支付成功。
> - 本文示例中的 ID、订单号和支付码均为模拟数据，不对应真实星球、内容、用户或订单。实际执行时必须通过只读接口查询并核对真实标识，不得直接复用示例值。

## 下单前查询价格

价格查询是只读操作。创建订单前使用 `call_zsxq_api` 按订单类型取得价格；接口金额单位均为“分”，向用户展示时除以 100 换算为“元”。`1 元 = 1 星球币`。

| 订单类型 | 查询方式 | 金额字段或规则 |
|----------|----------|----------------|
| `membership_fee` | `GET /v2/groups/{group_id}/public_info` | 确认 `body.resp_data.public_info.type` 为 `pay`，读取 `body.resp_data.public_info.policies.payment.amount`，无折扣 |
| `gift_card_fee` | `GET /v2/groups/{group_id}/public_info` | 确认 `body.resp_data.public_info.type` 为 `pay`；与加入星球相同，读取 `body.resp_data.public_info.policies.payment.amount`，无折扣 |
| `renewal_fee` | `GET /v2/groups/{group_id}` | 确认 `body.resp_data.group.type` 为 `pay`，读取基础价、当前用户有效期和续费折扣，按下方规则计算 |
| `back_issue` | `GET /v2/groups/{group_id}/back_issues/{back_issue_id}` | `body.resp_data.back_issue.amount` |
| `group_invite_code` | 无需查询 | 固定 `800 元`，即 `80000 分` |
| `question_fee`、`reward_user`、`reward_topic`、`reward_comment` | 无价格查询接口 | 使用用户明确指定的元金额，按 `元 × 100` 换算并确认整数 `amount`（分） |

调用示例均为底层接口工具参数：

```json
{
  "method": "GET",
  "path": "/v2/groups/123456789/public_info"
}
```

```json
{
  "method": "GET",
  "path": "/v2/groups/123456789"
}
```

```json
{
  "method": "GET",
  "path": "/v2/groups/123456789/back_issues/555666777888"
}
```

以上字段路径包含 `call_zsxq_api` 的外层 `body`；若当前宿主直接返回业务响应体，则从 `resp_data` 开始读取。

轻读价格接口同时需要 `group_id` 和 `back_issue_id`。若用户只提供轻读链接或 `back_issue_id`，且无法从已知上下文或链接中可靠取得所属 `group_id`，停止并请用户补充所属星球；不得猜测 `group_id`，也不得跳过查价直接下单。

### 续费价格计算

`GET /v2/groups/{group_id}` 的星球数据位于 `body.resp_data.group`（宿主直接返回业务响应体时为 `resp_data.group`）。在 `group` 内读取：

- 基础价：`policies.payment.amount`
- 当前用户到期时间：`user_specific.validity.end_time`
- 提前续费比例：`policies.renewal.advance_discounted_percentage`
- 过期 30 天内续费比例：`policies.renewal.grace_discounted_percentage`
- 过期超过 30 天续费比例：`policies.renewal.discounted_percentage`

将 `end_time` 按响应中的时区偏移解析为时间点，并与当前时间比较：

| 用户有效期 | 使用的折扣比例 |
|------------|----------------|
| 尚未到期（`当前时间 <= end_time`） | `advance_discounted_percentage` |
| 已过期且不超过 30 天 | `grace_discounted_percentage` |
| 已过期超过 30 天 | `discounted_percentage` |

计算公式：

```text
续费金额（分） = floor(policies.payment.amount * 对应 discounted_percentage / 100)
```

比例 `68` 表示支付原价的 68%，即 6.8 折；比例 `100` 表示无折扣。折扣字段缺失时按默认值 `100` 计算。向用户同时展示基础价、适用折扣、有效期到期时间和计算后的续费价，例如：`基础价 50 元，提前续费 8 折，应付 40 元`。

以下情况停止，不得创建订单：

- 付费加入或礼品卡的 `body.resp_data.public_info.type` 不是 `pay`，续费的 `body.resp_data.group.type` 不是 `pay`，或对应星球对象缺少 `policies.payment.amount`。
- 续费接口返回当前用户不是星球成员，或响应缺少 `body.resp_data.group`。
- 续费时缺少 `user_specific.validity.end_time`，导致无法选择折扣档位。
- 接口返回的金额不是非负整数，或折扣比例不在 `[50, 100]`。
- 轻读响应缺少 `body.resp_data.back_issue.amount`（或业务响应体中的 `resp_data.back_issue.amount`），或返回的 `group_id` / `back_issue_id` 与用户选择不一致。

## 命令

以下为底层接口工具调用参数，不是 shell 命令。

```json
{
  "method": "POST",
  "path": "/v2/wechat_orders",
  "body": {
    "req_data": {
      "type": "membership_fee",
      "group_id": "123456789"
    }
  }
}
```

## 参数

工具顶层参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `method` | **是** | 固定为 `POST` |
| `path` | **是** | 固定为 `/v2/wechat_orders` |
| `body.req_data` | 首次调用 **是** | 订单请求体；字段见下表 |
| `payment_retry_token` | 仅预下单失败重试 | `SKILLHUB_PREORDER_FAILED` 返回的短期签名凭据；重试时无需再传 `body` |
| `out_trade_no` | 否 | 与 `payment_retry_token` 一起校验订单；单独传入会被拒绝。**只能作为字符串原样保存和传递**，不得转换为数值；恢复时可省略，由签名凭据确定订单 |

`body.req_data` 字段：

| 字段 | 必填 | 适用范围与说明 |
|------|------|----------------|
| `type` | **是** | 从上方支持的订单类型中选择 |
| `group_id` | 按类型 | `membership_fee`、`gift_card_fee`、`renewal_fee`、`question_fee`、`reward_user` |
| `topic_id` | 按类型 | `reward_topic` |
| `comment_id` | 按类型 | `reward_comment` |
| `user_id` | 按类型 | `question_fee`、`reward_user` 的被提问/被赞赏用户 |
| `back_issue_id` | 按类型 | `back_issue` |
| `amount` | 按类型 | 仅 `question_fee`、`reward_user`、`reward_topic`、`reward_comment` 必填；整数，单位为“分”。用户以“元”指定时乘以 100 换算 |
| `pay_type` | 否 | 支付方式，缺省使用微信支付 |
| `coupon_code` | 否 | `membership_fee`、`renewal_fee` 使用的优惠券码 |
| `message` | 否 | `membership_fee` 的验证信息，0–30 字符 |

逐类型传参规则：

| 订单类型 | 中文含义 | 必填的 `req_data` 字段 | 可选字段 |
|----------|----------|-------------------------|----------|
| `membership_fee` | 付费加入 | `type`、`group_id` | `coupon_code`、`message` |
| `gift_card_fee` | 购买礼品卡 | `type`、`group_id` | — |
| `renewal_fee` | 续期 | `type`、`group_id` | `coupon_code` |
| `question_fee` | 付费提问 | `type`、`group_id`、`user_id`、`amount` | — |
| `reward_user` | 赞赏用户 | `type`、`group_id`、`user_id`、`amount` | — |
| `reward_topic` | 赞赏主题 | `type`、`topic_id`、`amount` | — |
| `reward_comment` | 赞赏评论 | `type`、`comment_id`、`amount` | — |
| `group_invite_code` | 购买创建星球邀请码 | `type` | — |
| `back_issue` | 购买轻读 | `type`、`back_issue_id` | — |

### 金额换算规则

- 接口 `amount` 的单位是“分”，必须传整数。
- 用户通常以“元”指定金额：`接口 amount（分） = 用户金额（元） × 100`。只能接受最多两位小数且乘积为整数分的元金额；无法精确换算时停止并请用户重新给出金额，不得四舍五入或截断。
- 向用户展示时使用“元”：`展示金额（元） = amount ÷ 100`。
- `1 元 = 1 星球币`，因此换算后的元数值也等于星球币数量。
- 示例：用户指定 `10 元`时传 `amount: 1000`；用户指定 `12.34 元`时传 `amount: 1234`，等值 `12.34 星球币`。

`pay_type` 省略时使用微信支付。除表中字段外，不要自行补充参数；尤其不要给付费加入、礼品卡、续期、创建星球邀请码或轻读订单传 `amount`。

## 输出

知识星球订单和 SkillHub 预下单均成功时，底层接口工具调用本身不是协议错误，但结构化业务结果是 402 支付挑战。此时 `success: false` 是协议约定；必须以 `code == "PAYMENT_REQUIRED"` 且 `status_code == 402` 识别待支付状态，不得按普通失败处理，也不得重试创建订单：

```json
{
  "success": false,
  "status_code": 402,
  "code": "PAYMENT_REQUIRED",
  "message": "该订单需要完成微信支付",
  "payment": {
    "provider": "WEIXINPAY",
    "payment_code": "MOCK_PAYMENT_CODE",
    "prompt": "请完成微信支付。",
    "out_trade_no": "90000000000000000001",
    "expires_at": 4102444800
  },
  "out_trade_no": "90000000000000000001"
}
```

同一结果还包含供支付宿主读取的 `_meta`：

```json
{
  "WeixinPay": {
    "WeixinPay-Required": "MOCK_PAYMENT_CODE",
    "prompt": "请完成微信支付。"
  },
  "X-Out-Trade-No": "90000000000000000001"
}
```

订单号可能同时出现在顶层 `out_trade_no`、`payment.out_trade_no` 和 `_meta.X-Out-Trade-No`。读取时，每个已出现的值都必须是非空字符串；多个位置同时存在时必须完全一致，否则停止并报告。订单号必须始终按原字符串保存和传递，不得转换为数值。

收到 `PAYMENT_REQUIRED` 不是失败，也不是支付成功；应让支持 Skill Pay 的宿主展示微信支付授权卡片，由用户确认。

`expires_at` 是 Unix 时间戳，单位为**秒**。与当前时间比较时使用当前 Unix 秒值（不能直接用毫秒级 `Date.now()`）；当前时间大于或等于 `expires_at` 时支付码已过期，必须停止。示例中的 `4102444800` 是模拟值，不对应真实订单。

SkillHub 预下单失败时，知识星球订单已经创建，响应会包含安全恢复所需字段：

```json
{
  "success": false,
  "status_code": 502,
  "code": "SKILLHUB_PREORDER_FAILED",
  "error": "MOCK_SKILLHUB_ERROR",
  "message": "SkillHub 预下单失败，可使用 payment_retry_token 重试，不会重复创建知识星球订单。",
  "out_trade_no": "90000000000000000001",
  "order_type": "membership_fee",
  "payment_retry_token": "MOCK_PAYMENT_RETRY_TOKEN",
  "payment": {
    "provider": "WEIXINPAY",
    "pay_data": {
      "type": "prepay_id",
      "value": "MOCK_PREPAY_ID"
    },
    "out_trade_no": "90000000000000000001",
    "payment_retry_token": "MOCK_PAYMENT_RETRY_TOKEN",
    "expires_at": 4102444800
  }
}
```

优先从顶层 `payment_retry_token` 读取恢复凭据；顶层缺失时可读取 `payment.payment_retry_token`。两处同时存在但值不一致，或两处均缺失/为空时停止并报告，不得重发订单 `body`。恢复凭据的 `expires_at` 同样是 Unix 秒级时间戳；过期后停止。

## 宿主微信支付授权

收到 `PAYMENT_REQUIRED` 后，直接按以下协议请求支付授权，无需访问外部接入文档：

1. 分别读取 `_meta.WeixinPay.WeixinPay-Required` 和 `payment.payment_code`。前者缺失或为空（包括 `_meta: {}`）时回退到后者；两处同时存在但值不一致时停止并报告；两处均缺失或为空时也停止，不得以空支付码调用支付工具。
2. 原样保留支付码，不解码、不修改、不向用户展示。若宿主提供官方 `weixinpay_pay`，仅将该支付码作为 `paymentCode` 参数调用：

```text
weixinpay_pay(paymentCode="<WeixinPay-Required 的原值>")
```

3. 宿主展示微信支付卡片后，将支付决定交给用户本人。agent 不得代替用户点击确认、自动授权或把创建订单时的确认视为支付授权。
4. 将 `out_trade_no` 原样保存为字符串，但不要把它传给 `weixinpay_pay`，也不得转换为数值。支付能力调用完成只表示已发起或处理授权流程；支付是否成功及订单是否履约，以知识星球原支付回调或业务页面状态为准。

以下情况必须停止，不得自动再次创建订单：

- 宿主没有官方 `weixinpay_pay`，或无法识别支付元数据：保留 `out_trade_no`，告知用户需在支持 Skill Pay 的宿主中完成支付。
- 用户取消或拒绝授权，支付能力返回失败，或当前 Unix 秒值大于等于响应中的 `expires_at`：报告当前状态并停止。
- 支付能力返回结果无法确定是否支付成功：不得声称成功，也不得仅凭用户口头陈述重放订单请求；引导用户在知识星球业务页面核对。

## 推荐工作流

1. 确认当前宿主是 WorkBuddy 且提供官方 `weixinpay_pay`。否则在创建订单前说明限制并停止。
2. 查询并核对目标 ID。赞赏评论需同时取得 `topic_id` 和 `comment_id`；轻读查价需同时取得 `group_id` 和 `back_issue_id`。按[下单前查询价格](#下单前查询价格)取得或计算固定价格，按逐类型传参规则整理必要字段，向用户以“元”展示对象、基础价/折扣（如适用）、应付金额和等值星球币；四类用户定价订单按[金额换算规则](#金额换算规则)将用户指定的元金额精确换算为整数分，再同时确认元值和 `amount`。
3. 使用 `call_zsxq_api` 创建订单。不要用 CLI `api raw` 绕过支付元数据；除付费提问和赞赏外，不要把查询或计算出的价格作为 `amount` 传入订单。
4. 收到 `PAYMENT_REQUIRED` 后，按[宿主微信支付授权](#宿主微信支付授权)处理支付码和 `out_trade_no`，由用户本人在微信支付卡片中确认。
5. 支付完成后的状态与履约由知识星球原支付链路处理。没有官方查单能力时，如实说明无法在本工具内核验，不要重复创建订单。
6. 只有收到 `SKILLHUB_PREORDER_FAILED` 时，才按下方恢复请求重试 SkillHub 预下单：

```json
{
  "method": "POST",
  "path": "/v2/wechat_orders",
  "payment_retry_token": "<原响应中的签名凭据>",
  "out_trade_no": "<原响应中的订单号>"
}
```

恢复请求必须省略 `body`。路径仍为 `/v2/wechat_orders`；不得重新发送原订单 body，否则可能创建重复订单。`out_trade_no` 可省略；若提供，只能原样使用响应中的字符串。

## 失败语义

- 知识星球创建订单失败：不进入 SkillHub 预下单，按原接口错误处理。
- `PAYMENT_REQUIRED`：订单已创建、待用户支付，不是工具失败；不要自动重试创建订单。
- `SKILLHUB_PREORDER_FAILED`：知识星球订单**已经创建**，仅 SkillHub 预下单失败；使用返回的 `payment_retry_token` 恢复，服务端不会再次创建知识星球订单。
- `ZSXQ_ORDER_PARSE_FAILED` / `PAYMENT_RETRY_TOKEN_FAILED`：订单可能已经创建，但无法安全进入支付流程；停止并报告，不得盲目重试创建。
- 用户取消、拒绝或支付卡片过期：停止，不得自动重新下单。用户明确要求重试时，重新确认金额和对象后再决定是否创建新订单。

## 错误说明

| 错误 | 原因与处理 |
|------|------------|
| `PAYMENT_REQUIRED`（402） | 正常支付挑战；交给支付宿主展示微信支付卡片 |
| `SKILLHUB_PREORDER_FAILED`（502） | 知识星球订单已创建；使用 `payment_retry_token` 原路径恢复，禁止重发订单 body |
| `SKILLHUB_NOT_CONFIGURED`（503） | SkillHub 支付配置不可用；联系服务管理员，不会创建知识星球订单 |
| `PAYMENT_RETRY_TOKEN_REQUIRED` | 单独提供了 `out_trade_no`；必须同时提供有效的 `payment_retry_token` |
| `INVALID_PAYMENT_RETRY_TOKEN` | 恢复凭据无效或已过期；停止，禁止凭订单号猜测恢复 |
| `PAYMENT_RETRY_ORDER_MISMATCH` | `out_trade_no` 与签名凭据不匹配；核对原响应，禁止继续 |
| `ZSXQ_ORDER_PARSE_FAILED` | 上游订单响应缺少受支持的支付凭据或订单号；停止并报告 |
| 优惠后价格、资格或风控类接口错误 | 加入/续期价格不满足平台规则，或用户/星球/赞赏对象不符合下单条件；展示原始 `code` / `info`，不要改价重试 |

通用错误（401、参数缺失等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [Skill Pay 购买场景](scenarios/purchase-with-skill-pay.md) — 从购买意图到支付挑战的完整编排
- [group-list](group-list.md) — 查询 `group_id`
- [topic-detail](topic-detail.md) — 核对主题及 `topic_id`
- [user-info](user-info.md) — 当前登录用户信息
- [SKILL.md](../SKILL.md) — 能力索引与支付安全规则
