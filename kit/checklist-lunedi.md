# Checklist lunedì (a regime: 90–150 min)

Le prime 2–3 giornate possono arrivare a 3–4 ore. Poi i master e i prompt sono già fatti.

## 0. Dati (5 min)

- [ ] Classifica di lega
- [ ] Risultati degli scontri
- [ ] Top 3 fantavoti / bonus
- [ ] Flop della giornata (0, autogol, squalifica, panchinaro lasciato fuori)
- [ ] Un fatto umano (cucchiaiata, gol al 95’, portiere eroe)

Incolla tutto in `giornate/gXX/dati.md`.

## 1. Script (15–20 min)

- [ ] Copia `kit/script-template.md` in `giornate/gXX/script.md`
- [ ] 130–160 parole, 5–6 beat, 45–60 secondi a voce
- [ ] Fatti veri, iperbole sullo stile, mai sul risultato
- [ ] Leggi ad alta voce una volta: se ti manca il fiato, taglia

## 2. Voce (5 min)

- [ ] ElevenLabs, voce salvata del progetto
- [ ] Incolla lo script, genera, scarica `voce.mp3`
- [ ] Se una frase “canta” male, rigenera solo quella e concatena (o ritenta tutto: costa poco)

## 3. Scene (45–75 min) — il pezzo lungo

- [ ] Scegli 3–5 guerrieri coinvolti (non tutta la lega)
- [ ] Per ciascuno: parti dai `master.png` già pronti
- [ ] 6–10 still di posa (prompt da `kit/prompt-scene.md`)
- [ ] Faceswap se la posa nuova ha perso il volto
- [ ] Image-to-video 4–6s, 2–3 tentativi max a clip
- [ ] Taglia i grezzi in `clips/` con `ffmpeg -t`

## 4. Timeline (15–25 min) — CapCut

- [ ] Apri il progetto della puntata prima (o creane uno 9:16, vedi [`docs/CAPCUT.md`](../docs/CAPCUT.md))
- [ ] Sostituisci i clip e `voce.mp3`
- [ ] 5 punchline (GOL / KO / POWER LEVEL)
- [ ] Auto captions in italiano, correggi i nomi
- [ ] Musica a −18 dB
- [ ] Esporta 1080p in `giornate/gXX/recap.mp4`

Piano B se CapCut ti sta sulle scatole:

- [ ] Compila `timeline.yaml`
- [ ] `python tools/assemble.py giornate/gXX`

## 5. Controllo (5 min)

- [ ] Durata 45–60s
- [ ] Si riconoscono i volti al primo colpo
- [ ] La musica non copre il narratore
- [ ] Nessun nome di personaggio ufficiale
- [ ] Manda in chat

## Se sei in ritardo (versione 40 min)

Hook + 4 clip + classifica still + voce. Niente trasformazione, niente secondo flop. La costanza batte il film.
