# Development Log

A full documentary of how Maimai's AIO Conversion (MAS) was built — session by session, decision by decision.

> **Note:** This project was built almost entirely through GitHub Copilot CLI sessions. What follows is the real history of what was asked, what was built, what broke, and how it was fixed.

---

## 🟦 Session 1 — Understanding the Codebase

**Goal:** Understand what already existed before building anything new.

Copilot explored the existing `skills/`, `tools/`, `converters/`, and `maimai.py` files to understand the project structure. At this point MAS already had:
- A working `maimai.py` main script
- `converters/` with MP3, MP4, FLAC, image conversion helpers
- `tools/` with parser utilities and subprocess wrappers
- Various skills/instructions for Copilot context

The initial system used a basic menu and ran conversions sequentially.

---

## 🟦 Session 2-4 — Database Conversion Design

**Questions asked:**
- How does the AXXX database conversion work?
- Does it go alphabetically from A000 to Z999?
- Could this be an interactive app?

**Decisions made:**
- Single AXXX detection: folder name matches `[A-Z]\d{3}` pattern
- Batch mode: parent folder containing AXXX sub-folders
- Interactive UI: yes — arrow-key menus with checklists

---

## 🟦 Session 5-9 — Replacing maichartconverter

**Problem:** The original chart conversion used `maichartconverter` — an existing open-source tool. The goal was to build something equivalent but our own.

**What was analysed:**
- The [MaichartConverter](https://github.com/Neskol/MaichartConverter) repo
- Its MaiLib library
- How it compiles `.ma2` → Simai format

**Decision:** Use `maiforge.exe` (the compiled MaiLib binary) as the backend engine for chart compilation. This gives us the same functionality while letting us control the wrapper and UX ourselves.

`maiforge` became the core tool for both single chart compilation and the full database pipeline.

---

## 🟦 Session 10-12 — CLI Design

**Questions asked:**
- What CLI flags should we implement?
- How should `--input`, `--output`, `--format`, `--difficulty`, `--id`, `--category`, `--rotate`, `--shift` work?

**CLI flags designed:**
- `--input` / `--output` — paths
- `--categorize N` — grouping mode (0-6)
- `--decimal` — level notation style
- `--use-number` — folder naming
- `--json` — log output
- `--zip` / `--adx` — packaging
- `--ignore-incomplete` — skip error songs
- Global tool path overrides (`--tool-ffmpeg`, etc.)

---

## 🟦 Session 13-14 — ZIP by Category

**Request:** "For `--zip`, make it per category folder instead of one big zip"

**Change made:** `--zip` now creates one archive per category sub-folder in the output, instead of zipping the entire output as one file. This makes importing into AstroDX more manageable.

---

## 🟦 Session 15-32 — Building & Testing the Converter

Over many short sessions, the custom chart converter was built step by step:

1. **Installed dependencies** — MaiLib NuGet package
2. **Initial test** — ran against a sample `.ma2` file
3. **Added maidata.txt content fixes** — reading and modifying output chart files
4. **Fixed `--output` subfolder behaviour** — output is now a subfolder inside the output directory named after the input folder
5. **Verified it works** ✅

This phase was iterative — build a bit, test, find an issue, fix, repeat.

---

## 🟦 Session 33-37 — Packaging and README

**Requests:**
- Package as `.exe`
- Create a README
- Rename the tool
- Make sure all parameters are documented

A `README.md` was generated covering all conversion modes, CLI flags, tool requirements, and credits.

---

## 🟦 Session 38-42 — Bug Fixes: Feature Restoration

**Problem:** After a rewrite, some previously-implemented features were lost.

**What was fixed:**
- `--ignore-errors` flag implementation restored
- Batch detection logic re-added
- The `[181/181 | 100%] Converting ma2 files...` progress display was restored

A `chat.json` from a previous session was used as reference to understand what had been built before and what needed to be re-implemented.

---

## 🟦 Session 43-44 — Utage (宴) Bug Investigation

**Problem:** "Why does almost every maidata show as 宴 (utage)?"

**Root cause found:** The difficulty detection logic was incorrectly classifying all songs as Utage because the Utage flag check was too broad. `Music.xml` has an `<utageKanjiName>` field that was being read as a positive match for all songs.

**Fix:** Tightened the utage detection to only trigger on songs that explicitly have `宴` in their `kanjiName` field with the correct type flag.

---

## 🟦 Session 45-51 — Temp File Handling and Batch Improvements

Multiple features were added over several sessions:

1. **Auto temp-file detection** — after batch/single detection, the script checks for existing temp files from a previous interrupted run and offers to continue or restart
2. **Stuck command investigation** — some maiforge commands were hanging; identified as waiting on paths that weren't being passed correctly
3. **Output path fix** — using `C:\Users\Me\Downloads\Output` was stripping the last component; fixed path handling to preserve the full path
4. **Batch "generate missing" option** — after pressing "generate missing", now shows the asset selection checklist (video/cover/mp3) like the regular flow
5. **Auto-skip existing temps** — if a folder already has temp/output files, it's skipped automatically in batch mode

---

## 🟦 Session 52-55 — UX Cleanup

**Improvements made:**
- Countdown timer added between conversion steps (gives you time to read output)
- Removed duplicate countdown that was being shown from an internal step (we had our own)
- Fixed batch resume detection: skip detection now based on **folder name match** only, not on whether files exist inside

---

## 🟦 Session 56-58 — Incomplete Song Handling

**Request:** "Only mark folders as incomplete when bg.png is missing AND `--ignore-incomplete` is on"

**Clarification:** "I mean either bg.png is missing OR `--ignore-incomplete` is on"

**Change:** The incomplete song handling logic was corrected — a song is only flagged as incomplete (and skipped) when:
- It's missing required assets (e.g. `bg.png`) **and**
- The `--ignore-incomplete` flag is active

Without the flag, missing assets cause the normal error flow.

---

## 🟦 Session 59-62 — Temp File / Resume Logic Overhaul

**Problems reported:**
1. "It deletes my temp files and redoes everything again"
2. "Whenever I press 2 (skip), it doesn't proceed"
3. Power outage interrupted a run — now half the folders are done and half aren't

**Solution designed:** A proper resume system:
- Detect which AXXX folders have already been processed (have output)
- Detect which have partial temp files (interrupted mid-run)
- Present clear choices: continue / redo / skip

---

## 🟦 Session 63 — Bug: "Didn't Proceed" (CLI Session)

**First session using the Copilot CLI agent model** (previous sessions used the regular chat model).

**Bug:** After selecting an option, the script didn't proceed to the next step.

**Root cause:** A missing `return` or incorrect state transition in the interactive flow after option selection. Fixed in the CLI agent session with full tool access.

---

## 🟦 Session 64 — Video Flag Cleanup

**Problem:** "I turned off video but the command still has `--video` in it"

**Fix:** The command builder was not respecting the video toggle — it was always appending `--video` regardless of the user's selection. Fixed to only include `--video` in the maiforge command when video conversion was actually selected.

---

## 🟦 Sessions 65-69 — Utage Doubling (Deep Dive)

**Problem:** Songs appearing as two folders: `100227-GARAKUTADOLLPLAY` and `100227-GARAKUTADOLLPLAY-Utage`

**Initial assumption:** A bug causing duplication.

**After investigation:** This is **correct behaviour**. The song `GARAKUTA DOLL PLAY` exists both as a regular song AND as a Utage variant with completely different chart data. They have separate Music.xml entries. Both should produce separate output folders.

**No fix needed** — the documentation was updated to clarify this.

---

## 🟦 Session 70 — Build Output Location

**Request:** "Put the build (exe) in the `root\maiforge` folder instead"

**Change:** The maiforge binary path was updated so the built executable lives in `maiforge/maiforge.exe` (the canonical location) rather than the deep `maioconverter-custom/dist/win-x64/` path.

---

## 🟦 Session 71 — ZIP by Category Command

**Question:** "What is the command to zip by category?"

Clarified that the flag is `--zip` and it works per-category folder.

---

## 🟦 Sessions 72-75 — ADX Support

**Requests:**
- "Change y/n to a checklist with Space/Enter"
- "Add `.adx` option (same as zip, just `.adx` extension for AstroDX)"
- "Add ADX per-track option"
- "Add 'Make folders as ADX files' to options 4 and 5"
- "Delete unnecessary things"

**Changes made:**
- The y/n confirmation for packaging was replaced with an arrow-key checklist:  `[ ] Zip per-category   [ ] ADX per-category   [ ] ADX per-track`
- `.adx` export implemented: same zip content, `.adx` extension
- Per-track ADX added: each song folder → individual `.adx`
- Cleanup of leftover code and commented-out sections

---

## 🟦 Sessions 76-78 — Improvements and Setup Script

**Request:** "In overall, any recommendations to improve or implement more features?"

**Copilot suggestions (implemented):**
- Tool status line on the main menu (shows ✓/✗ for each tool)
- Better progress display during batch runs

**First-time setup script (`setup.py`) built:**
- Checks Python version
- Detects and optionally installs .NET 8.0 Runtime
- Detects and optionally installs VC++ 2015-2022 Redistributable
- Auto-downloads ffmpeg (from BtbN builds)
- Auto-downloads vgmstream
- Prints manual instructions for flac, crid, AssetStudio
- Writes `.setup_done` marker

---

## 🟦 Session 79 — GitHub Push

First push to the GitHub repository at `https://github.com/LonerYlon/maiconverter`.

---

## 🟦 Session 80 — Full README

**Request:** "Make a full readme. Use your skills to make a good readme including all functions, links, and credits."

Generated `README.md` with:
- Feature table
- Requirements (Python, .NET, tool table)
- Setup instructions
- Folder structure diagram
- Usage (interactive + CLI)
- All conversion modes documented
- CLI flag reference
- Credits & third-party tools table

---

## 🟦 Sessions 81-88 — ZIP Packaging and setup.py Fixes

1. **`.NET` + VC++ detection** — setup.py was enhanced to actually check registry and `dotnet --list-runtimes` for installed versions, not just assume they're present
2. **ZIP creation** — `MaiConversion.zip` built from the repo, initially 41.6 MB (too much)
3. **Slimmed to 30.6 MB** — excluded `_thirdparty/`, `maichartconverter/`, and other dev-only files
4. **NameError bug** — `setup.py` had `_ffmpeg_extract` referenced in a dict before the function was defined. Fixed by moving the dict definitions after the function definitions and patching references with `TOOLS[1]["extract"] = _ffmpeg_extract`

---

## 🟦 Session 89 — Final Push

Git commit with the setup.py fix, pushed to GitHub.

---

## 🟦 Session 90 — GitHub Release v1.0

**Process:**
1. Copilot asked: release title → "MAIO Conversion v1.0"
2. Copilot asked: notes → highlights, known issues, to-be-fixed-soon
3. Copilot asked: attach zip? → yes, as "Mai AIO Conversion.zip"
4. Renamed `MaiConversion.zip` → `Mai AIO Conversion.zip`
5. Ran `gh release create v1.0 "Mai AIO Conversion.zip" --title "MAIO Conversion v1.0" ...`

**Status:** The upload command ran for 10+ minutes without completing (uploading a 30 MB file). The release creation outcome was unknown at end of session.

**To verify:** Check `gh release list` to see if v1.0 was created. If not, retry:
```bash
gh release create v1.0 "Mai AIO Conversion.zip" --title "MAIO Conversion v1.0" --notes "..."
```

---

## 📋 Summary

| What was built | How |
|---|---|
| Multi-mode conversion pipeline | Python (stdlib only, no pip deps) |
| Interactive TUI with checklists | ANSI escape codes + raw input |
| Full AXXX database pipeline | Wraps maiforge + vgmstream + ffmpeg + AssetStudio |
| ADX/ZIP packaging | Python `zipfile` module |
| First-run setup script | Python + winreg + urllib + subprocess |
| CLI mode | Python `argparse` |
| GitHub release | `gh` CLI |

**Total development time:** ~1 day (27 April 2026)  
**Total messages:** 91  
**Model used:** claude-sonnet-4.6 (via GitHub Copilot CLI)
