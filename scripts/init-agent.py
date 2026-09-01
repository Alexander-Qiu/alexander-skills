#!/usr/bin/env python3
"""Install alexander-skills into Codex or Claude Code profiles."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


class InstallError(RuntimeError):
    pass


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def agent_home(agent: str, home: Path) -> Path:
    if agent == "codex":
        return Path(os.environ.get("CODEX_HOME", home / ".codex"))
    if agent == "claude-code":
        return Path(os.environ.get("CLAUDE_HOME", home / ".claude"))
    raise InstallError(f"Unsupported agent: {agent}")


def ensure_source(repo: Path, relative: str) -> Path:
    source = repo / relative
    if not source.exists():
        raise InstallError(f"Missing source path: {source}")
    return source


def same_target(target: Path, source: Path) -> bool:
    if not target.is_symlink():
        return False
    try:
        return target.resolve() == source.resolve()
    except FileNotFoundError:
        return False


def backup_target(target: Path, target_root: Path, backup_dir: Path) -> Path:
    relative = target.relative_to(target_root)
    destination = backup_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(target), str(destination))
    return destination


def link_path(
    source: Path,
    target: Path,
    target_root: Path,
    *,
    replace: bool,
    backup_dir: Path | None,
    dry_run: bool,
) -> str:
    if target.exists() or target.is_symlink():
        if same_target(target, source):
            return f"current {target} -> {source}"
        if dry_run:
            if target.is_symlink():
                return f"would replace symlink {target} -> {source}"
            destination = backup_dir / target.relative_to(target_root) if backup_dir else None
            return f"would back up {target} -> {destination}; then link -> {source}"
        if target.is_symlink():
            target.unlink()
        else:
            assert replace and backup_dir is not None
            backup_target(target, target_root, backup_dir)

    if dry_run:
        return f"would link {target} -> {source}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source)
    return f"linked {target} -> {source}"


def install_specs(
    repo: Path,
    manifest: dict[str, Any],
    profile: dict[str, Any],
    target_root: Path,
) -> list[tuple[Path, Path]]:
    specs: list[tuple[Path, Path]] = []
    skill_defs = manifest["skills"]

    for skill_name in profile.get("skills", []):
        if skill_name not in skill_defs:
            raise InstallError(f"Profile references unknown skill: {skill_name}")
        source = ensure_source(repo, skill_defs[skill_name]["source"])
        if not (source / "SKILL.md").is_file():
            raise InstallError(f"Skill source has no SKILL.md: {source}")
        specs.append((source, target_root / "skills" / skill_name))

    for prompt in profile.get("prompts", []):
        source = ensure_source(repo, prompt["source"])
        specs.append((source, target_root / "prompts" / prompt["name"]))

    return specs


def preflight_targets(
    specs: list[tuple[Path, Path]],
    target_root: Path,
    *,
    replace: bool,
    backup_dir: Path | None,
) -> None:
    errors: list[str] = []
    for source, target in specs:
        if not (target.exists() or target.is_symlink()) or same_target(target, source):
            continue
        if not replace:
            kind = "symlink" if target.is_symlink() else "non-symlink"
            errors.append(f"Refusing to replace existing {kind}: {target}")
            continue
        if target.is_symlink():
            continue
        if backup_dir is None:
            errors.append(f"--backup-dir is required to replace existing non-symlink: {target}")
            continue
        destination = backup_dir / target.relative_to(target_root)
        if destination.exists() or destination.is_symlink():
            errors.append(f"Backup target already exists: {destination}")

    if errors:
        raise InstallError("Install preflight failed:\n" + "\n".join(errors))


def install_skill_links(
    repo: Path,
    manifest: dict[str, Any],
    profile: dict[str, Any],
    target_root: Path,
    *,
    replace: bool,
    backup_dir: Path | None,
    dry_run: bool,
) -> list[str]:
    messages: list[str] = []
    specs = install_specs(repo, manifest, profile, target_root)
    preflight_targets(specs, target_root, replace=replace, backup_dir=backup_dir)

    for source, target in specs:
        messages.append(
            link_path(
                source,
                target,
                target_root,
                replace=replace,
                backup_dir=backup_dir,
                dry_run=dry_run,
            )
        )

    return messages


def claude_plugin_commands(profile: dict[str, Any]) -> list[list[str]]:
    plugins = profile.get("plugins", {})
    commands: list[list[str]] = []
    for marketplace in plugins.get("marketplaces", []):
        commands.append(
            [
                "claude",
                "plugin",
                "marketplace",
                "add",
                marketplace["repo"],
                "--name",
                marketplace["name"],
            ]
        )
    for plugin in plugins.get("install", []):
        commands.append(["claude", "plugin", "install", plugin])
    return commands


def run_claude_plugins(profile: dict[str, Any], *, dry_run: bool, skip_plugins: bool) -> list[str]:
    if skip_plugins:
        return ["skipped Claude Code plugin installation"]

    commands = claude_plugin_commands(profile)
    if not commands:
        return []

    if dry_run:
        return [" ".join(command) for command in commands]

    if shutil.which("claude") is None:
        raise InstallError("claude command not found; re-run with --skip-plugins to install skills only")

    messages: list[str] = []
    for command in commands:
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command_text = " ".join(command)
        if completed.returncode == 0:
            messages.append(f"ok {command_text}")
        else:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise InstallError(f"Claude plugin command failed: {command_text}: {detail}")
    return messages


def install(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    manifest = load_manifest(args.manifest.resolve())
    try:
        profile = manifest["profiles"][args.agent][args.profile]
    except KeyError as exc:
        raise InstallError(f"Unknown profile {args.agent}/{args.profile}") from exc

    home = Path(args.home).expanduser().resolve()
    target_root = agent_home(args.agent, home)
    backup_dir = Path(args.backup_dir).expanduser().resolve() if args.backup_dir else None
    if backup_dir is not None:
        try:
            backup_dir.relative_to(target_root)
        except ValueError:
            pass
        else:
            raise InstallError("--backup-dir must be outside the agent target root")
    if args.dry_run:
        print(f"DRY RUN for {args.agent} profile {args.profile}")

    if args.agent == "claude-code" and not args.skip_plugins and not args.dry_run:
        if shutil.which("claude") is None:
            raise InstallError("claude command not found; re-run with --skip-plugins to install skills only")

    link_messages = install_skill_links(
        repo,
        manifest,
        profile,
        target_root,
        replace=args.replace,
        backup_dir=backup_dir,
        dry_run=args.dry_run,
    )
    plugin_messages = []
    if args.agent == "claude-code":
        plugin_messages = run_claude_plugins(profile, dry_run=args.dry_run, skip_plugins=args.skip_plugins)

    for message in link_messages + plugin_messages:
        print(message)
    if not args.dry_run:
        print(f"Installed {args.agent} profile {args.profile} into {target_root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    default_repo = Path(__file__).resolve().parents[1]
    parser.add_argument("--agent", required=True, choices=["codex", "claude-code"])
    parser.add_argument("--profile", default="default")
    parser.add_argument("--repo", type=Path, default=default_repo)
    parser.add_argument("--manifest", type=Path, default=default_repo / "manifests" / "skills.json")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--replace", action="store_true", help="replace existing conflicting targets")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="required with --replace when a conflicting target is a regular file or directory",
    )
    parser.add_argument("--skip-plugins", action="store_true", help="Claude Code: install skills only")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return install(args)
    except InstallError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
