# CLI Reference

Every conversion mode can be driven directly from the command line without entering the interactive menus.

```bash
python maimai.py <command> [options]
```

---

## Global Flags

These flags work on all commands:

| Flag | Description |
|---|---|
| `--no-header` | Suppress the title banner |
| `--quiet` | Suppress non-essential output |
| `--json-summary` | Print a JSON result summary to stdout |
| `--tool-ffmpeg PATH` | Override path to `ffmpeg.exe` |
| `--tool-ffprobe PATH` | Override path to `ffprobe.exe` |
| `--tool-vgmstream PATH` | Override path to `vgmstream-cli.exe` |
| `--tool-flac PATH` | Override path to `flac.exe` |
| `--tool-crid PATH` | Override path to `crid_mod.exe` |
| `--tool-maichartconverter PATH` | Override path to `maiforge.exe` |
| `--tool-assetstudio PATH` | Override path to `AssetStudio.CLI.exe` |

---

## Commands

### `mp4` — Video Conversion

Decrypt `.dat` USM files → `.mp4`

```bash
# Single file
python maimai.py mp4 single \
  --input  "C:\KDX\movie\0001.dat" \
  --output "C:\Output\videos"

# Batch (whole folder)
python maimai.py mp4 batch \
  --input  "C:\KDX\movie" \
  --output "C:\Output\videos" \
  [--policy overwrite|skip]
```

**Tools needed:** `crid_mod.exe`, `ffmpeg.exe`, `ffprobe.exe`

---

### `mp3` — Audio Conversion (lossy)

Decode `.awb` audio streams → `.mp3`

```bash
# Single
python maimai.py mp3 single \
  --input  "C:\KDX\sound\music.awb" \
  --output "C:\Output\audio"

# Batch
python maimai.py mp3 batch \
  --input  "C:\KDX\sound" \
  --output "C:\Output\audio" \
  [--policy overwrite|skip]
```

**Tools needed:** `vgmstream-cli.exe`, `ffmpeg.exe`

---

### `flac` — Audio Conversion (lossless)

Decode `.awb` audio streams → `.flac`

```bash
# Single
python maimai.py flac single \
  --input  "C:\KDX\sound\music.awb" \
  --output "C:\Output\audio"

# Batch
python maimai.py flac batch \
  --input  "C:\KDX\sound" \
  --output "C:\Output\audio" \
  [--policy overwrite|skip]
```

**Tools needed:** `vgmstream-cli.exe`, `flac.exe`, `ffmpeg.exe`

---

### `chart` — Chart Conversion

Compile `.ma2` binary charts → Simai text format

```bash
python maimai.py chart \
  --input  "C:\KDX\A000\music\0001\0001_00.ma2" \
  --output "C:\Output\charts" \
  [--policy overwrite|skip]
```

**Tools needed:** `maiforge.exe`

---

### `db` — Database Conversion (main pipeline)

Full AXXX folder → categorised song library

```bash
# Single AXXX folder
python maimai.py db \
  --root       "C:\KDX\A000" \
  --output     "C:\Output" \
  --categorize 2 \
  --music      "C:\KDX\A000\musicMP3" \
  --cover      "C:\KDX\A000\Jackets" \
  --auto-build

# Batch (folder containing multiple AXXX sub-folders)
python maimai.py db \
  --root       "C:\KDX" \
  --output     "C:\Output" \
  --categorize 2 \
  --auto-build \
  --adx-after
```

#### `db` flags

| Flag | Default | Description |
|---|---|---|
| `--root PATH` | *(required)* | AXXX folder or parent of AXXX folders |
| `--output PATH` | *(required)* | Where to write output |
| `--music PATH` | auto-detect | Path to `music*` / `musicMP3` folder |
| `--cover PATH` | auto-detect | Path to `Jackets` / `jacket` folder |
| `--video PATH` | auto-detect | Path to `movie` / `video` folder |
| `--categorize N` | `2` | Grouping mode (0–6, see below) |
| `--decimal` | off | Use `13.5` style instead of `13+` |
| `--use-number` | off | Name folders by music ID |
| `--json` | off | Write JSON log |
| `--zip` | off | Zip each category folder |
| `--adx` | off | Package each category as `.adx` |
| `--adx-track` | off | Package each song as `.adx` |
| `--adx-after` | off | Run ADX packaging after batch finishes |
| `--collection` | off | Generate collection manifest |
| `--ignore-incomplete` | off | Skip songs with missing assets |
| `--auto-build` | off | Auto-convert missing assets on the fly |
| `--policy` | `overwrite` | `overwrite` or `skip` existing output |

#### Categorize modes (`--categorize N`)

| N | Groups songs by |
|---|---|
| `0` | Genre |
| `1` | Level |
| `2` | Cabinet (default) |
| `3` | Composer |
| `4` | BPM |
| `5` | SD/DX chart type |
| `6` | Flat (no subfolders) |

---

### `image` — Image Extraction

Extract Unity `.ab` asset bundles → `.png`

```bash
# Single
python maimai.py image single \
  --input  "C:\KDX\A000\Jackets\000001.ab" \
  --output "C:\Output\images"

# Batch
python maimai.py image batch \
  --input  "C:\KDX\A000\Jackets" \
  --output "C:\Output\images" \
  [--policy overwrite|skip]
```

**Tools needed:** `AssetStudio.CLI.exe`

---

## Output Policy (`--policy`)

| Value | Behaviour |
|---|---|
| `overwrite` | Clear and redo existing output (default) |
| `skip` | Leave existing output folder untouched |

Use `skip` when resuming an interrupted batch run to avoid re-processing completed folders.
