# Anima uno still 9:16: respiro di camera + aura che pulsa.
# Uso: python tools/animate_still.py input.png output.mp4 --seconds 5
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "ffmpeg fallito")


def animate_still(src: Path, dest: Path, *, seconds: float, fps: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Crop da un canvas più grande: la camera "respira".
    # Glow: blur + screen blend con opacità sinusoidale = aura che pulsa.
    vf = (
        f"scale=1400:2488:force_original_aspect_ratio=increase,"
        f"crop=1080:1920:"
        f"'iw/2-540+18*sin(2*PI*t/3.2)':"
        f"'ih/2-960+10*sin(2*PI*t/4.1)',"
        f"eq=brightness='0.035*sin(2*PI*t/1.6)':saturation='1.05+0.08*sin(2*PI*t/1.6)',"
        f"split[base][glow];"
        f"[glow]boxblur=14:5,eq=brightness='0.22+0.18*sin(2*PI*t/1.35)'[g];"
        f"[base][g]blend=all_mode=screen:all_opacity=0.32,"
        f"fps={fps},format=yuv420p"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-framerate",
            str(fps),
            "-t",
            f"{seconds:.3f}",
            "-i",
            str(src),
            "-vf",
            vf,
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-t",
            f"{seconds:.3f}",
            str(dest),
        ]
    )


def interpolate_frames(frames: list[Path], dest: Path, *, seconds: float, fps: int) -> None:
    """Still in sequenza: ognuno respira, poi crossfade lungo (capelli/colpo che cambiano)."""
    if len(frames) < 2:
        raise SystemExit("servono almeno 2 frame")
    dest.parent.mkdir(parents=True, exist_ok=True)
    work = Path(dest.parent / f"_{dest.stem}_seq")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    try:
        n = len(frames)
        fade = min(1.7, seconds / (n + 0.5))
        piece = (seconds + fade * (n - 1)) / n
        clips: list[Path] = []
        for i, frame in enumerate(frames):
            clip = work / f"p{i:02d}.mp4"
            animate_still(frame, clip, seconds=piece, fps=fps)
            clips.append(clip)

        if n == 2:
            offset = piece - fade
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    str(clips[0]),
                    "-i",
                    str(clips[1]),
                    "-filter_complex",
                    (
                        f"[0:v][1:v]xfade=transition=fade:duration={fade:.3f}:offset={offset:.3f},"
                        "format=yuv420p[vout]"
                    ),
                    "-map",
                    "[vout]",
                    "-an",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "veryfast",
                    "-crf",
                    "18",
                    "-t",
                    f"{seconds:.3f}",
                    str(dest),
                ]
            )
        else:
            inputs: list[str] = []
            for clip in clips:
                inputs += ["-i", str(clip)]
            chain = []
            last = "0:v"
            t = piece
            for i in range(1, n):
                offset = t - fade
                out = f"x{i}"
                chain.append(
                    f"[{last}][{i}:v]xfade=transition=fade:duration={fade:.3f}:offset={offset:.3f}[{out}]"
                )
                last = out
                t = offset + piece
            graph = ";".join(chain) + f";[{last}]format=yuv420p[vout]"
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    *inputs,
                    "-filter_complex",
                    graph,
                    "-map",
                    "[vout]",
                    "-an",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "veryfast",
                    "-crf",
                    "18",
                    "-t",
                    f"{seconds:.3f}",
                    str(dest),
                ]
            )
        if dest.stat().st_size < 10_000:
            raise SystemExit(f"output troppo piccolo: {dest}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg non è in PATH")
    p = argparse.ArgumentParser()
    p.add_argument("input", nargs="+", type=Path)
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument("--seconds", type=float, default=5.0)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument(
        "--interp",
        action="store_true",
        help="Più PNG in sequenza: interpola il moto (colpo/trasformazione)",
    )
    args = p.parse_args()
    inputs = [path.expanduser().resolve() for path in args.input]
    for path in inputs:
        if not path.is_file():
            raise SystemExit(f"manca {path}")
    if args.interp or len(inputs) > 1:
        interpolate_frames(inputs, args.output, seconds=args.seconds, fps=args.fps)
    else:
        animate_still(inputs[0], args.output, seconds=args.seconds, fps=args.fps)
    print(f"ok: {args.output}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
