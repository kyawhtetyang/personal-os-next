"""Runtime implementation for capability: media.save."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def _fail(kind: str, message: str, hint: str, source_url: str) -> dict:
    return {
        "status": "failed",
        "capability": "media.save",
        "source_url": source_url,
        "error": {"kind": kind, "message": message, "hint": hint},
    }


def save_media(
    url: str,
    mode: str = "audio",
    audio_format: str = "mp3",
    video_format: str = "mp4",
    output_dir: str = "data/artifacts/media",
    overwrite: bool = False,
    browser: str | None = None,
    cookies: str | None = None,
) -> dict:
    if not shutil.which("yt-dlp"):
        return _fail(
            "PrerequisiteError",
            "yt-dlp is not installed or not on PATH.",
            "Install yt-dlp in the active environment, then retry.",
            url,
        )

    if mode == "audio" and audio_format == "mp3" and not shutil.which("ffmpeg"):
        return _fail(
            "PrerequisiteError",
            "ffmpeg is required for MP3 conversion but was not found.",
            "Install ffmpeg and ensure it is on PATH.",
            url,
        )

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    template = str(destination / "%(title)s.%(ext)s")

    command = ["yt-dlp", "--no-playlist", "-o", template]

    if overwrite:
        command.append("--force-overwrites")
    else:
        command.append("--no-overwrites")

    if browser:
        command += ["--cookies-from-browser", browser]
    elif cookies:
        command += ["--cookies", cookies]

    if mode == "audio":
        command += ["-x", "--audio-format", audio_format]
    elif mode == "video":
        if video_format == "mp4":
            command += ["--merge-output-format", "mp4"]
    else:
        return _fail(
            "ValidationError",
            f"Unsupported mode: {mode}",
            "Use audio or video.",
            url,
        )

    command.append(url)

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        return _fail(
            "MediaError",
            result.stderr.strip() or result.stdout.strip() or "Media download failed.",
            "Check network, source access, cookies/browser authentication and prerequisites.",
            url,
        )

    expected_extension = audio_format if mode == "audio" else video_format
    artifacts = sorted(destination.glob(f"*.{expected_extension}"), key=lambda p: p.stat().st_mtime)

    if not artifacts:
        return _fail(
            "VerificationError",
            f"Command completed but no .{expected_extension} artifact was found.",
            "Inspect yt-dlp output and output directory.",
            url,
        )

    artifact = artifacts[-1]
    return {
        "status": "success",
        "capability": "media.save",
        "source_url": url,
        "artifact_path": str(artifact),
        "format": artifact.suffix.lstrip("."),
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="media.save")
    parser.add_argument("url")
    parser.add_argument("--mode", choices=["audio", "video"], default="audio")
    parser.add_argument("--audio-format", choices=["original", "m4a", "mp3"], default="mp3")
    parser.add_argument("--video-format", choices=["original", "mp4"], default="mp4")
    parser.add_argument("--output-dir", default="data/artifacts/media")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--browser")
    parser.add_argument("--cookies")
    args = parser.parse_args()

    result = save_media(
        url=args.url,
        mode=args.mode,
        audio_format=args.audio_format,
        video_format=args.video_format,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
        browser=args.browser,
        cookies=args.cookies,
    )
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
