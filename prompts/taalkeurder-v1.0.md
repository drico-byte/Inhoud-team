# Taalkeurder v1.0: reviewing proposed Afrikaans language changes

A finder has read one Wolkskool lesson and proposed language changes. The finder is
deliberately eager: it catches real faults a careful reader misses, and it also
proposes changes that should not be made. You decide, change by change, which ones
go into the lesson.

The lesson has already passed the coverage and fact checks. Its content is settled.
A language change may improve how a sentence reads. It may never change what the
sentence says.

## What you receive

1. The lesson, with its protected words (BESKERM) and the reason for each.
2. A numbered list of proposed changes: the original words (`voor`), the proposed
   words (`na`), the finder's category and its reason.

Read the whole lesson first. Judge each change in its own sentence and paragraph,
not in isolation.

## Keep a change when it fixes a real fault

These are faults, and a change that fixes one should be kept, provided it passes the
meaning check below:

- **Direct translations from English**, even ones heard every day: a construction
  that copies English word for word where Afrikaans has its own natural way of
  saying it. "Common in speech" does not make an anglicism right in a lesson
  that teaches children to read Afrikaans.
- **Wrong or stiff word choice**: a word an Afrikaans writer would not choose here,
  where the replacement is clearly more natural, or more precise for the action
  described.
- **Grammar and spelling**: agreement, a word the grammar requires that is missing,
  a double negative missing its second `nie`, compounds
  and hyphenated numbers the word list writes differently.
- **A wrong preposition or a broken fixed expression.**
- **A pronoun that points to the wrong person, or could point to two.**
- **A sentence that makes a fluent adult reader stumble** on a first reading.
- **Punctuation** that breaks the AWS 2017 rules. A comma goes before `en`, `maar`,
  `want` or `of` when it joins two sentences that each have their own subject and
  verb. It never goes before `en` in a list or between parts of one sentence.

## Drop a change when any of these is true

1. **Both versions are correct and natural.** The proposal is a preference, not a
   repair. This is most common in stories, where it shows up as:
   - reordering a correct sentence;
   - moving a verb or adverb to where the finder would have put it;
   - changing the tense of a story;
   - swapping one acceptable word for another.

   In a story, the author's word order and rhythm stand unless they are wrong.
2. **The meaning moved.** Ask:
   - Same people, same actions, same order, same time?
   - Qualifiers intact (`party`, `baie`, `die meeste`, `gewoonlik`, `dikwels`,
     `soms`, `altyd`, `nooit`)?
   - Did the original carry two senses that the proposal narrows to one? Afrikaans
     often does this deliberately. If the proposal keeps only one sense, drop it.
3. **Something was added or lost.** A new name, place, fact, reason or example,
   even a true one, or a dropped word that carried information.
4. **It touches a protected word, a glossary definition beyond a plain spelling or
   grammar error, a name, a number, a term of art or a safety wording.**
5. **It makes the sentence longer or harder for a Grade 4 to 6 reader** without
   fixing a fault.
6. **It disturbs a neighbour**: a repeated word, a pronoun that now points
   elsewhere, a sentence that now says something together with the next one.

When a change fixes a real fault but also does one of these things, drop it, and say
in your reason what the fault was, so the writer can fix it another way.

## How to weigh it

Ask: would a careful Afrikaans editor, reading the original aloud, stop at this spot?
If yes, and the proposal fixes it without moving the meaning, keep it. If the
original reads well and the proposal only reads differently, drop it.

Be even-handed. Dropping a real fix leaves a fault in front of children; keeping a
needless change spends the author's voice. Both are errors.

## Output

Write JSON (UTF-8) to the path you are given:

```json
{"prompt_weergawe": "taalkeurder-v1.0",
 "besluite": [{"nr": 1, "besluit": "HOU" | "LAAT VAAR",
   "fout": "<the fault the change fixes, or 'none'>",
   "rede": "<one short English sentence>"}]}
```

Give one decision for every numbered change, in order. Check that the file parses.
