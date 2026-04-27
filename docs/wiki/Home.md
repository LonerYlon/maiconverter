# Maimai's AIO Conversion — Wiki

Welcome to the MAS (Maimai AIO System) wiki. This is a personal tool for converting maimai DX game assets (audio, video, charts, databases) into formats playable in [AstroDX](https://github.com/2394425147/astrodx) and similar custom clients.

---

> [!WARNING]
> **⚠ This project was built with AI assistance (GitHub Copilot). Expect bugs.**
>
> This tool is for **personal use only**. It was shared because people asked — not because it's production-ready. Use at your own risk. No official support or maintenance guarantees are made.

---

## Navigation

| Page | What it covers |
|---|---|
| [Getting Started](Getting-Started) | Installation, setup.py, first run |
| [Interactive Mode](Interactive-Mode) | Using the TUI menus |
| [CLI Reference](CLI-Reference) | All commands and flags |
| [MP4 Conversion](MP4-Conversion) | `.dat` → `.mp4` (USM video decrypt) |
| [MP3 Conversion](MP3-Conversion) | `.awb` → `.mp3` |
| [FLAC Conversion](FLAC-Conversion) | `.awb` → `.flac` (lossless) |
| [Chart Conversion](Chart-Conversion) | `.ma2` → Simai |
| [Database Conversion](Database-Conversion) | AXXX full pipeline (the big one) |
| [Image Conversion](Image-Conversion) | `.ab` → `.png` (jacket/bg extract) |
| [ADX and ZIP Export](ADX-and-ZIP-Export) | Packaging output for AstroDX |
| [Tool Reference](Tool-Reference) | Every bundled/external tool explained |
| [Troubleshooting](Troubleshooting) | Common problems and fixes |
| [Development Log](Development-Log) | Full history of what was built and why |

---

## What Does This Do?

```
Game Files (AXXX database)
        │
        ▼
  ┌─────────────────────────────────────────────────┐
  │            maimai.py (MAS)                       │
  │                                                  │
  │  .awb  ──► vgmstream ──► ffmpeg ──► .mp3 / .flac│
  │  .dat  ──► crid      ──► ffmpeg ──► .mp4         │
  │  .ab   ──► AssetStudio              ──► .png      │
  │  .ma2  ──► maiforge                ──► simai      │
  │  AXXX  ──► full pipeline ──► song library        │
  └─────────────────────────────────────────────────┘
        │
        ▼
  Output folder (optionally .zip or .adx per song/category)
```

The **Database Conversion** (option 5) is the main feature — it takes a full AXXX game dump and turns it into a ready-to-import AstroDX library.

---

## Quick Start

```bash
git clone https://github.com/LonerYlon/maiconverter.git
cd maiconverter
python setup.py        # check/install tools
python maimai.py       # launch the UI
```

→ See [Getting Started](Getting-Started) for the full guide.

---

## Project Credits

| Tool | Author |
|---|---|
| [vgmstream](https://github.com/vgmstream/vgmstream) | vgmstream contributors |
| [FFmpeg](https://www.ffmpeg.org/) | FFmpeg contributors |
| [CRID USM Decrypter](https://github.com/kokarare1212/CRID-usm-Decrypter) | kokarare1212 |
| [FLAC encoder](https://github.com/xiph/flac) | Xiph.Org Foundation |
| [AssetStudio CLI](https://github.com/Perfare/AssetStudio) | Perfare |
| [MaiLib / maiforge](https://github.com/Neskol/MaichartConverter) | Neskol |
| [AstroDX](https://github.com/2394425147/astrodx) | 2394425147 |

> This tool is not affiliated with or endorsed by SEGA.
