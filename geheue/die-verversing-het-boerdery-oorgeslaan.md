---
name: die-verversing-het-boerdery-oorgeslaan
description: The extract refresh silently skipped every Gr 4 farming lesson because it found folders by kaps_subonderwerp, not by the spec file name; "0 refreshed" was a lie. Fixed 7 Oct 2026.
metadata:
  type: project
---

**7 October 2026.** I fixed a farming spec, ran the refresh, it said `0 vernuwe`, and the
writer's extract still carried the old order. The refresh derived each lesson folder from
the spec's `kaps_subonderwerp` ("Voedsel en boerdery in Suid-Afrika"), while the runner
derives it from `--subonderwerp` → the spec FILE (`voedsel-en-boerdery`). No such folder,
so every farming extract was skipped as "nobody has started this lesson". Spec fixes only
arrived when the runner happened to be called for that lesson.

Fixed in the refresh script: it now resolves by the spec file name, as the runner does.
387 extracts resolve where 381 did; none dropped.

**How to apply:** after any spec fix, grep the writer's extract for the NEW wording before
briefing — a refresh count is not evidence that a particular extract moved. Same family as
[[n-ruil-wat-nie-pas-nie-moet-hard-faal]] and [[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]]:
a silent skip reports exactly like success.
