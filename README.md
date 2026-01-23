<div align="center">
  <img src="web/img/ResourceVersionBanner.png" alt="Resource Version Tracking by Pigeon Studios" width="2000" />
</div>

<div align="center">
  <h1>Pigeon Resource Versions</h1>
</div>

<div align="center">
  <strong>Public version & changelog endpoints for Pigeon Studios resources.</strong><br>
  Used by in-resource update checkers (FiveM) to determine whether a script is up to date.
</div>

---

## 🔍 Repository Information

| Field | Value |
|------|------|
| **Repository Name** | pigeon-resource-versions |
| **Category** | Version Endpoints |
| **Maintained By** | Pigeon Studios |
| **Purpose** | Public `version` + `changelog.txt` files for private/internal resources |

---

## 🧩 What This Repo Is

This repository does **not** contain full script source code.

It contains small, public files used by update checkers inside resources, such as:
- `version` (current release version)
- `changelog.txt` (patch notes / update notes)

This allows a resource hosted privately to still run a public update check via `raw.githubusercontent.com`.

---

## 📁 Structure

Each resource gets its own folder:
pigeon-resource-versions/
<resource-name>/
version
changelog.txt

Example:
pigeon-resource-versions/
taser-cartridge-system/
version
changelog.txt

---

## 🔗 Raw URL Format

### Version file
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/
<resource-name>/version

### Changelog file
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/
<resource-name>/changelog.txt

---

## 🛠 Adding / Updating a Resource Version

1) Update the resource folder:
- Bump `<resource-name>/version`
- Update `<resource-name>/changelog.txt` (optional)

2) Commit & push changes.

Resources using the update checker will automatically read the updated version.

---

## 🔐 Licensing

| Item | Details |
|------|---------|
| **Contains Source Code** | No |
| **Redistribution of Private Resources** | Not allowed |
| **Use of Version Files** | Allowed for update-check functionality only |

> ⚠️ This repository only publishes version metadata.  
> Any private scripts, assets, or proprietary systems remain the property of Pigeon Studios.

---

## 📄 Credits

© Pigeon Studios  
Version endpoint repository for internal/private FiveM resources.