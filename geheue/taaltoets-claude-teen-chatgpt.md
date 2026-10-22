---
name: taaltoets-claude-teen-chatgpt
description: "Blind Afrikaans test 22 Oct 2026, Claude vs ChatGPT on Gr 4 PSW lessons 1-6: Claude found 38 faults ChatGPT missed but had 17 changes rejected; a Claude language agent (taalnasiener-v1.0) is being tuned"
metadata:
  node_type: memory
  type: project
  originSessionId: fccc93f1-34d2-4da5-bb23-6910f798204b
  modified: 2026-10-22T07:36:24.713Z
---

Drico wants the content team to do its own Afrikaans language check instead of ChatGPT. Test, 22 Oct 2026: same original text (the version ChatGPT got on 9 Oct), same instruction (Drico's ChatGPT instruction), same protected words; Drico judged 76 differing sentences blind.

**Round 1:** Claude won 38 sentences ChatGPT left alone and 2 head-to-head; ChatGPT won 5 and 6 head-to-head. **17 Claude changes rejected** (original better) vs 3 for ChatGPT, nine of them word-order changes in the lesson 4 story. Example of meaning drift: "bly stil waar sy sit" (quiet AND motionless) became "bly stil sit" (motionless only). Claude flagged both unsafe sentences in the old body-safety lesson; ChatGPT kept them.

**Round 2:** `prompts/taalnasiener-v1.0.md` + `.claude/agents/wolkskool-taalnasiener.md` (name the fault or leave it; a meaning check per change; never touch protected words, glossary definitions or safety wording; stories are the author's voice). Rerun on the same six lessons. Prompt examples deliberately NOT taken from the test lessons, so the rerun isn't handed its answers. A fresh-lesson test is still owed for an unbiased read.

**Round 2 (strict single agent, taalnasiener-v1.0):** kept 1 of 40 wins, 0 rejected: far too cautious. **Round 3, two agents (`wolkskool-taalvinder` finds, `wolkskool-taalkeurder` decides HOU / LAAT VAAR / NA SKRYWER):** reviewer v1.0 kept 18 wins and 4 rejected; v1.1 (bar = Drico's "clearly better Afrikaans", glossary items to the writer, only BESKERM counts as safety) kept 25 wins and 7 rejected, in-sample. **Fresh test on lessons 7-12** against ChatGPT: blind page https://claude.ai/artifact/Re3J473F5Cnysh8EfLd9i5, key in `vars/sleutel.json`; **Result (71 sentences, blind):** Claude better 20, ChatGPT better 10, both fine 12; changes acceptable but unneeded: Claude 13, ChatGPT 9; rejected: Claude 2, ChatGPT 1; meaning reversed or nonsense: Claude 2 ("voel dit BY 'n ouma" became "VIR", feeling from vs towards), ChatGPT 1 ("die stam begin teken" after picking up scissors). Plus 23 AWS comma fixes only Claude made. Lesson: a preposition swap can flip who feels what toward whom; the meaning check must treat preposition changes as meaning changes.

**Round 4 (reviewer v1.2: preposition rule + Drico's calibration examples), health lessons 1-6, judged by a COLLEAGUE, not Drico:** neutral blind page https://claude.ai/artifact/R3BoRNY7gCaQJNVt4P9ymT (69 to judge, 17 comma-only), key in `r3/sleutel.json`.

**Comma rule (Drico checked it, 22 Oct):** AWS 2017 puts a comma before `en`/`maar`/`want`/`of` when it joins two sentences with their own subject and verb; never in a list or between parts of one sentence.

Test files: `Dump/Taaltoets Claude teen ChatGPT/` (sleutel.json = which version was which).

**Why:** ChatGPT's misses can't be fixed by prompting; Claude's overreach can. **How to apply:** judge a language agent on both counts, wins AND rejected changes; see [[n-regstelling-ontwrig-sy-bure]], [[onaantasbare-woorde-vir-die-taalnasiener]].
