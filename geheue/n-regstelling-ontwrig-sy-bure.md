---
name: n-regstelling-ontwrig-sy-bure
description: "The most reliable failure in this pipeline — a fix aimed at one finding activates an error somewhere else. Always ask \"what did this disturb\", not \"is it fixed\"."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T19:19:58.299Z
---

The single most useful operational lesson of 2026-08-21. It happened **seven times in one day**, across
four different lessons and both checkers.

## The instances

- **Plastic ball → clay brick.** Fixing a contested origin introduced a new object needing its own origin
  check.
- **Shell definition.** Dropping the wrong phrase "een hele stuk" also dropped "om die ruimte binne",
  which was the leg that separated a shell from a solid. A brick then satisfied the definition.
- **Nest wording.** Removing "los dele" (which let a reader classify a nest off our own page) produced
  "van gras of modder", which contradicted the block's own next three sentences.
- **The shark.** Added to make a cartilage exception concrete; a shark's vertebrae are cartilage, so it
  contradicted "the backbone is made of small bones" three sentences later.
- **The fern's stem.** Correctly giving a fern a stem turned a previously safe sentence two blocks away
  ("the stem holds the leaves and flowers high above the ground") into a falsehood.
- **The zebra and the hole.** True in isolation; false by juxtaposition, because the only animal named
  before it was a zebra.
- **The habitat size sentences.** Added to fix a definition error, then flagged as unrequested content by
  the coverage checker.

## Why it happens, and why nobody is being careless

The writer is looking at one block. The checker is looking at one claim. **Nothing in the process asks
"and what does this now sit next to?"** So the fix is judged against the finding it answers, which it
always satisfies, and never against the text around it.

Three recurring shapes:
- **A named example is a new factual claim.** Every concrete thing added must be read against the whole
  lesson, not just the sentence it repairs.
- **A deletion can strand a reference.** "Hierdie geraamte" pointed at the wrong thing once the shark was
  removed; cutting a zebra sentence left "die grasveld" arriving with a definite article and no
  introduction.
- **A correction can activate a latent error.** Nothing was wrong with the stem sentence until the fern
  was given a stem.

## What to do

**Add one line to every revision brief and every re-check request: "then read the whole lesson for what
this fix disturbed — not whether the finding is gone."** That single question caught the shark, the stem,
the zebra and the meerkat before any of them shipped. It costs one sentence.

And when a checker prescribes a fix, remember it is reasoning from its own finding outward. Three times
on 2026-08-21 a checker was right that something was wrong and its suggested fix would have introduced a
new error — see [[wanneer-vra-en-wanneer-doen]] and Drico's own early instruction that a checker "needs
reading rather than obeying".

## And once ACROSS two lessons — 2026-08-24

Term 2's lessons 14 and 15 ended up making opposite claims about folds. Lesson 14,
after a fact-check correction, says the fold lines in a paper pillar are the
**stiffest** part and give way last. Lesson 15 said there is nowhere a fold where the
tube can buckle, which says a fold is the **weak** place.

Both are defensible alone. A fold running lengthwise along a column is a stiffener; a
crease across paper is a weak hinge. A nine-year-old cannot hold that distinction and
should not have to.

**Neither checker could see it. Each reads one lesson.** The coverage checker can open
a sibling when told to — it opened lesson 14 to confirm the word *stut* was absent —
but nothing checks two finished lessons against each other as a matter of course.

Resolved by putting both lessons on the **same** mechanism: flat faces bulge outward
and stop carrying, a round wall has none. Sourced, and the two lessons now reinforce
each other.

**How to apply.** When a fact check corrects a *mechanism* rather than a fact, ask
which sibling lessons teach the same mechanism, and name them in the revision brief.
The risk is highest inside one sub-topic, where lessons deliberately build on each
other. Related: [[meting-dek-minder-as-die-lesse]].

## Give sibling lessons by PATH, not by name — a writer cannot browse

2026-08-25, Term 2 lesson 16. The brief told the writer to build on lesson 15 and on
Term 1's lesson 8, naming both. It could find neither: the writer agent has Read and
Write but no shell, so it cannot list a directory to find a file it was not handed. It
searched, failed, said so, and wrote the lesson from the brief alone — which is the
right behaviour, and the only reason the gap was visible.

**So whenever a brief asks for continuity with another lesson, paste the path.** The
same applies to a checker asked to cross-check a sibling.

Grade 4 NWT paths, for reference:
`konsepte/gr4/natuurwetenskappe-en-tegnologie/<subonderwerp-slug>/les-N.json`

And when the writer could not do it, the coverage checker can — it reads whatever paths
it is given. Hand the cross-check downstream rather than losing it.

**Give the report path too.** Twice on 2026-08-25 a coverage checker had no output path
in its brief and chose one — `.../nasien/les-1-dekking.json` once and
`.../verslae/les-1-dekking.json` once. The runner reads only
`<lesson-dir>/les-N.dekking.json`, so both had to be moved by hand before the verdict
could be read. Every checker brief needs the output path spelled out, the same as the
inputs.


## The neighbour that keeps getting forgotten: the heading

Gr 4 NWT Term 4, 2026-08-28, three times in one sitting. Each time a correction landed in
the sentence and left the **block heading** carrying the wording that had just been proved
false:

- *Wat is die Maan?* — the sentence became "our nearest large neighbour"; the heading still
  read "the nearest thing to us in space".
- *Waarvan die Aarde gemaak is* — the sentence limited rock to the outer part; the heading
  still read "the Earth is a big ball of rock".
- Same lesson, second round: caught only because a checker looking at a different block
  noticed it in passing.

**Why it is always the heading.** It is not part of the sentence being edited, so it falls
outside the writer's attention — and it is the most prominent line in the block, so it is
the version a learner actually remembers.

**What to do.** Every revision brief that corrects a claim must also ask for a sweep of the
headings, glossary entries and word list against the corrected wording. Asking "what did
this disturb" is not enough on its own; name the headings specifically.

## The cleanest example yet: a corrected state left an old action behind

2026-09-03, the Grade 4 water-safety story. A fact check found the drowning boy's
eyes looking straight at the girl who saw him; drowning eyes are closed or glassy
and unfocused, and the line undid the story's whole purpose. Fixed: he does not
look back, his eyes are open and focused on nothing.

The next check found what that took with it. Four sentences later, **"Neo se hande
het om die hout toegevou en hy het vasgehou."** A person in the drowning response
cannot perform a deliberate grasp — that is the textbook distinction between a
swimmer in distress, who can take a line and help with their own rescue, and a
drowning person, who cannot. While he still looked back at Marika he was
responsive and the grasp fitted. Making him unresponsive was right, and it
orphaned the grasp.

**The shape to look for: a fix that changes a character's or a system's STATE, with
an ACTION elsewhere that only the old state permitted.** The two sentences never
mention each other and no keyword links them. Searching for the words you changed
would not have found it.

Worse, the leftover taught the opposite of the lesson's own point — that a drowning
child will take the stick you hold out. That is exactly the expectation that makes
a rescuer decide the child must be fine, or go in when the reach fails.

So when a correction changes what someone can do, **re-read every later action they
perform**, not just the sentences near the edit.

## The sharpest form yet: I CLEARED the neighbour inside the fix that broke it

2026-09-22, Gr 4 SW, the locomotive lesson. A fact check found the study text
putting the engine's fire **under** the boiler. I corrected it at source — the fire
burns in a firebox that is part of the boiler, water around and above it — and in
the same note I wrote, in capitals, **"DIE eli10-BLOK IS AL REG"**, quoting its
closing sentence as proof.

It was right. It stopped being right the moment my own fix landed.

The intuition block opens by asking the child to picture a pot boiling **on the
stove**, and then holds pot and boiler side by side for six sentences without ever
breaking the correspondence for the heat source. While the study text also had the
fire underneath, the two blocks agreed and the stove was invisible. Once the study
text moved the fire inside, the stove was the only remaining answer to "where does
the fire burn" — and it is the wrong one. A targeted re-check of that block alone
found it; three ordinary checks had not.

**The shape: a clearance written at the moment of a fix is measured against the text
as it was BEFORE the fix.** It reads as settled afterwards — mine was in capitals,
with a quotation and a date — so the next reviser meets it as a closed question and
does not re-test it. That is worse than saying nothing, because a false guard also
shelters the fault (see [[my-regstelling-in-die-spek-was-self-die-volgende-fout]] and
[[n-reggemaakte-veld-kan-nog-n-ander-fout-dra]]).

**How to apply.** Never certify a neighbouring block in the same note that changes
its neighbour. If the fix makes you want to write "X is already right", that is
exactly the block to re-check *after* the fix lands — the impulse is the signal. And
when withdrawing such a line, withdraw the RULING and not only the error:
[[n-teruggetrekte-beslissing-bly-in-hoofletters-staan]].

**The second lesson, same day, same subject.** Once a mechanism is corrected in one
lesson, the other lessons that teach it need the *time* checked too, not only the
mechanism. The steamship lesson had the corrected internally-fired picture and then
named exactly one early ship — Fulton's 1807 boat, which was externally fired and
burned wood. Every sentence true, and the picture a child builds false. See
[[elke-sin-waar-die-prentjie-vals]].

---

**29 September 2026: the fix landed on the wrong half of the sentence.**

A fact check found a village food sentence carrying no quantifier while its three
siblings each carried one. I described the fault and asked for a quantifier. The writer
attached it correctly — and the result, *"they buy MOST of their food at a few small
shops"*, was false in a way the original had not been.

The original was vague about two things at once: how much, and where. Adding the
quantifier fixed the first and **sharpened the second into a claim**. Rural South African
households do buy most of their food, but they buy the bulk on a monthly trip to a
supermarket in the nearest town, where staples cost markedly less; the village shops
carry bread, milk, soap and the buying in between. A strengthened "most" pinned the
falsehood down where the loose sentence had only gestured at it.

**How to apply.** When a correction adds precision to a sentence, ask which clause the
precision attaches to. A quantifier, a date, a number or a named example makes the
*whole* sentence more assertive, not only the part that was faulty — so a neighbouring
clause that was merely vague becomes a claim someone can check. Before asking for the
fix, look at what else is in the sentence and say which part is meant to stay loose.

Related: [[n-versagting-vat-die-algemene-helfte-saam]] (the mirror: a softening takes the
general half with it), [[moenie-n-regstelling-verder-vat-as-die-bevinding-nie]],
[[toets-n-parallelle-stel-as-n-stel]].

## A wrong qualifier can be holding the place of the right one

**7 October 2026.** A glossary entry defining neglect said *one **serious** failure is
enough*. A fact check contradicted the severity word: no definition carries a severity
measure, and the form told the chronically but mildly neglected child — the commonest
case in South Africa — that hers did not count. I had it removed. That was right.

**The next fact check found the entry now wider than the law.** The statute confines
neglect to a child's **basic** needs, and the entry had never carried that word: its
threshold was simply what the child *needs*. While the severity word stood, it bounded
the claim by accident. Remove it and the entry says one unmet need of any kind is
neglect — and *attention* was in the entry's own list of needs.

**So the shape is: a qualifier that is wrong for one reason may be the only thing
bounding a claim for another.** Cutting it is still correct — but the cut has to be
paired with the bound that *should* have been there, and that bound is almost always the
source's own limiting word, which the draft quietly dropped long before.

**How to apply.** When a check kills a qualifier, do not just delete it. Ask:

1. **What was that word doing besides being wrong?** If it narrowed the claim, what
   narrows it now?
2. **Go back to the source and list its own limiting words** — "basic", "deliberate",
   "general", "in the care of" — and check each one is present. A draft that paraphrases
   a definition loses these first, and nothing notices while a wrong qualifier is
   standing in front of them.
3. **Narrowing by restoring the source's qualifier is not the same as narrowing by
   inventing a threshold.** One tracks the law, the other invents a bar. Say which you
   are doing; the fork is where these repairs keep failing.

**The tell** is a check that confirms a sentence and flags its neighbour in the same
breath: here one half ("it need not happen over and over") was confirmed outright while
the other half of the same sentence became unsettled. **Two halves of one sentence with
different verdicts means the bound is in the wrong place**, not that the sentence needs
softening.

Related: [[n-versagting-vat-die-algemene-helfte-saam]],
[[moenie-n-regstelling-verder-vat-as-die-bevinding-nie]] (the opposite failure — this
one is about not going far *enough*, and both are judged against the source rather than
against the finding's words), [[drie-maniere-om-n-bewering-reg-te-maak]].

## A placement claim migrates to whatever object the fix names next

**9 October 2026, one lesson, four rounds.** The same fault kept being repaired and kept
reappearing on a new object:

1. The period attached to the kingdom's ARISING instead of its existing. Fixed.
2. Then the kingdom itself was placed ON THE HILL. The hill was the capital; the kingdom
   was about thirty thousand square kilometres. Fixed.
3. Then the walls were never placed on the hill at all, so two blocks read as two
   different places. Fixed.
4. Then the CAPITAL was shrunk to the summit - and because the people below are
   described as being of the settlement, that one sentence put them outside the capital
   and rebuilt the two-places reading on its own.

**Two of those four, numbers 2 and 4, were caused by my own brief.** I wrote "attach the
period to the capital" - which was the right object, and I had not checked what the
capital WAS. It was the hill together with the settlement at its foot: king and a small
elite on top, the bulk of its people immediately below. The writer followed my
instruction exactly and produced a false sentence.

**So naming the right object is only half of it.** A placement claim has an object, and
when a repair moves the claim onto a new object it inherits the whole problem - the new
object has its own extent, and if I have not verified that extent I have just relocated
the error. The giveaway is that each round's fix was correct about the thing it fixed.

**How to apply.** When a brief says "attach this to X instead", write down what X's
extent is and where that came from, in the brief itself. If I cannot, the brief says so
and asks the writer to establish it. And after a placement repair, **re-read every other
sentence that places anything**, as a set - three of these four rounds were only visible
in the set, never in the sentence.

**9 October 2026 — a sharper version: NARROWING A PREMISE CAN INVALIDATE THE CONCLUSION
THAT RESTS ON IT.** A requirement put decision-making in one definite settlement, which
made a whole valley read as a single settlement, so I scoped it to a settlement generically.
The sentence became true. But the block CONCLUDES that the society therefore became more
organised during the period — and within-settlement leadership pre-dates the period by
centuries, so once the claim was scoped inside a settlement the conclusion no longer
followed. What actually grew was authority ABOVE the settlement. My fix was right and it
broke the paragraph's argument. After narrowing a claim, re-read whatever the paragraph
concludes FROM it and ask whether the narrower claim still carries that weight.

**A fix can also HELP a neighbour, and that is worth checking before escalating.** On
12 October 2026 I had pre-committed to escalating a false reading to the user if it survived a
sixth round, naming a refrain across four blocks as the remaining suspect. The coverage check
pointed out that an unrelated repair in the same revision — naming the agent of a farming
change — had moved "people from outside the valley" into one of those blocks, so only two
refrains now land before outside people first appear instead of four. The carrier I was about
to escalate had been weakened by a fix aimed at something else. **So when a fix lands, ask what
it STRENGTHENED as well as what it disturbed — and re-measure a pending escalation before
spending the user's attention on it.**
