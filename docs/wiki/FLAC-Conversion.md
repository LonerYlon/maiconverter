# FLAC Conversion

Converts maimai audio containers (`.awb`) to lossless `.flac`.

---

## Pipeline

```
.awb ──► vgmstream-cli.exe ──► .wav
                │
                └──► flac.exe ──► .flac
```

This is identical to the MP3 pipeline except the final encoder is `flac.exe` instead of ffmpeg's MP3 encoder.

---

## Required Tools

| Tool | Role |
|---|---|
| `vgmstream-cli.exe` | Decodes `.awb` streams to WAV |
| `flac.exe` | Encodes WAV to lossless FLAC |
| `ffmpeg.exe` | Used to normalize WAV before FLAC encoding |

---

## Interactive Mode (Option 3)

1. Select **3** from the main menu
2. Choose **Single** or **Batch**
3. Enter paths
4. Conversion starts

---

## CLI Mode

```bash
# Single
python maimai.py flac single \
  --input  "C:\KDX\musicMP3\music000001.awb" \
  --output "C:\Output\audio"

# Batch
python maimai.py flac batch \
  --input  "C:\KDX\musicMP3" \
  --output "C:\Output\audio" \
  --policy skip
```

---

## Notes

- `flac.exe` must be placed manually in `flac/` — see [Getting Started](Getting-Started#flacexe)
- FLAC files are significantly larger than MP3 but are bit-perfect lossless copies
- The Database Conversion pipeline does **not** use FLAC — it uses MP3 for the `track.mp3` in each AstroDX song package (AstroDX expects MP3)
