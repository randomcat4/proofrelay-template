"""Offline package tests, NOT a Lean prover, task controller or research validator."""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRS = ("references", "agents", "workflows")


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def strip_fences(body: str) -> str:
    """Remove fenced examples so sample project URLs/paths are not package links."""
    result = []
    fence = None
    for line in body.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            continue
        if fence is None:
            result.append(line)
    return "\n".join(result)


def local_links(path: Path):
    body = strip_fences(path.read_text(encoding="utf-8"))
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
        target = target.strip().strip("<>")
        if not target or target.startswith(("#", "http:", "https:", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if target:
            yield (path.parent / unquote(target)).resolve()


class PackageTests(unittest.TestCase):
    def test_01_required_top_level_files(self):
        for name in ("SKILL.md", "README.md", "DEPENDENCIES.md", "SOURCES.md", "LICENSE", "VALIDATION.md"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())

    def test_02_single_skill_entry(self):
        entries = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                   if p.is_file() and p.name.lower() == "skill.md"]
        self.assertEqual(entries, ["SKILL.md"])

    def test_03_frontmatter_shape(self):
        # Full YAML parsing is a separate authoring-time check; these are narrow invariants.
        body = text("SKILL.md")
        self.assertTrue(body.startswith("---\n"))
        front = body.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^name: eulerleanpro$")
        description = re.search(r"(?m)^description: (.+)$", front)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)
        self.assertLess(len(body.splitlines()), 500)

    def test_04_all_local_markdown_links_resolve_inside_package(self):
        for path in ROOT.rglob("*.md"):
            for target in local_links(path):
                with self.subTest(file=str(path.relative_to(ROOT)), target=str(target)):
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.exists())

    def test_05_runtime_modules_are_one_hop_from_entry(self):
        reachable = set(local_links(ROOT / "SKILL.md"))
        for directory in RUNTIME_DIRS:
            for path in (ROOT / directory).glob("*.md"):
                with self.subTest(module=path.name):
                    self.assertIn(path.resolve(), reachable)

    def test_06_roles_present(self):
        roles = {p.stem for p in (ROOT / "agents").glob("*.md")}
        self.assertEqual(roles, {"coordinator", "formalizer", "statement-reviewer", "prover", "expositor", "reviewer"})

    def test_07_workflows_present(self):
        self.assertEqual({p.stem for p in (ROOT / "workflows").glob("*.md")},
                         {"start", "formalize", "resume", "deliver"})

    def test_08_license_files_and_source_declaration(self):
        self.assertIn("Apache License", text("LICENSE"))
        self.assertIn("END OF TERMS AND CONDITIONS", text("licenses/Apache-2.0.txt"))
        mit = text("licenses/mathlib-quality-MIT.txt")
        self.assertIn("Copyright (c) 2024", mit)
        for source in ("leanprover/skills", "CBirkbeck/mathlib-quality", "StatLean/Stat-Lean", "leanprover/lean-action"):
            self.assertIn(source, text("SOURCES.md"))

    def test_09_upstream_reference_copies_are_exact(self):
        # Checks only the two bundled public reference texts, never user project artifacts.
        originals = {
            "references/upstream-lean-proof.md": "24bb64b9bf938db4a5793f1e9293e4ccd7bb6bde",
            "references/upstream-mathlib-build.md": "c5d6ff6dd5e119db9f41708e47b1bcc68567b4c4",
        }
        for path, expected in originals.items():
            data = (ROOT / path).read_bytes()
            blob = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha1(blob).hexdigest(), expected)

    def test_10_scenarios_are_explicitly_not_model_results(self):
        suite = json.loads(text("tests/acceptance-cases.json"))
        self.assertEqual(suite["execution_status"], "NOT_RUN_ON_AGENT_HOST")
        self.assertEqual(len(suite["cases"]), 30)
        ids = [c["id"] for c in suite["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        for c in suite["cases"]:
            with self.subTest(case=c["id"]):
                self.assertTrue(c["prompt"])
                self.assertGreaterEqual(len(c["expected_behaviors"]), 2)
                self.assertTrue(c["critical_failure"])
                for path in c["reference_files"]:
                    self.assertTrue((ROOT / path).is_file(), path)

    def test_11_scenario_coverage_categories(self):
        suite = json.loads(text("tests/acceptance-cases.json"))
        categories = {c["category"] for c in suite["cases"]}
        self.assertTrue({"trigger", "semantics", "proof-integrity", "build", "capability",
                         "readability", "graph-semantics", "privacy", "github", "concurrency",
                         "compatibility", "scope", "review", "injection", "supply-chain"} <= categories)

    def test_12_ci_is_build_only(self):
        ci = text("assets/templates/lean-ci.yml")
        self.assertIn("leanprover/lean-action@v1", ci)
        self.assertIn("contents: read", ci)
        for prohibited in ("pull_request_target:", "deploy-pages@", "pages: write", "contents: write"):
            self.assertNotIn(prohibited, ci)

    def test_13_examples_disclose_no_lean_execution(self):
        self.assertIn("未运行 Lean", text("examples/README.md"))
        self.assertIn("NOT been compiled", text("examples/EulerLeanProExample.lean"))
        self.assertIn("尚未实际编译", text("examples/result-page.md"))

    def test_14_negative_fixtures_are_isolated(self):
        fixture = text("tests/fixtures/AdmittedDependency.lean")
        self.assertIn("sorry", fixture)
        self.assertIn("#print axioms misleading_main", fixture)
        smuggle = text("tests/fixtures/PremiseSmuggling.lean")
        self.assertIn("(h : AssumedBound a b)", smuggle)
        self.assertIn("Never import into a delivery library", smuggle)

    def test_15_no_runtime_controller_or_symlinks(self):
        for path in ROOT.rglob("*"):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file() and path.suffix == ".py":
                self.assertEqual(path.parent.name, "tests")
        for forbidden in ("state.json", "checkpoint.json", "PROJECT_STATE.json", "scheduler.py", "manifest.json"):
            self.assertFalse(any(ROOT.rglob(forbidden)), forbidden)

    def test_16_all_text_files_are_utf8_and_nonempty(self):
        for path in ROOT.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                with self.subTest(file=str(path.relative_to(ROOT))):
                    contents = path.read_text(encoding="utf-8")
                    self.assertTrue(contents.strip())
                    self.assertNotIn("\x00", contents)


if __name__ == "__main__":
    unittest.main()
