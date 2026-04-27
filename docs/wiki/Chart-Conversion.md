# Chart Conversion

Compiles maimai `.ma2` binary chart files into Simai text format, the open format used by AstroDX and other custom clients.

---

## What are `.ma2` files?

`.ma2` is maimai DX's compiled binary chart format. Each song has multiple `.ma2` files — one per difficulty (Basic, Advanced, Expert, Master, Re:Master, Utage).

**Pipeline:**
```
.ma2 ──► maiforge.exe ──► maidata.txt (Simai format)
```

---

## Required Tools

| Tool | Role |
|---|---|
| `maiforge.exe` | Compiles `.ma2` to Simai `maidata.txt` |

---

## Interactive Mode (Option 4)

1. Select **4** from the main menu
2. Enter the input `.ma2` file path
3. Enter the output folder
4. Choose optional packaging:
   ```
   [ ] Save as .zip
   [ ] Save as .adx (AstroDX)
   ```
5. Conversion starts

---

## CLI Mode

```bash
python maimai.py chart \
  --input  "C:\KDX\A000\music\000001\000001_00.ma2" \
  --output "C:\Output\charts" \
  --policy skip
```

---

## Chart Difficulty Files

maimai DX names chart files by music ID + difficulty index:

| Filename | Difficulty |
|---|---|
| `XXXXX_00.ma2` | Basic |
| `XXXXX_01.ma2` | Advanced |
| `XXXXX_02.ma2` | Expert |
| `XXXXX_03.ma2` | Master |
| `XXXXX_04.ma2` | Re:Master |
| `XXXXX_05.ma2` | Utage (宴) |

The Database Conversion pipeline handles all of these automatically. The standalone Chart Conversion (option 4) is for single-file processing.

---

## Notes

- The output `maidata.txt` follows the Simai specification used by AstroDX
- For full song packages (with audio, jacket, metadata), use [Database Conversion](Database-Conversion) instead
- `maiforge.exe` is bundled — no manual install needed
