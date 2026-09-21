# Volti fotorealistici sul guerriero

Obiettivo: corpo e mondo in **grammatica Dragon Ball** (armatura, capelli a punta, aura, crateri, cielo arancione), viso **della persona vera**. È il look dei reel ibridi, non un ritratto manga.

## Perché lo still è il lock

I modelli image-to-video sono pessimi a tenere un volto identico per 10 shot. Il trucco è:

1. cuocere la faccia in un PNG master;
2. animare quel PNG per 4–6 secondi (zoom, aura, vento, scossa);
3. per un’altra posa, parti di nuovo dal master (o rifai swap sulla nuova posa), non da un video precedente.

```text
foto reale ──┐
             ├─ faceswap ─► master.png ─► clip 4-6s
corpo DB  ───┘
```

Se in clip la faccia “nuota”, il master era già debole. Rifai lo swap, non allungare il video.

## Foto sorgente

Per ogni amico (e per ogni calciatore che vuoi riconoscere al volo):

- 3–5 scatti, viso che riempie il frame
- frontale + tre quarti
- luce uniforme, niente controluce
- espressione neutra, bocca chiusa
- niente capelli sul viso, niente occhiali a specchio
- una foto “arrabbiato” e una “esultanza” se le hai: servono per gol vs flop

Calciatori: usa ritagli puliti (conferenza, photocard), non screenshot mossi dal telecronaca. Per la chat privata il rischio pratico è basso; resta comunque il diritto all’immagine, quindi meglio pochi volti-simbolo, non tutta la Serie A.

## Due look (stesso volto)

**Ibrido (consigliato per “sembra Dragon Ball”).** Corpo disegnato, testa reale. È volutamente un po’ meme: in un recap da lega funziona meglio del CGI perfetto.

**Live-action.** Persona reale in armatura Saiyan, pelle e tessuto fotografici, aura in CGI. Identità più stabile, meno “cartone”. Usalo se l’ibrido ti sembra troppo collage.

Parti dall’ibrido. Se dopo due giornate odii il collage, passi al live-action senza cambiare montaggio.

## Generare il corpo (senza innamorarti della faccia)

Prompt-base (copia e adatta da `kit/prompt-scene.md`):

> Original anime warrior, not an existing franchise character. Spiky hair, battle armor, glowing aura, cratered battlefield, dramatic orange sky, cinematic lighting, 9:16. Face will be replaced — keep head-on, eyes visible, no helmet, no hand covering the face.

Vincoli utili:

- testa frontale o tre quarti, mai di spalle
- viso grande nel frame (almeno 1/5 dell’altezza)
- niente maschere, bandeau sugli occhi, capelli sul naso
- un colore aura per fantasquadra, sempre lo stesso

## Faceswap fotorealistico

Ordine di attacco:

1. **FaceFusion** in locale — massimo controllo, gratis, da ingegnere. Prendi `master.png` come target e una foto reale come source. Alza `face enhancer` (GFPGAN/CodeFormer) se il viso esce morbido, ma non troppo: sennò diventa di plastica.
2. **Faceswap web** (Pixnova, insMind, ecc.) — per il pilota, zero install. Qualità più random.
3. **Flux Kontext con reference volto** — veloce, ma tende a *fondere* la faccia nello stile anime. Se succede, non è il tool giusto per te.

Check di accettazione del master (zooma al 100%):

- riconosci la persona in meno di un secondo
- denti/occhi non sono un pasticcio
- il collo non è un taglio netto da collage (un po’ di blend sul mento va bene)
- i capelli del guerriero restano del guerriero; non copiare la piega da ufficio dell’amico

Salva:

```text
personaggi/<id>/master.png          # identità lock, forma base
personaggi/<id>/master_ss.png       # stessa faccia, forma “arrabbiata” / aura oro
personaggi/<id>/master_ko.png       # stessa faccia, a terra, aura spenta
```

Tre master a persona bastano per un’intera stagione. Le scene settimanali sono varianti di posa, non nuovi personaggi.

## Dal master al clip

Image-to-video (Kling / Hailuo / Runway), **4–6 secondi**, prompt di moto non di identità:

> Slow push-in, aura flickering, hair moving in the wind, camera shake on impact, keep the same photorealistic face, do not change identity.

Regole:

- 2–3 tentativi a clip, poi passa oltre
- niente dialoghi: il narratore è fuori campo, le bocche chiuse
- se il volto collassa al secondo 3, tieni solo i primi 2.5s in timeline

## Consistenza tra 8 shot

Stessi tre file master. Stesso crop. Stesso colore aura. Stesso “orario” di luce (cielo arancione vs notte: scegline uno a giornata, non mischiare).

Se un amico non torna riconoscibile, riduci i suoi shot a **un** close-up del master e usa gli altri beat su paesaggio/esplosione/scouter. Meglio 2 facce perfette che 8 facce quasi.
