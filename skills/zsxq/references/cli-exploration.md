# 探索模式（CLI 通道）

当用户需求未命中已注册的场景或原子操作时，进入探索模式：通过 CLI 帮助和 API 列表发现能力。CLI 通道下 CLI 是能力真相源；MCP 通道下 [endpoint-catalog](endpoint-catalog.md) 是能力真相源。

CLI 通道按下文探索；MCP 通道没有 `api list` / `--help`，能力底表为上文 endpoint-catalog：底表与 [SKILL.md](../SKILL.md) 索引均未覆盖即视为平台暂无此能力，停止并考虑提示 NPS 反馈，不得臆造 path。

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

### 响应裁剪（shape / fields）

底层接口工具 `call_zsxq_api` 支持两个可选的响应裁剪参数（需新版服务端；旧版会静默忽略、不报错），用于压缩大响应、节省上下文：

```bash
# shape：按命名预设裁剪主实体（全部预设：topic.brief、topic.excerpt、
# comment.brief、member.brief、hashtag.brief、checkin.brief、column.brief、
# file.brief、image.brief、article.brief、group.brief、note.brief、user.brief）
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/groups/12345/topics","query":{"count":"10"},"shape":"topic.brief"}'

# fields：逗号分隔的点路径字段投影（相对于 body.resp_data），数组逐元素投影；
# 未匹配的路径进 _unknown_fields 提示而不报错；可与 shape 叠加（先 shape 后 fields）
zsxq-cli api call call_zsxq_api --params '{"method":"GET","path":"/v2/groups/12345/topics","query":{"count":"10"},"fields":"topics.topic_id,topics.title"}'
```

shape 的实体名**必须与响应的主实体匹配**：预设按 `resp_data` 下与实体同名的键定位（单数对象或复数列表），如评论接口要用 `comment.brief` 而非 `topic.brief`。**用错实体不报错但也不裁剪**（原样返回）；预设名拼错则请求发出前即报错并列出可用值。常用端点的实测对照：

| 端点（path） | 适用 shape | 裁剪后字段（实测） |
|---|---|---|
| `/v2/groups/{id}/topics` 等主题列表/详情 | `topic.brief` | topic_id、type、title、content、create_time、owner、group、counts、digested、sticky、images、files、annotation、text_type、creation_statement、modify_time、stick_time（17 个） |
| 同上 | `topic.excerpt` | topic_id、type、title、content、create_time、owner、group、counts、digested、sticky、images_count、files_count（12 个，附件只留计数） |
| `/v2/topics/{id}/comments` | `comment.brief` | comment_id、text、create_time、owner、likes_count |
| `/v2/groups/{id}/members` | `member.brief` | user_id、name、avatar_url、join_time |
| `/v2/groups/{id}/hashtags` | `hashtag.brief` | hashtag_id、title、topics_count |
| `/v2/groups` | `group.brief` | group_id、name、type、owner、background_url、risk_level、statistics |
| `/v2/users/self/notes` | `note.brief` | note_id、text、create_time、owner、likes_count、comments_count、reference 等（11 个） |
| 任意响应中的用户对象 | `user.brief` | user_id、name、avatar_url |

其余预设（checkin/column/file/image/article.brief）作用于对应实体的响应；需要确定性裁剪时用 `fields` 精确指定路径。

> [!IMPORTANT]
> `shape`/`fields` 是 `call_zsxq_api` 的顶层工具参数，**不是**上游 HTTP 参数。不要放进 `api raw` 的 `--query`/`--body`——新版 CLI 会直接报错（旧版 CLI 会透传给上游并被静默忽略，返回未裁剪数据）。MCP 通道的语义见 [endpoint-catalog](endpoint-catalog.md) 通用约定。

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
- MCP 通道探索发现的写法若值得沉淀，应先在 [endpoint-catalog](endpoint-catalog.md) 登记端点，再新增/更新原子 reference
- 探索多次失败、确认平台没有该能力时，考虑提示用户提交 NPS 反馈（见 [user-nps](user-nps.md)）

## 参考

- [auth-errors](auth-errors.md) — 认证与常见错误
- [SKILL.md](../SKILL.md) — 已注册能力索引
