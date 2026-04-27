# Tool Reference

This page describes every third-party tool that MAS depends on — what it does, where it lives, and how MAS calls it.

---

## maiforge.exe

**Purpose:** Compiles `.ma2` binary charts into Simai text format. Also handles the full database compilation pipeline (reading `Music.xml`, resolving song metadata, building `maidata.txt`).

**Where it lives:** `maiforge/maiforge.exe`  
**Auto-installed:** ✅ Bundled  
**Source:** [Neskol/MaichartConverter](https://github.com/Neskol/MaichartConverter)

### How MAS uses it

**Single chart:**
```
maiforge.exe chart-compile --input 0001_00.ma2 --output ./out/
```

**Full database:**
```
maiforge.exe db-compile \
  --input    C:\KDX\A000 \
  --output   C:\Output \
  --music    C:\KDX\A000\musicMP3 \
  --cover    C:\KDX\A000\Jackets \
  --categorize 2
```

### Notes
- maiforge is published as a **self-contained** single-file binary — no .NET installation needed for it
- If you see `--ignore-incomplete` in the command, that tells it to skip songs with missing `bg.png` or other assets instead of failing

---

## ffmpeg / ffprobe

**Purpose:** Audio and video encoding/decoding. Used to convert WAV intermediates to MP3, encode video, and probe file metadata.

**Where it lives:** `ffmpeg/ffmpeg.exe`, `ffmpeg/ffprobe.exe`  
**Auto-installed:** ✅ via `setup.py`  
**Source:** [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)

### How MAS uses it

**WAV → MP3:**
```
ffmpeg -i input.wav -q:a 2 output.mp3
```

**M2V + audio → MP4:**
```
ffmpeg -i video.m2v -i audio.wav -c:v copy -c:a aac output.mp4
```

**WAV → FLAC (intermediate step before flac.exe):**
```
ffmpeg -i input.wav output.wav    # normalize to PCM
```

### Notes
- `ffprobe` is used to detect audio stream counts inside `.awb` files to know how many tracks to extract
- Only the `GPL` build is downloaded — if you need `LGPL` for licensing reasons, download manually

---

## vgmstream-cli.exe

**Purpose:** Decodes game audio containers (`.awb`, `.acb`, `.hca`, etc.) into WAV format for further processing.

**Where it lives:** `vgmstream-win64/vgmstream-cli.exe`  
**Auto-installed:** ✅ via `setup.py`  
**Source:** [vgmstream/vgmstream](https://github.com/vgmstream/vgmstream/releases)

### How MAS uses it

```
vgmstream-cli.exe -o output.wav -s <stream_index> input.awb
```

For multi-stream AWB files, MAS iterates over all stream indices and extracts each one as a separate WAV, then passes each to ffmpeg.

### Notes
- vgmstream supports hundreds of game audio formats — it's one of the most comprehensive game audio decoders available
- The `vgmstream-win64/` folder should contain `vgmstream-cli.exe` plus various `.dll` files it needs (all extracted together by `setup.py`)

---

## flac.exe

**Purpose:** Encodes PCM WAV files into lossless FLAC format.

**Where it lives:** `flac/flac.exe`  
**Auto-installed:** ❌ Manual  
**Download:** [xiph/flac releases](https://github.com/xiph/flac/releases)

### How to install

1. Go to the [FLAC releases](https://github.com/xiph/flac/releases) page
2. Download the Windows binary zip (e.g. `flac-1.x.x-win.zip`)
3. Extract and place `flac.exe` inside the `flac/` folder

### How MAS uses it

```
flac.exe --best -o output.flac input.wav
```

### Notes
- Only needed if you use FLAC conversion (option 3)
- If missing, MP3 conversion still works fine

---

## crid_mod.exe / crid.exe

**Purpose:** Decrypts maimai's USM video containers (`.dat` files) into `.m2v` raw video stream, which ffmpeg then re-encodes to `.mp4`.

**Where it lives:** `crid/crid_mod.exe` (or `crid/crid.exe`)  
**Auto-installed:** ❌ Manual  
**Download:** [kokarare1212/CRID-usm-Decrypter](https://github.com/kokarare1212/CRID-usm-Decrypter)

### How to install

1. Download from the [CRID-usm-Decrypter](https://github.com/kokarare1212/CRID-usm-Decrypter) repository
2. Place `crid_mod.exe` (preferred) or `crid.exe` inside the `crid/` folder
3. MAS checks for both filenames automatically

### How MAS uses it

```
crid_mod.exe "input.dat" "output_dir/"
```

The tool produces a `.m2v` file alongside the `.dat`, which ffmpeg then picks up.

### Notes
- Only needed for MP4 / video conversion
- The `.dat` files are USM containers — a format used by CRI Middleware for game video

---

## AssetStudio.CLI.exe

**Purpose:** Extracts assets from Unity `.ab` (AssetBundle) files. MAS uses it to pull jacket images (`.png`) from the game's asset bundles.

**Where it lives:** `assetstudiocli/AssetStudio.CLI.exe`  
**Auto-installed:** ❌ Manual  
**Download:** [Perfare/AssetStudio](https://github.com/Perfare/AssetStudio)  
**Requires:** .NET 8.0 Runtime (x64) — `setup.py` installs this automatically

### How to install

1. Download `AssetStudio.CLI` from the [AssetStudio releases](https://github.com/Perfare/AssetStudio/releases)
2. Extract **all files** (the `.exe` needs its sibling DLLs) into the `assetstudiocli/` folder

### How MAS uses it

```
AssetStudio.CLI.exe export \
  --input  "C:\KDX\A000\Jackets" \
  --output "C:\Output\temp\jackets" \
  --type   Texture2D
```

MAS then flattens the nested output structure to find `.png` files.

### Notes
- Only needed for image conversion and the database pipeline when jacket images come from `.ab` bundles
- Requires **.NET 8.0 Runtime** — auto-installed by `setup.py`
- If you already have extracted `.png` jacket images elsewhere, point `--cover` to that folder instead

---

## Tool Detection Order

MAS checks for each tool in a priority list. The first found path is used:

| Tool | Check order |
|---|---|
| `maiforge.exe` | `maiforge/` → `maioconverter-custom/dist/win-x64/` |
| `ffmpeg.exe` | `ffmpeg/` |
| `vgmstream-cli.exe` | `vgmstream-win64/` |
| `flac.exe` | `flac/` |
| `crid_mod.exe` | `crid/crid_mod.exe` → `crid/crid.exe` |
| `AssetStudio.CLI.exe` | `assetstudiocli/` |

All paths can be overridden at runtime with `--tool-<name>` flags. See [CLI Reference](CLI-Reference).
