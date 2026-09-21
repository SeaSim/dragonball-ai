# Assembler recap 9:16
# Uso: python tools/assemble.py giornate/g01
# Dipende da ffmpeg in PATH, PyYAML e Pillow.
# I testi vanno in overlay PNG: il ffmpeg di Homebrew non include drawtext.
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Installa le dipendenze: pip install -r requirements.txt\n")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.stderr.write("Installa le dipendenze: pip install -r requirements.txt\n")
    sys.exit(1)

FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Supplemental/Impact.ttf"),
    Path("/Library/Fonts/Impact.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/Library/Fonts/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
]

DEMO_COLORS = [
    (26, 10, 46),
    (61, 26, 0),
    (11, 31, 58),
    (31, 0, 0),
    (16, 36, 16),
    (42, 16, 48),
    (58, 42, 0),
    (17, 17, 17),
]


class AssembleError(RuntimeError):
    pass


def run_ffmpeg(args: list[str], *, quiet: bool = True) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    if quiet:
        cmd += ["-loglevel", "error"]
    cmd += args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssembleError(proc.stderr.strip() or "ffmpeg è fallito")


def which_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise AssembleError("ffmpeg non è in PATH. Su Mac: brew install ffmpeg")


def find_font(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise AssembleError(f"Font non trovato: {path}")
        return path
    for candidate in FONT_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise AssembleError(
        "Nessun font TTF trovato. Imposta `font:` nel timeline.yaml con un path assoluto."
    )


def pil_font(font_path: Path, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError:
        return ImageFont.load_default()


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines() or [""]:
        words = raw.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def stroke_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font,
    fill=(255, 255, 255, 255),
    stroke=(0, 0, 0, 255),
    width: int = 4,
) -> None:
    x, y = xy
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=stroke)
    draw.text((x, y), text, font=font, fill=fill)


def render_text_png(
    dest: Path,
    text: str,
    *,
    size: tuple[int, int],
    font_path: Path,
    fontsize: int,
    y: int,
    opaque: tuple[int, int, int] | None = None,
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    bg = (*opaque, 255) if opaque else (0, 0, 0, 0)
    img = Image.new("RGBA", size, bg)
    draw = ImageDraw.Draw(img)
    font = pil_font(font_path, fontsize)
    lines = wrap_lines(draw, text, font, size[0] - 120)
    line_h = fontsize + 14
    total_h = line_h * len(lines)
    top = y - total_h // 2
    for index, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=font)
        w = box[2] - box[0]
        x = (size[0] - w) // 2
        stroke_text(draw, (x, top + index * line_h), line, font)
    img.save(dest)


def load_timeline(giornata: Path) -> dict:
    path = giornata / "timeline.yaml"
    if not path.is_file():
        raise AssembleError(f"Manca {path}")
    data = yaml.safe_load(path.read_text()) or {}
    if not data.get("clips"):
        raise AssembleError("timeline.yaml: lista `clips` vuota")
    return data


def clip_duration(clip: dict) -> float:
    try:
        value = float(clip["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise AssembleError(f"Clip senza duration valida: {clip}") from exc
    if value <= 0:
        raise AssembleError(f"duration deve essere > 0: {clip}")
    return value


def resolve_src(giornata: Path, clip: dict) -> Path:
    if "src" not in clip:
        raise AssembleError(f"Clip senza src: {clip}")
    path = (giornata / str(clip["src"])).resolve()
    if not path.is_file():
        raise AssembleError(f"File mancante: {path}")
    return path


def total_duration(clips: list[dict]) -> float:
    return sum(clip_duration(c) for c in clips)


def vf_fit(width: int, height: int, fps: int) -> str:
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"fps={fps},format=yuv420p"
    )


def vf_ken_burns(width: int, height: int, fps: int, duration: float) -> str:
    frames = max(int(round(duration * fps)), fps)
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},"
        f"zoompan=z='min(1.04+0.0009*on,1.12)':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps},"
        "format=yuv420p"
    )


def parse_srt(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", raw.strip())
    cues: list[dict] = []
    stamp = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
    )

    def seconds(h: str, m: str, s: str, ms: str) -> float:
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    for block in blocks:
        match = stamp.search(block)
        if not match:
            continue
        lines = [line for line in block.splitlines() if line.strip() and not line.strip().isdigit()]
        text_lines = [line for line in lines if "-->" not in line]
        if not text_lines:
            continue
        cues.append(
            {
                "start": seconds(*match.group(1, 2, 3, 4)),
                "end": seconds(*match.group(5, 6, 7, 8)),
                "text": "\n".join(text_lines),
            }
        )
    return cues


def render_segment(
    src: Path,
    dest: Path,
    *,
    duration: float,
    width: int,
    height: int,
    fps: int,
    punchline: str | None,
    ken_burns: bool,
    font: Path,
    overlay_dir: Path,
    index: int,
    title_card: bool = False,
) -> None:
    image = src.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    dur = f"{duration:.3f}"
    if image:
        vf = vf_ken_burns(width, height, fps, duration) if ken_burns else vf_fit(width, height, fps)
        # -t DEVE stare prima dello still, non tra i due -i (altrimenti ffmpeg gira all'infinito).
        base_args = ["-loop", "1", "-framerate", str(fps), "-t", dur, "-i", str(src)]
    else:
        # Se il grezzo è più corto della duration, congela l'ultimo frame.
        vf = vf_fit(width, height, fps) + ",tpad=stop_mode=clone:stop_duration=30"
        base_args = ["-i", str(src)]

    encode = [
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-r",
        str(fps),
        "-t",
        dur,
        str(dest),
    ]
    if image:
        encode = [
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-tune",
            "stillimage",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(fps),
            "-t",
            dur,
            str(dest),
        ]

    if punchline and str(punchline).strip():
        overlay = overlay_dir / f"punch_{index:02d}.png"
        title_card = bool(title_card)
        render_text_png(
            overlay,
            str(punchline).upper(),
            size=(width, height),
            font_path=font,
            fontsize=120 if title_card else 92,
            y=(height // 2 + 80) if title_card else height - 280,
        )
        if title_card:
            start, end = 0.0, duration
            vf_used = vf + ",eq=brightness=-0.22:saturation=0.72"
            enable = f"gte(t,{start:.2f})"
        else:
            start = 0.35
            end = min(duration - 0.25, max(start + 1.6, duration * 0.55))
            vf_used = vf
            enable = f"between(t,{start:.2f},{end:.2f})"
        run_ffmpeg(
            [
                *base_args,
                "-i",
                str(overlay),
                "-filter_complex",
                (
                    f"[0:v]{vf_used}[base];"
                    f"[base][1:v]overlay=0:0:enable='{enable}'[out]"
                ),
                "-map",
                "[out]",
                *encode,
            ]
        )
        return

    run_ffmpeg([*base_args, "-vf", vf, *encode])


def concat_segments(segments: list[Path], dest: Path) -> None:
    list_file = dest.parent / "concat.txt"
    lines = []
    for segment in segments:
        escaped = segment.as_posix().replace("'", "'\\''")
        lines.append(f"file '{escaped}'")
    list_file.write_text("\n".join(lines) + "\n")
    run_ffmpeg(
        [
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(dest),
        ]
    )


def burn_subtitles(
    video: Path,
    dest: Path,
    cues: list[dict],
    *,
    width: int,
    height: int,
    font: Path,
    work: Path,
) -> None:
    if not cues:
        shutil.copy2(video, dest)
        return

    overlays: list[tuple[Path, float, float]] = []
    for index, cue in enumerate(cues):
        png = work / f"sub_{index:02d}.png"
        render_text_png(
            png,
            cue["text"],
            size=(width, height),
            font_path=font,
            fontsize=42,
            y=height - 160,
        )
        overlays.append((png, cue["start"], cue["end"]))

    inputs = ["-i", str(video)]
    for png, _, _ in overlays:
        inputs += ["-i", str(png)]

    chain = []
    last = "0:v"
    for index, (_, start, end) in enumerate(overlays, start=1):
        out = "vout" if index == len(overlays) else f"s{index}"
        chain.append(
            f"[{last}][{index}:v]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})'[{out}]"
        )
        last = out

    run_ffmpeg(
        [
            *inputs,
            "-filter_complex",
            ";".join(chain),
            "-map",
            f"[{last}]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            str(dest),
        ]
    )


def probe_duration(path: Path) -> float | None:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def atempo_chain(speed: float) -> str:
    parts: list[str] = []
    ratio = max(0.25, min(4.0, speed))
    while ratio > 2.0 + 1e-6:
        parts.append("atempo=2.0")
        ratio /= 2.0
    while ratio < 0.5 - 1e-6:
        parts.append("atempo=0.5")
        ratio /= 0.5
    parts.append(f"atempo={ratio:.5f}")
    return ",".join(parts)


def mix_audio(
    video: Path,
    dest: Path,
    *,
    voice: Path | None,
    music: Path | None,
    music_volume: float,
    duration: float,
    voice_volume: float = 1.0,
    music_fit: bool = False,
) -> None:
    inputs = ["-i", str(video)]
    filters: list[str] = []
    audio_out = "0:a?"

    if voice is not None:
        inputs += ["-i", str(voice)]
        filters.append(
            f"[1:a]atrim=0:{duration:.3f},asetpts=PTS-STARTPTS,volume={voice_volume},"
            f"apad=whole_dur={duration:.3f},aformat=sample_fmts=fltp:channel_layouts=stereo[voice]"
        )
        audio_out = "[voice]"
        if music is not None:
            inputs += ["-i", str(music)]
            filters.append(music_filter(music, duration, music_volume, music_fit, label="2:a"))
            filters.append(
                "[voice][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
                "alimiter=limit=0.95:attack=5:release=50[aout]"
            )
            audio_out = "[aout]"
    elif music is not None:
        inputs += ["-i", str(music)]
        filters.append(music_filter(music, duration, music_volume, music_fit, label="1:a"))
        audio_out = "[music]"

    args = inputs
    if filters:
        args += ["-filter_complex", ";".join(filters), "-map", "0:v", "-map", audio_out]
    else:
        args += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        args += ["-map", "0:v", "-map", "1:a"]

    args += [
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{duration:.3f}",
        str(dest),
    ]
    run_ffmpeg(args)


def music_filter(
    music: Path, duration: float, volume: float, music_fit: bool, *, label: str
) -> str:
    tail = (
        f"volume={volume},apad=whole_dur={duration:.3f},"
        "aformat=sample_fmts=fltp:channel_layouts=stereo[music]"
    )
    if music_fit:
        music_dur = probe_duration(music)
        if music_dur and music_dur > 0.2:
            speed = music_dur / duration
            return f"[{label}]{atempo_chain(speed)},asetpts=PTS-STARTPTS,{tail}"
    return (
        f"[{label}]atrim=0:{duration:.3f},asetpts=PTS-STARTPTS,{tail}"
    )


def check_timeline(giornata: Path, data: dict) -> list[str]:
    notes: list[str] = []
    clips = data["clips"]
    duration = total_duration(clips)
    notes.append(f"clip: {len(clips)}")
    notes.append(f"durata video: {duration:.1f}s")
    if duration < 40 or duration > 70:
        notes.append("avviso: durata fuori da 40–70s (il recap tipico è 45–60s)")

    missing = []
    for clip in clips:
        src = giornata / str(clip["src"])
        if not src.is_file():
            missing.append(str(src.relative_to(giornata)))
    voice = data.get("voice")
    if voice and not (giornata / voice).is_file():
        missing.append(str(voice))
    music = data.get("music")
    if music and not (giornata / music).is_file():
        missing.append(str(music))
    subs = data.get("subtitles")
    if subs and not (giornata / subs).is_file():
        missing.append(str(subs))

    if missing:
        notes.append("file mancanti:\n  - " + "\n  - ".join(missing))
    else:
        notes.append("tutti i file della timeline esistono")
    return notes


def write_placeholder_still(
    path: Path, label: str, color: tuple[int, int, int], font: Path, size: tuple[int, int]
) -> None:
    render_text_png(
        path,
        str(label).upper(),
        size=size,
        font_path=font,
        fontsize=72,
        y=size[1] // 2,
        opaque=color,
    )


def write_placeholder_voice(path: Path, duration: float) -> None:
    run_ffmpeg(
        [
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=180:sample_rate=44100:duration={duration:.3f}",
            "-q:a",
            "6",
            str(path),
        ]
    )


def demo_assets(giornata: Path, data: dict, font: Path) -> None:
    width = int(data.get("width", 1080))
    height = int(data.get("height", 1920))
    for index, clip in enumerate(data["clips"]):
        src = giornata / str(clip["src"])
        if src.is_file():
            continue
        if src.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            raise AssembleError(
                f"--demo crea solo still. Converti {clip['src']} in png o genera il mp4 a mano."
            )
        label = clip.get("punchline") or clip["src"]
        write_placeholder_still(src, str(label), DEMO_COLORS[index % len(DEMO_COLORS)], font, (width, height))
        print(f"demo still: {src.relative_to(giornata)}", flush=True)

    duration = total_duration(data["clips"])
    voice_name = data.get("voice") or "voce.mp3"
    voice = giornata / voice_name
    if not voice.is_file():
        write_placeholder_voice(voice, duration)
        print(f"demo voce (beep): {voice.relative_to(giornata)}", flush=True)


def assemble(giornata: Path, data: dict) -> Path:
    which_ffmpeg()
    width = int(data.get("width", 1080))
    height = int(data.get("height", 1920))
    fps = int(data.get("fps", 30))
    font = find_font(data.get("font"))
    duration = total_duration(data["clips"])
    output = giornata / data.get("output", "recap.mp4")

    voice = giornata / data["voice"] if data.get("voice") else None
    music = giornata / data["music"] if data.get("music") else None
    subtitles = giornata / data["subtitles"] if data.get("subtitles") else None
    if voice is not None and not voice.is_file():
        raise AssembleError(f"Manca la voce: {voice}")
    if music is not None and not music.is_file():
        raise AssembleError(f"Manca la musica: {music}")
    if subtitles is not None and not subtitles.is_file():
        raise AssembleError(f"Mancano i sottotitoli: {subtitles}")

    work = Path(tempfile.mkdtemp(prefix="recap_", dir=str(giornata)))
    try:
        segments: list[Path] = []
        for index, clip in enumerate(data["clips"]):
            src = resolve_src(giornata, clip)
            dest = work / f"seg_{index:02d}.mp4"
            print(f"[{index + 1}/{len(data['clips'])}] {clip['src']}", flush=True)
            render_segment(
                src,
                dest,
                duration=clip_duration(clip),
                width=width,
                height=height,
                fps=fps,
                punchline=clip.get("punchline"),
                ken_burns=bool(clip.get("ken_burns", False)),
                font=font,
                overlay_dir=work,
                index=index,
                title_card=bool(clip.get("title_card", False)),
            )
            segments.append(dest)

        silent = work / "silent.mp4"
        concat_segments(segments, silent)

        subtitled = work / "subtitled.mp4"
        cues = parse_srt(subtitles) if subtitles else []
        burn_subtitles(silent, subtitled, cues, width=width, height=height, font=font, work=work)

        mix_audio(
            subtitled,
            output,
            voice=voice,
            music=music,
            music_volume=float(data.get("music_volume", 0.16)),
            duration=duration,
            voice_volume=float(data.get("voice_volume", 1.0)),
            music_fit=bool(data.get("music_fit", False)),
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monta un recap 9:16 da una cartella giornata (timeline.yaml)."
    )
    parser.add_argument("giornata", type=Path, help="Cartella, es. giornate/g01")
    parser.add_argument("--check", action="store_true", help="Valida file e durate, non renderizza")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Crea still colorati e un beep se mancano i media (utile per l'esempio)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    giornata = args.giornata.expanduser().resolve()
    if not giornata.is_dir():
        raise AssembleError(f"Cartella inesistente: {giornata}")

    which_ffmpeg()
    data = load_timeline(giornata)
    font = find_font(data.get("font"))

    if args.demo:
        demo_assets(giornata, data, font)

    notes = check_timeline(giornata, data)
    for note in notes:
        print(note)

    if args.check:
        return 0

    output = assemble(giornata, data)
    print(f"ok: {output}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssembleError as exc:
        sys.stderr.write(f"errore: {exc}\n")
        raise SystemExit(1)
