#!/usr/bin/env python3
"""
Teste pentru citirea scorului din răspuns (`verificainainte/scor.py`).

Rulare: python tests/test_scor.py
Fără API, fără rețea, fără cheie — se poate rula oricând, gratuit.

Regula pe care o apără: un răspuns cu scor trebuie recunoscut indiferent de cum
îl împachetează modelul în markdown, iar unul fără scor trebuie să iasă None, nu
o etichetă ghicită din corpul textului. Numărul de răspunsuri fără scor e semnalul
că regula de ieșire din format s-a lărgit — dacă îl citim greșit, semnalul minte.

Partea a doua trece funcția peste toate răspunsurile reale salvate în
`rezultate/` și afișează câte rămân fără scor. Cifra e informativă, nu un prag:
scenariul 09 iese din format prin definiție.
"""
import json
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AICI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AICI.parent / "verificainainte"))
from scor import ETICHETE, extrage_scor  # noqa: E402

CAZURI = [
    ("forma din exemplul de prompt", "STOP\n\nSCOR: CRITIC\n\nTIPAR DETECTAT: ...", "CRITIC"),
    ("eticheta îngroșată", "SCOR: **RIDICAT**\n\nTIPAR DETECTAT: ...", "RIDICAT"),
    ("toată linia îngroșată", "**SCOR: MEDIU**\n\nTIPAR DETECTAT: ...", "MEDIU"),
    ("titlul îngroșat, eticheta nu", "**SCOR:** SCĂZUT\n\nTIPAR DETECTAT: ...", "SCĂZUT"),
    ("fără spațiu după două puncte", "SCOR:CRITIC", "CRITIC"),
    ("ca titlu markdown", "## SCOR: CRITIC", "CRITIC"),
    (
        "ieșire din format legitimă (scenariul 09) — niciun scor, nu unul ghicit",
        "Mesajul tău nu descrie o situație cu risc financiar. Dacă primești un "
        "mesaj despre bani, plăți sau conturi, revino cu textul lui.",
        None,
    ),
    (
        "eticheta apare doar în proză — nu e scor",
        "Riscul este SCĂZUT în acest caz, dar verifică oricum la bancă.",
        None,
    ),
    (
        "cuvântul SCOR fără etichetă validă",
        "SCOR: NEDETERMINAT\n\nTIPAR DETECTAT: ...",
        None,
    ),
    ("răspuns gol", "", None),
]


def main():
    esecuri = 0
    for nume, intrare, asteptat in CAZURI:
        obtinut = extrage_scor(intrare)
        if obtinut == asteptat:
            print(f"  OK   {nume}")
        else:
            esecuri += 1
            print(f"  EȘEC {nume}\n       așteptat: {asteptat!r} | obținut: {obtinut!r}")

    print(f"\n{len(CAZURI) - esecuri}/{len(CAZURI)} cazuri trecute")

    # ── peste răspunsurile reale salvate ────────────────────────────────────
    fisiere = sorted((AICI / "rezultate").glob("*.json"))
    total = fara = 0
    pe_scenariu = {}
    banner_gresit = 0
    for f in fisiere:
        for r in json.load(open(f, encoding="utf-8")):
            raspuns = r.get("raspuns")
            if not raspuns:
                continue
            total += 1
            linie = extrage_scor(raspuns)
            if linie is None:
                fara += 1
                pe_scenariu[r["id"]] = pe_scenariu.get(r["id"], 0) + 1
            else:
                # ce ar alege detecteazaScor() din App.jsx: prima etichetă găsită
                # oriunde în text, în ordinea din SCORURI
                afisat = next((e for e in ETICHETE if e in raspuns), None)
                if afisat != linie:
                    banner_gresit += 1
                    print(f"  BANNER: linia spune {linie}, frontendul ar arăta {afisat}")

    print(f"\n{total} răspunsuri reale din {len(fisiere)} rulări")
    print(f"  fără linia SCOR: {fara}" + (f" — {pe_scenariu}" if pe_scenariu else ""))
    print(f"  banner diferit de linie: {banner_gresit}")
    return 1 if esecuri else 0


if __name__ == "__main__":
    sys.exit(main())
