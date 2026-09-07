# Runtime CLI

The canonical command entry point is:

```bash
python -m runtime <domain> <command>
```

## Media

Save audio as MP3:

```bash
python -m runtime media save "URL" --mode audio --audio-format mp3
```

Save video:

```bash
python -m runtime media save "URL" --mode video --video-format mp4
```

Use browser cookies when source access requires authentication:

```bash
python -m runtime media save "URL" --browser chrome
```

The CLI is an interface. Capability definitions remain in `system/`, and execution remains in `runtime/capabilities/`.
