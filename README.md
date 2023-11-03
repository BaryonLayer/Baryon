# Baryon
Modular concept of the steam compatibility layer

## Installation

1. Download latest release
2. Run `baryon_installer`
3. Copy any proton version to `/path/to/steam/compatibilitytools.d` and set `"require_tool_appid" "2118251514"` in `toolmanifest.vdf`. Don't forget to create and edit, `compatibilytool.vdf`, example in Proton-ge repo.

## Configuration

Is configured using environment variables.

Config example in `~/.config/baryon/baryon.conf`
```json
{
  "environ": {
    "BARYON_FPS": "144+72+0",
    "BARYON_RENICE": "1",
    "BARYON_GAMEMODE": "1",
    "BARYON_ALWAYSRUN": "1",
    "BARYON_START": "somecmd_start",
    "BARYON_END": "somecmd_end"
  }
}

```

## Creating installer for Devs
`pyinstaller -F --add-data Baryon:Baryon baryon_installer.py`
