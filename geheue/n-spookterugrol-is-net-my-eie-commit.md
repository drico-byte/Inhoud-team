---
name: n-spookterugrol-is-net-my-eie-commit
description: An agent that surveys a file across one of my commits reports a phantom revert, because the file now matches a HEAD that moved under it.
metadata:
  type: feedback
---

**1 October 2026.** A careful agent reported that "a third party discarded the
working-tree changes" to a specification mid-flight: its first read hashed an
uncommitted state, its second matched HEAD exactly, and it warned that other
modified files "may have gone with it". Nothing had been reverted. **I had
committed in between**, so the file legitimately matched the new HEAD.

**Why:** an agent's git status is a snapshot from when it was spawned, and HEAD
is not. Across a commit, both of its footings move at once — so matching HEAD
looks like a discard rather than like a commit. I commit while agents run
routinely, because runs are long and three machines share this work, so this
will keep happening.

**How to apply:** when an agent reports lost or reverted work, **check
`git log -1 --stat` and `git show HEAD:<path>` before believing it** — if my own
commit sits between its two reads, and the commit contains the content, nothing
was lost. The expensive version of this mistake is the inverse: taking the
report at face value and "restoring" work on top of good changes. An agent's
byte-gated write is the real protection, and it holds whether HEAD moved or not.
Cheap preventive: say in the brief that I may commit while it works, so matching
HEAD is expected. Related: [[n-agent-wat-faal-kan-sy-werk-klaar-he]].
