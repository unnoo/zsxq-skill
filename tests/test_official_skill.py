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
  version: "3.1.0"
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
        self.assertIn('version: "3.1.0"', text)

    def test_sanitize_requires_description(self):
        broken = "---\nname: zsxq\n---\n\n# x\n"
        with self.assertRaises(og.BuildError):
            og.sanitize_frontmatter(broken, "官方描述")


if __name__ == "__main__":
    unittest.main()
