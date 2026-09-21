# Recap Fantacalcio — omaggio Dragon Ball

Video di **45–60 secondi** a fine giornata, per la chat della lega.

Non è la serie ufficiale: guerrieri **originali**, voce **epica originale** (non il narratore vero), musiche di libreria. I volti di amici e calciatori restano **fotorealistici** e vengono montati sul corpo del guerriero.

## Come funziona, in una frase

Ogni lunedì: risultati → script da narratore → audio → 8–12 clip corte con faccia reale su corpo Saiyan-like → **CapCut** monta il 9:16.

```text
dati giornata → script 45-60s → voce TTS
                              ↘
foto/master still → face-swap fotoreale → clip 4-6s → CapCut → recap.mp4
```

Il volto si cubica **nello still**, non nel video. Se “non è lui”, rifai la foto-base, non il montaggio.

## Cosa ti serve (stack minimo)

| Pezzo | Tool | Costo indicativo |
| --- | --- | --- |
| Voce | [ElevenLabs](https://elevenlabs.io) Voice Design (italiano, grave, teatrale) | 6–22 $/mese |
| Corpo guerriero | Flux Kontext / Midjourney / Kling Image | 5–15 $/mese |
| Volto fotoreale | [FaceFusion](https://github.com/facefusion/facefusion) in locale, oppure un faceswap web | 0 € in locale |
| Motion | Kling 2.6 Pro (image-to-video via fal.ai) | ~0,40–0,80 € a clip da 5s |
| Montaggio | CapCut Desktop | 0 € |
| Piano B | questo repo + `ffmpeg` | 0 € |

Totale realistico: **25–60 €/mese** + **1,5–3 ore** a giornata dopo il setup.

Mac: `brew install ffmpeg`. Poi:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Setup una tantum (un weekend)

1. Chiedi il consenso in chat (foto usate solo per i recap della lega).
2. Per ogni persona: 3–5 foto frontali, luce buona, bocca chiusa, niente occhiali se possibile. Mettili in `personaggi/<id>/foto/`.
3. Compila `personaggi/<id>/scheda.yaml` copiando `_template.yaml`.
4. Genera **un** master still per guerriero (corpo + aura). Poi faceswap della faccia reale. Salva `personaggi/<id>/master.png`.
5. Crea la voce su ElevenLabs (istruzioni in `kit/voce-elevenlabs.md`).
6. Fai **un** pilota con `giornate/esempio-g01/` per capire i tempi veri.

Dettaglio volti: [`docs/VOLTI.md`](docs/VOLTI.md).  
Image-to-video (Kling): [`docs/I2V.md`](docs/I2V.md).  
Prima sessione CapCut (20 min): [`docs/CAPCUT.md`](docs/CAPCUT.md).  
Montaggio / assembler di riserva: [`docs/MONTAGGIO.md`](docs/MONTAGGIO.md).

## Ogni lunedì

Checklist: [`kit/checklist-lunedi.md`](kit/checklist-lunedi.md).

```bash
python tools/assemble.py giornate/esempio-g01
```

L’esempio usa still finti e un beep al posto della voce: serve a verificare `ffmpeg`, non a pubblicare.

## Cosa non fare

- Non clonare la voce del narratore ufficiale.
- Non usare Goku, Vegeta, Freezer, sigla o frame della serie.
- Non chiedere a un modello video un piano-sequenza da 60 secondi: escono morphing e la faccia collassa.
- Non stilizzare la faccia in manga. Se il tool “anime-izza” il volto, alza il peso del faceswap o cambia tool.
