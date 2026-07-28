# 迁移旧版 skill（migrate-legacy-skills）

将本机安装的旧版 5 个知识星球 skill（`zsxq-shared`、`zsxq-group`、`zsxq-topic`、`zsxq-user`、`zsxq-note`）安全迁移到单一 `zsxq` skill。**默认只检查、只报告；移动或删除文件必须经用户显式确认。**

## 适用意图

- 「检查一下我装的知识星球 skill 有没有旧版」
- 「清理/迁移/卸载旧版 zsxq skill」
- 「升级到新版 zsxq skill」
- 安装新版后发现新旧 skill 并存、触发混乱

## 不适用情况

- 全新安装（机器上从未装过旧版）→ 直接按 INSTALL.md 安装，无需本场景
- 卸载 zsxq-cli 或退出登录 → 见 [auth-errors](../auth-errors.md)
- 用户想删除的是自建 skill（如自己写的日报、巡检 skill）→ 不属于本场景，按用户指示单独处理

## 所需输入

无必填输入。可选：用户指定只检查某个作用域（如「只看全局的」）。

## 使用的原子操作

本场景不调用 zsxq-cli，只做本地文件系统的检查与移动（`ls` / 读 frontmatter / `mv`）。

## 执行流程

### 第一步：扫描安装作用域

对以下目录逐一检查（不存在的跳过）：

| 平台 | 全局作用域 | 项目作用域 |
|------|-----------|-----------|
| Claude Code | `~/.claude/skills/` | `<项目>/.claude/skills/` |
| Codex | `~/.agents/skills/`（部分版本为 `~/.codex/skills/`） | `<项目>/.agents/skills/` |
| 其他（Cursor / OpenClaw 等） | 按该平台文档确认 skill 发现目录 | 同左 |

Codex 的发现目录随版本不同（`~/.agents/skills/` 与 `~/.codex/skills/` 都可能存在），两者都要检查；哪个真正被扫描以该机器上 Codex 的实际配置为准。无法确认发现目录的平台，跳过并在报告中标注「未扫描」，不做猜测。

### 第二步：精确识别旧 skill

判定标准（两条同时满足才算旧 skill）：

1. 目录名是以下五个之一：`zsxq-shared`、`zsxq-group`、`zsxq-topic`、`zsxq-user`、`zsxq-note`
2. 目录内 `SKILL.md` frontmatter 的 `name:` 字段与目录名一致

**禁止用 `zsxq-*` 通配匹配** —— 用户自建的 skill（如 `zsxq-daily-report`）不在迁移范围内，误删会破坏用户自己的工具。

补充判定规则：

- **符号链接**：发现目录下的条目若是符号链接（常见于多平台共享一份实体，如 `~/.claude/skills/zsxq-shared -> ~/.agents/skills/zsxq-shared`），对链接读取其指向实体的 `SKILL.md` 做上述判定；链接与实体分别记录在各自所在的作用域清单中
- **异常项**：目录名命中五旧名但 `name:` 字段不一致（或缺 SKILL.md）的目录，不列入迁移，但作为「异常项」写进报告提示用户人工核查 —— 它占用旧名，可能造成触发混乱

同时记录：新版 `zsxq` skill 是否已安装（存在 `zsxq/SKILL.md` 且 `name: zsxq`）。

### 第三步：检查自建 skill 的引用

在各作用域中，对**不属于**上述五个旧 skill 的其他 skill，检查其 **Markdown 文档中的相对路径引用**是否指向旧 skill 路径（如 `../zsxq-shared/SKILL.md`）。数据文件（`.tsv` / `.json` 等）里的字符串提及不算引用，忽略。命中的列入报告：这些链接在迁移后会失效，需要用户自行改指新版入口（如 `../zsxq/references/auth-errors.md`）。**不要代改用户自建 skill。**

### 第四步：展示迁移计划，等待确认

汇总报告给用户：

- 各作用域发现的旧 skill 清单（路径 + 版本号）
- 新版 `zsxq` 是否已安装；未安装则先按 INSTALL.md 安装，验证后再继续
- **可达性检查**：对每个含旧 skill 的作用域，确认移除旧 skill 后该作用域仍有可用的 `zsxq`（同作用域已装新版，或全局作用域已装新版可被该平台解析）。若某作用域移除后会「零 zsxq 能力」，在计划中标红，提示用户先在该作用域或全局安装新版
- 将要执行的动作：把旧 skill 目录移动到备份目录 `~/.zsxq-skill-backup/<日期时间>/<作用域标识>/`（在 skill 发现目录之外，不会被再次加载）
- 受影响的自建 skill 引用清单（如有）

**到这里为止是默认行为的终点。** 用户未明确同意前，不做任何移动或删除。

### 第五步：执行迁移（需用户确认后）

1. 创建备份目录 `~/.zsxq-skill-backup/<YYYYMMDD-HHMMSS>/`。在其中写一个 `manifest.tsv`，**每移动一项就追加一行**，记录还原所需的映射：
   ```
   原始绝对路径<TAB>备份内相对路径<TAB>类型(dir|symlink)<TAB>符号链接目标(仅 symlink)
   ```
   例如：`/Users/me/.claude/skills/zsxq-group<TAB>claude-global/zsxq-group<TAB>dir<TAB>`
2. 按 manifest 把旧 skill 条目移动到备份目录：**符号链接只移动链接本身**（用 manifest 记下它的原目标，保留其指向内容不动，待实体所在作用域处理时一并移动实体）；实体目录整体移动。备份内用 `<作用域标识>/<原目录名>` 的子路径避免同名冲突
3. 重新扫描各作用域，确认五个旧名（含链接与实体）一个都不再出现，且**每个安装了新版的作用域恰好发现一个 `zsxq`**、无旧名残留
4. 向用户报告结果：备份位置、`manifest.tsv` 路径、最终 skill 清单、需要手动更新的自建 skill 引用

## 分支与停止条件

- 未发现任何旧 skill → 报告「无需迁移」，结束
- 新版 `zsxq` 未安装且用户拒绝安装 → 停止，不动旧 skill（避免删旧后无可用版本）
- 某含旧 skill 的作用域移除后会「零 zsxq 能力」（该作用域和全局都没有新版）→ 提示用户先安装新版；用户坚持移除时明确告知该作用域将暂时不可用
- 用户只要检查报告 → 第四步结束
- 某作用域无写权限 → 跳过该作用域并在报告中标注，不中断其他作用域

## 用户确认点

1. 移动旧 skill 前：逐项列出将被移动的目录，取得明确同意
2. 新版未安装时：安装动作（`npx skills add`）执行前确认
3. 用户自建 skill 的引用修改：只报告，改不改由用户决定

## 完成标准

- 所有被扫描作用域中，五个旧 skill 名（含符号链接）精确匹配数为 0
- 每个安装了新版的作用域恰好发现一个 `zsxq` skill（多平台各装一份属正常）
- 移除旧 skill 的作用域均仍有可达的 `zsxq`（同作用域或全局），无「零能力」作用域
- 备份目录存在且含 `manifest.tsv` 与被移出的旧 skill（可按 manifest 回滚）

## 失败与回退

任何一步失败（移动出错、验证不通过、用户反悔）：读取备份目录的 `manifest.tsv`，把每行「备份内相对路径」的条目移回其「原始绝对路径」（symlink 行按记录的原目标重建链接），恢复迁移前状态。manifest 是回退的唯一依据，因此第五步必须先写 manifest 再移动。备份目录按日期时间命名，多次迁移互不覆盖。确认新版稳定后，用户可自行删除备份目录。

## 附加资源

- 安装指南：仓库 `INSTALL.md`（<https://github.com/unnoo/zsxq-skill/blob/main/INSTALL.md>）
- 认证与常见错误：[auth-errors](../auth-errors.md)
