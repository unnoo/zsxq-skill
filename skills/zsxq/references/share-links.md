# 分享链接拼接

当用户需要分享星球或主题链接时，使用以下模板拼接。输出时同时提供电脑端和手机端。

## 主题链接

- 电脑端：`https://wx.zsxq.com/group/{group_id}/topic/{topic_id}`
- 手机端：`https://wx.zsxq.com/mweb/views/topicdetail/topicdetail.html?topic_id={topic_id}&group_id={group_id}`

## 星球链接

- 电脑端：`https://wx.zsxq.com/group/{group_id}`
- 手机端：`https://wx.zsxq.com/mweb/views/topic/topic.html?group_id={group_id}`

## 说明

- `group_id` / `topic_id` 均为纯数字，不确定时先用 [group-list](group-list.md) / [topic-search](topic-search.md) 查询确认
- 笔记（Note）暂无稳定的分享链接拼接模板：`note +create` / `note +detail` 只返回 `note_id`、`text`、`create_time`，没有 URL 字段。不要凭 `note_id` 臆造链接；如用户需要笔记分享地址，让其在客户端「分享」处获取

## 参考

- [group-list](group-list.md) — 获取 group_id
- [topic-detail](topic-detail.md) — 获取主题信息
