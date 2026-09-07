"""Capability-specific work for media.save."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
from runtime.core.result import failure, success


def _fail(kind, message, hint, source_url):
    return failure("media.save", {"kind": kind, "message": message, "hint": hint}, data={"source_url": source_url})


def save_media(url, mode="audio", audio_format="mp3", video_format="mp4", output_dir="data/artifacts/media", overwrite=False, browser=None, cookies=None):
    if mode not in {"audio", "video"}:
        return _fail("ValidationError", f"Unsupported mode: {mode}", "Use audio or video.", url)
    if not shutil.which("yt-dlp"):
        return _fail("PrerequisiteError", "yt-dlp is not installed or not on PATH.", "Install yt-dlp in the active environment.", url)
    if mode == "audio" and audio_format == "mp3" and not shutil.which("ffmpeg"):
        return _fail("PrerequisiteError", "ffmpeg is required for MP3 conversion but was not found.", "Install ffmpeg and ensure it is on PATH.", url)

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    before = {p.resolve() for p in destination.glob("*") if p.is_file()}
    command = ["yt-dlp", "--no-playlist", "-o", str(destination / "%(title)s.%(ext)s"), "--print", "after_move:filepath", "--force-overwrites" if overwrite else "--no-overwrites"]
    if browser:
        command += ["--cookies-from-browser", browser]
    elif cookies:
        command += ["--cookies", cookies]
    if mode == "audio":
        command += ["-x"]
        if audio_format != "original":
            command += ["--audio-format", audio_format]
    elif video_format == "mp4":
        command += ["--merge-output-format", "mp4"]
    command.append(url)

    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return _fail("MediaError", result.stderr.strip() or result.stdout.strip() or "Media download failed.", "Check network, source access, authentication and prerequisites.", url)

    created = sorted({p.resolve() for p in destination.glob("*") if p.is_file()} - before, key=lambda p: p.stat().st_mtime)
    reported = [Path(line.strip()).expanduser().resolve() for line in result.stdout.splitlines() if line.strip() and Path(line.strip()).expanduser().is_file()]
    if mode == "audio" and audio_format != "original":
        created = [p for p in created if p.suffix.lower() == f".{audio_format}"]
        reported = [p for p in reported if p.suffix.lower() == f".{audio_format}"]
    candidates = created or reported
    if not candidates:
        return _fail("VerificationError", "Command completed but no expected artifact was found.", "Inspect yt-dlp output and output directory.", url)

    artifact = candidates[-1]
    return success("media.save", data={
        "source_url": url,
        "artifact_path": str(artifact),
        "artifact_type": "media",
        "format": artifact.suffix.lstrip("."),
    })
