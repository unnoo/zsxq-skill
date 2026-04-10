---
name: zsxq-note
version: 1.1.0
description: "知识星球笔记管理：创建个人文字笔记、查看笔记列表。当用户需要在知识星球记录个人笔记、随手记录想法、或查看历史笔记时使用。"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli note --help"
---

# note (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md)，其中包含认证、错误处理规则。**

## Core Concepts

- **笔记（Note）**：个人私密（或特定权限）的文字记录，仅支持纯文本，不支持图片。与主题（Topic）不同，笔记是个人维度的内容。

## Shortcuts（推荐优先使用）

| Shortcut | 说明 |
|----------|------|
| [`+create`](references/zsxq-note-create.md) | 创建一条个人文字笔记，仅支持纯文本 |
| [`+list`](references/zsxq-note-list.md) | 查看自己的笔记列表，支持分页 |
