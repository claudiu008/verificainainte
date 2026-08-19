#!/usr/bin/env python3
"""
Teste pentru verificatorul de citări (`verificainainte/citari.py`).

Rulare: python tests/test_citari.py
Fără API, fără rețea, fără cheie — se poate rula oricând, gratuit.

Regula pe care o apără: verificatorul are voie să completeze un alineat lipsă și
să șteargă un articol inventat, dar NU are voie să atingă o citare corectă. Un
verificator care strică ieșiri bune e mai rău decât unul care lasă să treacă
articole greșite — vezi „Verifică testul înainte să verifici codul" din README.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "verificainainte"))
from citari import verifica_citari  # noqa: E402

# (nume, intrare, ieșire așteptată sau None dacă textul trebuie să rămână identic,
#  acțiuni așteptate în jurnal)
CAZURI = [
    (
        "completează alineatul lipsă la Codul penal — abaterea văzută în rulările reale",
        "A pretinde calitatea de polițist se pedepsește ca înșelăciune (art. 244 Cod Penal).",
        "A pretinde calitatea de polițist se pedepsește ca înșelăciune (art. 244 alin. (2) Cod Penal).",
        ["completat"],
    ),
    (
        "completează și când legea e numită înainte",
        "Legea 218/2002, art. 31 prevede invitarea în scris.",
        "Legea 218/2002, art. 31 alin. (1) lit. c) prevede invitarea în scris.",
        ["completat"],
    ),
    (
        "citarea corectă din exemplul de prompt rămâne neatinsă",
        "TEMEI JURIDIC: ANAF comunică actele fiscale doar în scris (Legea 207/2015, art. 47).",
        None,
        [],
    ),
    (
        "citarea completă cu alineat rămâne neatinsă",
        "A pretinde calitatea de angajat al băncii se pedepsește ca înșelăciune "
        "(art. 244 alin. (2) Cod Penal, închisoare de la unu la 5 ani).",
        None,
        [],
    ),
    (
        "art. 49 Legea 129/2019 e legitim fără alineat — promptul îl descrie cu mai multe",
        "Contul tău devine canal pentru bani din infracțiuni (Legea 129/2019, art. 49).",
        None,
        [],
    ),
    (
        "art. 11 alin. (1) din Legea 207/2015 rămâne neatins",
        "Personalul ANAF păstrează secretul fiscal (art. 11 alin. (1) din Legea 207/2015).",
        None,
        [],
    ),
    (
        "art. 3 alin. (4) lit. f) se rezolvă pe OUG 104/2021, nu pe OUG 93/2012",
        "DNSC cooperează cu organele de urmărire penală (art. 3 alin. (4) lit. f) OUG 104/2021).",
        None,
        [],
    ),
    (
        "articol inexistent în legea numită — se elimină trimiterea",
        "ANAF nu te sună niciodată, conform art. 5 din Legea 207/2015. Închide apelul.",
        "ANAF nu te sună niciodată. Închide apelul.",
        ["eliminat"],
    ),
    (
        "articol inventat între paranteze — cade toată paranteza",
        "Fapta e infracțiune (art. 999 Cod penal) și se raportează la poliție.",
        "Fapta e infracțiune și se raportează la poliție.",
        ["eliminat"],
    ),
    (
        "articol inventat în mijlocul frazei — fraza rămâne citibilă",
        "Situația e sancționată de art. 412 din Legea 129/2019 și se anunță băncii.",
        "Situația e sancționată și se anunță băncii.",
        ["eliminat"],
    ),
    (
        "numărul apare în mai multe acte, iar textul nu spune în care — se lasă, se notează",
        "Atribuțiile sunt prevăzute la art. 2 și nu includ conturile persoanelor fizice.",
        None,
        ["ambiguu"],
    ),
    (
        "art. 113 alin. (4) trece, dar se notează — capcana semantică din audit",
        "Banca nu cere date (art. 113 alin. (4) OUG 99/2006).",
        None,
        ["de_revizuit"],
    ),
    (
        "răspuns fără nicio citare — nimic de făcut",
        "TEMEI JURIDIC: Comercianții legitimi nu solicită confirmarea unei comenzi "
        "inexistente prin linkuri în email — semnalul indică phishing.",
        None,
        [],
    ),
    (
        "art. 21^5 OUG 93/2012 — numerotarea cu indice nu derutează verificatorul",
        "Amenzile ASF privesc entitățile reglementate (art. 21^5 OUG 93/2012).",
        None,
        [],
    ),
]


def main():
    esecuri = 0
    for nume, intrare, asteptat, actiuni_asteptate in CAZURI:
        asteptat = intrare if asteptat is None else asteptat
        obtinut, jurnal = verifica_citari(intrare)
        actiuni = [n["actiune"] for n in jurnal]
        ok_text = obtinut == asteptat
        ok_jurnal = actiuni == actiuni_asteptate
        if ok_text and ok_jurnal:
            print(f"  OK   {nume}")
            continue
        esecuri += 1
        print(f"  EȘEC {nume}")
        if not ok_text:
            print(f"       așteptat: {asteptat!r}")
            print(f"       obținut : {obtinut!r}")
        if not ok_jurnal:
            print(f"       jurnal așteptat: {actiuni_asteptate} | obținut: {actiuni}")

    print(f"\n{len(CAZURI) - esecuri}/{len(CAZURI)} cazuri trecute")
    return 1 if esecuri else 0


if __name__ == "__main__":
    sys.exit(main())
