from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Literal

from fastmcp.server import FastMCP


SERVER = FastMCP("kimi-codex-mcp")

SCRIPT_DIR = Path(__file__).resolve().parent
CODEX_WITH_MCP_DIR = SCRIPT_DIR.parent.parent / "codex-with-mcp" / "scripts"
CALL_CODEX = CODEX_WITH_MCP_DIR / "call-codex.sh"
START_CODEX_MCP = CODEX_WITH_MCP_DIR / "start-codex-mcp.sh"

Route = Literal["default", "ondemand-gemini"]
CALL_CODEX_TIMEOUT_SECONDS = int(os.environ.get("KIMI_CODEX_CALL_TIMEOUT_SECONDS", "30"))


def _ondemand_server_cmd() -> str:
    key = os.environ.get("ZENMUX_ONDEMAND_API_KEY")
    if not key:
        raise RuntimeError("ZENMUX_ONDEMAND_API_KEY is required for route=ondemand-gemini")

    inner = " ".join(
        [
            shlex.quote(str(START_CODEX_MCP)),
            "-c",
            shlex.quote("model_provider=zenmux"),
            "-c",
            shlex.quote('model=google/gemini-3-flash-preview'),
            "-c",
            shlex.quote('model_providers.zenmux.name="ZenMux On-Demand"'),
            "-c",
            shlex.quote('model_providers.zenmux.base_url="https://zenmux.ai/api/v1"'),
            "-c",
            shlex.quote(
                f'model_providers.zenmux.experimental_bearer_token="{key}"'
            ),
            "-c",
            shlex.quote('model_providers.zenmux.wire_api="responses"'),
        ]
    )
    return f"bash -lc {shlex.quote(inner)}"


def _build_command(
    *,
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
        cmd.extend(["--server-cmd", _ondemand_server_cmd()])

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
        parts = []
        for item in payload.get("content", []):
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        raise RuntimeError("\n".join(parts) or "Codex returned an error")

    if "threadId" not in payload or "content" not in payload:
        raise RuntimeError(f"unexpected Codex payload: {payload}")

    return {"threadId": payload["threadId"], "content": payload["content"]}


def _run_codex(
    *,
    prompt: str,
    cwd: str,
    route: Route,
    sandbox: str = "read-only",
    approval_policy: str = "never",
    developer_instructions: str | None = None,
    thread_id: str | None = None,
) -> dict[str, str]:
    cmd = _build_command(
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


def _should_fallback(exc: RuntimeError) -> bool:
    text = str(exc).lower()
    return (
        "no mcp response" in text
        or "connection closed" in text
        or "timed out" in text
        or "quota" in text
        or "forbidden" in text
        or "unauthorized" in text
        or "missing api key" in text
        or "stream disconnected" in text
    )


@SERVER.tool
def codex(
    prompt: str,
    cwd: str = ".",
    route: Route = "default",
    sandbox: str = "read-only",
    approval_policy: str = "never",
    developer_instructions: str | None = None,
) -> dict[str, str]:
    """Run Codex through a Kimi-friendly MCP wrapper."""
    try:
        return _run_codex(
            prompt=prompt,
            cwd=cwd,
            route=route,
            sandbox=sandbox,
            approval_policy=approval_policy,
            developer_instructions=developer_instructions,
        )
    except RuntimeError as exc:
        if route != "default" or not os.environ.get("ZENMUX_ONDEMAND_API_KEY"):
            raise
        if not _should_fallback(exc):
            raise

        payload = _run_codex(
            prompt=prompt,
            cwd=cwd,
            route="ondemand-gemini",
            sandbox=sandbox,
            approval_policy=approval_policy,
            developer_instructions=developer_instructions,
        )
        payload["fallbackFrom"] = "default"
        payload["fallbackReason"] = str(exc)
        return payload


@SERVER.tool
def codex_reply(
    thread_id: str,
    prompt: str,
    route: Route = "default",
) -> dict[str, str]:
    """Continue a previous Codex thread through the Kimi-friendly wrapper."""

    return _run_codex(
        prompt=prompt,
        cwd=".",
        route=route,
        thread_id=thread_id,
    )


if __name__ == "__main__":
    SERVER.run(transport="stdio", show_banner=False)
