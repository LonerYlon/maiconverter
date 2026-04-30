import struct
from pathlib import Path

_PREVIEW_SIG = bytes([0xe7, 0x04])
_PREVIEW_AFTER_START = bytes([0x07, 0xd0, 0x04, 0x00, 0x02, 0x00, 0x01, 0x07, 0xd1, 0x04, 0x00])


def get_preview_timing(acb_path: Path):
    """Return (start_ms, end_ms) for the preview clip from an ACB file, or None if not found.

    The end_ms value already includes the fade-out duration, so the full clip
    is [start_ms, end_ms].  Returns None when the file has no preview command block.
    """
    try:
        data = acb_path.read_bytes()
    except OSError:
        return None
    for i in range(len(data) - 22):
        if data[i:i+2] == _PREVIEW_SIG and data[i+6:i+17] == _PREVIEW_AFTER_START:
            start_ms = struct.unpack('>I', data[i+2:i+6])[0]
            end_b = data[i+17:i+20]
            end_ms = (end_b[0] << 16) | (end_b[1] << 8) | end_b[2]
            fade_ms = struct.unpack('>H', data[i+20:i+22])[0]
            return start_ms, end_ms + fade_ms
    return None


def inject_demo_timing_into_maidata(maidata_path: Path, start_ms: int, end_ms: int) -> bool:
    """Write &demo_seek and &demo_len into maidata.txt for AstroDX preview support.

    Always places them right after &genreid=, removing any existing occurrence first.
    Falls back to inserting before &inote_ / &E if &genreid= is not found.
    Returns True on success.
    """
    try:
        text = maidata_path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return False

    demo_seek = start_ms / 1000.0
    demo_len = (end_ms - start_ms) / 1000.0
    seek_line = f"&demo_seek={demo_seek:.3f}\n"
    len_line  = f"&demo_len={demo_len:.3f}\n"

    # Strip any existing demo lines first
    lines = [l for l in text.splitlines(keepends=True)
             if not l.startswith("&demo_seek=") and not l.startswith("&demo_len=")]

    # Find insertion point: right after &genreid=
    insert_at = None
    for idx, line in enumerate(lines):
        if line.startswith("&genreid="):
            insert_at = idx + 1
            break
    if insert_at is None:
        # Fallback: before &inote_ or &E
        insert_at = len(lines)
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("&inote_") or stripped == "&E":
                insert_at = idx
                break

    lines[insert_at:insert_at] = [seek_line, len_line]

    try:
        maidata_path.write_text("".join(lines), encoding="utf-8")
        return True
    except OSError:
        return False


def build_mp3_output_path(awb_file: Path, output_root: Path):
    return output_root / f"{awb_file.stem}.mp3"


def build_temp_wav_path(awb_file: Path):
    return awb_file.with_suffix(".wav")


def build_vgmstream_wav_command(awb_file: Path, temp_wav: Path, resolved_tools: dict):
    vgm_exe = resolved_tools["vgmstream-cli.exe"]
    return [
        str(vgm_exe),
        "-o", str(temp_wav),
        str(awb_file),
    ]


def build_ffmpeg_mp3_command(wav_file: Path, output_mp3: Path, resolved_tools: dict):
    ffmpeg_exe = resolved_tools["ffmpeg.exe"]
    return [
        str(ffmpeg_exe),
        "-y",
        "-i", str(wav_file),
        "-vn",
        "-acodec", "libmp3lame",
        "-q:a", "4",
        "-threads", "2",
        str(output_mp3),
    ]
