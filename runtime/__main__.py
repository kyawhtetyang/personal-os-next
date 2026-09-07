"""Canonical Personal OS runtime CLI."""
from __future__ import annotations
import argparse,json
from runtime.capabilities.media_save import save_media
from runtime.health import check

def build_parser():
    parser=argparse.ArgumentParser(prog="python -m runtime")
    domains=parser.add_subparsers(dest="domain",required=True)
    media=domains.add_parser("media"); commands=media.add_subparsers(dest="command",required=True)
    save=commands.add_parser("save"); save.add_argument("url"); save.add_argument("--mode",choices=["audio","video"],default="audio"); save.add_argument("--audio-format",choices=["original","m4a","mp3"],default="mp3"); save.add_argument("--video-format",choices=["original","mp4"],default="mp4"); save.add_argument("--output-dir",default="data/artifacts/media"); save.add_argument("--overwrite",action="store_true"); save.add_argument("--browser"); save.add_argument("--cookies")
    health=domains.add_parser("health"); health.add_subparsers(dest="command",required=True).add_parser("check")
    return parser

def main():
    parser=build_parser(); args=parser.parse_args()
    if args.domain=="health" and args.command=="check": result=check()
    elif args.domain=="media" and args.command=="save": result=save_media(url=args.url,mode=args.mode,audio_format=args.audio_format,video_format=args.video_format,output_dir=args.output_dir,overwrite=args.overwrite,browser=args.browser,cookies=args.cookies)
    else: parser.error("Unsupported command"); return
    print(json.dumps(result,indent=2)); raise SystemExit(0 if result["status"] in {"success","healthy"} else 1)
if __name__=="__main__": main()
