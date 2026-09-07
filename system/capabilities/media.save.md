# Capability: media.save

## Identifier
media.save

## Purpose
Save supported media from a URL as audio or video.

## Inputs
Required:
- url: string

Optional:
- mode: audio | video (default: audio)
- audio_format: mp3 | m4a | original
- video_format: mp4 | original
- output_dir: path
- overwrite: boolean
- browser: browser name
- cookies: cookie file path

## Outputs
Success:
- status
- artifact_path
- format
- source_url

Failure:
- status
- error kind
- message
- actionable hint

## Requirements
- yt-dlp
- ffmpeg when conversion is required
- network access
- optional browser/cookie access when source authentication is required

## Verification
Success requires:
1. Command exits successfully.
2. Expected artifact exists.
3. Artifact extension matches requested format when conversion was requested.

## Contract Rule
The capability contract is stable.
Runtime implementation may change.