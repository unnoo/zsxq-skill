# MCP 通道端点目录（call_zsxq_api 能力底表）

MCP 通道下所有操作通过底层接口工具 `call_zsxq_api` 调用，参数形如 `{method, path, query?, body?}`。本表是唯一能力底表：**表中没有的端点不得臆造调用**；操作视角的参数约束与确认项以各原子 reference 为准。

通用约定：

- 写接口的 body 必须显式包 `req_data`：`body: {"req_data": {...}}`（工具不会自动包装）。
- 响应信封：`{success, status_code, body}`；业务数据在 `body.resp_data`，业务失败看 `body.succeeded == false` 与 `body.code` / `body.error`。权限拒绝（未开通 Skill 权限、查他人足迹等）不走信封，直接返回 `{success: false, error: "…"}`，无 `status_code`/`body`。
- 分页：列表接口用 `count` 控制条数、`end_time` 翻页；取本页最后一条的 `create_time` 原值作为下一页 `end_time`（评论接口用返回的 `index` 作下一页 `index`）。实测翻页边界会重复本页末条，需按 `topic_id` 去重。
- 时间格式：`scheduled_time` 等时间为 `2006-01-02T15:04:05.000+0800`（UTC+8，毫秒三位）。
- 下文 `{base}` 省略不写，path 以 `/v2/` 或 `/v3/` 开头。

## 只读端点

| 能力 | method | path | query / 说明 |
|------|--------|------|--------------|
| 当前用户信息 | GET | `/v2/users/self` | 无；返回 `body.resp_data.user.user_id` 供其他接口使用 |
| 我加入/创建的星球 | GET | `/v2/groups` | 无 query（CLI 的 `--limit`/`--scope` 只是工具层校验，不上送） |
| 星球最新主题 | GET | `/v2/groups/{group_id}/topics` | `count`（对应 CLI `--limit`，默认 20）；`end_time` 可选；`scope` 仅非 `all` 时传 |
| 星球标签 | GET | `/v2/groups/{group_id}/hashtags` | 无 |
| 标签下主题 | GET | `/v2/hashtags/{hashtag_id}/topics` | `count`、`with_hashtag=true`、`end_time` 可选 |
| 主题详情 | GET | `/v2/topics/{topic_id}/info` | 无。长文（`inline_article_url`）不做服务端回填，透传返回原始字段 |
| 主题评论 | GET | `/v2/topics/{topic_id}/comments` | `sort_type=by_interactions_count`、`count`、`with_sticky=false`、`index` 可选（翻页游标） |
| 用户足迹 | GET | `/v2/users/{user_id}/footprints` | `count`、`filter=all`；限定星球时 `filter=group&group_id={id}&filter_group_id={id}`；`end_time` 可选；仅可查本人 |
| 用户笔记列表 | GET | `/v2/users/{user_id}/footprints` | 同上但 `filter=note`；从 `footprints[]` 的 `note` 字段取笔记 |
| 搜索星球 | GET | `/v2/search/groups` | `keyword`、`scope=joined`、`count=4` |
| 搜索星球成员 | GET | `/v2/search/groups/{group_id}/members` | `keyword`、`count`（对应 `--limit`，≤50） |
| 星球内搜索主题 | GET | `/v2/search/groups/{group_id}/topics` | `keyword`、`count=20`。注意：这是官方搜索，与 CLI `topic +search` 的语义排序不同（CLI 走增强检索编排） |
| 我发起的提问 | GET | `/v2/users/self/topics/questions` | `filter`（`unanswered`/`answered`）、`count`、`end_time` 可选 |
| 向我发起的提问 | GET | `/v2/users/self/topics/answers` | 同上 |
| 定时任务列表 | GET | `/v2/groups/{group_id}/scheduled_jobs` | 无；任务数组在 `body.resp_data.jobs[]` |
| 定时任务配额统计 | GET | `/v2/groups/{group_id}/scheduled_jobs/statistics` | 无；需星主/管理员，否则 `权限不足` |
| 笔记详情 | GET | `/v2/notes/{note_id}` | 无 |
| 星球成员列表 | GET | `/v2/groups/{group_id}/members` | query 字段见 [group-members](group-members.md) |
| 星球专栏列表 | GET | `/v2/groups/{group_id}/columns` | 无 |
| 主题所属专栏 | GET | `/v2/topics/{topic_id}/attached_columns` | 无；需星主/管理员，否则 `权限不足` |
| 星球公开信息（查价） | GET | `/v2/groups/{group_id}/public_info` | 见 [wechat-order-create](wechat-order-create.md#下单前查询价格) |
| 星球详情（续费查价） | GET | `/v2/groups/{group_id}` | 同上 |
| 轻读详情（查价） | GET | `/v2/groups/{group_id}/back_issues/{back_issue_id}` | 同上 |

## 写入端点（均需用户确认，安全规则见 SKILL.md）

| 能力 | method | path | body（`req_data` 内字段） |
|------|--------|------|---------------------------|
| 发布主题（talk） | POST | `/v2/groups/{group_id}/topics` | `type:"talk"`、`text`；可选 `title`、`text_type:"markdown"`、`creation_statement`（`aigc`/`personal_perspective`/`none`）、`image_ids[]`、`file_ids[]`、`vote_uid`、`checkin_id`（数字） |
| 发布提问（q&a） | POST | `/v2/groups/{group_id}/topics` | `type:"q&a"`、`text`、`questionee_id`；可选 `anonymous:true`；不带 title/image/file/vote |
| 创建投票（发帖前置） | POST | `/v3/votes` | `title`、`options:[{title}]`；从响应取 `vote.uid` 作为发帖的 `vote_uid` |
| 编辑主题 | PUT | `/v2/groups/{group_id}/topics/{topic_id}` | 全量合并：`type`、`text`、`image_ids`、`file_ids`、`mentioned_user_ids:[]`、`creation_statement`；talk 有投票时带 `vote_uid`。先 GET 详情读取当前值再合并 |
| 评论 / 楼中楼 | POST | `/v2/topics/{topic_id}/comments` | `text`、`image_ids:[]`、`mentioned_user_ids:[]`；可选 `replied_comment_id`、`file_ids` |
| 回答提问 | POST | `/v2/topics/{topic_id}/answer` | `text`、`image_ids:[]` |
| 设置精华/置顶 | PUT | `/v2/topics/{topic_id}` | `digested:true/false` 或 `sticky:true/false`（只传要改的字段） |
| 设置主题标签 | PUT | `/v2/topics/{topic_id}` | `annotation`：把每个标签拼接为 `<e type="hashtag" hid="0" title="%23标签%23" />`（标签去空白、补 `#`、URL 编码后串联）；为完整标签集合，全量替换 |
| 定时发布主题 | POST | `/v2/groups/{group_id}/scheduled_jobs` | `topic:{text, image_ids?, file_ids?}`、`scheduled_time`。创建成功返回空 `resp_data`，`job_id` 需从列表接口读取 |
| 修改定时任务 | PUT | `/v2/groups/{group_id}/scheduled_jobs/{job_id}` | 同上；先 GET 列表找到该 job，保留未提供字段 |
| 定时回答 | POST | `/v2/groups/{group_id}/scheduled_jobs` | `answer:{topic_id, text, image_ids?, silenced?}`、`scheduled_time`；`group_id` 从主题详情读取。创建成功返回空 `resp_data`，`job_id` 从列表接口读取 |
| 取消定时任务 | DELETE | `/v2/groups/{group_id}/scheduled_jobs/{job_id}` | 无 body |
| 删除主题 | DELETE | `/v2/topics/{topic_id}` | 无 body，不可恢复 |
| 设置主题所属专栏 | POST | `/v2/topics/{topic_id}/attached_columns` | `column_ids:[...]`，全量替换 |
| 创建专栏 | POST | `/v2/groups/{group_id}/columns` | `name` |
| 修改星球设置 | PUT | `/v2/groups/{group_id}` | 可选 `name`、`description`、`background_url`、`promo_image_ids`（`[]` 清空） |
| 提交 NPS | POST | `/v2/nps` | `source:"ai_tool"`、`score`（1-10 整数）、`suggestion` |
| 创建笔记 | POST | `/v2/notes` | `text`、`image_ids:[]`；可选 `text_type` |
| 编辑笔记 | PUT | `/v2/notes/{note_id}` | `text`；可选 `image_ids`（整体替换；先 GET 读当前值） |
| 删除笔记 | DELETE | `/v2/notes/{note_id}` | 无 body，不可恢复 |
| 上传凭证（仅第一步） | POST | `/v2/uploads` | `type:"image"/"file"`、`size`（字节）；file 类型加 `name`；星球亮点图加 `usage:"promo"` |
| 创建微信订单 | POST | `/v2/wechat_orders` | 见 [wechat-order-create](wechat-order-create.md)（Skill Pay，仅 MCP 通道） |

## 通道缺口（仅 CLI 通道）

- **附件实际上传**：`POST /v2/uploads` 只拿到七牛 `upload_token`，第二步是 multipart 二进制直传七牛域名，不经过 MCP。含附件的操作（topic +create/+edit/+reply/+answer/+schedule、note +create/+edit、group +settings 的图片）在 MCP 通道只能发纯文本，或依赖宿主自行完成 multipart 上传后把 `image_ids`/`file_ids` 带入。
- **认证命令族**（auth login/logout/status、doctor、config show）：纯 CLI；MCP 通道的认证问题见 [auth-errors](auth-errors.md)。
- **能力发现**（`api list`、`--help`）：纯 CLI；MCP 通道以本目录为准。

## 参考

- [SKILL.md](../SKILL.md) — 执行通道判定与安全规则
- [cli-exploration](cli-exploration.md) — CLI 通道探索模式
- [auth-errors](auth-errors.md) — 认证与常见错误
