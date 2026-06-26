#!/usr/bin/env python3
"""Build and validate Pigeon Studios resource version endpoints."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
SKIP_DIRS = {".git", ".github", "tools", "web", "schema"}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def require_string(data: dict, key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path.relative_to(ROOT)}: missing string field '{key}'")
    return value.strip()


def require_notes(data: dict, path: Path) -> list[str]:
    notes = data.get("notes")
    if not isinstance(notes, list) or not notes:
        raise ValidationError(f"{path.relative_to(ROOT)}: 'notes' must be a non-empty array")

    clean_notes: list[str] = []
    for index, note in enumerate(notes, start=1):
        if not isinstance(note, str) or not note.strip():
            raise ValidationError(f"{path.relative_to(ROOT)}: note #{index} must be a non-empty string")
        clean_notes.append(note.strip())

    return clean_notes


def validate_release(resource_dir: Path) -> dict:
    path = resource_dir / "latest.json"
    if not path.exists():
        raise ValidationError(f"{resource_dir.relative_to(ROOT)}: missing latest.json")

    data = load_json(path)
    schema_version = data.get("schema_version")
    if schema_version != 1:
        raise ValidationError(f"{path.relative_to(ROOT)}: schema_version must be 1")

    slug = require_string(data, "slug", path)
    name = require_string(data, "name", path)
    version = require_string(data, "version", path)
    released_at = require_string(data, "released_at", path)
    title = require_string(data, "title", path)
    notes = require_notes(data, path)

    if slug != resource_dir.name:
        raise ValidationError(f"{path.relative_to(ROOT)}: slug must match folder name '{resource_dir.name}'")

    if not SEMVER_RE.match(version):
        raise ValidationError(f"{path.relative_to(ROOT)}: version must use semantic versioning, got '{version}'")

    try:
        date.fromisoformat(released_at)
    except ValueError as exc:
        raise ValidationError(f"{path.relative_to(ROOT)}: released_at must be YYYY-MM-DD") from exc

    status = data.get("status", "active")
    if status not in {"active", "deprecated", "archived"}:
        raise ValidationError(f"{path.relative_to(ROOT)}: status must be active, deprecated, or archived")

    repository = data.get("repository")
    if repository is not None and not isinstance(repository, str):
        raise ValidationError(f"{path.relative_to(ROOT)}: repository must be a string when provided")

    links = data.get("links", {})
    if links is not None and not isinstance(links, dict):
        raise ValidationError(f"{path.relative_to(ROOT)}: links must be an object when provided")

    return {
        "slug": slug,
        "name": name,
        "status": status,
        "version": version,
        "tag": data.get("tag") or f"v{version}",
        "released_at": released_at,
        "title": title,
        "notes": notes,
        "repository": repository or "",
        "links": links or {},
    }


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def build() -> list[dict]:
    resources: list[dict] = []

    for resource_dir in sorted(path for path in ROOT.iterdir() if path.is_dir() and path.name not in SKIP_DIRS):
        release = validate_release(resource_dir)
        resources.append(release)

        write_text(resource_dir / "version", release["version"] + "\n")
        write_text(resource_dir / "changelog.txt", "\n".join(f"- {note}" for note in release["notes"]) + "\n")

    generated_date = max((release["released_at"] for release in resources), default="1970-01-01")

    registry = {
        "schema_version": 1,
        "brand": "Pigeon Studios Group",
        "generated_at": f"{generated_date}T00:00:00Z",
        "resources": {
            release["slug"]: {
                "name": release["name"],
                "status": release["status"],
                "version": release["version"],
                "tag": release["tag"],
                "released_at": release["released_at"],
                "title": release["title"],
                "repository": release["repository"],
                "latest": f"{release['slug']}/latest.json",
                "version_file": f"{release['slug']}/version",
                "changelog_file": f"{release['slug']}/changelog.txt",
            }
            for release in resources
        },
    }

    write_json(ROOT / "registry.json", registry)
    return resources


def main() -> int:
    try:
        resources = build()
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Built registry for {len(resources)} resource(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
