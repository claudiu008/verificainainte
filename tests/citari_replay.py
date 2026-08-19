#!/usr/bin/env python3
"""
Rulează verificatorul de citări peste TOATE răspunsurile reale salvate în
`rezultate/` și arată exact ce ar fi schimbat în producție.

Rulare: python tests/citari_replay.py
Fără API, fără rețea, fără cheie — zero cost, oricâte rulări.

De ce există: testele din `test_citari.py` verifică cazuri scrise de mână, adică
ce m-am gândit eu să verific. Aici intră ieșiri pe care modelul le-a produs
efectiv, de-a lungul mai multor versiuni de prompt. Dacă verificatorul ar strica
răspunsuri bune, aici se vede — pe text real, nu pe text imaginat.

Se rulează după orice modificare a catalogului din `citari.py` sau a secțiunii
CADRUL JURIDIC din prompt.
"""
import json
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AICI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AICI.parent / "verificainainte"))
from citari import verifica_citari  # noqa: E402


def diferente(vechi, nou):
    """Prima și ultima poziție în care textele diferă — pentru afișare scurtă."""
    i = 0
    while i < min(len(vechi), len(nou)) and vechi[i] == nou[i]:
        i += 1
    j = 0
    while (j < min(len(vechi), len(nou)) - i
           and vechi[len(vechi) - 1 - j] == nou[len(nou) - 1 - j]):
        j += 1
    return (vechi[max(0, i - 40):len(vechi) - j + 20],
            nou[max(0, i - 40):len(nou) - j + 20])


def main():
    fisiere = sorted((AICI / "rezultate").glob("*.json"))
    if not fisiere:
        sys.exit("Nu există rezultate salvate în tests/rezultate/")

    total = neatinse = schimbate = 0
    contor = {"completat": 0, "eliminat": 0, "ambiguu": 0, "de_revizuit": 0}

    for f in fisiere:
        inregistrari = json.load(open(f, encoding="utf-8"))
        for r in inregistrari:
            raspuns = r.get("raspuns")
            if not raspuns:
                continue
            total += 1
            nou, jurnal = verifica_citari(raspuns)
            for nota in jurnal:
                contor[nota["actiune"]] = contor.get(nota["actiune"], 0) + 1
            if nou == raspuns:
                neatinse += 1
            else:
                schimbate += 1
                print(f"\n── {f.name} · {r.get('id', '?')} ─────────────────────")
                for nota in jurnal:
                    if nota["actiune"] in ("completat", "eliminat"):
                        print(f"   [{nota['actiune']}] {nota['citare']} — {nota['motiv']}")
                inainte, dupa = diferente(raspuns, nou)
                print(f"   înainte: …{inainte.strip()}…")
                print(f"   după   : …{dupa.strip()}…")

    print(f"\n{total} răspunsuri reale din {len(fisiere)} rulări")
    print(f"  neatinse: {neatinse}   modificate: {schimbate}")
    print("  jurnal: " + ", ".join(f"{k}={v}" for k, v in contor.items() if v))
    if contor.get("eliminat"):
        print("\nATENȚIE: eliminări pe răspunsuri istorice — verifică fiecare mai sus. "
              "O eliminare corectă înseamnă un articol inventat; una greșită înseamnă "
              "un articol lipsă din catalogul din citari.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
