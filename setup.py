#!/usr/bin/env python3
"""
setup.py — First-time setup for Maimai's AIO Conversion
Run this once before using maimai.py to verify / install all required tools.
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SETUP_DONE = ROOT / ".setup_done"

# ── colour helpers (no third-party deps) ─────────────────────────────────────

WINDOWS = os.name == "nt"

def _c(code, text):
    if WINDOWS:
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
    return f"\033[{code}m{text}\033[0m"

OK   = lambda t: _c("32", t)
WARN = lambda t: _c("33", t)
ERR  = lambda t: _c("31", t)
BOLD = lambda t: _c("1",  t)
DIM  = lambda t: _c("2",  t)

# ── tool manifest ─────────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "maiforge.exe",
        "label": "maiforge  (database / chart compiler)",
        "candidates": [
            ROOT / "maiforge"            / "maiforge.exe",
            ROOT / "maioconverter-custom" / "dist" / "win-x64" / "maiforge.exe",
        ],
        "auto": False,
        "note": "Already bundled in the maiforge/ folder.",
    },
    {
        "name": "ffmpeg.exe",
        "label": "ffmpeg    (audio / video encoding)",
        "candidates": [ROOT / "ffmpeg" / "ffmpeg.exe"],
        "auto": True,
        "download_url": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
        "extract": _ffmpeg_extract,   # filled in below
        "note": "Auto-download from github.com/BtbN/FFmpeg-Builds",
    },
    {
        "name": "vgmstream-cli.exe",
        "label": "vgmstream (audio stream decoding)",
        "candidates": [ROOT / "vgmstream-win64" / "vgmstream-cli.exe"],
        "auto": True,
        "download_url": "https://github.com/vgmstream/vgmstream/releases/latest/download/vgmstream-win.zip",
        "extract": _vgmstream_extract,
        "note": "Auto-download from github.com/vgmstream/vgmstream",
    },
    {
        "name": "flac.exe",
        "label": "flac      (lossless audio encoder)",
        "candidates": [ROOT / "flac" / "flac.exe"],
        "auto": False,
        "note": (
            "Download from https://github.com/xiph/flac/releases\n"
            "              Place flac.exe inside the  flac/  folder."
        ),
    },
    {
        "name": "crid_mod.exe",
        "label": "crid      (USM video decrypter)",
        "candidates": [
            ROOT / "crid" / "crid_mod.exe",
            ROOT / "crid" / "crid.exe",
        ],
        "auto": False,
        "note": (
            "Download from https://github.com/kokarare1212/CRID-usm-Decrypter\n"
            "              Place crid_mod.exe (or crid.exe) inside the  crid/  folder."
        ),
    },
    {
        "name": "AssetStudio.CLI.exe",
        "label": "AssetStudio CLI (Unity asset extractor)",
        "candidates": [ROOT / "assetstudiocli" / "AssetStudio.CLI.exe"],
        "auto": False,
        "note": (
            "Download from https://github.com/Perfare/AssetStudio\n"
            "              Place AssetStudio.CLI.exe inside the  assetstudiocli/  folder."
        ),
    },
]

# ── extract helpers (referenced above) ───────────────────────────────────────

def _ffmpeg_extract(zip_path: Path):
    dest = ROOT / "ffmpeg"
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            fname = Path(member).name
            if fname in ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe") and "/bin/" in member:
                data = zf.read(member)
                (dest / fname).write_bytes(data)
                print(f"    extracted {fname}")


def _vgmstream_extract(zip_path: Path):
    dest = ROOT / "vgmstream-win64"
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            fname = Path(member).name
            if fname.endswith(".exe") or fname.endswith(".dll"):
                data = zf.read(member)
                (dest / fname).write_bytes(data)
        print(f"    extracted to vgmstream-win64/")


# patch the forward references now that functions are defined
TOOLS[1]["extract"] = _ffmpeg_extract
TOOLS[2]["extract"] = _vgmstream_extract

# ── helpers ───────────────────────────────────────────────────────────────────

def find_tool(tool: dict) -> Path | None:
    for c in tool["candidates"]:
        if c.is_file():
            return c
    return None


def download_with_progress(url: str, dest: Path):
    print(f"  Downloading {url}")
    def _reporthook(count, block_size, total):
        if total <= 0:
            return
        pct = min(int(count * block_size * 100 / total), 100)
        bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
        print(f"\r    [{bar}] {pct:3d}%", end="", flush=True)
    urllib.request.urlretrieve(url, dest, reporthook=_reporthook)
    print()  # newline after bar


def try_auto_install(tool: dict) -> bool:
    tmp = ROOT / f"_setup_tmp_{tool['name']}.zip"
    try:
        download_with_progress(tool["download_url"], tmp)
        tool["extract"](tmp)
        return True
    except Exception as e:
        print(ERR(f"    Download failed: {e}"))
        return False
    finally:
        if tmp.exists():
            tmp.unlink()


def check_python():
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 10):
        print(ERR(f"  Python {major}.{minor} detected — Python 3.10+ is required."))
        print(WARN("  Please upgrade: https://www.python.org/downloads/"))
        return False
    print(OK(f"  Python {major}.{minor} ✓"))
    return True


# ── .NET runtime checks ───────────────────────────────────────────────────────

# Tools that need a specific .NET runtime (not self-contained)
DOTNET_REQUIREMENTS = [
    {
        "label":   "AssetStudio.CLI.exe",
        "version": "8.0",
        "major":   8,
        "installer_url": (
            "https://aka.ms/dotnet/8.0/dotnet-runtime-win-x64.exe"
        ),
        "installer_name": "dotnet-runtime-8.0-win-x64.exe",
        "info_url": "https://dotnet.microsoft.com/en-us/download/dotnet/8.0",
    },
]


def _get_installed_dotnet_versions() -> list[str]:
    """Returns a list of installed .NET runtime version strings, e.g. ['6.0.25', '8.0.4']."""
    try:
        result = subprocess.run(
            ["dotnet", "--list-runtimes"],
            capture_output=True, text=True, timeout=10
        )
        versions = []
        for line in result.stdout.splitlines():
            # Lines look like: Microsoft.NETCore.App 8.0.4 [C:\Program Files\dotnet\...]
            if line.startswith("Microsoft.NETCore.App"):
                parts = line.split()
                if len(parts) >= 2:
                    versions.append(parts[1])
        return versions
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def _dotnet_runtime_ok(required_major: int, installed: list[str]) -> str | None:
    """Returns the version string if a matching major is installed, else None."""
    for v in installed:
        try:
            if int(v.split(".")[0]) == required_major:
                return v
        except ValueError:
            pass
    return None


def _install_dotnet_runtime(req: dict) -> bool:
    """Download and silently run the .NET runtime installer."""
    tmp = ROOT / req["installer_name"]
    try:
        download_with_progress(req["installer_url"], tmp)
        print(f"  Running installer (UAC prompt may appear)...")
        result = subprocess.run(
            [str(tmp), "/install", "/quiet", "/norestart"],
            timeout=300
        )
        return result.returncode == 0
    except Exception as e:
        print(ERR(f"    Installer failed: {e}"))
        return False
    finally:
        if tmp.exists():
            tmp.unlink()


def check_dotnet_runtimes() -> bool:
    """Check all required .NET runtimes. Returns True if all present."""
    installed = _get_installed_dotnet_versions()

    all_ok = True
    for req in DOTNET_REQUIREMENTS:
        found = _dotnet_runtime_ok(req["major"], installed)
        if found:
            print(OK(f"  ✓ .NET {req['major']}.x  (found {found})  — required by {req['label']}"))
        else:
            print(ERR(f"  ✗ .NET {req['major']}.x  — required by {req['label']}"))
            all_ok = False

    return all_ok


def offer_dotnet_install() -> list[str]:
    """Offer to auto-install missing .NET runtimes. Returns list of still-missing major versions."""
    installed = _get_installed_dotnet_versions()
    missing = [r for r in DOTNET_REQUIREMENTS if not _dotnet_runtime_ok(r["major"], installed)]
    if not missing:
        return []

    print(BOLD("\n[ .NET Runtime — Auto-install ]"))
    for req in missing:
        print(f"  {WARN('!')} .NET {req['version']} Runtime is missing.")
        print(DIM(f"      Info: {req['info_url']}"))

    ans = input(
        f"\n  Download and install {len(missing)} .NET runtime(s) automatically? (y/n): "
    ).strip().lower()

    still_missing = []
    if ans == "y":
        for req in missing:
            print(f"\n  Downloading .NET {req['version']} Runtime installer...")
            ok = _install_dotnet_runtime(req)
            # re-check after install
            new_installed = _get_installed_dotnet_versions()
            if ok and _dotnet_runtime_ok(req["major"], new_installed):
                print(OK(f"  ✓ .NET {req['version']} Runtime installed successfully."))
            else:
                print(ERR(f"  ✗ .NET {req['version']} Runtime install failed."))
                print(WARN(f"    Please install manually: {req['info_url']}"))
                still_missing.append(req["version"])
    else:
        for req in missing:
            print(WARN(f"  Please install .NET {req['version']} Runtime manually: {req['info_url']}"))
            still_missing.append(req["version"])

    return still_missing


# ── main ──────────────────────────────────────────────────────────────────────

def run_setup(force=False):
    print()
    print(BOLD("━" * 58))
    print(BOLD("  Maimai's AIO Conversion — First-time Setup"))
    print(BOLD("━" * 58))
    print()

    # ── Python version ────────────────────────────────────────
    print(BOLD("[ Python ]"))
    py_ok = check_python()
    print()

    # ── .NET Runtimes ─────────────────────────────────────────
    print(BOLD("[ .NET Runtimes ]"))
    dotnet_ok = check_dotnet_runtimes()
    print()
    missing_dotnet = []
    if not dotnet_ok:
        missing_dotnet = offer_dotnet_install()
        print()

    # ── Tools ─────────────────────────────────────────────────
    print(BOLD("[ Tools ]"))
    missing = []
    for tool in TOOLS:
        found = find_tool(tool)
        if found:
            print(f"  {OK('✓')} {tool['label']}")
            print(DIM(f"      {found}"))
        else:
            print(f"  {ERR('✗')} {tool['label']}")
            missing.append(tool)
    print()

    if not missing:
        print(OK("  All tools are present!"))
    else:
        # separate auto-installable from manual
        auto_tools   = [t for t in missing if t["auto"]]
        manual_tools = [t for t in missing if not t["auto"]]

        if auto_tools:
            print(BOLD("[ Auto-install ]"))
            ans = input(
                f"  {len(auto_tools)} tool(s) can be downloaded automatically. Proceed? (y/n): "
            ).strip().lower()
            if ans == "y":
                for tool in auto_tools:
                    print(f"\n  Installing {tool['label']} ...")
                    ok = try_auto_install(tool)
                    if ok and find_tool(tool):
                        print(OK(f"  ✓ {tool['name']} installed."))
                        missing.remove(tool)
                    else:
                        print(ERR(f"  ✗ {tool['name']} install failed — see note below."))
            print()

        still_missing = [t for t in missing if not find_tool(t)]
        if still_missing:
            print(BOLD("[ Manual steps required ]"))
            for tool in still_missing:
                print(f"\n  {WARN('!')} {tool['label']}")
                for line in tool["note"].split("\n"):
                    print(f"      {line}")
            print()

    # ── Write .setup_done ────────────────────────────────────
    remaining = [t for t in TOOLS if not find_tool(t)]
    state = {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "missing_tools": [t["name"] for t in remaining],
        "missing_dotnet": missing_dotnet,
        "complete": len(remaining) == 0 and len(missing_dotnet) == 0,
    }
    SETUP_DONE.write_text(json.dumps(state, indent=2))

    if state["complete"]:
        print(OK("  Setup complete! You can now run:  python maimai.py"))
    else:
        issues = len(remaining) + len(missing_dotnet)
        print(WARN(f"  Setup done with {issues} item(s) still missing."))
        print(WARN("  Those modes will ask you for the tool path when you first use them."))

    print()


def is_setup_done() -> bool:
    """Returns True if setup was previously completed successfully."""
    if not SETUP_DONE.exists():
        return False
    try:
        state = json.loads(SETUP_DONE.read_text())
        return state.get("complete", False)
    except Exception:
        return False


def nudge_if_needed():
    """
    Called from maimai.py on startup.
    Prints a one-line suggestion if setup has never been run.
    """
    if not SETUP_DONE.exists():
        print(WARN("  ⚠  First time? Run  python setup.py  to check / install tools."))
        print()


if __name__ == "__main__":
    force = "--force" in sys.argv
    if not force and is_setup_done():
        print()
        print(OK("  Setup was already completed."))
        print(DIM("  Run  python setup.py --force  to run it again."))
        print()
        sys.exit(0)
    run_setup(force=force)
