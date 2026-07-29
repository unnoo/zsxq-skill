#!/usr/bin/env python3
"""zsxq-skill 文档静态校验器。

从仓库根运行：python3 scripts/check-docs.py

检查项：
  1. 相对链接可达（skills/ 与 docs/ 下所有 md 的 [..](rel) 链接不死链）
  2. 场景文件含 H1 + CLAUDE.md 规定的 10 个小节
  3. 写入/删除类 reference（含 > [!CAUTION]）结构完整（命令/参数/错误说明/参考）
  4. 验证报告与日志：已存在的 docs/verification/<id>.md 结构完整、其引用的日志文件存在
  5. 提示（warning，不失败）：带 CAUTION 的写操作 reference 尚无验证报告

退出码：有 error 返回 1，否则 0（warning 不影响退出码）。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "zsxq")
REF = os.path.join(SKILL, "references")
SCEN = os.path.join(REF, "scenarios")
VERIF = os.path.join(ROOT, "docs", "verification")

LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

SCENARIO_SECTIONS = [
    "## 适用意图", "## 不适用情况", "## 所需输入", "## 使用的原子操作",
    "## 执行流程", "## 分支与停止条件", "## 用户确认点", "## 完成标准",
    "## 失败与回退", "## 附加资源",
]
WRITE_REF_SECTIONS = ["## 命令", "## 参数", "## 错误说明", "## 参考"]
REPORT_SECTIONS = ["## 测试用例", "## 结论"]

errors, warns, checked_links = [], [], 0


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def rel(path):
    return os.path.relpath(path, ROOT)


def check_links(path):
    """校验一个 md 内的相对链接是否可达。"""
    global checked_links
    txt = read(path)
    base = os.path.dirname(path)
    for m in LINK.finditer(txt):
        tgt = m.group(1).strip()
        if tgt.startswith(("http://", "https://", "#", "mailto:")):
            continue
        relpart = tgt.split("#", 1)[0]
        if not relpart:
            continue
        checked_links += 1
        abspath = os.path.normpath(os.path.join(base, relpart))
        if not os.path.exists(abspath):
            errors.append(f"[死链] {rel(path)} -> {tgt}")


def walk_md(root):
    out = []
    for dp, _, fs in os.walk(root):
        for fn in fs:
            if fn.endswith(".md"):
                out.append(os.path.join(dp, fn))
    return out


# 1. 所有 md 的相对链接（skills/ + docs/）；模板文件（_ 开头）含占位符，跳过链接检查
all_md = []
for base in (SKILL, os.path.join(ROOT, "docs")):
    if os.path.isdir(base):
        all_md += walk_md(base)
for p in all_md:
    if os.path.basename(p).startswith("_"):
        continue
    check_links(p)

# 2. 场景文件 H1 + 10 节
for fn in sorted(os.listdir(SCEN)):
    if not fn.endswith(".md"):
        continue
    txt = read(os.path.join(SCEN, fn))
    if not txt.lstrip().startswith("# "):
        errors.append(f"[无H1] scenarios/{fn}")
    for sec in SCENARIO_SECTIONS:
        if sec not in txt:
            errors.append(f"[缺节] scenarios/{fn} 缺 {sec}")

# 3. 写入/删除类 reference（含 CAUTION）结构完整 + 4. 是否有验证报告
write_refs = []
for fn in sorted(os.listdir(REF)):
    if not fn.endswith(".md"):
        continue
    p = os.path.join(REF, fn)
    txt = read(p)
    if "> [!CAUTION]" not in txt:
        continue
    write_refs.append(fn)
    for sec in WRITE_REF_SECTIONS:
        if sec not in txt:
            errors.append(f"[缺节] references/{fn} 缺 {sec}")

# 5. 验证报告：已存在的报告结构完整 + 引用的日志存在；写操作缺报告→warn
def report_exists(rid):
    return os.path.exists(os.path.join(VERIF, f"{rid}.md"))

if os.path.isdir(VERIF):
    for fn in sorted(os.listdir(VERIF)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        p = os.path.join(VERIF, fn)
        txt = read(p)
        for sec in REPORT_SECTIONS:
            if sec not in txt:
                errors.append(f"[报告缺节] docs/verification/{fn} 缺 {sec}")
        logf = os.path.join(VERIF, "logs", fn[:-3] + ".log")
        if not os.path.exists(logf):
            errors.append(f"[缺日志] docs/verification/{fn} 无配套 logs/{fn[:-3]}.log")

for fn in write_refs:
    rid = fn[:-3]
    if not report_exists(rid):
        warns.append(f"写操作 references/{fn} 尚无验证报告 docs/verification/{rid}.md（新增/修改此操作时应补）")

# 汇总
print(f"扫描 {len(all_md)} 个 md，校验 {checked_links} 条相对链接，"
      f"识别 {len(write_refs)} 个写操作 reference。\n")
if errors:
    print("❌ 发现问题：")
    for e in errors:
        print("  -", e)
else:
    print("✓ 无死链、场景 10 节齐全、写操作 reference 结构完整、验证报告与日志配套。")
if warns:
    print("\n⚠️ 提示（不影响退出码）：")
    for w in warns:
        print("  -", w)
sys.exit(1 if errors else 0)
