import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import official_skill as og


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def config_for(root: Path, **official_overrides) -> dict:
    official = {
        "output": "dist/official/zsxq",
        "name": "zsxq",
        "description": "测试描述",
        "exclude": ["scripts/**"],
        "limits": {
            "body_bytes": 32768,
            "resource_bytes": 16384,
            "resource_count": 50,
            "total_bytes": 262144,
            "description_bytes": 1024,
        },
        "residualForbidden": ["zsxq-cli", "scripts/", "npm ", "npx ", "node "],
    }
    official.update(official_overrides)
    return {"_root": str(root), "source": "skills/zsxq", "official": official}


SKILL = """---
name: zsxq
description: "长描述"
metadata:
  version: "3.2.0"
  channels: "cli / mcp"
  cliHelp: "zsxq-cli --help"
---

# zsxq
"""


class ConfigTest(unittest.TestCase):
    def test_exclude_directory_glob(self):
        self.assertTrue(og.is_excluded("scripts/scenarios/x.js", ["scripts/**"]))
        self.assertTrue(og.is_excluded("references/scenarios/a/b.md",
                                       ["references/scenarios/a/**"]))
        self.assertFalse(og.is_excluded("references/a.md",
                                        ["references/scenarios/a/**"]))

    def test_collect_files_separates_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "skills/zsxq/SKILL.md", SKILL)
            write(root / "skills/zsxq/references/a.md", "# a\n")
            write(root / "skills/zsxq/scripts/x.js", "x")
            included, excluded = og.collect_files(
                root, root / "skills/zsxq", ["scripts/**"])
            self.assertEqual(included, ["SKILL.md", "references/a.md"])
            self.assertEqual(excluded, ["scripts/x.js"])

    def test_validate_sizes_rejects_oversize_resource(self):
        limits = og.Limits(32768, 16, 50, 262144, 1024)
        with self.assertRaises(og.BuildError):
            og.validate_sizes({"SKILL.md": "x", "a.md": "y" * 17}, limits)

    def test_validate_sizes_rejects_too_many_resources(self):
        limits = og.Limits(32768, 16, 1, 262144, 1024)
        with self.assertRaises(og.BuildError):
            og.validate_sizes({"SKILL.md": "x", "a.md": "y", "b.md": "z"}, limits)


class NamingTest(unittest.TestCase):
    def test_load_config_requires_output_basename_equal_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "skill-package.json"
            path.write_text(json.dumps(config_for(root), ensure_ascii=False),
                            encoding="utf-8")
            self.assertEqual(
                og.load_config(path)["official"]["output"], "dist/official/zsxq")
            path.write_text(
                json.dumps(config_for(root, output="dist/official/zsxq-official"),
                           ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(og.BuildError):
                og.load_config(path)

    def test_build_rejects_frontmatter_name_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "skills/zsxq/SKILL.md",
                  SKILL.replace("name: zsxq", "name: zsxq-legacy"))
            with self.assertRaises(og.BuildError):
                og.build(config_for(root))


class BuildTest(unittest.TestCase):
    def test_build_writes_only_markdown_and_skips_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "skills/zsxq/SKILL.md", SKILL)
            write(root / "skills/zsxq/references/a.md", "# a\n")
            write(root / "skills/zsxq/scripts/x.js", "x")
            report = og.build(config_for(root))
            out = root / "dist/official/zsxq"
            self.assertTrue((out / "SKILL.md").exists())
            self.assertTrue((out / "references/a.md").exists())
            self.assertFalse((out / "scripts").exists())
            self.assertEqual(report.files["references/a.md"], 4)
            self.assertTrue((root / "dist/official/report.json").exists())

    def test_build_rejects_non_markdown_outside_exclude(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "skills/zsxq/SKILL.md", SKILL)
            write(root / "skills/zsxq/logo.png", "x")
            with self.assertRaises(og.BuildError):
                og.build(config_for(root))


class CliRegionTest(unittest.TestCase):
    def test_strip_removes_only_marked_region(self):
        text = "A\n<!-- cli-only:start -->\nCLI\n<!-- cli-only:end -->\nB\n"
        self.assertEqual(og.strip_cli_regions(text).strip(), "A\nB")

    def test_strip_rejects_unclosed_region(self):
        with self.assertRaises(og.BuildError):
            og.strip_cli_regions("<!-- cli-only:start -->\nCLI\n")

    def test_strip_rejects_unpaired_end(self):
        with self.assertRaises(og.BuildError):
            og.strip_cli_regions("X\n<!-- cli-only:end -->\n")


class FrontmatterTest(unittest.TestCase):
    def test_sanitize_replaces_description_and_removes_cli_help(self):
        text = og.sanitize_frontmatter(SKILL, "官方描述")
        self.assertIn('description: "官方描述"', text)
        self.assertNotIn("cliHelp", text)
        self.assertIn('channels: "mcp（call_zsxq_api）"', text)
        self.assertIn('version: "3.2.0"', text)

    def test_sanitize_requires_description(self):
        broken = "---\nname: zsxq\n---\n\n# x\n"
        with self.assertRaises(og.BuildError):
            og.sanitize_frontmatter(broken, "官方描述")


DUAL_PARAMS = """## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 星球 ID |
| `--json` | 否 | 输出 JSON |
| `--files <paths>` | 否 | 附件 |
| `--ai` / `--ai-mode` | 否 | AI 声明 |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--group-id` | path `/v2/groups/{group_id}/topics` |
| `--files` | 仅 CLI 通道（附件上传缺口） |
| `--ai` / `--ai-mode` | `req_data.creation_statement` |
"""

RAW_PARAMS = """## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `<group_id>` | **是** | 星球 ID |
| `scope` | 否 | 范围 |
| `count` | **是** | 数量 |

### 通道映射

| CLI 形式 | HTTP 字段 |
|----------|-----------|
| `<group_id>`（路径） | path `/v2/groups/{group_id}/checkins` |
| `--query` JSON | 同名 query 参数 |
"""

ESCAPED_PIPE_PARAMS = """## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic-id <id>` | **是** | 主题 ID |
| `--digested true\\|false` | 否 | 是否设为精华（`true` 设置 / `false` 取消）；不传则保持现状 |
| `--sticky true\\|false` | 否 | 是否置顶（`true` 置顶 / `false` 取消）；不传则保持现状 |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--topic-id` | path `/v2/topics/{topic_id}` |
| `--digested true\\|false` | `req_data.digested` |
| `--sticky true\\|false` | `req_data.sticky` |
"""

NON_FIELD_PARAMS = """## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--limit <n>` | 否 | 最多返回数量 |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--limit` | 不上送（由工具在本地校验与截断） |
"""

DUP_FIELD_PARAMS = """## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--ai` | 否 | 声明 AI 生成 |
| `--ai-mode <mode>` | 否 | 声明模式：`aigc` / `none` |

### 通道映射

| CLI flag | HTTP 字段 |
|----------|-----------|
| `--ai` / `--ai-mode` | `req_data.creation_statement` |
"""


class ParamMergeTest(unittest.TestCase):
    def test_cli_flags_merge_to_fields_and_cli_only_rows_drop(self):
        merged = og.merge_official_params(DUAL_PARAMS, "topic.md")
        self.assertIn("path `/v2/groups/{group_id}/topics`", merged)
        self.assertIn("`req_data.creation_statement`", merged)
        self.assertNotIn("--json", merged)
        self.assertNotIn("--files", merged)
        self.assertNotIn("### 通道映射", merged)
        self.assertIn("| 字段 / 位置 | 必填 | 说明 |", merged)

    def test_raw_http_params_are_preserved(self):
        merged = og.merge_official_params(RAW_PARAMS, "checkins.md")
        self.assertIn("| `<group_id>` | **是** |", merged)
        self.assertIn("| `scope` | 否 |", merged)
        self.assertNotIn("--query", merged)
        self.assertNotIn("### 通道映射", merged)

    def test_unmapped_flag_fails(self):
        text = DUAL_PARAMS.replace(
            "| `--group-id` | path `/v2/groups/{group_id}/topics` |\n", "")
        with self.assertRaises(og.BuildError):
            og.merge_official_params(text, "topic.md")

    def test_missing_mapping_requires_mcp_only_marker(self):
        text = DUAL_PARAMS.split("### 通道映射")[0]
        with self.assertRaises(og.BuildError):
            og.merge_official_params(text, "topic.md")
        marked = "<!-- params:mcp-only -->\n\n" + text
        self.assertEqual(og.merge_official_params(marked, "topic.md"), marked)

    def test_mapping_only_field_is_appended(self):
        text = RAW_PARAMS.replace(
            "| `--query` JSON | 同名 query 参数 |",
            "| `--query` JSON | 同名 query 参数 |\n| `--scope` | `query.scope` |",
        )
        merged = og.merge_official_params(text, "checkins.md")
        self.assertIn("`query.scope`", merged)

    def test_escaped_pipe_keeps_cells_and_fields(self):
        merged = og.merge_official_params(ESCAPED_PIPE_PARAMS, "topic-set.md")
        self.assertIn("| `req_data.digested` | 否 | 是否设为精华", merged)
        self.assertIn("| `req_data.sticky` | 否 | 是否置顶", merged)
        self.assertNotIn("`false` | false`", merged)
        rows = [line for line in merged.split("\n")
                if line.startswith("|") and not line.startswith("|---")
                and not line.startswith("| 字段 / 位置")]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(len(og._split_row(row)), 3, row)

    def test_non_field_mapping_drops_row(self):
        merged = og.merge_official_params(NON_FIELD_PARAMS, "group-list.md")
        self.assertNotIn("不上送", merged)
        self.assertIn("该操作无额外 MCP 参数", merged)

    def test_duplicate_field_rows_merge_into_one(self):
        merged = og.merge_official_params(DUP_FIELD_PARAMS, "topic.md")
        hits = [line for line in merged.split("\n")
                if line.startswith("| `req_data.creation_statement`")]
        self.assertEqual(len(hits), 1)
        self.assertIn("声明 AI 生成", hits[0])
        self.assertIn("声明模式：`aigc` / `none`", hits[0])

    def test_merged_table_keeps_blank_line_before_next_heading(self):
        text = RAW_PARAMS + "\n## 输出\n\n正文\n"
        merged = og.merge_official_params(text, "checkins.md")
        self.assertIn("\n\n## 输出", merged)

    def test_shape_check_rejects_wrong_column_count(self):
        with self.assertRaises(og.BuildError):
            og._check_shape([["a", "b"]], "x.md")
        og._check_shape([["a", "b", "c"]], "x.md")


class LinkAndResidualTest(unittest.TestCase):
    def test_prune_drops_row_when_all_links_excluded(self):
        texts = {
            "SKILL.md": "| 场景 | 入口 |\n|---|---|\n"
                        "| 视频 | [x](video.md) |\n"
                        "| 巡场 | [y](patrol.md) |\n"
        }
        out, dropped = og.prune_table_rows(texts, {"video.md"})
        self.assertNotIn("video.md", out["SKILL.md"])
        self.assertIn("patrol.md", out["SKILL.md"])
        self.assertEqual(len(dropped), 1)

    def test_prune_rejects_mixed_row(self):
        texts = {"SKILL.md": "| [x](video.md) [y](patrol.md) |\n"}
        with self.assertRaises(og.BuildError):
            og.prune_table_rows(texts, {"video.md"})

    def test_prune_rejects_non_table_excluded_link(self):
        texts = {"SKILL.md": "见 [x](video.md)\n"}
        with self.assertRaises(og.BuildError):
            og.prune_table_rows(texts, {"video.md"})

    def test_check_links_rejects_dead_link(self):
        with self.assertRaises(og.BuildError):
            og.check_links({"SKILL.md": "[x](missing.md)"})

    def test_check_links_accepts_anchor_and_http(self):
        og.check_links({"SKILL.md": "[x](#a) [y](https://example.com)"})

    def test_check_residual_rejects_cli_tokens_and_flags(self):
        texts = {"SKILL.md": "run zsxq-cli topic +create --group-id 1\n"}
        with self.assertRaises(og.BuildError):
            og.check_residual(texts, ["zsxq-cli"])


if __name__ == "__main__":
    unittest.main()
