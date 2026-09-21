# Image-to-video — Kling (il look da social)

ffmpeg sul posto **non basta**. I reel che hai visto usano un modello I2V (di solito Kling): lo still del guerriero diventa 5 secondi di corpo che respira, aura che si muove, colpo che parte.

Qui usiamo **Kling 2.6 Pro via [fal.ai](https://fal.ai)** — stesso tipo di motore, da terminale.

## Costo (ordine di grandezza)

- 5 secondi Pro: circa **0,40–0,80 €** a clip
- Un guerriero (in piedi + colpo + SS) ≈ **1,5–2,5 €**
- Tre guerrieri, una volta: **5–8 €**
- Ogni giornata poi rigeneri solo le scene nuove, non tutti i master

Piano **std** (`--model std`) costa meno, qualità più da “AI”; per il recap usa **pro**.

## Setup una tantum

1. Account su https://fal.ai/dashboard/keys
2. Crea una API key
3. Nel repo:

```bash
cp .env.example .env
# incolla FAL_KEY=...
source .venv/bin/activate
pip install -r requirements.txt
```

## Comandi

```bash
# Tiziano in piedi (respiro + aura)
python tools/i2v.py personaggi/tiziano/master.png --scene stand \
  -o personaggi/tiziano/anim/clip_master.mp4

# Colpo
python tools/i2v.py personaggi/tiziano/master_colpo.png --scene colpo \
  -o personaggi/tiziano/anim/clip_colpo.mp4

# Trasformazione (capelli → biondo)
python tools/i2v.py personaggi/tiziano/master_ss_pre.png --scene ss \
  -o personaggi/tiziano/anim/clip_trasformazione.mp4
```

Scene: `stand` | `colpo` | `ss`. Durata 5s default, `--seconds 10` se serve.

Audio Kling **spento**: parla solo il narratore in montaggio.

## Cosa non chiedere al modello

- Un piano-sequenza da 60 secondi
- Che inventi la faccia (parte dallo still già cotto)
- Dialoghi / lip-sync
