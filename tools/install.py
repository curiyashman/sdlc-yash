#!/usr/bin/env python3
"""Install PDLC skills once at Cursor user root (all projects), not per product.

  python tools/install.py
  python tools/install.py --preset full
  python tools/install.py --claude
  python tools/install.py --plugin-local
  python tools/install.py --dry-run

Skills land in ~/.cursor/skills/ so every product workspace can use them.
Each product still keeps its own docs/pdlc/ (tracker, PRDs, etc.) — that is
not installed here. Use product-00 / pdlc-next inside the product to set that up.

Do not copy these skills into a product's .cursor/skills/ unless you have a
reason to pin a fork for that one repo.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_NAME = "pdlc-skills"

# Team folder → skill name prefixes (or exact names for Common).
TEAMS = {
    "Common": ("pdlc-",),
    "Product": ("product-",),
    "Design": ("design-",),
    "Development": ("dev-",),
    "QA": ("qa-",),
    "Deployment": ("deploy-",),
    "Security": ("sec-",),
}

PRESETS = {
    "minimal": ("Common", "Product", "Development"),
    "default": ("Common", "Product", "Design", "Development"),
    "full": tuple(TEAMS.keys()),
}

LEGACY = (
    *(f"pdlc-{i:02d}" for i in range(13)),
    "workflow-architect",
    "fullstack-architect",
    "research-driven-prd",
    "prd-to-ux-ui",
    "requirements-to-stories",
    "product-brainstorm",
    "devops-sre-expert",
    "schema-design-interview",
    "design-system-architect",
    "design-system-spec",
)


def skill_dirs(teams: tuple[str, ...]) -> list[tuple[str, str]]:
    """Return (skill_name, absolute_source_dir) from flat skills/ when present."""
    flat = os.path.join(REPO, "skills")
    out: list[tuple[str, str]] = []
    if os.path.isdir(flat):
        wanted_prefixes = []
        for team in teams:
            wanted_prefixes.extend(TEAMS[team])
        for name in sorted(os.listdir(flat)):
            src = os.path.join(flat, name)
            if not os.path.isdir(src) or not os.path.isfile(os.path.join(src, "SKILL.md")):
                continue
            if any(name.startswith(p) for p in wanted_prefixes):
                out.append((name, src))
        return out
    # Fallback: team folders (before build has written skills/).
    for team in teams:
        base = os.path.join(REPO, team)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            src = os.path.join(base, name)
            if os.path.isdir(src) and os.path.isfile(os.path.join(src, "SKILL.md")):
                out.append((name, src))
    return out


def copy_skill(src: str, dest_root: str, name: str, dry_run: bool) -> None:
    dest = os.path.join(dest_root, name)
    if dry_run:
        print(f"  would install {name} → {dest}")
        return
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"  installed {name}")


def install_skills(dest_roots: list[str], teams: tuple[str, ...], dry_run: bool) -> int:
    items = skill_dirs(teams)
    if not items:
        print("No skills found. Run: python source/build.py", file=sys.stderr)
        return 1
    for dest_root in dest_roots:
        print(f"→ {dest_root}")
        if not dry_run:
            os.makedirs(dest_root, exist_ok=True)
        for name, src in items:
            copy_skill(src, dest_root, name, dry_run)
    return 0


def remove_legacy(dest_roots: list[str], dry_run: bool) -> None:
    for dest_root in dest_roots:
        if not os.path.isdir(dest_root):
            continue
        for name in LEGACY:
            path = os.path.join(dest_root, name)
            if os.path.isdir(path):
                if dry_run:
                    print(f"  would remove legacy {path}")
                else:
                    shutil.rmtree(path)
                    print(f"  removed legacy {name}")


def install_plugin_local(dry_run: bool) -> int:
    """Symlink this repo into ~/.cursor/plugins/local for Cursor Plugin loading."""
    local = os.path.expanduser("~/.cursor/plugins/local")
    dest = os.path.join(local, PLUGIN_NAME)
    print(f"→ plugin local {dest}")
    if dry_run:
        print(f"  would link {REPO} → {dest}")
        return 0
    os.makedirs(local, exist_ok=True)
    if os.path.islink(dest) or os.path.isfile(dest):
        os.remove(dest)
    elif os.path.isdir(dest):
        shutil.rmtree(dest)
    os.symlink(REPO, dest)
    print(f"  linked {REPO}")
    print("  Reload Cursor (Developer: Reload Window) to pick up the plugin.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Install PDLC skills at Cursor user root (all projects)."
    )
    p.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="default",
        help="minimal=P+D+pdlc-next; default=+Design; full=all six teams (default: default)",
    )
    p.add_argument(
        "--claude",
        action="store_true",
        help="Also install into ~/.claude/skills/ (Claude Code + Cursor compat)",
    )
    p.add_argument(
        "--plugin-local",
        action="store_true",
        help="Symlink this repo to ~/.cursor/plugins/local/pdlc-skills",
    )
    p.add_argument(
        "--clean-legacy",
        action="store_true",
        help="Remove older competing skill folders from the install targets",
    )
    p.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    args = p.parse_args()

    teams = PRESETS[args.preset]
    cursor_skills = os.path.expanduser("~/.cursor/skills")
    dests = [cursor_skills]
    if args.claude:
        dests.append(os.path.expanduser("~/.claude/skills"))

    print(f"Preset: {args.preset} ({', '.join(teams)})")
    print("Scope: Cursor user root (every project). Product docs stay in each product repo.")
    rc = install_skills(dests, teams, args.dry_run)
    if args.clean_legacy:
        remove_legacy(dests, args.dry_run)
    if args.plugin_local:
        rc = install_plugin_local(args.dry_run) or rc

    if rc == 0 and not args.dry_run:
        print("Done. Open any product workspace and run /pdlc-next (or ask 'what next').")
    return rc


if __name__ == "__main__":
    sys.exit(main())
