"""Validate real copied distributions, including deliberately broken ones."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class DistributionValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "plugin"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(
            ".git", ".claude", ".venv", "__pycache__", ".pytest_cache"))

    def run_validator(self):
        script = self.root / "scripts/validate.py"
        self.assertTrue(script.is_file(), "distribution validator not implemented")
        return subprocess.run([sys.executable, str(script)], cwd=self.temp.name,
                              text=True, capture_output=True)

    def assert_rejected(self, fragment):
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(fragment, result.stdout + result.stderr)

    def edit_json(self, name, mutate):
        path = self.root / name
        data = json.loads(path.read_text())
        mutate(data)
        path.write_text(json.dumps(data))

    def test_clean_export_resolves_and_registers(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        smoke = subprocess.run([sys.executable, str(self.root / "__init__.py")],
                               cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(smoke.returncode, 0, smoke.stderr)

    def test_missing_shared_reference_rejected(self):
        (self.root / "references/execution.md").unlink()
        self.assert_rejected("references/execution.md")

    def test_missing_helper_skill_rejected(self):
        shutil.rmtree(self.root / "skills/tdd")
        self.assert_rejected("tdd")

    def test_frontmatter_name_must_match_directory(self):
        path = self.root / "skills/shaping/SKILL.md"
        path.write_text(path.read_text().replace("name: shaping", "name: wrong"))
        self.assert_rejected("name")

    def test_invalid_yaml_scalar_rejected(self):
        path = self.root / "skills/shaping/SKILL.md"
        path.write_text(path.read_text().replace("name: shaping", "name: [shaping]"))
        self.assert_rejected("frontmatter")

    def test_version_drift_rejected(self):
        self.edit_json(".codex-plugin/plugin.json",
                       lambda d: d.update(version="9.0.0"))
        self.assert_rejected("version")

    def test_marketplace_identity_drift_rejected(self):
        self.edit_json(".agents/plugins/marketplace.json",
                       lambda d: d["plugins"][0].update(name="grove"))
        self.assert_rejected("mascah-skills")

    def test_release_target_must_exist(self):
        self.edit_json("release-please-config.json", lambda d:
                       d["packages"]["."]["extra-files"].append("cli/grove/__init__.py"))
        self.assert_rejected("release target")

    def test_release_updater_must_target_version_field(self):
        self.edit_json("release-please-config.json", lambda d:
                       d["packages"]["."]["extra-files"][0].update(jsonpath="$.absent"))
        self.assert_rejected("release updater")

    def test_explicit_missing_skill_invocation_rejected(self):
        path = self.root / "skills/implement/SKILL.md"
        path.write_text(path.read_text() + "\nInvoke `missing-helper` before delivery.\n")
        self.assert_rejected("missing skill invocation")

    def test_malformed_manifest_shape_reports_structured_error(self):
        (self.root / ".claude-plugin/plugin.json").write_text("[]")
        self.assert_rejected("ERROR: manifest metadata")

    def test_hermes_inventory_drift_rejected(self):
        path = self.root / "__init__.py"
        path.write_text(path.read_text().replace('"tdd",', '"absent-helper",'))
        self.assert_rejected("Hermes")

    def test_broken_anchor_rejected(self):
        path = self.root / "skills/shaping/SKILL.md"
        path.write_text(path.read_text() + "\n[missing](../../references/workflow.md#absent)\n")
        self.assert_rejected("anchor")

    def test_escape_from_package_rejected(self):
        path = self.root / "skills/shaping/SKILL.md"
        path.write_text(path.read_text() + "\n[outside](../../../external.md)\n")
        self.assert_rejected("outside package")

    def test_retired_runtime_instruction_rejected(self):
        path = self.root / "skills/implement/SKILL.md"
        path.write_text(path.read_text() + "\nRun `grove status` before changes.\n")
        self.assert_rejected("retired")


if __name__ == "__main__":
    unittest.main()
