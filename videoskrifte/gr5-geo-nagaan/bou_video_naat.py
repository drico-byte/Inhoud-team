"""Build video_naat-per-les.json for Gr 5 Geography from the claim checks.

Reads the four or five claim-check files in this folder and the year profile,
and writes one distilled video_naat per register ID (G5_GEO_NN). The planner
reads it; a script injects it into each spec lesson after the planner writes it.

    python -X utf8 videoskrifte/gr5-geo-nagaan/bou_video_naat.py
"""
import glob
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
WORTEL = os.path.dirname(os.path.dirname(HIER))
PROFIEL = os.path.join(WORTEL, "profiele", "gr5-sw-geografie-profiel.json")
UIT = os.path.join(HIER, "video_naat-per-les.json")

# Word flags overruled by standing decisions: (video word, reason).
OORHEERS = {
    "wêrelderfenisterrein": "Graad 5 SW Geskiedenis het 'wêrelderfenisterrein' deurgaans besluit (12 November 2026); Geografie hou dieselfde woord.",
}

HANTEER = (
    "Moet die video NIE weerspreek nie en moet die vals of misleidende bewering ook nie herhaal nie: "
    "'n leerder wat kyk en dan lees, moet nie twee stories kry nie - hy moet net nie die vals een 'n tweede "
    "keer teekom nie. Skryf die ware vorm, of laat die punt weg. Gebruik dieselfde woord as die video vir "
    "dieselfde ding, behalwe waar die video se woord nie die gevestigde term is nie: dan lei die gevestigde "
    "woord (KABV s'n waar KABV een het) en die video se woord volg een keer tussen hakies. Waar die verskil "
    "net spelling is, staan die gevestigde spelling alleen. 'n Bewering gemerk 'onseker' word nie as feit "
    "geskryf nie: laat dit weg, of gebruik die bes-gesteunde lesing met 'n omtrent-woord. KABV-inhoud wat "
    "die video mis, kom in die teks (Lampies, 17 November 2026); inhoud in die video bo KABV hoef die teks "
    "nie te dra nie."
)

EKSTRA = {
    "G5_GEO_07": ["Video H1 10 leer hoogtelyne (kontoere). KABV sluit kontoere by Graad 5 uit; die teks noem hulle NIE (Lampies, 17 November 2026) en weerspreek die video ook nie. Die teks leer skakering (kleure) en punthoogtes."],
    "G5_GEO_06": ["Die video noem van Afrika se groot stede net Johannesburg. KABV noem ook Kaïro, Lagos en Nairobi: die teks dra al vier (Lampies, 17 November 2026)."],
    "G5_GEO_09": ["Die video het nie die Maletsunyane-waterval nie. KABV noem hom: die teks dra hom (Lampies, 17 November 2026)."],
    "G5_GEO_16": ["Waar 'n voorstel hieronder 'n betekenis vir 'Gariep' gee of die koning by die naam noem, wen die spesifikasie: die teks gee GEEN betekenis vir Gariep nie (soos Graad 5 Geskiedenis) en skryf net 'die Portugese koning' (spesifikasie-feitetoets, 17 November 2026)."],
    "G5_GEO_05": ["Die video gebruik Eswatini. Die teks skryf die eerste keer 'Eswatini (Swaziland)', daarna net 'Eswatini' (Lampies, 17 November 2026)."],
}


def main():
    profiel = json.load(open(PROFIEL, encoding="utf-8"))
    per_video = {}
    for pad in sorted(glob.glob(os.path.join(HIER, "h*.json"))):
        d = json.load(open(pad, encoding="utf-8"))
        h = d["hoofstuk"]
        for v in d["videos"]:
            sleutel = f"H{h} {int(v['video']):02d}"
            if sleutel in per_video:
                sys.exit(f"Video {sleutel} twice ({pad})")
            per_video[sleutel] = v
    uit = {}
    vermis = []
    for sub in profiel["subonderwerpe"].values():
        for les in sub["lesse"]:
            woorde, nie_gevestig, dek, probleme = [], [], [], []
            for vid in les["videos"]:
                v = per_video.get(vid)
                if v is None:
                    vermis.append(vid)
                    continue
                for w in v.get("woorde_wat_die_video_gebruik", []):
                    if w not in woorde:
                        woorde.append(w)
                for w in v.get("woord_nie_gevestig_nie", []):
                    if any(k in w["video_se_woord"].lower() for k in OORHEERS):
                        continue
                    nie_gevestig.append(w)
                dek += [f"[{vid}] {x}" for x in v.get("wat_die_video_dek", [])]
                for p in v.get("probleme", []):
                    probleme.append({
                        "video": vid,
                        "bewering_in_die_video": p["bewering"],
                        "uitspraak": p["uitspraak"],
                        "waarom_nie": p["waarom"],
                        "bronne": p.get("bronne", []),
                    })
            naat = {
                "bestaan": True,
                "videos": les["videos"],
                "nota": "Die video's vir hierdie les is REEDS gemaak, voor die teks, en word nie oorgemaak nie. "
                        "Hierdie veld is 'n DISTILLAAT van die videoskrif(te), nagegaan op 17 November 2026 teen "
                        "bronne buite enige handboek - nie die skrif self nie. KABV bly die bron vir inhoud en struktuur.",
                "woorde_wat_die_video_gebruik": woorde,
                "woord_nie_gevestig_nie": nie_gevestig,
                "wat_die_video_dek": dek,
                "moenie_hierdie_bewerings_herhaal_nie": probleme,
                "hoe_om_die_verskil_te_hanteer": HANTEER,
            }
            if les["id"] in EKSTRA:
                naat["besluite"] = EKSTRA[les["id"]]
            uit[les["id"]] = naat
    if vermis:
        sys.exit(f"No claim check for: {', '.join(vermis)}")
    gebruik = {v for n in uit.values() for v in n["videos"]}
    oor = sorted(set(per_video) - gebruik)
    if oor:
        sys.exit(f"Checked videos no lesson uses: {', '.join(oor)}")
    json.dump(uit, open(UIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(x["moenie_hierdie_bewerings_herhaal_nie"]) for x in uit.values())
    print(f"{len(uit)} lessons, {len(per_video)} videos, {n} claims routed -> {UIT}")


if __name__ == "__main__":
    main()
