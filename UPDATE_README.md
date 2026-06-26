# Updating Resource Versions

This is the update workflow for Pigeon Studios Group FiveM resources.

The private resource repo contains the actual code. This `pigeon-resource-versions` repo contains the public version metadata that in-resource version checkers read.

## Quick Rule

Update both places:

1. Private resource repo: update `fxmanifest.lua`
2. Version registry repo: update `<resource>/latest.json`

Then run the registry builder.

## What The Checker Reads

Each resource checker reads:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/<resource-slug>/latest.json
```

Example for PayRoll:

```text
https://raw.githubusercontent.com/WelshPigeon/pigeon-resource-versions/main/payroll/latest.json
```

## Resource Repo Update

In the private resource repo, update `fxmanifest.lua`.

Example:

```lua
version '1.0.4'
psg_version_slug 'payroll'
```

The `version` value is the installed/local version.

The `psg_version_slug` value must match the folder name in this repo.

## Version Registry Update

In this repo, edit:

```text
<resource-slug>/latest.json
```

Example:

```text
payroll/latest.json
```

Update these fields:

```json
{
  "version": "1.0.4",
  "tag": "v1.0.4",
  "released_at": "2026-06-26",
  "title": "Short release title",
  "notes": [
    "Added something useful.",
    "Fixed something important.",
    "Improved something noticeable."
  ]
}
```

## Build Generated Files

After editing `latest.json`, run:

```powershell
& 'C:\Users\pigeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools\build_registry.py
```

This regenerates:

```text
registry.json
<resource-slug>/version
<resource-slug>/changelog.txt
```

Do not manually edit generated files unless you are debugging.

## Commit And Push

Commit and push the private resource repo.

Then commit and push this version registry repo.

Example registry commit:

```bash
git add payroll/latest.json payroll/version payroll/changelog.txt registry.json
git commit -m "Update PayRoll to v1.0.4"
git push
```

## PayRoll Example

Private PayRoll repo:

```text
fxmanifest.lua
```

Set:

```lua
version '1.0.4'
psg_version_slug 'payroll'
```

Version registry repo:

```text
D:\Development\Pigeon Studios\pigeon-resource-versions\payroll\latest.json
```

Set:

```json
"version": "1.0.4",
"tag": "v1.0.4",
"released_at": "2026-06-26"
```

Then run:

```powershell
& 'C:\Users\pigeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools\build_registry.py
```

## Adding A New Resource

Create a new folder:

```text
my-resource/
```

Add:

```text
my-resource/latest.json
```

Use this structure:

```json
{
  "schema_version": 1,
  "slug": "my-resource",
  "name": "My Resource",
  "status": "active",
  "repository": "WelshPigeon/my-resource",
  "version": "1.0.0",
  "tag": "v1.0.0",
  "released_at": "2026-06-26",
  "title": "Initial release",
  "notes": [
    "Initial production release."
  ],
  "links": {
    "support": "https://pigeonstudios.co.uk"
  }
}
```

Run the builder:

```powershell
& 'C:\Users\pigeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools\build_registry.py
```

Then commit the new folder and generated files.

## Common Mistakes

- Do not forget to update `fxmanifest.lua` in the actual resource.
- Do not forget to update `<resource>/latest.json` in this repo.
- Do not manually edit `<resource>/version`; it is generated.
- Do not manually edit `<resource>/changelog.txt`; it is generated.
- Keep `version` and `tag` matching, for example `1.0.4` and `v1.0.4`.
- Keep `slug` matching the folder name exactly.

## Mental Model

```text
fxmanifest.lua = what the server has installed
latest.json    = what PSG says is latest
version        = generated legacy endpoint
changelog.txt  = generated legacy endpoint
registry.json  = generated index of all resources
```
