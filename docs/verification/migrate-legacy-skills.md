# 验证报告：migrate-legacy-skills

| 项 | 值 |
|----|----|
| 被测文档 | `references/scenarios/migrate-legacy-skills.md` |
| 分类 | 本地文件系统场景（迁移/清理旧版 zsxq skill，**不触网、不调 CLI 写接口**） |
| zsxq-cli 版本 | v0.4.9（本场景不依赖 CLI 写操作） |
| 测试日期 | 2026-07-29 |
| 测试对象 | 本机 `~/.claude/skills/` 与 `~/.agents/skills/` 真实安装状态 |
| 原始日志 | [`logs/migrate-legacy-skills.log`](logs/migrate-legacy-skills.log) |
| 授权 | 只读探查本地安装目录；**未执行任何 mv/rm**（场景在"新版未安装"处即停，符合默认边界） |

## 测试用例

> 主干：识别旧版 skill → 确认新版已安装 → 移除旧版。本机新版 zsxq **未安装**，故主干在"确认新版"处按设计停止，不进入移动/删除。

| # | 用例（意图） | 执行的命令 | 预期 | 实际（真实输出摘录） | 结论 |
|---|------------|-----------|------|---------------------|------|
| 1 | 识别旧版 skill 安装位置与形态 | `ls -la ~/.claude/skills/` | 列出已装 skill | 旧版 5 个（`zsxq-group/-topic/-note/-comment/-shared`）均为 **symlink → `~/.agents/skills/<name>`** | ✅ |
| 2 | 核对旧版实体与版本 | `cat ~/.agents/skills/zsxq-*/SKILL.md`（读 frontmatter） | name/version 可读 | 5 个实体 `name:` 与目录名一致，version 均 `1.3.1` | ✅ |
| 3 | 区分"旧版 skill"与"自建 skill" | 对照 5 个旧版名单 | 自建 skill 不被误纳入迁移 | `zsxq-check-group`、`zsxq-daily-report` 为自建，**不在** 5 名单内 → 正确排除 | ✅ |
| 4 | 确认新版 zsxq 是否已安装 | `ls ~/.claude/skills/zsxq ~/.agents/skills/zsxq` | 判定新版状态 | 两处均 **不存在**新版单一 `zsxq` skill | ✅ |
| 5 | 分支判定：新版未安装 → 停在移动前 | （场景分支逻辑） | 不执行任何 mv/rm，仅产出报告 | 命中"新版未安装"停止条件；**未执行**删除/移动，输出待迁移清单 | ✅（安全停止） |
| 6 | 边界：symlink 形态的处理提示 | （读场景对 symlink 的说明） | 提示 symlink vs 实体差异 | 旧版是 symlink，删除 symlink 不动实体；场景应提示用户 `~/.agents/skills` 下实体去留 | ✅ 已在报告体现 |

## 实测校准了哪些文档假设

- **旧版真实形态是 symlink 而非目录实体**：`~/.claude/skills/zsxq-*` 全部指向 `~/.agents/skills/<name>`。迁移/清理时删 symlink ≠ 删实体，场景须区分两层（本机实测确认这一形态，场景描述应显式覆盖 symlink 情形）。
- **"旧版 skill"判定应基于固定 5 名单**：`zsxq-group/-topic/-note/-comment/-shared`。自建的 `zsxq-check-group`、`zsxq-daily-report` 名字前缀相同但**不属**旧版套件，不能因前缀 `zsxq-` 就纳入迁移——实测验证了按精确名单排除的必要性。
- **默认停止边界正确**：新版未安装时，场景停在"报告待迁移清单"而不擅自删除旧版——保证不会出现"旧版删了、新版没装"的空窗。实测命中该分支且未产生副作用。

## 安全测试策略

- **策略**：纯只读探查（`ls`/`cat`），**零 mv、零 rm**。
- **为何不执行迁移**：本机新版 `zsxq` 未安装，场景默认边界即"新版未安装 → 停在移动前"。若强行删旧版会造成"两版皆无"的可用性缺口，违背场景设计；故遵循停止条件不动文件。
- **net-zero**：未改动 `~/.claude/skills` 与 `~/.agents/skills` 任何条目，本机安装状态与测试前一致。

## 未覆盖 / 已知风险

- **实际移动/删除路径未执行**（新版未安装即停，属场景设计边界而非缺陷）。完整回填条件：先安装新版 `zsxq`，再在隔离环境跑"识别→确认新版→移除旧版 symlink→保留/清理实体"全链路，验证移动的幂等与回滚提示。
- symlink 指向的实体（`~/.agents/skills/*`）删除策略需用户确认——场景应在"用户确认点"明确"删 symlink 还是连实体一起删"，本次未到该步。

## 结论

**通过（按默认停止边界安全停止）。**

旧版识别、实体版本核对、自建 skill 排除、新版存在性判定四步均按文档工作；命中"新版未安装 → 停在移动前"分支并零副作用停止，符合场景设计。实测校准出"旧版为 symlink 形态""按 5 名单精确排除自建 skill"两点，建议在场景文档显式覆盖。移动/删除路径受限于"新版未装"边界未执行，回填条件已写明。
