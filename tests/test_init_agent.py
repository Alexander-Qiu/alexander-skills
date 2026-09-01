import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_AGENT = REPO_ROOT / "scripts" / "init-agent.py"
ROOT_INSTALL = REPO_ROOT / "install.sh"


class InitAgentTests(unittest.TestCase):
    def run_installer(self, *args, home: Path, check: bool = True):
        env = os.environ.copy()
        env.pop("CODEX_HOME", None)
        env.pop("CLAUDE_HOME", None)
        env["HOME"] = str(home)
        return subprocess.run(
            [sys.executable, str(INIT_AGENT), "--repo", str(REPO_ROOT), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )

    def test_codex_default_profile_installs_only_curated_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = self.run_installer("--agent", "codex", home=home)

            codex_home = home / ".codex"
            self.assertIn("Installed codex profile default", result.stdout)
            self.assertTrue((codex_home / "skills" / "pdf").is_symlink())
            self.assertEqual(
                (codex_home / "skills" / "pdf").resolve(),
                (REPO_ROOT / "skills" / "pdf").resolve(),
            )
            self.assertTrue((codex_home / "skills" / "docx").is_symlink())
            self.assertTrue((codex_home / "skills" / "swarming-with-luna").is_symlink())
            self.assertTrue((codex_home / "skills" / "humanizer").is_symlink())
            self.assertTrue((codex_home / "skills" / "humanizer-zh").is_symlink())
            self.assertEqual(
                (codex_home / "skills" / "humanizer").resolve(),
                (REPO_ROOT / "third-party" / "humanizer").resolve(),
            )
            self.assertEqual(
                (codex_home / "skills" / "humanizer-zh").resolve(),
                (REPO_ROOT / "third-party" / "humanizer-zh").resolve(),
            )
            self.assertFalse((codex_home / "skills" / "pua").exists())
            self.assertFalse((codex_home / "skills" / "brainstorming").exists())
            self.assertFalse((codex_home / "prompts" / "pua.md").exists())

    def test_claude_code_default_profile_installs_skills_without_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = self.run_installer(
                "--agent",
                "claude-code",
                "--skip-plugins",
                home=home,
            )

            claude_home = home / ".claude"
            self.assertIn("Installed claude-code profile default", result.stdout)
            self.assertTrue((claude_home / "skills" / "pdf").is_symlink())
            self.assertTrue((claude_home / "skills" / "docx").is_symlink())
            self.assertTrue((claude_home / "skills" / "humanizer").is_symlink())
            self.assertTrue((claude_home / "skills" / "humanizer-zh").is_symlink())
            self.assertFalse((claude_home / "skills" / "Claudeception").exists())
            self.assertFalse((claude_home / "skills" / "swarming-with-luna").exists())
            self.assertFalse((claude_home / "plugins").exists())

    def test_claude_code_dry_run_lists_plugin_commands_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = self.run_installer(
                "--agent",
                "claude-code",
                "--profile",
                "plugins",
                "--dry-run",
                home=home,
            )

            self.assertIn("DRY RUN", result.stdout)
            self.assertIn(
                "claude plugin marketplace add anthropics/claude-plugins-official",
                result.stdout,
            )
            self.assertIn("claude plugin install code-review@claude-plugins-official", result.stdout)
            self.assertNotIn("superpowers@claude-plugins-official", result.stdout)
            self.assertFalse((home / ".claude").exists())

    def test_optional_frontend_profile_installs_only_frontend_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            self.run_installer("--agent", "codex", "--profile", "frontend", home=home)

            skills = home / ".codex" / "skills"
            self.assertTrue((skills / "frontend-design").is_symlink())
            self.assertTrue((skills / "frontend-slides").is_symlink())
            self.assertFalse((skills / "docx").exists())

    def test_missing_source_preflight_leaves_no_partial_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            manifest_path = root / "manifest.json"
            manifest = json.loads((REPO_ROOT / "manifests" / "skills.json").read_text(encoding="utf-8"))
            manifest["skills"]["missing-test-skill"] = {"source": "skills/does-not-exist"}
            manifest["profiles"]["codex"]["broken"] = {
                "skills": ["pdf", "missing-test-skill"]
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = self.run_installer(
                "--agent",
                "codex",
                "--profile",
                "broken",
                "--manifest",
                str(manifest_path),
                home=home,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing source path", result.stderr)
            self.assertFalse((home / ".codex" / "skills" / "pdf").exists())

    def test_existing_non_link_target_is_not_overwritten_without_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            existing = home / ".codex" / "skills" / "pdf"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("user content", encoding="utf-8")

            result = self.run_installer("--agent", "codex", home=home, check=False)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to replace existing non-symlink", result.stderr)
            self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "user content")

    def test_replace_regular_directory_requires_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            existing = home / ".codex" / "skills" / "pdf"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("user content", encoding="utf-8")

            result = self.run_installer(
                "--agent",
                "codex",
                "--replace",
                home=home,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--backup-dir is required", result.stderr)
            self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "user content")

    def test_replace_backs_up_regular_directory_before_linking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            backup = root / "backup"
            existing = home / ".codex" / "skills" / "pdf"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("user content", encoding="utf-8")

            self.run_installer(
                "--agent",
                "codex",
                "--replace",
                "--backup-dir",
                str(backup),
                home=home,
            )

            self.assertTrue(existing.is_symlink())
            self.assertEqual(
                (backup / "skills" / "pdf" / "SKILL.md").read_text(encoding="utf-8"),
                "user content",
            )

    def test_replace_refuses_existing_backup_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            backup = root / "backup"
            existing = home / ".codex" / "skills" / "pdf"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("current user content", encoding="utf-8")
            occupied = backup / "skills" / "pdf"
            occupied.mkdir(parents=True)
            (occupied / "SKILL.md").write_text("older backup", encoding="utf-8")

            result = self.run_installer(
                "--agent",
                "codex",
                "--replace",
                "--backup-dir",
                str(backup),
                home=home,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Backup target already exists", result.stderr)
            self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "current user content")
            self.assertEqual((occupied / "SKILL.md").read_text(encoding="utf-8"), "older backup")

    def test_root_install_wrapper_delegates_to_installer(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = subprocess.run(
                [str(ROOT_INSTALL), "--agent", "codex", "--repo", str(REPO_ROOT), "--home", str(home)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            self.assertIn("Installed codex profile default", result.stdout)
            self.assertTrue((home / ".codex" / "skills" / "pdf").is_symlink())


if __name__ == "__main__":
    unittest.main()
