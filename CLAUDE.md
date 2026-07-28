# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

zsxq-skill is the official skill package for `zsxq-cli` (知识星球 CLI). It contains **documentation-only skill definitions** — no application code, no build system, no tests. All files are Markdown (scenario scripts under `scripts/`, when added, are the only executable code).

The skill is consumed by AI agents (Claude Code, Codex, Cursor, OpenClaw) to learn how to operate the 知识星球 platform via `zsxq-cli`.

> Codex/Cursor/OpenClaw 等 agent 通过 [`AGENTS.md`](AGENTS.md) 指向本文件；本文件是面向所有 agent 的唯一开发指南，文中 "Claude Code" 可泛指当前所用 agent。

## Architecture

只发布**一个** `zsxq` skill：

```
skills/zsxq/
├── SKILL.md                 # 触发、执行模式路由、能力索引、全局安全规则
├── references/
│   ├── auth-errors.md       # 认证、通用错误表、CLI 未安装恢复
│   ├── cli-exploration.md   # 探索模式：--help / api list / api call / api raw
│   ├── share-links.md       # 分享链接拼接模板
│   ├── <domain>-<verb>.md   # 原子操作 reference（group-list、topic-create …）
│   └── scenarios/
│       └── <scenario-id>.md # 场景入口（如 migrate-legacy-skills.md）
├── scripts/scenarios/<scenario-id>/   # 场景脚本（确定性代码，按需）
└── assets/scenarios/<scenario-id>/    # 场景模板/静态资源（按需）
```

- `SKILL.md` 只负责触发、路由、能力索引和全局安全规则；命令细节全部在 reference 按需加载
- 场景目录中**不得**创建 `SKILL.md`，避免被识别为独立 skill

### 执行模式（写文档时须维持这个路由结构）

```
命中场景 -> 按场景入口文档编排
否则命中原子操作 -> 读对应 reference 直接执行
否则 -> 探索模式（cli-exploration.md）
```

原子操作和场景执行时不得预先运行无关的 `doctor`、`--help` 或 `api list`；仅在能力不匹配或调用失败时回退到探索模式。

## Key Conventions

### SKILL.md frontmatter format

```yaml
---
name: zsxq
description: "触发描述（中文，含关键词以便 AI 匹配触发）"
metadata:
  version: 2.0.0
  requires:
    bins: ["zsxq-cli"]
  cliHelp: "zsxq-cli --help"
---
```

`description` 字段直接决定 AI 何时触发该 skill，修改时确保包含所有相关操作的关键词（含场景触发语）。

### Reference doc 统一模板

reference 顶部不加"前置条件"行；认证/登录相关内容统一在 `auth-errors.md`，不在各 reference 重复。

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
## 错误说明          <-- 仅列特有错误；末尾 fallback 一行到 auth-errors.md#常见错误处理
## 参考              <-- 相关 reference / SKILL.md 链接
```

**只读类**（list / detail / search / info / footprints / topics / hashtags / ...）顺序：

```
# 标题
描述
## 命令
## 参数
## 输出（表格模式）  <-- 表头与 CLI 实际输出一致
## 说明              <-- 命令特性、限制、与近义命令的差异（如 footprints vs group +topics）
## 错误说明          <-- 仅列特有错误；末尾 fallback 一行到 auth-errors.md#常见错误处理
## 参考
```

> JSON 示例不写 `// 注释`，因为标准 JSON 不支持。需要解释字段时另起一段或用列表说明。

### 错误说明信息分层

`references/auth-errors.md` 的 `## 常见错误处理` 表是通用错误（401、403、404、参数缺失、`--end-time` 解析失败、CLI 未安装）的唯一来源。下游 reference 的「错误说明」节遵守：

- 只列**该命令特有**的错误（如 `--score must be 1–10`、`code: 100262`、`问题已回答`）
- 表格末尾追加一行 fallback：「通用错误（401、参数缺失等）见 `[auth-errors](auth-errors.md#常见错误处理)`。」
- 如果该命令没有任何特有错误，错误说明节只写 fallback 一行

### Two types of CLI operations

1. **Shortcuts** (`zsxq-cli <domain> +<verb>`) — 高级封装命令，有专属 reference doc，在 SKILL.md 对应 domain 的 Shortcuts 表注册
2. **API calls** — 分两种：
   - `zsxq-cli api call <tool> --params '<json>'` — 调用底层接口工具，在 SKILL.md 的 API 表注册
   - `zsxq-cli api raw --method <METHOD> --path <path>` — 原始 HTTP 调用（如 DELETE），单列「原始 HTTP 调用」小节并链接 reference doc

> 措辞约定：不使用「MCP 工具」/「MCP 未封装」等内部实现术语，统一用「底层接口工具」/「原始 HTTP 接口」面向用户描述。

### Safety rules

- 写入（create / edit / reply / answer / nps）和删除（delete）的 reference doc 必须包含 `> [!CAUTION]` 块，列出执行前需向用户确认的具体项目
- SKILL.md `## 安全规则` 节给出 token、写入意图确认、ID 查询前置、`api raw` 不绕过约束等全局规则；reference 不重复
- 当心可见性陷阱：笔记（Note）是公开内容，**任何持有链接的人都可访问**；description / reference / SKILL.md 三处需保持一致

## Adding a New Operation

1. 在 `skills/zsxq/references/` 下创建 `<domain>-<verb>.md`，按"Reference doc 统一模板"组织小节顺序
2. 在 `skills/zsxq/SKILL.md` 中注册：
   - Shortcut 加到对应 domain 的 Shortcuts 表
   - 通过 `api call` 暴露的高级操作加到 API 表
   - 通过 `api raw` 暴露的操作单列在「原始 HTTP 调用」小节，命令模板加表格 + reference 链接
   - 快速索引表加一行
3. 如果是新操作类型或新关键词，更新 SKILL.md frontmatter 的 `description` 以包含新关键词
4. 错误：通用错误归 `auth-errors.md`，新增的命令特有错误才写在 reference 的「错误说明」节

## Adding a New Scenario

场景必须同时满足：表达业务目标（而非单个 CLI 动作）；需要组合 ≥ 2 个独立操作或包含稳定的复杂处理逻辑。查 ID、确认内容、验证结果属于原子操作的前后置步骤，不单独算场景。

1. 场景 ID 用小写英文连字符、「动词 + 业务结果」（如 `summarize-recent-topics`），不加 `scenario-` 前缀、不用序号
2. 创建稳定入口 `skills/zsxq/references/scenarios/<scenario-id>.md`，按以下小节组织：

```
# 场景名称
## 适用意图
## 不适用情况
## 所需输入
## 使用的原子操作
## 执行流程
## 分支与停止条件
## 用户确认点
## 完成标准
## 失败与回退
## 附加资源
```

3. 简单场景只用入口文件；复杂场景保持入口不变，附加文档放 `references/scenarios/<scenario-id>/`，脚本放 `scripts/scenarios/<scenario-id>/`，静态资源放 `assets/scenarios/<scenario-id>/`
4. 在 SKILL.md 的「场景（Scenarios）」表注册入口 + 触发语；快速索引表加一行；description 补充触发关键词
5. 场景只负责编排；命令参数和错误语义以原子操作 reference 为唯一来源
6. 场景脚本要求：显式输入不猜 ID、结构化输入输出、不读写 token、非零退出码表示失败、写入类提供 dry-run 且保留用户确认、完成实际运行验证。简单 CLI 编排不得封装为脚本
