<div align="center">
  <img src="web/img/ResourceVersionBanner.png" alt="Pigeon Studios Group resource version registry" width="2000" />
</div>

<div align="center">
  <h1>Pigeon Resource Versions</h1>
  <strong>Public version metadata for private Pigeon Studios Group FiveM resources.</strong>
</div>

---

## Purpose

This repository does not contain private resource source code.

It publishes small public metadata files used by in-resource update checkers. This lets private resources check whether they are current without exposing their code.

## Source Of Truth

Each resource folder contains a canonical file:

```text
<resource>/latest.json
```

Humans edit `latest.json`. The compatibility files are generated:

```text
<resource>/version
<resource>/changelog.txt
registry.json
```

This keeps old checkers working while giving new checkers structured metadata.

## Endpoint Formats

Root registry:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/registry.json
```

Latest resource metadata:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/<resource>/latest.json
```

Legacy version endpoint:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/<resource>/version
```

Legacy changelog endpoint:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/<resource>/changelog.txt
```

## latest.json Format

Schema:

```text
schema/latest.schema.json
```

```json
{
  "schema_version": 1,
  "slug": "payroll",
  "name": "PayRoll",
  "status": "active",
  "repository": "WelshPigeon/PayRoll",
  "version": "1.0.3",
  "tag": "v1.0.3",
  "released_at": "2026-06-26",
  "title": "Scoped payments and audit logging",
  "notes": [
    "Added /payall command with scope support.",
    "Added Discord audit logging."
  ],
  "links": {
    "support": "https://pigeonstudios.co.uk"
  }
}
```

Required fields:

- `schema_version`
- `slug`
- `name`
- `status`
- `version`
- `released_at`
- `title`
- `notes`

## Updating A Resource

1. Edit `<resource>/latest.json`.
2. Run:

```bash
python tools/build_registry.py
```

3. Commit the changed `latest.json`, `version`, `changelog.txt`, and `registry.json`.
4. Push to `main`.

## Adding A Resource

1. Create a folder using the resource slug:

```text
my-resource/
```

2. Add `my-resource/latest.json`.
3. Run:

```bash
python tools/build_registry.py
```

4. Commit the generated files.

## Validation

GitHub Actions runs the registry builder and fails if generated files are not committed.

The builder validates:

- JSON syntax
- `schema_version` is `1`
- folder slug matches `slug`
- semantic version format
- `released_at` uses `YYYY-MM-DD`
- non-empty release notes
- valid resource status

## Branding

Maintained by Pigeon Studios Group.

Website: https://pigeonstudios.co.uk
