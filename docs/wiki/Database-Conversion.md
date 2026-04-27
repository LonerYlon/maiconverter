# Database Conversion

The Database Conversion (option **5** in the menu, command `db`) is the core feature of MAS. It takes an AXXX game data folder and produces a fully compiled, categorised song library.

---

## What is an AXXX Folder?

maimai DX stores its data in versioned folders named with a letter + 3 digits (e.g. `A000`, `M100`, `L300`). Each folder contains:

```
A000/
├── music/          ← .ma2 chart files + Music.xml metadata
├── musicMP3/       ← .awb audio containers
├── Jackets/        ← .ab Unity jacket images
├── movie/          ← .dat encrypted USM videos
└── ...
```

The pipeline processes all of these together to produce one output folder per song.

---

## Auto-Detection

You don't need to specify which mode — the script detects automatically:

| Input folder | Mode |
|---|---|
| `A000/` (name matches `[A-Z]\d{3}`) | **Single AXXX** |
| `KDX/` (contains `A000/`, `M100/`, etc.) | **Batch** |

Non-AXXX folders inside a batch root are silently ignored.

---

## Pipeline Steps

For each song in the AXXX folder:

```
Music.xml ──► parse metadata (title, artist, BPM, genre, levels)
    │
    ├── .ma2 charts ──► maiforge ──► maidata.txt (simai format)
    │
    ├── .awb audio  ──► vgmstream ──► WAV ──► ffmpeg ──► .mp3
    │
    ├── .ab jacket  ──► AssetStudio.CLI ──► .png (cover)
    │
    └── .dat video  ──► crid_mod ──► .m2v ──► ffmpeg ──► .mp4
```

Output per song:
```
Output/
└── [Category]/
    └── [SongName]/
        ├── maidata.txt
        ├── track.mp3
        ├── bg.png
        └── mv.mp4  (if video was present)
```

---

## Options Reference

### Categorization (`--categorize N`)

Controls how song folders are grouped:

| N | Groups by | Example folder names |
|---|---|---|
| `0` | Genre | `POPS & ANIME/`, `niconico/` |
| `1` | Level | `12/`, `13/`, `14+/` |
| `2` | Cabinet (default) | `MaimaiDX/`, `FiNALE/` |
| `3` | Composer | `HoneyWorks/`, `YOASOBI/` |
| `4` | BPM | `BPM_140-159/` |
| `5` | SD/DX chart type | `DX/`, `SD/` |
| `6` | Flat | *(no subfolders)* |

### Skip / Overwrite (`--policy`)

| Value | Behaviour |
|---|---|
| `overwrite` | Clears and redoes existing output folder |
| `skip` | Leaves existing folder untouched |

> **Tip:** Use `skip` to resume an interrupted batch run.

### Missing Assets

| Flag | Behaviour when an asset is missing |
|---|---|
| *(default)* | Marks song as incomplete, continues |
| `--ignore-incomplete` | Silently skips incomplete songs |
| `--auto-build` | Attempts to convert missing assets on the fly |

---

## Batch Mode

When the root folder contains multiple AXXX sub-folders, the script:

1. Discovers all `[A-Z]\d{3}` sub-folders
2. Checks each for existing temp/output files
3. Asks if you want to:
   - **Process all** (including already-done ones)
   - **Generate missing only** (skip folders with existing output)
4. Runs the full pipeline per AXXX folder
5. Optionally packages all output after completion (`--adx-after`)

### Skip Detection

Before processing each AXXX folder the script checks:
- Is there an output folder with the **exact same name** already in the output directory?
- If yes and policy is `skip` → that folder is skipped entirely

---

## Utage (宴) Songs

Utage songs are special challenge charts. MAS handles them correctly:

- They are detected by the `宴` flag in `Music.xml`
- Output folder gets a `-Utage` suffix: e.g. `100227-GARAKUTADOLLPLAY-Utage`
- The non-utage version and utage version produce **separate output folders** — this is intentional

If you see both `100227-GARAKUTADOLLPLAY` and `100227-GARAKUTADOLLPLAY-Utage` in your output, that's correct — they contain different chart data.

---

## ADX & ZIP Packaging

After conversion, you can package the output for AstroDX:

| Option | Result |
|---|---|
| `--zip` | Each category folder → `.zip` archive |
| `--adx` | Each category folder → `.adx` file (same as zip, different extension) |
| `--adx-track` | Each song folder → individual `.adx` file |
| `--adx-after` | Run packaging after the batch finishes |

→ See [ADX and ZIP Export](ADX-and-ZIP-Export) for details.

---

## Temp Files

The pipeline creates intermediate files during conversion (WAV intermediates, extracted images, etc.). These are:
- Stored temporarily in the output folder
- Cleaned up automatically after each song is fully processed
- **Not** cleaned up if the process is interrupted

If you restart after an interruption, temp files from the previous run are detected and you're asked what to do:
- **Continue from where it left off** (uses existing temps)
- **Redo from scratch** (deletes old temps and restarts)

---

## Example: Full Batch Run

```bash
python maimai.py db \
  --root       "C:\KDX" \
  --output     "C:\AstroDX\Songs" \
  --categorize 2 \
  --auto-build \
  --ignore-incomplete \
  --adx-after \
  --policy skip
```

This will:
1. Find all AXXX folders inside `C:\KDX`
2. Skip any that already have output
3. Process each one — building missing audio/images on the fly
4. Skip songs with errors
5. After everything is done, package all categories as `.adx` files
