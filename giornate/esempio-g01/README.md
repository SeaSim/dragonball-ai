# Esempio tecnico — non è un recap vero

I still e la voce **non** sono nel repo (sarebbero finti e pesanti). Li crea l'assembler:

```bash
python tools/assemble.py giornate/esempio-g01 --demo
python tools/assemble.py giornate/esempio-g01
```

Otteni `recap.mp4` 9:16 con cartelli colorati, beep al posto del narratore, punchline e sottotitoli. Serve a verificare ffmpeg e il ritmo, non a mandarlo in chat.

Quando hai i media veri: sostituisci gli png in `stills/` (o metti mp4 in `clips/` e aggiorna gli `src` nel YAML) e `voce.mp3` da ElevenLabs. Togli `--demo`.
