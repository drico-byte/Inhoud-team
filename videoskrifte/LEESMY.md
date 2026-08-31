# Video scripts — inputs, not content

Wolkskool's own video scripts, extracted from the Word documents Drico keeps in
`Marelie videos/`. Extract a new one with:

```bash
python bin/docxteks.py "<file.docx>" --uit videoskrifte/<name>.txt
```

**A script never goes to an agent raw.** It is not a source for content and not a
source for structure — CAPS is. See "When the video was made first" in
`skills/wolkskool-inhoudstandaard/SKILL.md`: the script is read here, its claims are
checked, and only a distilled `video_naat` object reaches a lesson specification.

These are committed because a fresh clone needs them to reproduce a seam. They carry
no rights problem — they are ours — which is why they sit here and not in `bronne/`.

## Gr 4 Geskiedenis, Kwartaal 3 — "Vervoer oor tyd heen"

`gr4-sw-geskiedenis-vervoer-oor-tyd-heen.txt`, 10 video lessons against 13 CAPS
items. **The videos merge three pairs of CAPS bullets, and skip one CAPS item
entirely.** Mapped 31 August 2026:

| Video | CAPS item |
|---|---|
| 1 Diere as vervoer op land | *diere* |
| 2 Die wiel, karre, waens, koetse en die fiets | *karre, waens en koetse* **+** *die fiets* — merged, and adds the wheel, which CAPS does not name |
| 3 Die stoomenjin en die trein | *die stoomenjin en die trein* |
| 4 Die motor | *die motor* |
| 5 Algemene vorms van moderne vervoer op grond | *algemene vorms van vervoer van mense en goedere op grond vandag* |
| — | **`Gevallestudie: skade aan die omgewing: uitlaatgasse in 'n groot stad` — no video, and DROPPED by Drico on 31 August 2026.** CAPS gives it its own hour and its own line, and the profiler measures it separately (182 words), so it was never inside the 2 321. Video 5 names air pollution among several challenges; there is no case study. |
| 6 Vlotte, kano's en rietbote EN sommige van die eerste seilskepe | *Vlotte, kano's en rietbote* **+** *Sommige van die eerste seilskepe* — merged |
| 7 Die eerste stoomskepe en moderne vorms van vervoer op water | *Die eerste stoomskepe* **+** *Moderne vorms van vervoer van water* — merged |
| 8 Lugballonne en lugskepe | *Ballonne en lugskepe* |
| 9 Die Wright broers | *Wright broers en die uitvinding van die eerste vliegtuig* |
| 10 Moderne vorme van lugvervoer | *Moderne vorme van lugvervoer* — and spends much of its length on space exploration, which CAPS does not name here |

**The text follows the video's division.** Drico ruled on 31 August 2026, after seeing
this mapping: *"Lets merge the caps topics such that it matches the video's when we are
doing this backwards process."* His reason is the argument worth keeping — these videos
were made by a teacher out of how she actually teaches the topic, so the seams carry
information a CAPS bullet list does not.

Coverage does not loosen. Every bullet is still covered in full and every item CAPS names
explicitly is still mandatory; only the seams move. And a merged lesson gets **one**
lesson's budget: *"We treat it as one lesson, therefore the volume should be suitable for
one lesson as well."* So the sub-topic volume is divided by the new, smaller lesson count,
and merging spends length rather than buying it.

The case study is **dropped** — Drico, same day: *"Dont worry about that gevallestudy at
all."*

### The shape that follows

| Sub-topic | Measured | Lessons | Budget each |
|---|---|---|---|
| Vervoer op land | 2 321 | **5** (bullets 2+3 merged) | 464 |
| Vervoer op water | 1 001 | **2** (1+2 merged, 3+4 merged) | 500 |
| Vervoer in die lug | 835 | **3** (no merges) | 278 |

Ten lessons against ten videos. Two things to know about those numbers.

**The air figure is not yet trustworthy, and 278 is a placeholder.** 835 is bounded by the
page the profiler was told to stop at, not by a real section end. Passing the CAPS Term 4
topic name as an end marker made it worse, not better: the air section then ran to page 158
and 3 215 words, which is more than the six-hour land section for a two-hour sub-topic. The
standard's own cross-check says page counts track the CAPS hours at roughly two pages per
hour — land 12 pages for 6 hours and water 6 for 4 both fit, while air at 6 pages for 2
hours does not. So the air section probably ends around page 144 and its pages need mapping
**by hand, by a person**, using the profiler's headings worksheet. That worksheet never goes
to an agent; only the page numbers come back.

**Water: the approved specification records 1 028 for the same six pages**, measured on an
earlier run, against 1 001 here — a 2.7% OCR difference. Use the figure from the current
config so all four sub-topics come from one run.

**The already-drafted water lesson is now partial.** "Vlotte, kano's en rietbote" was
written against a four-lesson split. Under this ruling it merges with the sailing-ships
bullet, so that draft covers half of what its lesson will owe. It was never approved, so
nothing is delivered — but the water specification has to be replanned before it is
touched again.

## Claims in these scripts that are false

Checked before any of it reached a specification. Each one is recorded in the relevant
lesson's `video_naat` so the writer routes around it rather than repeating it.

**Video 1, diere.** *"Donkies kan nie baie ver loop sonder kos en water nie"* — backwards:
a donkey tolerates thirst better than a horse and a working donkey in heat drinks about
20 l/day against a horse's 40–60. *"Hulle kan soms koppig wees"* — a myth; it is
self-preservation in a prey animal.

**Video 8, lugballonne.** *"Die skaap se naam was Montgolfier — vernoem na die twee
broers"* — the sheep on the 19 September 1783 Versailles flight was named **Montauciel**
("climb-to-the-sky"). The brothers were the Montgolfiers; the sheep was not named after
them.

**Video 2, die wiel en die fiets.** *"'n Wa is 'n toegemaakte voertuig met vier wiele
wat deur osse getrek word"* — "closed" is the **coach's** defining feature, and the same
script says so two lines later. What separates a wagon from a coach is purpose: a wagon
carries goods, a coach carries people. A wagon may be open or closed, and the South
African example — the ossewa — is open with a canvas over it.

**Video 3, die stoomenjin en die trein.** *"Hy het toe 'n lokomotief gebou wat hy 'Die
Vuurpyl' genoem het"* — the Rocket (1829) was designed by **Robert** Stephenson, George's
son, with George collaborating, and built at Robert Stephenson and Company. Not false so
much as one name short. The better anchor for what the specification actually wants from
Stephenson — that someone showed steam worked as a public service — is **Locomotion No. 1**
(1825), which was George's and opened the Stockton & Darlington. The video's "about 30 km/h"
for early trains checks out: the Rocket averaged about 19 km/h at Rainhill and topped 48.

Still flagged and **not yet verified either way**: video 10 attributing Sputnik 1 to
"Rusland" rather than the Soviet Union, and video 8's Hindenburg at "three rugby fields"
long (it was 245 m, so nearer two and a half).

## And one thing the standard already rules out

Video 7 spends a large share of its length on the Titanic. The content standard names
the Titanic specifically as failing the Aanvulling test — "a dramatic shipwreck story
is colour, not mechanism". That is fine in a video, which carries the interest. **The
text must not follow it there.**
