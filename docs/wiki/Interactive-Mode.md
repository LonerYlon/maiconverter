# Interactive Mode

Running `python maimai.py` with no arguments launches the interactive TUI (text user interface).

---

## Main Menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Maimai's AIO Conversion
  Created by Ryuki
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [1] MP4 Conversion   (.dat → .mp4)
  [2] MP3 Conversion   (.awb → .mp3)
  [3] FLAC Conversion  (.awb → .flac)
  [4] Chart Conversion (.ma2 → simai)
  [5] Database Conversion (AXXX Full Pipeline)
  [6] Image Conversion (.ab → .png)
  [0] Exit

  Tools: ✓ vgmstream  ✓ ffmpeg  ✓ crid  ✓ flac  ✓ maiforge  ✓ AssetStudio
```

- **Tool status row** — shows ✓ (found) or ✗ (missing) for each tool at a glance
- Missing tools show ✗ but you can still use modes that don't need them

---

## Navigation

| Input | Action |
|---|---|
| `1`–`6` | Enter that conversion mode |
| `0` | Exit the application |
| `↑` / `↓` | Move selection in checklists |
| `Space` | Toggle a checklist item |
| `Enter` | Confirm selection |
| `Esc` | Cancel / go back |

---

## After Choosing a Mode

Each mode guides you through:
1. **Path prompts** — enter your input file/folder and output folder
2. **Option checklists** — toggle extras with Space (e.g. zip output, ADX format, skip errors)
3. **Confirmation** — press Enter to start

### Countdown Between Steps

After each conversion step, a short countdown is displayed before proceeding. This gives you time to read any output before the screen clears.

---

## Tool Missing Warning

If a required tool for the selected mode is missing, the script will:
1. Print a warning and explain which tool is needed
2. Ask you to enter the full path to the tool manually for this session
3. Or let you cancel and fix it via `setup.py`

---

## Option 5 — Database Conversion Checklist

This is the most feature-rich mode. After you enter paths, it presents an arrow-key checklist:

```
Select database options:
  ◉ Categorize by: Cabinet (default)
  ○ Categorize by: Genre
  ○ ...
  [ ] Force decimal levels (13.5 instead of 13+)
  [ ] Use music ID as folder name
  [ ] Create JSON log
  [x] Zip per-category
  [ ] ADX per-category
  [ ] ADX per-track
  [ ] Ignore errors / incomplete songs
```

Use `↑`/`↓` to move, `Space` to toggle, `Enter` to confirm.

→ See [Database Conversion](Database-Conversion) for a full explanation of each option.

---

## Batch vs Single Detection (Options 1–3)

For audio/video modes, after entering the input path the script asks:
- **Single** — one file
- **Batch** — a whole folder (all matching files are processed)

For **Database Conversion** (option 5), the mode is auto-detected:
- If the input folder name matches `[A-Z]NNN` (e.g. `A000`) → **single AXXX mode**
- If the folder *contains* AXXX sub-folders → **batch mode**

---

## Tip: Skipping the Menu

You can bypass interactive mode entirely using CLI arguments:

```bash
python maimai.py mp3 batch --input C:\KDX\music --output C:\Out
python maimai.py db --root C:\KDX\A000 --output C:\Out --categorize 2
```

→ See [CLI Reference](CLI-Reference) for the full command list.
