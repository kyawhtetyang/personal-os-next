"""Canonical Personal OS runtime CLI."""
from __future__ import annotations
import argparse
import json

from runtime.context import ContextAssembler, ContextRequest
from runtime.context.projections import project_json, project_markdown
from runtime.core.registry import get_capability, list_capabilities
from runtime.core.discovery import discover
from runtime.execution import ExecutionEngine, ExecutionRequest
from runtime.health import check

def build_parser():
    parser = argparse.ArgumentParser(prog="python -m runtime")
    domains = parser.add_subparsers(dest="domain", required=True)
    domains.add_parser("discover")
    capabilities = domains.add_parser("capabilities")
    capability_commands = capabilities.add_subparsers(dest="command", required=True)
    capability_commands.add_parser("list")
    show = capability_commands.add_parser("show")
    show.add_argument("capability_id")
    media = domains.add_parser("media")
    commands = media.add_subparsers(dest="command", required=True)
    save = commands.add_parser("save")
    save.add_argument("url")
    save.add_argument("--mode", choices=["audio", "video"], default="audio")
    save.add_argument("--audio-format", choices=["original", "m4a", "mp3"], default="mp3")
    save.add_argument("--video-format", choices=["original", "mp4"], default="mp4")
    save.add_argument("--output-dir", default="data/artifacts/media")
    save.add_argument("--overwrite", action="store_true")
    save.add_argument("--browser")
    save.add_argument("--cookies")
    context = domains.add_parser("context")
    context_commands = context.add_subparsers(dest="command", required=True)
    context_show = context_commands.add_parser("show")
    context_show.add_argument("--purpose", required=True)
    context_show.add_argument("--query")
    context_show.add_argument("--source", action="append", dest="sources")
    context_show.add_argument("--format", choices=["json", "markdown"], default="markdown")
    health = domains.add_parser("health")
    health.add_subparsers(dest="command", required=True).add_parser("check")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.domain == "discover":
        result = discover()
    elif args.domain == "capabilities" and args.command == "list":
        result = {"status": "success", "capabilities": list_capabilities()}
    elif args.domain == "capabilities" and args.command == "show":
        capability = get_capability(args.capability_id)
        result = {"status": "success", "capability": capability} if capability else {"status": "failed", "error": {"kind": "NotFoundError", "message": f"Unknown capability: {args.capability_id}"}}
    elif args.domain == "health" and args.command == "check":
        result = check()
    elif args.domain == "media" and args.command == "save":
        request = ExecutionRequest("media.save", {"url": args.url}, {
            "mode": args.mode, "audio_format": args.audio_format, "video_format": args.video_format,
            "output_dir": args.output_dir, "overwrite": args.overwrite, "browser": args.browser, "cookies": args.cookies,
        })
        result = ExecutionEngine().execute(request)
    elif args.domain == "context" and args.command == "show":
        context = ContextAssembler().assemble(ContextRequest(args.purpose, query=args.query, sources=args.sources))
        if args.format == "markdown":
            print(project_markdown(context))
            raise SystemExit(0)
        result = {"status": "success", "context": project_json(context)}
    else:
        parser.error("Unsupported command")
        return
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] in {"success", "healthy"} else 1)

if __name__ == "__main__":
    main()
