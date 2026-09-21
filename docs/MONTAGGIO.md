# Montaggio da zero

Non ti serve una laurea in Premiere. Un recap è una **playlist di clip** con una voce sopra e quattro scritte. Da ingegnere: timeline = lista ordinata, traccia = layer, taglio = `duration`.

Percorso principale di questo repo: YAML + `ffmpeg`.

CapCut è un optional. Impari le 8 gesture in un caffè, se dopo il primo assemble vuoi flash e shake più comodi.

## Anatomia di 50 secondi

| Tempo | Cosa succede | Asset |
| --- | --- | --- |
| 0–4s | Hook (“La Terra trema…”) | clip più spettacolare + punchline titolo |
| 4–14s | Beat 1 (capocannoniere / scontro) | 2 clip |
| 14–24s | Beat 2 (flop o autogol) | 2 clip |
| 24–36s | Beat 3 (rimonta / trasformazione) | 2 clip |
| 36–46s | Beat 4 (classifica come power level) | still classifica + 1 clip |
| 46–55s | Chiusura narratore | cielo / sfera / logo lega |

8–12 pezzi. Nessuno più lungo di 6 secondi. Il ritmo è il 70% dell’effetto “Dragon Ball”.

## Assembler (quello che userai tu)

Nella cartella di una giornata ti servono:

```text
giornate/g01/
  timeline.yaml
  voce.mp3              # da ElevenLabs
  musica.mp3            # opzionale, libreria royalty-free
  sottotitoli.srt       # opzionale
  clips/                # mp4 già tagliati
  stills/               # png/jpg, l'assembler fa il Ken Burns
```

```bash
# dry-run: controlla file e durate
python tools/assemble.py giornate/esempio-g01 --check

# render
python tools/assemble.py giornate/esempio-g01
```

Output: `giornate/g01/recap.mp4` a 1080×1920.

Cosa fa lo script:

1. Ogni clip viene scalato/paddato a 9:16 (niente stiramento).
2. Gli still diventano clip con zoom lento.
3. Concatena in ordine.
4. Mixa voce (volume 1.0) e musica (volume basso, default 0.16).
5. Overlay delle punchline (PNG via Pillow: il ffmpeg di Homebrew non ha `drawtext`).
6. Sottotitoli se c’è un `.srt`, stesso sistema.

Se `ffmpeg` manca: `brew install ffmpeg`.

## Come tagliare i grezzi senza “saper montare”

I tool di generazione ti danno già mp4 di 5–10s. Non serve un NLE per accorciarli:

```bash
# primi 4.5 secondi, senza ricalcolare tutto
ffmpeg -y -i grezzo.mp4 -t 4.5 -c copy clips/03_gol.mp4

# se -c copy non taglia sul keyframe e “salta”:
ffmpeg -y -i grezzo.mp4 -t 4.5 -an clips/03_gol.mp4
```

L’audio dei clip **si butta**: parla solo il narratore.

## Sottotitoli

File `.srt` semplice (già nell’esempio). Un blocco = una frase del narratore. Tempi a orecchio dopo il primo ascolto della voce: metti play, annota quando inizia ogni periodo.

In CapCut esiste “caption automatiche”: utile, ma l’SRT ti resta versionato nel repo.

## Punchline a schermo

Roba da scouter, poche, grandi, mai insieme al sottotitolo lungo:

- `GOL`
- `FLOP`
- `+15`
- `KO`
- `POWER LEVEL`

Nel YAML: campo `punchline` sul clip. Lo script le mette in basso, font grosso. Una ogni 8–10 secondi, non su ogni inquadratura. Lo zoom lento (`ken_burns: true`) è spento di default: è lento e non serve per WhatsApp.

## CapCut — il montaggio vero

CapCut non è più un optional: è lì che il recap prende il ritmo (shake, flash, caption, punchline).

Guida da 20 minuti, con l’esempio già in repo: [`docs/CAPCUT.md`](CAPCUT.md).

Assembler Python: smoke test e piano B, se un lunedì non vuoi aprire la GUI.
