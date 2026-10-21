---
name: n-laslap-se-backslash-oorleef-nie
description: "Backslash escapes in a patch script arrive halved, so anchors miss silently and a written line came out syntactically broken. Anchor on backslash-free text; build escapes with chr()."
metadata:
  node_type: memory
  type: feedback
---

**8 October 2026.** Editing scripts by script, four attempts failed in a row for one
reason: **a backslash I wrote did not arrive.** What I sent as the two characters
`backslash n` reached Python as a real newline, and what I sent as a doubled backslash
reached it as a single one.

Three distinct symptoms, all from that:

1. **An anchor that cannot match.** I anchored a replacement on a line containing an
   escape. By the time Python compared, my copy held a newline where the file held two
   literal characters, so the match failed — on text I had just read and could see.
2. **Written code that does not parse.** A replacement containing `newline="backslash n"`
   was written out with a real newline inside the string literal, leaving an unterminated
   string in a working file. It parsed fine as *my* script and broke the *target*.
3. **Minutes lost to the wrong hypothesis.** Each time I first went looking for a
   mismatch in whitespace or quoting, because the file plainly contained what I had typed.

**How to apply.**

* **Anchor on text with no backslash in it.** There is almost always a nearby line
  without one. A docstring sentence or a format string is a better anchor than the line
  you actually want to change.
* **Build the characters instead of escaping them.** `chr(10)` for a newline, `chr(92)`
  for a backslash, `chr(9)` for a tab — in both the anchor and the replacement. Write
  `newline=chr(10)` in generated code rather than the escape.
* **Use literal characters for Unicode**, not `backslash u` escapes, in anything I
  generate: an em dash typed as itself cannot be halved.
* **When the edit is long, write the patch to a file and run the file.** The shell is
  where this happens; a file on disk is not reinterpreted.
* **Keep asserting that the match happened.** Every one of these failed *loudly* and
  changed nothing, which is the only reason none of them became a silent no-op reported
  as success — see [[n-ruil-wat-nie-pas-nie-moet-hard-faal]]. That rule earned its
  keep three times in one sitting.

**Also: a long heredoc can fail to parse at all.** On 12 October 2026 a ~130-line patch sent
as `cat > f.py <<'PY'` died with "unexpected EOF while looking for matching quote" — nothing
written, nothing run. The content had no backslashes; the length and the density of
apostrophes in Afrikaans (`'n` on nearly every line) were enough. This file already says to
use the Write tool for long patches, and I did not. Write the file with the file tool and run
it as a second step; keep heredocs for a handful of lines.
