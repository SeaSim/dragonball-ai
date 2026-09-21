# Voce — ElevenLabs, senza clonare nessuno

Non caricare puntate della serie, non clonare il narratore ufficiale. Si **progetta** una voce nuova, stesso mestiere (cronista cosmico).

## Voice Design (una tantum)

In ElevenLabs → Voice Design / Voice Create, prompt tipo:

```text
Uomo italiano, 55-65 anni, voce baritonale molto grave, dizione chiara da doppiatore,
ritmo solenne da narratore di un anime di battaglia, pause teatrali,
zero ironia da stand-up, zero accento regionale marcato, calore eroico.
```

Genera 4–5 candidati. Ascolta **questa** frase di test:

> Nel silenzio che segue il fischio finale, una sola verità resta in piedi.

Se sembra un audiolibro per bambini o un GPS, scarta. Vuoi pietra e fiato, non entusiasmo da spot.

Salva la voce nel workspace con nome `narratore-lega`.

Piano: **Starter** basta per i recap (60s a puntata). **Creator** solo se vuoi più tentativi / qualità.

## Ogni puntata

1. Incolla lo script di `giornate/gXX/script.md`.
2. Stability alta (voce ferma), similarity alta.
3. Non esagerare con “exaggeration”: sennò recita da musical.
4. Scarica MP3 in `giornate/gXX/voce.mp3`.

Se una riga esce stonata, spezza lo script in due generazioni e concatena:

```bash
ffmpeg -y -i parte1.mp3 -i parte2.mp3 -filter_complex concat=n=2:v=0:a=1 voce.mp3
```

## Durata

~2.6–3.0 parole al secondo in italiano solenne. 150 parole ≈ 50–55s. Se l’audio supera i 62s, taglia lo script, non accelerare la voce.
