# ADX and ZIP Export

MAS can package output folders as `.zip` archives or `.adx` files for direct import into [AstroDX](https://github.com/2394425147/astrodx).

---

## What is an ADX File?

`.adx` is just a `.zip` file with a different extension. AstroDX reads `.adx` files as song packages — each one contains a `maidata.txt`, audio file, cover image, and optionally a video.

There is **no structural difference** between a `.zip` and a `.adx` — the extension is what AstroDX recognises.

---

## Packaging Options

| Option | CLI flag | Result |
|---|---|---|
| Zip per-category | `--zip` | One `.zip` per category folder |
| ADX per-category | `--adx` | One `.adx` per category folder |
| ADX per-track | `--adx-track` | One `.adx` per individual song |
| Package after batch | `--adx-after` | Run packaging after the full batch finishes |

You can combine `--zip` and `--adx-track` (or any combination) — each produces its own set of files.

---

## Per-Category vs Per-Track

### Per-Category (--adx or --zip)

Packages all songs in a category into one archive:

```
Output/
└── MaimaiDX.adx       ← contains all songs in the MaimaiDX category
└── POPS & ANIME.adx
└── niconico.adx
```

Good for: importing a whole category at once into AstroDX.

### Per-Track (--adx-track)

Packages each individual song as its own archive:

```
Output/
└── MaimaiDX/
    ├── 000001-MiraiCapsule.adx
    ├── 000002-HardToExplain.adx
    └── ...
```

Good for: selective import, sharing individual songs.

---

## Where the Archives Go

Archives are written alongside the converted song folders in the output directory. **Original folders are kept** — the archives are additions, not replacements.

If you want to clean up the original folders after archiving, do it manually or with a batch delete.

---

## Interactive Checklist (Option 5)

In interactive mode (Database Conversion), you select packaging via the options checklist:

```
  [ ] Zip per-category
  [ ] ADX per-category
  [ ] ADX per-track
```

Toggle with **Space**, confirm with **Enter**.

---

## Using with AstroDX

1. Copy your `.adx` files to your AstroDX `songs/` folder (or import via the app)
2. AstroDX reads the `maidata.txt` inside each archive to load the chart
3. Audio, jacket, and video are loaded by their standard filenames (`track.mp3`, `bg.png`, `mv.mp4`)

---

## Notes

- The `.adx` extension is specific to AstroDX — other maimai tools may not recognise it
- A `.zip` with the same content will work if you rename it to `.adx`
- Large databases (hundreds of songs) produce large archives — per-track is better for sharing individual songs
