from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Literal

from fastmcp.server import FastMCP


SERVER = FastMCP("kimi-codex-mcp")

SCRIPT_DIR = Path(__file__).resolve().parent
CALL_CODEX = SCRIPT_DIR / "call-codex.sh"

Route = Literal["default", "ondemand-gemini"]
Mode = Literal["exec", "review", "resume"]
CALL_CODEX_TIMEOUT_SECONDS = int(os.environ.get("KIMI_CODEX_CALL_TIMEOUT_SECONDS", "120"))


def _build_command(
    *,
    mode: Mode,
    prompt: str,
    cwd: str,
    route: Route,
    sandbox: str = "read-only",
    approval_policy: str = "never",
    developer_instructions: str | None = None,
    thread_id: str | None = None,
) -> list[str]:
    cmd = [
        str(CALL_CODEX),
        "--mode",
        mode,
        "--prompt",
        prompt,
        "--cwd",
        cwd,
        "--sandbox",
        sandbox,
        "--approval-policy",
        approval_policy,
    ]

    if route == "ondemand-gemini":
        cmd.extend(
            [
                "--provider",
                "zenmux",
                "--model",
                "google/gemini-3-flash-preview",
            ]
        )

    if developer_instructions:
        cmd.extend(["--developer-instructions", developer_instructions])

    if thread_id:
        cmd.extend(["--thread-id", thread_id])

    return cmd


def _parse_output(stdout: str, stderr: str, returncode: int) -> dict[str, str]:
    text = stdout.strip()
    if not text:
        raise RuntimeError(stderr.strip() or f"call-codex.sh failed with exit code {returncode}")

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"failed to parse call-codex.sh output: {exc}: {text}") from exc

    if payload.get("isError"):
        raise RuntimeError(payload.get("error") or payload.get("content") or "Codex returned an error")

    if "content" not in payload:
        raise RuntimeError(f"unexpected Codex payload: {payload}")

    return {
        "threadId": payload.get("threadId", ""),
        "content": payload["content"],
        "mode": payload.get("mode", "exec"),
    }


def _run_codex(
    *,
    mode: Mode,
    prompt: str,
    cwd: str,
    route: Route,
    sandbox: str = "read-only",
    approval_policy: str = "never",
    developer_instructions: str | None = None,
    thread_id: str | None = None,
) -> dict[str, str]:
    cmd = _build_command(
        mode=mode,
        prompt=prompt,
        cwd=cwd,
        route=route,
        sandbox=sandbox,
        approval_policy=approval_policy,
        developer_instructions=developer_instructions,
        thread_id=thread_id,
    )
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=CALL_CODEX_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"call-codex.sh timed out after {CALL_CODEX_TIMEOUT_SECONDS}s"
        ) from exc
    payload = _parse_output(result.stdout, result.stderr, result.returncode)
    payload["route"] = route
    return payload


@SERVER.tool
def codex(
    prompt: str,
    cwd: str = ".",
    route: Route = "default",
    sandbox: str = "read-only",
    approval_policy: str = "never",
    developer_instructions: str | None = None,
) -> dict[str, str]:
    """Run a one-shot Codex task through the Kimi-friendly wrapper."""
    return _run_codex(
        mode="exec",
        prompt=prompt,
        cwd=cwd,
        route=route,
        sandbox=sandbox,
        approval_policy=approval_policy,
        developer_instructions=developer_instructions,
    )


@SERVER.tool
def codex_review(
    prompt: str = "Review the current uncommitted changes and propose improvements.",
    cwd: str = ".",
    route: Route = "default",
) -> dict[str, str]:
    """Review the current working tree in a single stateless Codex call."""
    return _run_codex(
        mode="review",
        prompt=prompt,
        cwd=cwd,
        route=route,
    )


@SERVER.tool
def codex_reply(
    thread_id: str,
    prompt: str,
    route: Route = "default",
) -> dict[str, str]:
    """Continue a previous Codex thread through the Kimi-friendly wrapper."""

    return _run_codex(
        mode="resume",
        prompt=prompt,
        cwd=".",
        route=route,
        thread_id=thread_id,
    )


if __name__ == "__main__":
    SERVER.run(transport="stdio", show_banner=False)
