#!/bin/bash

set -euo pipefail

DEFAULT_FALLBACK_PROVIDER="zenmux"
DEFAULT_FALLBACK_MODEL="google/gemini-3-flash-preview"
CONFIG_FILE="${CODEX_CONFIG_FILE:-$HOME/.codex/config.toml}"

python3 - "$CONFIG_FILE" "$DEFAULT_FALLBACK_PROVIDER" "$DEFAULT_FALLBACK_MODEL" <<'PY'
import json
import pathlib
import sys

config_path = pathlib.Path(sys.argv[1]).expanduser()
fallback_provider = sys.argv[2]
fallback_model = sys.argv[3]

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

result = {
    "has_fallback": False,
    "fallback_provider": fallback_provider,
    "fallback_model": fallback_model,
    "message": f"No usable `{fallback_provider}` provider found in {config_path}.",
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
                "message": (
                    f"Default Codex config failed. Falling back to `{fallback_provider}` with "
                    f"`{fallback_model}` from {config_path}."
                ),
            }
    except Exception as exc:
        result["message"] = f"Failed to inspect {config_path}: {exc}"

print(json.dumps(result))
PY
