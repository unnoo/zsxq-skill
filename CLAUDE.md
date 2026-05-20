# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

zsxq-skill is the official skill package for `zsxq-cli` (知识星球 CLI). It contains **documentation-only skill definitions** — no application code, no build system, no tests. All files are Markdown.

The skills are consumed by AI agents (Claude Code, Cursor, OpenClaw) to learn how to operate the 知识星球 platform via `zsxq-cli`.

## Architecture

```
skills/
├── zsxq-shared/SKILL.md          # 共享基础：认证、API 调用规范、链接拼接、安全规则、通用错误码
├── zsxq-group/                    # 星球管理：+list, +topics, +hashtags
├── zsxq-topic/                    # 主题管理：+search, +detail, +create, +edit, +reply, +answer, +delete（通过 api raw）
├── zsxq-user/                     # 用户信息与反馈：+info, +footprints, +nps
└── zsxq-note/                     # 笔记管理：+create, +list, +detail, +edit, +delete
```

Each skill directory follows a fixed structure:
- `SKILL.md` — YAML frontmatter (name, version, description, metadata) + 顶部按需提示（首次/401 时读 shared）+ Core Concepts + Resource Relationships + Shortcuts 表 + API 表（如有）
- `references/<skill>-<verb>.md` — per-command reference doc（按下文统一模板）

## Key Conventions

### SKILL.md frontmatter format

```yaml
---
name: zsxq-<domain>
version: 1.3.0
description: "触发描述（中文，含关键词以便 AI 匹配触发）"
metadata:
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli <domain> --help"
---
```

`description` 字段直接决定 AI 何时触发该 skill，修改时确保包含所有相关操作的关键词。当前所有 SKILL.md 版本统一为 `1.3.0`，新一轮跨 skill 改动时一起 bump。

### SKILL.md body 顶部按需提示

domain SKILL.md 顶部不再写"必须先读 shared"，改为按需触发：

```markdown
> 首次使用或遇到认证错误（401 / token 过期 / `not logged in`）时，先读 [`../zsxq-shared/SKILL.md`](../zsxq-shared/SKILL.md) 了解登录与 API 调用约定。日常调用已登录账户时无需每次重读。
```

reference 文档**不重复**这条提示（之前每个 reference 顶部都有"前置条件"行已统一删除），只在与 shared 相关的字段（如错误说明 fallback）里链接回去。

### Reference doc 统一模板

reference 顶部不再加"前置条件"行（避免与 SKILL.md 顶部提示重复）。

**写入/删除类**（create / edit / reply / answer / delete / nps）顺序：

```
# 标题（如 # topic +create（发布主题））
描述（一句话说明做什么）

> [!CAUTION]   <-- 写入/删除必须有，列出执行前需向用户确认的项目
> [!IMPORTANT] <-- 如有特殊约束（如"只能编辑自己的"、"每题只能回答一次"）

## 命令              <-- 至少给一个最小可用示例；多文件、多形式按需补充
## 参数              <-- 表格：参数 / 必填 / 说明
## 输出              <-- 如非纯成功提示则给示例（JSON 示例避免 // 注释）
## 推荐工作流        <-- 一个标准流程；过渡步骤（"获取 X"、"查找待 X"）作为这一节的子步骤
## 失败语义          <-- 一句话描述失败是否原子回滚
## 错误说明          <-- 仅列特有错误；末尾 fallback 一行到 shared#常见错误处理
## 参考              <-- 相关 reference / shared 链接
```

**只读类**（list / detail / search / info / footprints / topics / hashtags / ...）顺序：

```
# 标题
描述
## 命令
## 参数
## 输出（表格模式）  <-- 表头与 CLI 实际输出一致
## 说明              <-- 命令特性、限制、与近义命令的差异（如 footprints vs group +topics）
## 错误说明          <-- 仅列特有错误；末尾 fallback 一行到 shared#常见错误处理
## 参考
```

> JSON 示例不写 `// 注释`，因为标准 JSON 不支持。需要解释字段时另起一段或用列表说明。

### 错误说明信息分层

shared `## 常见错误处理` 表是通用错误（401、403、404、参数缺失、`--end-time` 解析失败）的唯一来源。下游 reference 的「错误说明」节遵守：

- 只列**该命令特有**的错误（如 `--score must be 0–10`、`code: 100262`、`问题已回答`）
- 表格末尾追加一行 fallback：「通用错误（401、参数缺失等）见 [zsxq-shared](../../zsxq-shared/SKILL.md#常见错误处理)。」
- 如果该命令没有任何特有错误，错误说明节只写 fallback 一行

### Two types of CLI operations

1. **Shortcuts** (`zsxq-cli <domain> +<verb>`) — 高级封装命令，有专属 reference doc，在 SKILL.md 的 Shortcuts 表注册
2. **API calls** — 分两种：
   - `zsxq-cli api call <tool> --params '<json>'` — 调用底层接口工具，在 SKILL.md 的 API 表注册
   - `zsxq-cli api raw --method <METHOD> --path <path>` — 原始 HTTP 调用（如 DELETE），单列「原始 HTTP 调用」小节并链接 reference doc

> 措辞约定：不使用「MCP 工具」/「MCP 未封装」等内部实现术语，统一用「底层接口工具」/「原始 HTTP 接口」面向用户描述。

### Safety rules

- 写入（create / edit / reply / answer / nps）和删除（delete）的 reference doc 必须包含 `> [!CAUTION]` 块，列出执行前需向用户确认的具体项目
- shared `## 安全规则` 节给出 token、写入意图确认、ID 查询前置等通用规则；reference 不重复
- 当心可见性陷阱：笔记（Note）是公开内容，**任何持有链接的人都可访问**；description / reference / SKILL.md 三处需保持一致

## Adding a New Operation

1. 在 `skills/<domain>/references/` 下创建 `zsxq-<domain>-<verb>.md`，按"Reference doc 统一模板"组织小节顺序
2. 在 `skills/<domain>/SKILL.md` 中注册：
   - Shortcut 加到 Shortcuts 表
   - 通过 `api call` 暴露的高级操作加到 API 表
   - 通过 `api raw` 暴露的操作单列在「原始 HTTP 调用」小节，命令模板加表格 + reference 链接
3. 如果是新操作类型或新关键词，更新 SKILL.md frontmatter 的 `description` 以包含新关键词
4. 错误：通用错误归 shared，新增的命令特有错误才写在 reference 的「错误说明」节