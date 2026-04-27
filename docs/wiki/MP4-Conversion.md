# MP4 Conversion

Converts encrypted maimai USM video files (`.dat`) to standard `.mp4`.

---

## What are `.dat` files?

maimai DX stores its background videos as CRI USM containers with `.dat` extension. They need to be decrypted before any video player or encoder can read them.

**Pipeline:**
```
.dat ──► crid_mod.exe ──► .m2v (raw MPEG-2 video)
                │
                └──► ffmpeg ──► .mp4
```

---

## Required Tools

| Tool | Role |
|---|---|
| `crid_mod.exe` | Decrypts the `.dat` USM container |
| `ffmpeg.exe` | Re-encodes `.m2v` to `.mp4` |
| `ffprobe.exe` | Probes file info |

---

## Interactive Mode (Option 1)

1. Select **1** from the main menu
2. Choose **Single** or **Batch**
3. Enter the input path (`.dat` file or folder)
4. Enter the output folder
5. Conversion starts

---

## CLI Mode

```bash
# Single file
python maimai.py mp4 single \
  --input  "C:\KDX\movie\0001.dat" \
  --output "C:\Output\videos"

# Batch folder
python maimai.py mp4 batch \
  --input  "C:\KDX\movie" \
  --output "C:\Output\videos" \
  --policy skip
```

---

## Output

Each `.dat` produces one `.mp4` with the same base name:
```
0001.dat → 0001.mp4
```

---

## Notes

- `crid_mod.exe` must be placed in `crid/` manually — see [Tool Reference](Tool-Reference#cridmodexe--cridexe)
- Intermediate `.m2v` files are cleaned up automatically after successful conversion
- Some `.dat` files may be audio-only (no video stream) — these are skipped
