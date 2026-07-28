# CLI 探索与直接调用 API

当用户需求未命中已注册的场景或原子操作时，进入探索模式：通过 CLI 帮助和 API 列表发现能力。CLI 是能力真相源。

## 探索顺序

按以下顺序逐层深入，找到能满足需求的调用方式即停止：

1. `zsxq-cli --help` — 查看所有 domain 和全局命令
2. `zsxq-cli <domain> --help` — 查看该 domain 的 shortcut 列表
3. `zsxq-cli api list` — 列出所有可用底层接口工具及参数
4. `zsxq-cli api call <tool> --params '<json>'` — 调用底层接口工具
5. `zsxq-cli api raw --method <METHOD> --path <path>` — 仅用于前述方式未覆盖的接口

> 已注册的原子操作和场景**不需要**探索 —— 直接按 reference 执行。仅在能力不匹配或调用失败时才回退到探索模式。

## api call

优先使用 `api call`：它是封装好的底层接口工具，参数以结构化 JSON 传入，比手写 `api raw` 的 method/path 更不易出错：

```bash
zsxq-cli api call get_self_info --params '{}'
zsxq-cli api call search_groups --params '{"keyword":"Go语言"}'
zsxq-cli api call get_user_footprints --params '{"user_id":"123456"}'
```

## api raw

`api raw` 用于 `api call` 尚未覆盖的接口，直接发起原始 HTTP 调用：

```bash
zsxq-cli api raw --method GET --path /v3/users/self
zsxq-cli api raw --method PUT --path /v2/topics/123 --body '{"text":"新内容"}'
```

> `--body` 支持简写，自动包装 `req_data`；响应已去除三层嵌套，直接返回数据内容。

## 探索约束

- 探索发现的**写入接口**仍须执行用户确认，`api raw` 写入不得绕过原子操作的安全约束（见 [SKILL.md 安全规则](../SKILL.md#安全规则)）
- 动态发现的结果不自动视为正式文档 —— 如某个探索出的用法值得沉淀，应新增原子操作 reference
- 探索多次失败、确认平台没有该能力时，考虑提示用户提交 NPS 反馈（见 [user-nps](user-nps.md)）

## 参考

- [auth-errors](auth-errors.md) — 认证与常见错误
- [SKILL.md](../SKILL.md) — 已注册能力索引
