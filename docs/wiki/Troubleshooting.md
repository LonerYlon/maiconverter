# Troubleshooting

Common problems and how to fix them.

---

## Setup Issues

### `python` is not recognised

Make sure Python is on your PATH. Reinstall from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation.

### setup.py fails on .NET install

The .NET installer requires administrator rights. A UAC prompt should appear. If it doesn't or fails:
1. Download the installer manually: [.NET 8.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)
2. Run it manually as Administrator

### `NameError: name '_ffmpeg_extract' is not defined`

This was a bug in earlier versions of `setup.py` where the extract functions were referenced before being defined. **Fixed in the current version.** If you hit it, pull the latest version:
```bash
git pull
```

---

## Conversion Issues

### `The path is empty. (Parameter 'path')`

Seen in stderr from maiforge — usually means a source file path was empty or couldn't be resolved. This happens when:
- The AXXX folder is missing expected sub-folders (`music/`, `musicMP3/`, etc.)
- An asset path has trailing spaces or special characters

Use `--ignore-incomplete` to skip these songs and continue.

### Utage songs appear as two folders

If you see `100227-GARAKUTADOLLPLAY` AND `100227-GARAKUTADOLLPLAY-Utage` — this is **intentional and correct**. They contain different chart data (regular vs. Utage challenge chart). Both folders should be there.

### Video file not being converted

Check that:
1. `crid_mod.exe` is in the `crid/` folder
2. The `.dat` file is in the `movie/` or `video/` folder inside the AXXX directory
3. Video asset detection: MAS looks for `movie/` or `video/` folder names inside the AXXX root

### Audio has multiple tracks / wrong track

AWB files can contain multiple streams. MAS extracts all of them. If you want only one, use the standalone MP3 conversion and specify the exact `.awb` file, then pick the right stream manually.

### `--output` path not creating the right folder

Make sure the path doesn't end with a backslash. Use:
```
C:\Users\Me\Downloads\Output
```
Not:
```
C:\Users\Me\Downloads\Output\
```

Also, the script creates a **sub-folder inside the output path** with the same name as the input AXXX folder. So if your AXXX is `A000` and output is `C:\Output`, you'll get `C:\Output\A000\`.

---

## Batch Issues

### Batch gets stuck / hangs

This can happen if maiforge or another subprocess hangs waiting for input. Press **Ctrl+C** to cancel, then restart with `--policy skip` to resume from where you left off:
```bash
python maimai.py db --root ... --output ... --policy skip
```

### Already-done folders are being processed again

Use `--policy skip`. The skip check is based on whether an **output folder with the same name** already exists — not on whether the folder has files inside it.

### Temp files from interrupted run

If a run was interrupted (power outage, Ctrl+C), temp files may remain. On the next run, MAS will detect these and ask whether to:
- **Continue** using the existing temps (resume)
- **Restart** (delete and redo from scratch)

## Still stuck?

Check if there's an existing [issue on GitHub](https://github.com/LonerYlon/maiconverter/issues), or open a new one describing:
1. What you did
2. What error message appeared
3. Which mode you were using
4. Your OS and Python version
