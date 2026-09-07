"""Runtime environment health checks."""
from __future__ import annotations
import shutil

def check():
    checks=[]
    for name in ("python","yt-dlp","ffmpeg"):
        checks.append({"name":name,"available":bool(shutil.which(name)),"path":shutil.which(name)})
    return {"status":"healthy" if all(x["available"] for x in checks) else "degraded","checks":checks}
