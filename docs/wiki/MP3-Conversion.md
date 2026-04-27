# MP3 Conversion

Converts maimai audio containers (`.awb`) to `.mp3`.

---

## What are `.awb` files?

maimai DX stores audio in ACB/AWB container format (CRI ADX2). Each AWB file can contain multiple audio streams (one per difficulty or variant). MAS extracts all streams as separate tracks.

**Pipeline:**
```
.awb ──► vgmstream-cli.exe ──► .wav (per stream)
                │
                └──► ffmpeg ──► .mp3
```

---

## Required Tools

| Tool | Role |
|---|---|
| `vgmstream-cli.exe` | Decodes `.awb` streams to WAV |
| `ffmpeg.exe` | Encodes WAV to MP3 |

---

## Interactive Mode (Option 2)

1. Select **2** from the main menu
2. Choose **Single** or **Batch**
3. Enter the input path (`.awb` file or folder of AWBs)
4. Enter the output folder
5. Conversion starts

---

## CLI Mode

```bash
# Single file
python maimai.py mp3 single \
  --input  "C:\KDX\musicMP3\music000001.awb" \
  --output "C:\Output\audio"

# Batch
python maimai.py mp3 batch \
  --input  "C:\KDX\musicMP3" \
  --output "C:\Output\audio" \
  --policy skip
```

---

## Output

Each `.awb` produces one or more `.mp3` files (one per audio stream):
```
music000001.awb → music000001_00.mp3
                  music000001_01.mp3  (if multiple streams)
```

---

## Notes

- Temporary `.wav` files are created and cleaned up automatically
- Multi-stream AWBs are fully supported — each stream becomes its own file
- The Database Conversion pipeline uses this same logic internally for the `track.mp3` in each song folder
