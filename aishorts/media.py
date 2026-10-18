"""Pipeline local incremental: inspect, analyze, render. Sem API de inferência."""
import argparse
import hashlib
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(args, cwd=None):
    subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-nostdin", *args],
                   check=True, cwd=cwd)


def inspect(source):
    import av
    with av.open(str(source)) as c:
        streams = [{"index": s.index, "type": s.type, "codec": s.codec_context.name,
                    "metadata": dict(s.metadata)} for s in c.streams]
        video = c.streams.video[0]
        return {"file": str(source), "duration": c.duration / av.time_base if c.duration else None,
                "width": video.width, "height": video.height, "streams": streams}


def stamp(t):
    ms = max(0, round(t * 1000))
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"