from __future__ import annotations

import fnmatch
import json
import posixpath
import re
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLI_START = "<!-- cli-only:start -->"
CLI_END = "<!-- cli-only:end -->"

TABLE_RE = r"\|[^\n]*\n\|[\s:|-]+\n(?:\|[^\n]*\n?)+"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FLAG_RE = re.compile(r"(?<!-)--[a-z][a-z0-9-]*")
CLI_ONLY_FLAGS = {"--json", "--files", "--markdown-file", "--help",
                  "--version", "--dry-run"}
COMPOSITE_FLAGS = {"--query", "--body"}
INFO_MARKER = "<!-- params:mcp-only -->"


class BuildError(Exception):
    pass


@dataclass(frozen=True)
class Limits:
    body_bytes: int
    resource_bytes: int
    resource_count: int
    total_bytes: int
    description_bytes: int


@dataclass
class Report:
    output: str
    files: dict[str, int]
    total_bytes: int
    limits: Limits
    dropped_rows: list[str] = field(default_factory=list)
    merged_params: int = 0

    def render(self) -> str:
        resources = len(self.files) - 1
        lines = [
            "官方 Skill 构建报告",
            f"输出目录: {self.output}",
            f"文件: {len(self.files)}（SKILL.md + {resources} 个资源）",
            f"总字节: {self.total_bytes} / {self.limits.total_bytes}"
            f"（剩余 {self.limits.total_bytes - self.total_bytes}）",
            f"合并参数表: {self.merged_params} 个文件",
        ]
        for rel in sorted(self.files):
            lines.append(f"  {self.files[rel]:7d}  {rel}")
        if self.dropped_rows:
            lines.append("被删除的表格行:")
            lines.extend(f"  - {row}" for row in self.dropped_rows)
        return "\n".join(lines)


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    config["_root"] = str(path.parent)
    for key in ("source", "official"):
        if key not in config:
            raise BuildError(f"配置缺少 {key}")
    official = config["official"]
    for key in ("output", "name", "description", "exclude", "limits",
                "residualForbidden"):
        if key not in official:
            raise BuildError(f"配置缺少 official.{key}")
    official["limits"] = Limits(**official["limits"])
    if not re.fullmatch(r"[a-z0-9-]{1,64}", official["name"]):
        raise BuildError("official.name 必须是小写字母、数字、连字符")
    if "\n" in official["description"] or '"' in official["description"]:
        raise BuildError("official.description 必须是单行且不含双引号")
    desc_bytes = len(official["description"].encode("utf-8"))
    if desc_bytes > official["limits"].description_bytes:
        raise BuildError(
            f"official.description {desc_bytes} 字节超过上限 "
            f"{official['limits'].description_bytes}"
        )
    return config


def is_excluded(rel: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**"):
            base = pattern[:-3]
            if rel == base or rel.startswith(base + "/"):
                return True
        elif fnmatch.fnmatchcase(rel, pattern):
            return True
    return False


def collect_files(root: Path, source: Path, exclude: list[str]) -> tuple[list[str], list[str]]:
    included: list[str] = []
    excluded: list[str] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        if is_excluded(rel, exclude):
            excluded.append(rel)
        else:
            included.append(rel)
    return included, excluded


def normalize_content(text: str) -> str:
    text = text.removeprefix("\ufeff")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_cli_regions(text: str) -> str:
    out: list[str] = []
    in_cli = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == CLI_START:
            if in_cli:
                raise BuildError("cli-only:start 嵌套")
            in_cli = True
            continue
        if stripped == CLI_END:
            if not in_cli:
                raise BuildError("出现未配对的 cli-only:end")
            in_cli = False
            continue
        if not in_cli:
            out.append(line)
    if in_cli:
        raise BuildError("cli-only:start 未闭合")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


def sanitize_frontmatter(text: str, description: str) -> str:
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        raise BuildError("SKILL.md 首行必须是 ---")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise BuildError("SKILL.md frontmatter 未闭合") from exc
    out: list[str] = []
    replaced = False
    for line in lines[1:end]:
        stripped = line.strip()
        if line.startswith("description:"):
            out.append(f'description: "{description}"')
            replaced = True
        elif stripped.startswith("cliHelp:"):
            continue
        elif stripped.startswith("channels:"):
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f'{indent}channels: "mcp（call_zsxq_api）"')
        else:
            out.append(line)
    if not replaced:
        raise BuildError("SKILL.md frontmatter 缺少 description")
    return "\n".join([lines[0], *out, *lines[end:]])


def _split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _parse_table(block: str) -> list[list[str]]:
    lines = [line for line in block.strip().split("\n")
             if line.strip().startswith("|")]
    if len(lines) < 2:
        raise BuildError("表格格式不正确")
    return [_split_row(line) for line in lines[2:]]


def _render_table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(out)


def _flags(cell: str) -> list[str]:
    return re.findall(r"--[a-z][a-z0-9-]*", cell)


def merge_official_params(text: str, rel: str) -> str:
    param = re.search(r"(## 参数[ \t]*\n\n)(" + TABLE_RE + ")", text)
    if not param:
        return text
    mapping = re.search(r"\n### 通道映射[ \t]*\n\n(" + TABLE_RE + ")", text)
    if not mapping:
        if INFO_MARKER in text:
            return text
        raise BuildError(
            f"{rel}: 「## 参数」缺少「### 通道映射」；"
            f"MCP 专用文档请加 {INFO_MARKER}"
        )

    param_rows = _parse_table(param.group(2))
    mapping_rows = _parse_table(mapping.group(1))
    flag_to_field: dict[str, str] = {}
    for row in mapping_rows:
        if len(row) < 2:
            raise BuildError(f"{rel}: 通道映射行列数不足")
        for flag in _flags(row[0]):
            flag_to_field[flag] = row[1]

    merged: list[list[str]] = []
    used: set[str] = set()
    for row in param_rows:
        if len(row) < 3:
            raise BuildError(f"{rel}: 参数行列数不足: {' | '.join(row)}")
        flags = _flags(row[0])
        if not flags:
            merged.append([row[0], row[1], row[2]])
            continue
        used.update(flags)
        if all(flag in CLI_ONLY_FLAGS for flag in flags):
            continue
        fields: list[str] = []
        skip = False
        for flag in flags:
            if flag not in flag_to_field:
                raise BuildError(f"{rel}: 参数 {flag} 缺少通道映射")
            field = flag_to_field[flag]
            if "仅 CLI 通道" in field:
                skip = True
                break
            fields.append(field)
        if skip:
            continue
        merged.append([" / ".join(dict.fromkeys(fields)), row[1], row[2]])

    for row in mapping_rows:
        flags = _flags(row[0])
        if not flags or any(flag in used for flag in flags):
            continue
        if all(flag in COMPOSITE_FLAGS for flag in flags):
            continue
        if "hidden" in row[0] or "不上送" in row[1] or "无对应字段" in row[1]:
            continue
        merged.append([row[1], "—", "通道映射补充字段"])

    if not merged:
        merged = [["—", "—", "该操作无额外 MCP 参数，字段见调用示例"]]

    without_mapping = text[: mapping.start()] + text[mapping.end():]
    without_mapping = re.sub(r"\n{3,}", "\n\n", without_mapping)
    param = re.search(r"(## 参数[ \t]*\n\n)(" + TABLE_RE + ")", without_mapping)
    if not param:
        raise BuildError(f"{rel}: 移除通道映射后找不到参数表")
    table = _render_table(["字段 / 位置", "必填", "说明"], merged)
    return (without_mapping[: param.start(2)] + table
            + without_mapping[param.end(2):])


def _resolve_link(rel: str, target: str) -> str | None:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0]
    if not target:
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))


def prune_table_rows(
    texts: dict[str, str], excluded: set[str]
) -> tuple[dict[str, str], list[str]]:
    out: dict[str, str] = {}
    dropped: list[str] = []
    for rel, text in texts.items():
        kept: list[str] = []
        for line in text.split("\n"):
            resolved = [
                target for target in (
                    _resolve_link(rel, raw) for raw in LINK_RE.findall(line)
                ) if target
            ]
            if not resolved:
                kept.append(line)
                continue
            hit = [target for target in resolved if target in excluded]
            if not hit:
                kept.append(line)
                continue
            if line.lstrip().startswith("|") and len(hit) == len(resolved):
                dropped.append(f"{rel}: {line.strip()}")
                continue
            raise BuildError(
                f"{rel}: 链接指向被排除文件或混合行: {line.strip()}")
        out[rel] = "\n".join(kept)
    return out, dropped


def check_links(texts: dict[str, str]) -> None:
    problems: list[str] = []
    for rel, text in sorted(texts.items()):
        for lineno, line in enumerate(text.split("\n"), 1):
            for raw in LINK_RE.findall(line):
                target = _resolve_link(rel, raw)
                if target is not None and target not in texts:
                    problems.append(f"{rel}:{lineno}: 死链 -> {raw}")
    if problems:
        raise BuildError("死链:\n" + "\n".join(problems))


def check_residual(texts: dict[str, str], forbidden: list[str]) -> None:
    problems: list[str] = []
    for rel, text in sorted(texts.items()):
        for lineno, line in enumerate(text.split("\n"), 1):
            for token in forbidden:
                if token in line:
                    problems.append(
                        f"{rel}:{lineno}: 残留 {token!r}: {line.strip()}")
            if FLAG_RE.search(line):
                problems.append(
                    f"{rel}:{lineno}: 残留 CLI flag: {line.strip()}")
    if problems:
        raise BuildError("CLI 残留:\n" + "\n".join(problems))


def validate_sizes(texts: dict[str, str], limits: Limits) -> None:
    if "SKILL.md" not in texts:
        raise BuildError("缺少 SKILL.md")
    if len(texts["SKILL.md"].encode("utf-8")) > limits.body_bytes:
        raise BuildError("SKILL.md 超过正文上限")
    resources = {rel: text for rel, text in texts.items() if rel != "SKILL.md"}
    if len(resources) > limits.resource_count:
        raise BuildError(
            f"资源 {len(resources)} 个超过上限 {limits.resource_count}")
    total = 0
    for rel, text in texts.items():
        size = len(text.encode("utf-8"))
        if rel != "SKILL.md" and size > limits.resource_bytes:
            raise BuildError(
                f"{rel} 大小 {size} 超过单资源上限 {limits.resource_bytes}")
        total += size
    if total > limits.total_bytes:
        raise BuildError(
            f"总字节 {total} 超过上限 {limits.total_bytes}")


def build(config: dict, check_only: bool = False) -> Report:
    root = Path(config["_root"])
    source = root / config["source"]
    official = config["official"]
    limits: Limits = official["limits"]
    if isinstance(limits, dict):
        limits = Limits(**limits)
        official["limits"] = limits
    included, excluded = collect_files(root, source, official["exclude"])

    texts: dict[str, str] = {}
    for rel in included:
        path = source / rel
        if path.suffix != ".md":
            raise BuildError(f"{rel}: 只允许 .md 文件")
        texts[rel] = normalize_content(path.read_text(encoding="utf-8"))
    if "SKILL.md" not in texts:
        raise BuildError("源目录缺少 SKILL.md")

    merged_params = 0
    for rel in list(texts):
        before = texts[rel]
        texts[rel] = merge_official_params(before, rel)
        if texts[rel] != before:
            merged_params += 1

    texts = {rel: strip_cli_regions(text) for rel, text in texts.items()}
    texts["SKILL.md"] = sanitize_frontmatter(
        texts["SKILL.md"], config["official"]["description"])

    texts, dropped = prune_table_rows(texts, set(excluded))
    texts = {rel: re.sub(r"\n{3,}", "\n\n", text)
             for rel, text in texts.items()}
    check_links(texts)
    check_residual(texts, config["official"]["residualForbidden"])

    validate_sizes(texts, limits)
    files = {rel: len(text.encode("utf-8")) for rel, text in texts.items()}
    total = sum(files.values())
    output = "(check mode)" if check_only else official["output"]
    if not check_only:
        out_dir = root / official["output"]
        if out_dir.exists():
            shutil.rmtree(out_dir)
        for rel, text in texts.items():
            path = out_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        report_path = out_dir.parent / "report.json"
        report_path.write_text(
            json.dumps({
                "output": official["output"],
                "files": files,
                "total_bytes": total,
                "limits": asdict(limits),
                "dropped_rows": [],
                "merged_params": merged_params,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return Report(output=output, files=files, total_bytes=total,
                  limits=limits, dropped_rows=dropped,
                  merged_params=merged_params)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="构建 Console 官方版 zsxq skill")
    parser.add_argument("--check", action="store_true",
                        help="在临时目录构建并校验，不写 dist/")
    parser.add_argument("--config", default=str(ROOT / "skill-package.json"))
    args = parser.parse_args()
    try:
        config = load_config(Path(args.config))
        report = build(config, check_only=args.check)
    except BuildError as exc:
        print(f"❌ 构建失败：\n{exc}")
        return 1
    print(report.render())
    return 0
