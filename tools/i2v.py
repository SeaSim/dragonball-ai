# Image-to-video (Kling via fal.ai)
# python tools/i2v.py personaggi/tiziano/master.png --scene stand
from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


PROMPTS = {
    "stand": (
        "Cinematic live-action shot. The same warrior stays in frame, identity locked, "
        "photorealistic face unchanged. He breathes, chest rises slightly, eyes blink once. "
        "Ki aura around the body swirls and flickers like fire in slow motion, particles of energy "
        "rising. Hair and cape-less armor catch a wind from the aura. Slow push-in. "
        "Mouth closed, no talking, no extra characters, no morphing."
    ),
    "colpo": (
        "Cinematic live-action. Same warrior, identity locked, photorealistic face unchanged. "
        "He leans forward and fires a ki energy blast from his palm toward the camera, "
        "shockwave, debris flying, aura flaring, camera shake on impact. "
        "Mouth closed, no talking, no extra characters, keep the same face."
    ),
    "ss": (
        "Cinematic live-action Super Saiyan-like transformation. Same warrior, identity locked. "
        "He screams powering up, lightning strikes, ground cracks, aura explodes from white-gold "
        "to raging gold, hair stands up and turns golden blonde while the FACE stays the same person. "
        "Camera slow orbit. No extra characters, no morphing into a different person."
    ),
}

NEGATIVE = (
    "blur, morphing face, identity change, extra people, cartoon, anime still, "
    "slideshow, jitter, text, watermark, talking, lip sync"
)

MODELS = {
    "pro": "fal-ai/kling-video/v2.6/pro/image-to-video",
    "std": "fal-ai/kling-video/v2.1/standard/image-to-video",
}


def image_to_data_url(path: Path) -> str:
    import base64

    raw = path.read_bytes()
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix)
    if mime is None:
        mime = "image/jpeg" if raw[:3] == b"\xff\xd8\xff" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def resolve_image_url(image: Path) -> str:
    import fal_client

    try:
        return fal_client.upload_file(str(image))
    except Exception as exc:
        print(f"upload CDN non disponibile ({type(exc).__name__}), uso data-URI", flush=True)
        return image_to_data_url(image)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(
        description="Image-to-video Kling (fal.ai). Serve FAL_KEY in .env"
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("--scene", choices=sorted(PROMPTS), default="stand")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--model", choices=sorted(MODELS), default="pro")
    parser.add_argument("--seconds", choices=("5", "10"), default="5")
    parser.add_argument("--prompt", default="")
    args = parser.parse_args()

    if not os.environ.get("FAL_KEY"):
        sys.stderr.write(
            "Manca FAL_KEY.\n"
            "1. Crea un account su https://fal.ai/dashboard/keys\n"
            "2. Copia .env.example in .env e incolla la chiave\n"
            "3. Ripeti questo comando\n"
        )
        return 2

    image = args.image.expanduser().resolve()
    if not image.is_file():
        sys.stderr.write(f"manca {image}\n")
        return 1

    try:
        import fal_client
    except ImportError:
        sys.stderr.write("pip install fal-client\n")
        return 1

    prompt = args.prompt.strip() or PROMPTS[args.scene]
    print(f"upload {image.name} …", flush=True)
    image_url = resolve_image_url(image)
    model = MODELS[args.model]
    print(f"kling {args.model} {args.seconds}s scene={args.scene} …", flush=True)

    def on_queue_update(update) -> None:
        if isinstance(update, fal_client.InProgress):
            for log in update.logs or []:
                msg = log.get("message") if isinstance(log, dict) else None
                if msg:
                    print(msg, flush=True)

    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "prompt": prompt,
                "start_image_url": image_url,
                "duration": args.seconds,
                "negative_prompt": NEGATIVE,
                "generate_audio": False,
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
    except Exception as exc:
        body = getattr(getattr(exc, "response", None), "text", "")
        sys.stderr.write(f"kling errore: {exc}\n")
        if body:
            sys.stderr.write(body[:1200] + "\n")
        return 1

    video = (result or {}).get("video") or {}
    url = video.get("url") if isinstance(video, dict) else None
    if not url:
        sys.stderr.write(f"risposta inattesa: {result}\n")
        return 1

    output = args.output or image.with_name(f"{image.stem}_{args.scene}_i2v.mp4")
    print(f"download {url}", flush=True)
    download(url, output)
    print(f"ok: {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
