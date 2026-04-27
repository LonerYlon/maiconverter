# Getting Started

This page walks you through installing and running Maimai's AIO Conversion (MAS) for the first time.

---

## Requirements

### System
- **Windows 10 / 11** (64-bit) — the bundled tools are Windows binaries
- **Python 3.10 or newer** — [python.org/downloads](https://www.python.org/downloads/)

### Runtimes (checked/installed by setup.py)
| Runtime | Required by | Auto-install |
|---|---|---|
| .NET 8.0 Runtime (x64) | AssetStudio.CLI.exe | ✅ via `setup.py` |
| Visual C++ 2015–2022 Redistributable (x64) | AssetStudio, vgmstream | ✅ via `setup.py` |

### Tools
| Tool | Required for | How to get |
|---|---|---|
| `ffmpeg.exe` + `ffprobe.exe` | Audio/video encoding | ✅ Auto-downloaded by `setup.py` |
| `vgmstream-cli.exe` | `.awb` decoding | ✅ Auto-downloaded by `setup.py` |
| `maiforge.exe` | Charts + database compilation | ✅ Bundled in `maiforge/` |
| `flac.exe` | Lossless FLAC encoding | ⬇ Manual — see below |
| `crid_mod.exe` | `.dat` USM video decrypt | ⬇ Manual — see below |
| `AssetStudio.CLI.exe` | `.ab` Unity asset extraction | ⬇ Manual — see below |

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/LonerYlon/maiconverter.git
cd maiconverter
```

Or download the ZIP from the [Releases](https://github.com/LonerYlon/maiconverter/releases) page and extract it anywhere.

### 2. Run setup

```bash
python setup.py
```

This will:
- ✅ Check your Python version
- ✅ Detect installed .NET and VC++ runtimes
- ✅ Offer to auto-install missing .NET 8.0 and VC++ 2022 (a UAC prompt may appear)
- ✅ Auto-download `ffmpeg` from [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
- ✅ Auto-download `vgmstream` from [vgmstream/vgmstream](https://github.com/vgmstream/vgmstream/releases)
- ℹ️ Print manual instructions for `flac`, `crid`, and `AssetStudio`

### 3. Manual tools (if you need them)

#### flac.exe
1. Download the latest Windows release from [xiph/flac releases](https://github.com/xiph/flac/releases)
2. Extract and place `flac.exe` into the `flac/` folder

#### crid_mod.exe (USM video decrypter)
1. Download from [kokarare1212/CRID-usm-Decrypter](https://github.com/kokarare1212/CRID-usm-Decrypter)
2. Place `crid_mod.exe` (or `crid.exe`) into the `crid/` folder

#### AssetStudio.CLI.exe
1. Download from [Perfare/AssetStudio](https://github.com/Perfare/AssetStudio)
2. Place `AssetStudio.CLI.exe` (and its sibling DLLs) into the `assetstudiocli/` folder
3. Requires **.NET 8.0 Runtime** (setup.py will install it)

### 4. Launch

```bash
python maimai.py
```

---

## Folder Structure After Setup

```
maiconverter/
├── maimai.py               ← Main script — run this
├── setup.py                ← First-time setup
├── .setup_done             ← Created after setup completes
│
├── maiforge/
│   └── maiforge.exe        ← Bundled (included)
│
├── ffmpeg/
│   ├── ffmpeg.exe          ← Auto-downloaded
│   └── ffprobe.exe         ← Auto-downloaded
│
├── vgmstream-win64/
│   └── vgmstream-cli.exe   ← Auto-downloaded
│
├── flac/
│   └── flac.exe            ← Manual
│
├── crid/
│   └── crid_mod.exe        ← Manual
│
├── assetstudiocli/
│   └── AssetStudio.CLI.exe ← Manual
│
├── converters/             ← Python conversion helpers
├── tools/                  ← Python utilities
└── skills/                 ← Copilot prompt context (not needed at runtime)
```

---

## Running Setup Again

```bash
python setup.py           # skips if already done
python setup.py --force   # always re-runs checks
```

The `.setup_done` file stores the last status. If tools are still missing, `maimai.py` will print a reminder on launch.

---

## Next Step

→ [Interactive Mode](Interactive-Mode) — learn how to navigate the TUI menus  
→ [CLI Reference](CLI-Reference) — skip the menus and drive it from scripts
