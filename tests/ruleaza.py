#!/usr/bin/env python3
"""
Rulează scenariile fixe împotriva API-ului live și salvează rezultatele.

Utilizare:
    python ruleaza.py                 # rulează și salvează
    python ruleaza.py --compara FIȘIER  # compară cu o rulare anterioară

Rezultatele se salvează în rezultate/YYYY-MM-DD-HHMM.json
Contează mai puțin rezultatul absolut, mai mult DIFERENȚA față de rularea trecută.
"""
import json, os, re, sys, time, urllib.request
from datetime import datetime

API = os.environ.get("API_URL", "https://verificainainte-production.up.railway.app")
PAUZA = 7  # secunde între cereri — limita e 10/minut


def cheama(text):
    req = urllib.request.Request(
        f"{API}/analyze",
        data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())["rezultat"]


def extrage_scor(r):
    m = re.search(r"SCOR:\s*([A-ZĂÂÎȘȚ]+)", r)
    return m.group(1) if m else "?"


def extrage_tipar(r):
    m = re.search(r"TIPAR DETECTAT:\s*(.+)", r)
    return m.group(1).strip()[:70] if m else "?"


def articole(r):
    return sorted(set(re.findall(r"[Aa]rt\.\s*\d+[^),.\n]*", r)))


def main():
    sc = json.load(open("scenarii.json", encoding="utf-8"))["scenarii"]
    out = []
    for i, s in enumerate(sc, 1):
        print(f"[{i}/{len(sc)}] {s['id']} ... ", end="", flush=True)
        try:
            r = cheama(s["text"])
            rec = {
                "id": s["id"],
                "scor": extrage_scor(r),
                "asteptat": s["asteptat_scor"],
                "tipar": extrage_tipar(r),
                "articole": articole(r),
                "cuvinte": len(r.split()),
                "raspuns": r,
            }
            print(f"{rec['scor']} ({rec['cuvinte']} cuv.)")
        except Exception as e:
            rec = {"id": s["id"], "eroare": str(e)}
            print(f"EROARE: {e}")
        out.append(rec)
        if i < len(sc):
            time.sleep(PAUZA)

    os.makedirs("rezultate", exist_ok=True)
    nume = f"rezultate/{datetime.now():%Y-%m-%d-%H%M}.json"
    json.dump(out, open(nume, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"\n{'ID':<26}{'SCOR':<12}{'AȘTEPTAT':<20}{'CUV.':<7}ARTICOLE")
    print("-" * 95)
    for r in out:
        if "eroare" in r:
            print(f"{r['id']:<26}EROARE")
            continue
        ok = r["scor"] in r["asteptat"]
        print(f"{r['id']:<26}{r['scor']:<12}{r['asteptat']:<20}{r['cuvinte']:<7}"
              f"{len(r['articole'])}  {'' if ok else '  ⚠ DIFERIT'}")
    print(f"\nSalvat: {nume}")


def compara(vechi_path):
    vechi = {r["id"]: r for r in json.load(open(vechi_path, encoding="utf-8"))}
    fisiere = sorted(os.listdir("rezultate"))
    nou = {r["id"]: r for r in json.load(open(f"rezultate/{fisiere[-1]}", encoding="utf-8"))}
    print(f"{vechi_path}  ->  rezultate/{fisiere[-1]}\n")
    for k in nou:
        v, n = vechi.get(k, {}), nou[k]
        if v.get("scor") != n.get("scor"):
            print(f"⚠ {k}: SCOR {v.get('scor')} -> {n.get('scor')}")
        if set(v.get("articole", [])) != set(n.get("articole", [])):
            print(f"⚠ {k}: articole {v.get('articole')} -> {n.get('articole')}")
        d = n.get("cuvinte", 0) - v.get("cuvinte", 0)
        if abs(d) > 60:
            print(f"  {k}: lungime {v.get('cuvinte')} -> {n.get('cuvinte')} ({d:+})")
    print("\n(fără linii de mai sus = nicio regresie detectată)")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--compara":
        compara(sys.argv[2])
    else:
        main()
