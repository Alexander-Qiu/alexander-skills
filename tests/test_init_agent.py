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

    def test_codex_default_profile_installs_skills_and_prompt_symlinks(self):
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
            self.assertTrue((codex_home / "skills" / "frontend-slides").is_symlink())
            self.assertEqual(
                (codex_home / "skills" / "frontend-slides").resolve(),
                (
                    REPO_ROOT
                    / "third-party"
                    / "frontend-slides"
                    / "plugins"
                    / "frontend-slides"
                    / "skills"
                    / "frontend-slides"
                ).resolve(),
            )
            self.assertTrue((codex_home / "skills" / "pua").is_symlink())
            self.assertEqual(
                (codex_home / "skills" / "pua").resolve(),
                (REPO_ROOT / "third-party" / "pua" / "codex" / "pua").resolve(),
            )
            self.assertTrue((codex_home / "prompts" / "pua.md").is_symlink())

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
            self.assertTrue((claude_home / "skills" / "frontend-slides").is_symlink())
            self.assertTrue((claude_home / "skills" / "Claudeception").is_symlink())
            self.assertFalse((claude_home / "plugins").exists())

    def test_claude_code_dry_run_lists_plugin_commands_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = self.run_installer(
                "--agent",
                "claude-code",
                "--dry-run",
                home=home,
            )

            self.assertIn("DRY RUN", result.stdout)
            self.assertIn(
                "claude plugin marketplace add anthropics/claude-plugins-official",
                result.stdout,
            )
            self.assertIn("claude plugin install superpowers@claude-plugins-official", result.stdout)
            self.assertFalse((home / ".claude").exists())

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
