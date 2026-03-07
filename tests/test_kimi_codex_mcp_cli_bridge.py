import json
import os
import pathlib
import subprocess
import tempfile
import textwrap
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CALL_CODEX = REPO_ROOT / "skills" / "kimi-codex-mcp" / "scripts" / "call-codex.sh"


FAKE_CODEX = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json
    import os
    import pathlib
    import sys

    argv = sys.argv[1:]
    log_path = pathlib.Path(os.environ["CODEX_FAKE_LOG"])
    call_count_path = pathlib.Path(os.environ["CODEX_FAKE_COUNT"])
    count = int(call_count_path.read_text() or "0") if call_count_path.exists() else 0
    count += 1
    call_count_path.write_text(str(count))

    output_path = None
    model = None
    provider = None
    mode = "exec"

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "-o":
            output_path = argv[i + 1]
            i += 2
            continue
        if arg == "-m":
            model = argv[i + 1]
            i += 2
            continue
        if arg == "-c" and argv[i + 1].startswith("model_provider="):
            provider = argv[i + 1].split("=", 1)[1]
            i += 2
            continue
        if arg == "review":
            mode = "review"
        i += 1

    if mode == "exec" and argv and "Review the current uncommitted changes" in argv[-1]:
        mode = "review"

    log_entry = {
        "argv": argv,
        "mode": mode,
        "provider": provider,
        "model": model,
        "count": count,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_entry) + "\\n")

    if os.environ.get("CODEX_FAKE_FAIL_FIRST") == "1" and count == 1 and provider is None:
        print("subscription quota limit", file=sys.stderr)
        sys.exit(1)

    if output_path:
        pathlib.Path(output_path).write_text(
            f"{mode} ok #{count} provider={provider or 'default'} model={model or 'default'}",
            encoding="utf-8",
        )

    print(json.dumps({"type": "thread.started", "thread_id": f"thread-{count}"}))
    print(json.dumps({"type": "turn.completed"}))
    """
)


class KimiCodexMcpCliBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self.tempdir.name)
        self.bin_dir = self.tmp / "bin"
        self.bin_dir.mkdir()
        self.fake_codex = self.bin_dir / "codex"
        self.fake_codex.write_text(FAKE_CODEX, encoding="utf-8")
        self.fake_codex.chmod(0o755)

        self.log_path = self.tmp / "codex.log"
        self.count_path = self.tmp / "codex.count"
        self.home_dir = self.tmp / "home"
        self.home_dir.mkdir()
        codex_dir = self.home_dir / ".codex"
        codex_dir.mkdir()
        (codex_dir / "codex-mcp.env").write_text(
            "ZENMUX_ONDEMAND_API_KEY=test-key\\n", encoding="utf-8"
        )

        self.env = os.environ.copy()
        self.env["PATH"] = f"{self.bin_dir}:{self.env['PATH']}"
        self.env["HOME"] = str(self.home_dir)
        self.env["CODEX_FAKE_LOG"] = str(self.log_path)
        self.env["CODEX_FAKE_COUNT"] = str(self.count_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_call(self, *args: str, expect_success: bool = True, extra_env: dict | None = None):
        env = self.env.copy()
        if extra_env:
            env.update(extra_env)
        result = subprocess.run(
            [str(CALL_CODEX), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if expect_success and result.returncode != 0:
            self.fail(f"call-codex.sh failed: stdout={result.stdout!r} stderr={result.stderr!r}")
        return result

    def read_log(self):
        if not self.log_path.exists():
            return []
        return [
            json.loads(line)
            for line in self.log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_review_mode_uses_direct_codex_exec(self):
        result = self.run_call(
            "--mode",
            "review",
            "--prompt",
            "Review current work",
            "--cwd",
            str(REPO_ROOT),
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "review")
        self.assertEqual(payload["threadId"], "thread-1")
        self.assertIn("review ok #1", payload["content"])

        log_entries = self.read_log()
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0]["mode"], "review")
        self.assertEqual(log_entries[0]["argv"][0], "exec")
        self.assertNotIn("review", log_entries[0]["argv"])
        self.assertIn("Review the current uncommitted changes", log_entries[0]["argv"][-1])

    def test_default_mode_falls_back_to_ondemand_provider(self):
        result = self.run_call(
            "--prompt",
            "Say hello",
            "--cwd",
            str(REPO_ROOT),
            extra_env={"CODEX_FAKE_FAIL_FIRST": "1"},
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["threadId"], "thread-2")
        self.assertIn("provider=zenmux", payload["content"])
        self.assertIn("model=google/gemini-3-flash-preview", payload["content"])

        log_entries = self.read_log()
        self.assertEqual(len(log_entries), 2)
        self.assertIsNone(log_entries[0]["provider"])
        self.assertEqual(log_entries[1]["provider"], "zenmux")
        self.assertEqual(log_entries[1]["model"], "google/gemini-3-flash-preview")

    def test_review_mode_stays_stateless_across_three_calls(self):
        for _ in range(3):
            result = self.run_call(
                "--mode",
                "review",
                "--prompt",
                "Review current work",
                "--cwd",
                str(REPO_ROOT),
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "review")
            self.assertIn("review ok", payload["content"])

        log_entries = self.read_log()
        self.assertEqual(len(log_entries), 3)
        self.assertEqual([entry["mode"] for entry in log_entries], ["review", "review", "review"])
        self.assertEqual([entry["count"] for entry in log_entries], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
