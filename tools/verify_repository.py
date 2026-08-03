#!/usr/bin/env python3
"""Check source hashes, finite JSON values, and relative Markdown links."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


def committed_digest(root: Path, path: Path) -> str:
    if not (root / ".git").exists():
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            pass
        else:
            data = data.replace(b"\r\n", b"\n")
        return hashlib.sha256(data).hexdigest()
    relative = path.relative_to(root).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return ""
    return hashlib.sha256(result.stdout).hexdigest()


def worktree_changed(root: Path, path: Path) -> bool:
    if not (root / ".git").exists():
        return False
    relative = path.relative_to(root).as_posix()
    return subprocess.run(
        ["git", "diff", "--quiet", "--no-ext-diff", "HEAD", "--", relative],
        cwd=root,
        check=False,
    ).returncode != 0


def walk_numbers(value, location: str, failures: list[str]) -> int:
    count = 0
    if isinstance(value, dict):
        for key, item in value.items():
            count += walk_numbers(item, f"{location}.{key}", failures)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            count += walk_numbers(item, f"{location}[{index}]", failures)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        count += 1
        if not math.isfinite(value):
            failures.append(f"non-finite numeric value: {location}")
    return count


def markdown_links(root: Path) -> list[str]:
    failures = []
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for document in sorted(root.rglob("*.md")):
        if "reference" in document.parts:
            continue
        for raw in pattern.findall(document.read_text(encoding="utf-8")):
            target = raw.strip().split("#", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            resolved = root / target.lstrip("/") if target.startswith("/") else document.parent / target
            if not resolved.exists():
                failures.append(f"broken link: {document.relative_to(root)} -> {raw}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []

    manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = root / item["path"]
        if not path.is_file():
            failures.append(f"missing source file: {item['path']}")
        elif worktree_changed(root, path):
            failures.append(f"source file differs from the committed snapshot: {item['path']}")
        elif committed_digest(root, path) != item["sha256"]:
            failures.append(f"source hash changed: {item['path']}")

    numeric_count = 0
    for path in sorted((root / "reference").rglob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid JSON: {path.relative_to(root)}: {exc}")
            continue
        numeric_count += walk_numbers(value, str(path.relative_to(root)), failures)

    failures.extend(markdown_links(root))
    if failures:
        print("repository verification failed")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"repository verification holds: {len(manifest['files'])} source hashes, "
          f"{numeric_count} finite numeric leaves, no broken public links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
