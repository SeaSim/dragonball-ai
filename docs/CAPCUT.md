# CapCut — prima sessione (20 minuti)

Sì, impari quello che ti serve. Non è Premiere: è una timeline con drag-and-drop e 6 scorciatoie. Dopo un recap montato a mano, il lunedì successivo è copia-incolla.

Usa **CapCut Desktop** (Mac), gratis. Evita il telefono: i file della giornata stanno già sul disco.

Traduzione mentale:

| CapCut | Quello che già conosci |
| --- | --- |
| Timeline | array di segmenti in ordine |
| Traccia sopra | layer |
| Split (`Cmd+B`) | splice all’indice t |
| Delete | splice out (a volte lascia un buco) |
| Shift+Delete | splice out + compact (ripple) |
| Testo | overlay con durata propria |
| Volume | gain in dB |
| Export | encode H.264 |

## Scorciatoie (queste, basta)

| Azione | Mac |
| --- | --- |
| Play / pausa | Spazio |
| Split sul playhead | `Cmd+B` |
| Annulla | `Cmd+Z` |
| Elimina e chiudi il buco | `Shift+Delete` |
| Zoom timeline | `Cmd+` / `Cmd-` |
| Esporta | `Cmd+E` |

Se sbagli, `Cmd+Z`. Sempre.

## Esercizio: monta l’esempio in 20 minuti

Non aspettare i volti veri. Usa `giornate/esempio-g01/stills/` e `voce.mp3` (anche il beep va bene: stai imparando i gesti, non l’arte).

### 1. Progetto (2 min)

1. Scarica [CapCut Desktop](https://www.capcut.com/tools/desktop-video-editor) e apri.
2. **Nuovo progetto**.
3. In alto, rapporto **9:16**. Risoluzione 1080×1920 se te la chiede. 30 fps.
4. Salva col nome `lega-g01` (CapCut tiene i progetti nella sua cartella, non nel repo: va bene).

### 2. Importa (2 min)

Media → Importa → seleziona:

- tutti i png in `giornate/esempio-g01/stills/`
- `voce.mp3`

Trascina gli still sulla timeline **in ordine** (01 hook → 07 chiusura), uno dopo l’altro sulla stessa riga. Sono fotogrammi: CapCut gli dà una durata di default (spesso 3–5s).

La voce **non** va sulla stessa riga dei video. Trascinala sulla traccia audio sotto, allineata a t=0.

### 3. Dura 50 secondi (5 min)

Obiettivo: il video finisce insieme alla voce.

- Clicca uno still → tira il **bordo destro** per allungarlo/accorciarlo.
- Se uno still è troppo lungo: playhead a metà → `Cmd+B` → seleziona il pezzo di troppo → `Shift+Delete`.
- Se tra due clip c’è un buco nero, seleziona il buco o usa ripple (`Shift+Delete` sul vuoto / tira i clip a sinistra).

Durata target degli still, per copiare il recap d’esempio:

| Clip | Secondi |
| --- | --- |
| 01 hook | 5.5 |
| 02 gol | 8 |
| 03 flop | 6.5 |
| 04 rimonta | 7.5 |
| 05 para | 6 |
| 06 classifica | 8 |
| 07 chiusura | 8.5 |

Totale 50s. Non essere preciso al frame: ±0.3s è invisibile su WhatsApp.

Audio dei clip video: se CapCut ha tenuto un silenzio/rumore, clicca il clip → volume a **0**. Parla solo il narratore.

### 4. Punchline (5 min)

Testo → **Testo predefinito** (o “Default text”). Scrivi `GIORNATA 1`.

Poi, a destra:

- Font grosso (Impact / Montserrat ExtraBold / quello più “scouter”)
- Bianco
- Contorno nero spesso (Outline)
- Centro orizzontale, verso il **basso** ma non attaccato al bordo (WhatsApp copre i 80px bassi)

La scritta è un clip sulla traccia sopra. Accorciala a **1.5–2.5 secondi**. Duplica (`Cmd+D` o Alt-trascina) e cambia la parola:

- `GOL`
- `KO`
- `RIMONTA`
- `PARA`
- `POWER LEVEL`

Una punchline ogni 8–10 secondi, in sincrono col beat. Non su ogni inquadratura.

Quando il look ti piace: clic destro sul testo → **Crea preset** / salva stile. La settimana dopo è un click.

### 5. Due effetti, non di più (3 min)

Solo sul taglio del gol (tra hook e `GOL`):

1. Seleziona il clip del gol.
2. Pannello **Effetti** → cerca `shake` o `tremolio` → 0.4–0.8s.
3. Stesso taglio: cerca `flash` / `white flash` / `bagliore`. Un fotogramma bianco.

Stop. Niente glitch, speed ramp, RGB split, mask. Su un recap da 50s due colpi bastano; dieci sembrano un template TikTok del 2019.

### 6. Caption (2 min)

Pannello **Caption** / **Sottotitoli** → **Auto captions** → italiano → genera.

Poi:

- Font più piccolo delle punchline
- Due righe max
- Le sposti un po’ **sopra** le punchline, così non si litigano
- Correggi le stupidaggini (nomi della lega, “Saiyan”, fantavoti)

Se l’auto-caption è un disastro, usa `sottotitoli.srt` (Importa sottotitoli) oppure niente: la voce epica si capisce comunque.

### 7. Musica, piano (1 min)

Audio → musica di libreria CapCut (è già licenziata per social; per WhatsApp privati ancora meglio). Niente sigle.

Volume della musica: **−18 / −22 dB**. La voce deve restare il canale principale. Se CapCut ha “auto ducking” / abbassa musica quando parla, accendilo.

### 8. Esporta (1 min)

`Cmd+E`:

- 1080p
- 30 fps
- Codec H.264 / mp4
- Bitrate alto / “consigliato”

Salva una copia anche in `giornate/gXX/recap.mp4` così resta col resto della giornata.

## Flusso del lunedì, da settimana 2

Non rimonterai da zero. Duplica il progetto CapCut della puntata prima (`File → Duplica` / “Save as”).

1. Tieni la struttura: 7 slot, testi preset, volumi, export.
2. Sostituisci i clip: tasto destro sul clip in timeline → **Sostituisci** (Replace) con il nuovo mp4. La durata e gli effetti restano.
3. Sostituisci `voce.mp3`.
4. Riscrivi 5 punchline.
5. Rigenera le caption.
6. Esporta.

Tempo vero a regime: **15–25 minuti** di CapCut, dopo che i clip e la voce sono pronti. Il collo di bottiglia resta la generazione scene, non il montaggio.

## Cosa non toccare (ancora)

- Color grading / LUT
- Keyframe a mano sul testo (i preset di CapCut già animano)
- Speed ramping
- AI “auto reframe” (i tuoi clip sono già 9:16)
- Plugin e template “Dragon Ball” del marketplace: spesso usano IP della serie e font/sigla. I tuoi preset bastano.

## Se ti blocchi

| Sintomo | Causa tipica | Fix |
| --- | --- | --- |
| Bande nere ai lati | clip 16:9 in canvas 9:16 | clic sul clip → riempi / scala finché copre |
| Voce in ritardo | audio non parte da 0 | tira `voce.mp3` all’inizio della timeline |
| Punchline tagliata da WhatsApp | troppo in basso | alza di ~80–100 px |
| Video a 16:9 in export | rapporto progetto sbagliato | 9:16 **prima** di importare, o Ratio in alto |
| Faccia tagliata | still troppo zoomato | scala indietro, tieni gli occhi nel terzo medio |

Assembler Python: resta lo smoke test e il piano B (`python tools/assemble.py giornate/gXX`). Il recap che manderai in chat, dopo questa sessione, lo farai in CapCut.
