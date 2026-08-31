---
name: teks-loop-parallel-met-n-video
description: A Wolkskool lesson is a video plus our text in parallel — one of each per CAPS heading. The text stands alone as the revision instrument. Gr 4 Sosiale Wetenskappe is the exception: its videos were made first.
metadata:
  type: project
---

Learned from Drico on 2026-08-19, and it was not in the repository before: the platform
is video-first. A video explains the concept; our text runs parallel to it. **One video
and one text per CAPS content heading** — so "Lewende en nie-lewende dinge" is two
videos and two texts, not five.

**The text stands alone, and Drico agreed 100%.** It is not a companion that fills gaps.
A learner revising the night before a test reads rather than rewatching, so the text is
the revision instrument — which is why textbook parity is the right budget anchor and not
something thinner. And a learner on a slow connection must be able to learn the whole
concept from text alone, which matters more here than almost anywhere.

**The analogy is largely the video's job.** Video is the best medium for showing a bean
swelling or water pushing back on a hand. This is the strongest argument for the `eli10`
layer being zero or one per lesson — not page weight, but that a written analogy
duplicates, worse, what the video just did well. It also explains why the HTML team
reached for interactivity on that block: they were trying to make text behave like video.

**SETTLED, after I got the direction wrong twice in one conversation.** The video is made
AFTER the text and uses it as a guide. The video maker covers everything the text covers
and adds more for interest. So:

- The text must never contain something the video misses, and the two must never disagree
  — which is why the video comes second.
- **The text is the floor, not the ceiling.** It carries the curriculum completely and
  correctly; the video carries the interest.
- **Everything in the text is a commitment the video must honour**, so a block that need
  not be there is a constraint on the video maker, not just page weight. Drico's point,
  and the sharpest argument in the whole discussion.
- **The vivid comparison is the video's job and it does it better.** So the `eli10` layer
  is zero or one and **the default is none** — reserved for a concept that cannot be
  stated concretely at all.

Standing alone means a learner can LEARN the concept from text with no video and no
images. It does not mean the text must be as vivid as film.

**Boundaries:** where text and video disagree, the text follows the video, and the video
should follow CAPS. Here all three already agree.

**The drift gap largely closes** once videos are generated from the text, since one derives
from the other. It stays open for videos made before that changeover. Related: [[moenie-op-voorkoms-sorteer-nie]]

## The exception: Gr 4 Sosiale Wetenskappe was made the other way round

Drico, 31 August 2026: the Grade 4 SW videos were made **before** any text, and will
not be remade — "we have no choice since the videos took a lot of time to create".
So for that subject everything above about the video following the text is inverted,
and the guarantees it buys are gone: the text can no longer be the floor the video
honours, because the video is already finished.

**What does not change:** the lesson still comes from CAPS. A video script is not a
source for content and not a source for structure. Drico said it first and
unprompted — "the script doesnt become the text content. We still do what we always
do, we just have an extra guide now."

**What the script is genuinely worth**, in order: the same word for the same thing
(drift between a video and a text is the drift problem with no repair path); the same
example, so the learner builds one picture; and knowing what the video already
carried well, so the text does not rebuild it.

**The danger it carries:** a script has been through no fact checker. The first one
read had two false claims in four lines — that a donkey cannot walk far without food
and water (a donkey tolerates thirst *better* than a horse, ~20 l/day against 40–60
for a working horse in heat) and that donkeys are stubborn (a myth; it is
self-preservation in a prey animal). Repeating either would have laundered an error
through a checked pipeline into something that looks verified.

**So a script enters as a distilled `video_naat` object in the spec, never raw** —
the words used, what was covered, and every claim the text must not repeat with the
reason. The planner and writer read it; the fact checker never does, for the same
reason it never reads the spec. **Where the video is wrong, route around it**: do not
repeat it and do not correct it either, or a learner who watches and then reads gets
two stories. Then tell Drico, because the video is his call.

Written into `skills/wolkskool-inhoudstandaard/SKILL.md` and `CLAUDE.md` the same day.
