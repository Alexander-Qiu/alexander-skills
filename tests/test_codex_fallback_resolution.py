import json
import os
import pathlib
import subprocess
import tempfile
import unittest


REPO_ROOT = pathlib.Path("/mnt/data/qrz-dev/mem/alexander-skills")
CODEX_RESOLVER = REPO_ROOT / "skills" / "codex-with-mcp" / "scripts" / "select-codex-target.sh"
KIMI_RESOLVER = REPO_ROOT / "skills" / "kimi-codex-mcp" / "scripts" / "select-codex-target.sh"


class CodexFallbackResolutionTest(unittest.TestCase):
    def run_resolver(self, script: pathlib.Path, *, config_text: str = "", env_text: str = "") -> dict:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            config_path = tmp / "config.toml"
            env_path = tmp / "codex-mcp.env"
            config_path.write_text(config_text)
            env_path.write_text(env_text)

            env = os.environ.copy()
            env["CODEX_CONFIG_FILE"] = str(config_path)
            env["CODEX_MCP_ENV_FILE"] = str(env_path)

            result = subprocess.run(
                [str(script)],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            return json.loads(result.stdout)

    def test_codex_resolver_supports_env_fallback(self) -> None:
        data = self.run_resolver(
            CODEX_RESOLVER,
            env_text="ZENMUX_ONDEMAND_API_KEY=sk-test\n",
        )
        self.assertTrue(data["has_fallback"])
        self.assertEqual(data["fallback_provider"], "zenmux")
        self.assertEqual(data["fallback_model"], "google/gemini-3-flash-preview")

    def test_kimi_resolver_matches_codex_default_then_fallback_policy(self) -> None:
        data = self.run_resolver(
            KIMI_RESOLVER,
            env_text="ZENMUX_ONDEMAND_API_KEY=sk-test\n",
        )
        self.assertTrue(data["has_fallback"])
        self.assertEqual(data["fallback_provider"], "zenmux")
        self.assertEqual(data["fallback_model"], "google/gemini-3-flash-preview")


if __name__ == "__main__":
    unittest.main()
