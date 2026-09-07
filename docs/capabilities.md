# Capabilities

## Design

Capabilities are the primary unit of OS functionality.

Each capability has:

1. Human-readable definition in system/capabilities/
2. Stable machine-readable contract in system/contracts/
3. Runtime implementation in runtime/capabilities/
4. Verification behavior in implementation
5. Tests in tests/

## Current

### media.save

Purpose:
Save URL-based media as audio or video.

Flow:

Request
→ media.save contract
→ runtime/capabilities/media_save.py
→ yt-dlp / ffmpeg
→ artifact verification
→ structured result
