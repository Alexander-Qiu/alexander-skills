#!/bin/bash

set -euo pipefail

DEFAULT_FALLBACK_PROVIDER="zenmux"
DEFAULT_FALLBACK_MODEL="google/gemini-3-flash-preview"
CONFIG_FILE="${CODEX_CONFIG_FILE:-$HOME/.codex/config.toml}"
ENV_FILE="${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
START_NATIVE_MCP="$SCRIPT_DIR/start-native-codex-mcp.sh"

python3 - "$CONFIG_FILE" "$ENV_FILE" "$DEFAULT_FALLBACK_PROVIDER" "$DEFAULT_FALLBACK_MODEL" "$START_NATIVE_MCP" <<'PY'
import json
import pathlib
import shlex
import sys

config_path = pathlib.Path(sys.argv[1]).expanduser()
env_path = pathlib.Path(sys.argv[2]).expanduser()
fallback_provider = sys.argv[3]
fallback_model = sys.argv[4]
start_native_mcp = sys.argv[5]

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def load_env_file(path: pathlib.Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip("'").strip('"')
    return data


result = {
    "has_fallback": False,
    "fallback_provider": fallback_provider,
    "fallback_model": fallback_model,
    "fallback_server_cmd": "",
    "message": f"No usable `{fallback_provider}` provider found in {config_path} or {env_path}.",
}

if config_path.exists():
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
        providers = config.get("model_providers", {})
        provider = providers.get(fallback_provider)
        if provider and provider.get("base_url") and (
            provider.get("experimental_bearer_token") or provider.get("env_key")
        ):
            result = {
                "has_fallback": True,
                "fallback_provider": fallback_provider,
                "fallback_model": fallback_model,
                "fallback_server_cmd": "",
                "message": (
                    f"Default Codex config failed. Falling back to `{fallback_provider}` with "
                    f"`{fallback_model}` from {config_path}."
                ),
            }
    except Exception as exc:
        result["message"] = f"Failed to inspect {config_path}: {exc}"

if not result["has_fallback"]:
    env_data = load_env_file(env_path)
    key = env_data.get("ZENMUX_ONDEMAND_API_KEY")
    if key:
        server_cmd = " ".join(
            [
                shlex.quote(start_native_mcp),
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
        result = {
            "has_fallback": True,
            "fallback_provider": fallback_provider,
            "fallback_model": fallback_model,
            "fallback_server_cmd": server_cmd,
            "message": (
                f"Default Codex config failed. Falling back to `{fallback_provider}` with "
                f"`{fallback_model}` from {env_path}."
            ),
        }

print(json.dumps(result))
PY
