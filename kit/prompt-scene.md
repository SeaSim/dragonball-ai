# Libreria prompt — 6 tipi di scena

Tutti i prompt sono in inglese perché i generatori obbediscono meglio. Aggiungi sempre, in coda:

```text
Original character, not an existing franchise character, not Goku, not Vegeta.
Photorealistic human face already on the warrior (do not stylize the face into anime).
Vertical 9:16, cinematic, head visible, no helmet, no hand on the face.
```

Sostituisci `AURA` con il colore della fantasquadra (gold / blue / crimson / white).

## 0. Master corpo (una tantum, prima dello swap)

```text
Medium shot of an original Saiyan-like anime warrior standing on a cratered battlefield,
spiky hair, battle armor with shoulder plates, AURA ki energy raging,
dramatic orange sunset sky, strong rim light, face toward camera, eyes visible,
9:16 poster frame, ultra detailed body and costume, face is placeholder.
```

Poi faceswap fotorealistico → `master.png`.

## 1. Hook / power level

```text
Same original warrior as reference, photorealistic face unchanged,
low angle hero shot, scouter-like orange HUD numbers in the sky,
AURA exploding, rocks floating, camera slightly below,
9:16, 4 seconds of slow push-in.
```

Punchline tipica: `GIORNATA 4` / `POWER LEVEL`.

## 2. Gol / colpo finale

```text
Same warrior, photorealistic face unchanged, both hands forward firing a massive
spiral ki blast toward camera, shockwave, debris, hair whipping,
motion blur on the energy only, face sharp,
9:16, 5 seconds.
```

Punchline: `GOL` / `+15`.

## 3. Flop / KO

```text
Same warrior, photorealistic face unchanged, fallen on one knee in the crater,
AURA dying, smoke, rain of pebbles, defeated but proud,
cinematic close-up, 9:16, 4 seconds, slow drift.
```

Punchline: `KO` / `FLOP`.

## 4. Trasformazione / rimonta

```text
Same warrior, photorealistic face unchanged, screaming upward,
lightning around the body, AURA blooming from white to gold,
ground cracking, slow motion, 9:16, 5 seconds.
```

Punchline: `RIMONTA`.

## 5. Portiere / barriera

```text
Same warrior, photorealistic face unchanged, arms crossed, spherical ki shield
blocking a beam, sparks on the barrier, wide stance, 9:16, 4 seconds.
```

Punchline: `PARA`.

## 6. Scontro diretto (due fantasquadre)

Genera **due still** (un guerriero ciascuno, stesso cielo), poi in montaggio: taglio rapido A/B, non un unico frame con due facce swapate (fallisce quasi sempre).

```text
Profile shot, original warrior facing right, photorealistic face,
AURA, battlefield, room on the right side of frame for the opponent,
9:16.
```

Speculare `facing left` per l’altro.

## Image-to-video (stesso per tutti)

```text
Keep identity and photorealistic face locked. Subtle motion only:
aura flicker, hair in wind, camera push-in, light shake on impact.
No talking, mouth closed, no extra characters, no morphing.
```
