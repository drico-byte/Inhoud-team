---
name: lesnommers-loop-deur-die-jaar
description: "Lesson numbers run 1..~30 across the whole year, not per term. File name is Drico's CAPS index; the lesson title is the learner's hero and is deliberately different."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T14:04:50.768Z
---

Drico, 2026-08-21: "We can continue the numbering from 8 until the end. I think it will be like 30
lessons total." And, on the two names: "Yes the name in die lesson doesnt have to match file name.
Thats just to see that i have everything mentioned in caps."

## The numbering

**Continuous across the year, not restarting per term.** Gr 4 Natuurwetenskappe en Tegnologie: Term 1's
theme "Lewe en lewende dinge" is lessons **1 to 8**, so Term 2 begins at **9**. He expects roughly
**30 lessons for the year**.

The order follows his term-plan spreadsheet row order, not the order lessons happen to get finished. He
corrected his own files once to bring them back in line with the plan, so the number is a real index:

1. Lewende dinge · 2. Nie-lewende dinge · 3. Strukture van plante · 4. Strukture van diere ·
5. Wat plante benodig vir groei · 6. Verskillende habitatte · 7. Behoefte aan habitatte ·
8. Diere skuilings

## Two names per lesson, doing two different jobs

**The PDF file name** is `N_<CAPS-matching label>.pdf` — his own index, so the folder sorts against his
term plan and he can see at a glance that everything CAPS mentions is present. These are the labels from
the plan's "Inhoud en konsepte (les)" column.

**The lesson's `titel`** is the learner-facing hero heading and is deliberately different — "Die dele van
'n plant" against the file's "3_Strukture van plante". Do not try to make them match; forcing one word to
do both jobs makes one of them worse. See [[elke-les-kry-n-eie-naam]].

## How the files get there

He copies from the pipeline's output in `lees/<graad>/<vak>/` and renames by hand. **The pipeline does not
emit his convention**, because the number and the label live in his spreadsheet, not in any file the
pipeline reads.

Two consequences worth remembering. His copies go stale whenever a lesson is revised, and lessons are
often revised three or four times before they are final — on 2026-08-21 four of his six copies were behind
and all four had new titles. So **tell him which of his copies are stale after any revision round**; a
straight mtime comparison against the lesson JSON answers it. And an offer already made once and not taken
up: if he hands over the term plan as data, the tool could emit `N_label.pdf` directly and he would stop
renaming. Worth raising again if the hand-renaming starts costing him real time at thirty lessons.
