# Image Conversion

Extracts jacket art and background images from Unity `.ab` (AssetBundle) files.

---

## What are `.ab` files?

maimai DX packages its jacket images (song cover art) as Unity AssetBundle files with `.ab` extension. Each `.ab` contains one or more `Texture2D` assets that can be extracted as `.png`.

**Pipeline:**
```
.ab ──► AssetStudio.CLI.exe ──► Texture2D assets ──► .png
```

---

## Required Tools

| Tool | Role |
|---|---|
| `AssetStudio.CLI.exe` | Extracts Texture2D from Unity bundles |
| .NET 8.0 Runtime | Required by AssetStudio CLI |

---

## Interactive Mode (Option 6)

1. Select **6** from the main menu
2. Choose **Single** (one `.ab` file) or **Batch** (whole folder of `.ab` files)
3. Enter paths
4. Extraction starts

---

## CLI Mode

```bash
# Single bundle
python maimai.py image single \
  --input  "C:\KDX\A000\Jackets\000001.ab" \
  --output "C:\Output\images"

# Batch
python maimai.py image batch \
  --input  "C:\KDX\A000\Jackets" \
  --output "C:\Output\images" \
  --policy skip
```

---

## Output Structure

AssetStudio outputs files in a nested structure. MAS flattens this automatically:

```
# Raw AssetStudio output (flattened by MAS):
000001.png
000002.png
000003.png
...
```

---

## Notes

- AssetStudio.CLI.exe must be installed manually in `assetstudiocli/` — see [Getting Started](Getting-Started#assetstudiocliexe)
- Requires .NET 8.0 Runtime — `setup.py` installs this automatically
- The Database Conversion pipeline calls this internally for jackets when `--cover` points to a `Jackets/` folder containing `.ab` files
- If you already have pre-extracted `.png` jacket images, you can skip this step and point `--cover` directly at that folder
