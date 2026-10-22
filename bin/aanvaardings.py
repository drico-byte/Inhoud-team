#!/usr/bin/env python3
"""A dated, item-level record that a person has accepted ONE unresolvable fact.

WHY THIS EXISTS. The standing rule where sources genuinely conflict is to keep the
best-supported reading and disclose the conflict in one sentence. A lesson that does
exactly that is still reported MENS_NODIG -- correctly, because the underlying fact is
unresolved and that is a person's call -- and until now there was no way for a person
to make that call and have the pipeline see it. So such a lesson could never ship.
Gr 6 Sosiale Wetenskappe lesson 5 (Fatima Meer's first banning order: 1952 in the
secondary record, 1954 in her own sworn testimony) sat in that position with clean
coverage and text that every source check called correct.

WHAT A RECORD MAY AND MAY NOT DO. Approved by Lampies, 7 October 2026.

  * It names ONE item of ONE lesson's fact report, by the item's own text and by a
    fingerprint over that item. There is no field that means "this lesson", "all
    items" or anything else plural, and matching is equality on a sha256 digest, so
    there is no wildcard to write and none to interpret. A blanket acceptance is not
    something this refuses -- it is something it cannot express.
  * Every item that holds the verdict up must be accepted individually. One
    unaccepted item and sign-off refuses, as it did before.
  * Only an `onseker` item may be accepted. A `weerspreek` item is a claim a source
    contradicts, and a false claim is narrowed, cut or explained -- never accepted.
  * The fingerprint covers the whole item, its status and the evidence included, so
    an acceptance lapses the moment the report's text for that item changes. An
    accepted item that could drift would be a hole later content falls into.

WHERE THE RECORD LIVES: beside the draft, as `les-N.aanvaardings.json`.

  * Beside the fact report it rules on, in the folder a person already opens to read
    that report, and git-tracked, so the ruling and its date are visible in the
    repository and in its history.
  * A separate FILE, not a field of the lesson. hardloop.konsep_hash covers the
    lesson's own fields, so a ruling written into the lesson would move the content
    fingerprint and archive both finished check reports -- the lesson would pay for
    its own sign-off with a fresh, web-heavy fact check.
  * Nothing regenerates it. `spek/` and `feite-kopie/` are rewritten on every run;
    `.hek`, `.dekking`, `.feite` and `.eli10` are written by the gate and the
    checkers and archived away when a draft changes; `.staat` is the runner's. This
    suffix is written by a person only, and the runner's archive list does not
    mention it -- correctly, because whether a ruling survives a revision is decided
    by the fingerprint and not by the file surviving.

THE SHAPE, exactly -- unknown keys are refused rather than ignored, so that nobody
can add a field that reads like a blanket and have it quietly do nothing:

    {
      "skema_weergawe": "1.0",
      "les": "gr6/sosiale-wetenskappe/demokrasie-en-burgerskap/les-5",
      "aanvaardings": [
        {
          "bewering": "<the item's `bewering`, verbatim>",
          "item_vingerafdruk": "sha256:<64 hex>",
          "datum": "2026-10-07",
          "deur": "Lampies",
          "rede": "<why this one cannot be settled, and why the lesson's handling of "
                  "it is right>"
        }
      ]
    }

`bin/keur-goed-na-handnasien.py --wys-items` prints the fingerprint and a record to
fill in. Take it from there rather than computing a digest by hand: the same function
produces the value and checks it, which is the only arrangement that cannot drift.
"""

import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paaie as P  # noqa: E402

SKEMA_WEERGAWE = "1.0"

# A fact item with either status stops the lesson. Only the first may be accepted.
OPHOU_STATUS = ("weerspreek", "onseker")
AANVAARBAAR_STATUS = ("onseker",)

TOP_VELDE = {"skema_weergawe", "les", "aanvaardings"}
TOP_VERPLIG = {"les", "aanvaardings"}
INSKRYWING_VELDE = {"bewering", "item_vingerafdruk", "datum", "deur", "rede"}

REDE_MINIMUM = 20       # a reason, not a tick
VINGERAFDRUK_VORM = re.compile(r"^sha256:[0-9a-f]{64}$")
DATUM_VORM = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ------------------------------------------------------------------ identity
def item_vingerafdruk(item):
    """The fingerprint of one fact-report item, over the WHOLE item.

    Deliberately not hardloop.konsep_hash: that one drops `status` on purpose, and
    an item's status is the first thing an acceptance must not survive a change to.
    Deliberately the whole item rather than its claim text: the evidence is what
    made the item unresolvable, so a record that outlived a change to `bron` would
    be an acceptance of a judgement nobody made.
    """
    blob = json.dumps(item, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def les_id(les_pad):
    """'gr6/sosiale-wetenskappe/demokrasie-en-burgerskap/les-5' for a draft path.

    Derived from the path of the file actually being read, rather than rebuilt from
    a subject and a grade, so it cannot name a different lesson from the one whose
    report is open.
    """
    rel = os.path.relpath(os.path.abspath(les_pad), P.KONSEPTE)
    if rel.endswith(".json"):
        rel = rel[:-len(".json")]
    return rel.replace(os.sep, "/")


def pad(les_pad):
    """Where a person writes the record."""
    return P.newe(les_pad, "aanvaardings")


def ophou_items(verslag):
    """The items of a fact report that hold its verdict up."""
    return [i for i in (verslag or {}).get("items", [])
            if isinstance(i, dict) and i.get("status") in OPHOU_STATUS]


# ------------------------------------------------------------------ the verdict
class Uitslag:
    """What the acceptance records say about one fact report.

    `alles_aanvaar` is the only thing a caller may route on, and it is true only when
    a record exists, is wholly valid, and accounts for every item that holds the
    verdict up. Everything else is for telling a person why not.
    """

    def __init__(self):
        self.het_rekord = False
        self.rekord_pad = None
        self.alles_aanvaar = False
        self.aanvaar = []        # [(item, inskrywing)] -- validly accepted
        self.redes = []          # why this record is not honoured, in full
        self.ophou = []          # the items that hold the verdict up
        self._verslag = {}

    @property
    def feite_vir_roetering(self):
        """The fact report with the accepted items removed.

        For deciding which BLOCKS failed this round. An accepted item must not add
        its block to the keeps-failing tally, or the lessons this mechanism exists
        for would escalate for repeatedly carrying the very item a person settled.
        Only ever used when `alles_aanvaar`; otherwise the real report is routed on.
        """
        if not self.alles_aanvaar:
            return self._verslag
        weg = {id(i) for i, _ in self.aanvaar}
        return dict(self._verslag,
                    items=[i for i in self._verslag.get("items", [])
                           if id(i) not in weg])

    def reels(self):
        """Lines for a person. Never silent: an accepted item is printed in full."""
        uit = []
        for item, ins in self.aanvaar:
            uit.append(f"ACCEPTED by {ins['deur']} on {ins['datum']}: "
                       f"{str(item.get('bewering',''))[:110]}")
            uit.append(f"             reason: {ins['rede'][:160]}")
            uit.append(f"             item    {ins['item_vingerafdruk']}")
        uit.extend(self.redes)
        return uit


def _lees_rekord(p, uitslag):
    try:
        rekord = P.lees_json(p)
    except (OSError, ValueError) as e:
        uitslag.redes.append(f"{P.rel(p)} is not readable JSON ({e}); nothing is accepted.")
        return None
    if not isinstance(rekord, dict):
        uitslag.redes.append(f"{P.rel(p)} must be a JSON object; nothing is accepted.")
        return None
    onbekend = sorted(set(rekord) - TOP_VELDE)
    if onbekend:
        # Refused rather than ignored, on purpose. A field nobody reads is how a
        # blanket acceptance gets written, believed and relied on.
        uitslag.redes.append(
            f"{P.rel(p)} carries field(s) this record has no meaning for: "
            f"{', '.join(onbekend)}. Only {', '.join(sorted(TOP_VELDE))} exist. "
            f"Nothing is accepted.")
        return None
    kort = sorted(TOP_VERPLIG - set(rekord))
    if kort:
        uitslag.redes.append(f"{P.rel(p)} is missing {', '.join(kort)}; nothing is accepted.")
        return None
    return rekord


def _keur_inskrywing(n, ins, uitslag):
    """Validate one entry's own shape. Returns True when it may be matched."""
    waar = f"{P.rel(uitslag.rekord_pad)} entry {n}"
    if not isinstance(ins, dict):
        uitslag.redes.append(f"{waar} is not an object; nothing is accepted.")
        return False
    onbekend = sorted(set(ins) - INSKRYWING_VELDE)
    if onbekend:
        uitslag.redes.append(f"{waar} carries unknown field(s): {', '.join(onbekend)}. "
                             f"Nothing is accepted.")
        return False
    kort = sorted(INSKRYWING_VELDE - set(ins))
    if kort:
        uitslag.redes.append(f"{waar} is missing {', '.join(kort)}; nothing is accepted.")
        return False
    goed = True
    if not isinstance(ins["bewering"], str) or not ins["bewering"].strip():
        uitslag.redes.append(f"{waar}: 'bewering' must be the item's own text, verbatim.")
        goed = False
    if not isinstance(ins["item_vingerafdruk"], str) \
            or not VINGERAFDRUK_VORM.match(ins["item_vingerafdruk"]):
        uitslag.redes.append(
            f"{waar}: 'item_vingerafdruk' must be 'sha256:' and 64 hex characters, as "
            f"--wys-items prints it. There is no pattern or wildcard form.")
        goed = False
    if not isinstance(ins["datum"], str) or not DATUM_VORM.match(ins["datum"]):
        uitslag.redes.append(f"{waar}: 'datum' must be a date, as YYYY-MM-DD.")
        goed = False
    else:
        try:
            datetime.date.fromisoformat(ins["datum"])
        except ValueError:
            uitslag.redes.append(f"{waar}: 'datum' is not a real date.")
            goed = False
    if not isinstance(ins["deur"], str) or not ins["deur"].strip():
        uitslag.redes.append(f"{waar}: 'deur' must name the person who accepted it.")
        goed = False
    if not isinstance(ins["rede"], str) or len(ins["rede"].strip()) < REDE_MINIMUM:
        uitslag.redes.append(
            f"{waar}: 'rede' must say why the fact cannot be settled and why the "
            f"lesson's handling of it is right, in at least {REDE_MINIMUM} characters. "
            f"A later reader holds the line only if the reason travels with it.")
        goed = False
    return goed


def beoordeel(les_pad, verslag):
    """Read the lesson's acceptance record and judge it against this fact report.

    Pure except for reading the record. Never writes, never signs anything off, and
    returns a false `alles_aanvaar` for every doubt rather than raising.
    """
    u = Uitslag()
    u._verslag = verslag or {}
    u.ophou = ophou_items(verslag)
    u.rekord_pad = pad(les_pad)

    if not os.path.exists(u.rekord_pad):
        if u.ophou:
            u.redes.append(
                f"No acceptance record at {P.rel(u.rekord_pad)}. "
                f"{len(u.ophou)} item(s) hold the fact verdict up and none is accepted.")
        return u

    u.het_rekord = True
    rekord = _lees_rekord(u.rekord_pad, u)
    if rekord is None:
        return u

    verwag = les_id(les_pad)
    if rekord.get("les") != verwag:
        u.redes.append(f"{P.rel(u.rekord_pad)} names lesson '{rekord.get('les')}' and sits "
                       f"beside '{verwag}'. Nothing is accepted.")
        return u

    inskrywings = rekord.get("aanvaardings")
    if not isinstance(inskrywings, list) or not inskrywings:
        u.redes.append(f"{P.rel(u.rekord_pad)}: 'aanvaardings' must be a non-empty list "
                       f"of records, one per item. Nothing is accepted.")
        return u

    if not u.ophou:
        # Not a refusal: with nothing holding the verdict up this record changes no
        # outcome. It is said out loud because a record left behind after a repair
        # looks, to the next reader, like an item that is still being carried.
        u.redes.append(
            f"{P.rel(u.rekord_pad)} applies to nothing: no item of this fact report "
            f"holds its verdict up. The lesson needs no acceptance; remove the record.")
        return u

    # By fingerprint, over the items that hold the verdict up. Equality on a digest,
    # so one entry can only ever reach one item's worth of text.
    per_afdruk = {}
    for item in u.ophou:
        per_afdruk.setdefault(item_vingerafdruk(item), []).append(item)

    ok = True
    gedek = {}
    for n, ins in enumerate(inskrywings, 1):
        if not _keur_inskrywing(n, ins, u):
            ok = False
            continue
        afdruk = ins["item_vingerafdruk"]
        treffers = per_afdruk.get(afdruk, [])
        waar = f"{P.rel(u.rekord_pad)} entry {n}"
        if not treffers:
            u.redes.append(
                f"{waar} names no item that holds this fact report up. Either the "
                f"report's text for that item has changed -- in which case the "
                f"acceptance has lapsed and the item must be judged again -- or the "
                f"record was written for another report. Nothing is accepted.")
            ok = False
            continue
        if len(treffers) > 1:
            u.redes.append(
                f"{waar} matches {len(treffers)} items: this report carries "
                f"byte-identical duplicates, so one record cannot name one of them. "
                f"Fix the report. Nothing is accepted.")
            ok = False
            continue
        item = treffers[0]
        if afdruk in gedek:
            u.redes.append(f"{waar} accepts the same item as entry {gedek[afdruk]}. "
                           f"One record per item. Nothing is accepted.")
            ok = False
            continue
        if item.get("status") not in AANVAARBAAR_STATUS:
            u.redes.append(
                f"{waar} accepts an item whose status is '{item.get('status')}'. Only "
                f"'onseker' may be accepted: a contradicted claim is false, and a "
                f"false claim is narrowed, cut or explained -- never accepted.")
            ok = False
            continue
        if ins["bewering"] != item.get("bewering"):
            u.redes.append(
                f"{waar}: 'bewering' does not match the item it fingerprints, word for "
                f"word. The record must say in plain text which item it accepts, so a "
                f"person reading it can tell without running anything.")
            ok = False
            continue
        gedek[afdruk] = n
        u.aanvaar.append((item, ins))

    for item in u.ophou:
        if item_vingerafdruk(item) not in gedek:
            u.redes.append(
                f"{P.rel(u.rekord_pad)} does not accept this item, so sign-off refuses: "
                f"[{item.get('status')}] {str(item.get('bewering',''))[:100]}")
            ok = False

    if not ok:
        u.aanvaar = []
        return u

    u.alles_aanvaar = True
    return u


# ------------------------------------------------------------------ helping a person
def voorbeeld_rekord(les_pad, verslag):
    """A record to fill in, with the fingerprints already computed.

    Printed rather than written: the dates, the name and the reasons are a person's,
    and a file this script created would be a record of nothing.
    """
    items = ophou_items(verslag)
    reels = [f"Items holding the fact verdict up: {len(items)}"]
    if not items:
        reels.append("  none -- this lesson needs no acceptance record.")
        return reels
    inskrywings = []
    for item in items:
        status = item.get("status")
        reels.append("")
        reels.append(f"  [{status}] block: {item.get('blok')}")
        reels.append(f"    {str(item.get('bewering',''))}")
        reels.append(f"    fingerprint  {item_vingerafdruk(item)}")
        if status not in AANVAARBAAR_STATUS:
            reels.append("    NOT ACCEPTABLE: a 'weerspreek' item is a claim a source "
                         "contradicts. Narrow it, cut it or teach the mechanism.")
            continue
        inskrywings.append({
            "bewering": item.get("bewering"),
            "item_vingerafdruk": item_vingerafdruk(item),
            "datum": "YYYY-MM-DD",
            "deur": "<who accepted it>",
            "rede": "<why the fact cannot be settled, and why this lesson's handling "
                    "of it is right>",
        })
    if not inskrywings:
        return reels
    rekord = {"skema_weergawe": SKEMA_WEERGAWE, "les": les_id(les_pad),
              "aanvaardings": inskrywings}
    reels.append("")
    reels.append(f"Write this to {P.rel(pad(les_pad))}, with the dates, the name and the")
    reels.append("reasons filled in. Do not edit a fingerprint: it is what makes the")
    reels.append("acceptance lapse if the report's text for that item ever changes.")
    reels.append("")
    reels.extend(json.dumps(rekord, ensure_ascii=False, indent=2).splitlines())
    return reels
