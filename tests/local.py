#!/usr/bin/env python3
"""
Testează SYSTEM_PROMPT direct pe API-ul Anthropic, FĂRĂ să atingă producția.

Diferența față de ruleaza.py:
  ruleaza.py  -> cheamă backendul live  -> cheia de PRODUCȚIE, rate limit, contor SQLite poluat
  local.py    -> cheamă direct Anthropic -> cheia de DEV, fără rate limit, fără poluare

Foloseşte-l pe ăsta pentru orice test de prompt. Pe celălalt doar când vrei să
verifici că lanțul complet (rețea + backend + prompt) funcționează.

Setup:
    pip install anthropic
    # în .env, lângă cheia de producție:
    ANTHROPIC_API_KEY_DEV=sk-ant-...

Utilizare:
    python local.py                    # toate scenariile, o dată
    python local.py 03                 # doar scenariul care începe cu "03"
    python local.py 03 --repeta 5      # de 5 ori, ca să separi zgomotul de tipar
"""
import json, os, re, sys, pathlib
from datetime import datetime

# Consola Windows e cp1252 și nu poate tipări „⚠" sau diacriticele — fără asta,
# scriptul crapă exact când un scenariu iese diferit, adică atunci când contează.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("Lipsește pachetul: pip install anthropic")

try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv(pathlib.Path(__file__).parent.parent / "verificainainte" / ".env")
except ImportError:
    pass

AICI = pathlib.Path(__file__).parent
MAIN = AICI.parent / "verificainainte" / "main.py"
MODEL = os.environ.get("TEST_MODEL", "claude-haiku-4-5-20251001")

# „dev" e numele vechi, încă folosit în .env-ul local; ANTHROPIC_API_KEY_DEV e cel documentat.
cheie = os.environ.get("ANTHROPIC_API_KEY_DEV") or os.environ.get("dev")
if not cheie:
    sys.exit("Lipsește ANTHROPIC_API_KEY_DEV (sau dev) în .env. "
             "NU folosi cheia de producție pentru teste.")


def citeste_prompt():
    """Citește SYSTEM_PROMPT direct din main.py — mereu versiunea curentă din repo."""
    s = MAIN.read_text(encoding="utf-8")
    return s.split('SYSTEM_PROMPT = """')[1].split('"""')[0]


def scor(r):
    m = re.search(r"SCOR:\s*([A-ZĂÂÎȘȚ]+)", r)
    return m.group(1) if m else "—"


def tipar(r):
    m = re.search(r"TIPAR DETECTAT:\s*(.+)", r)
    return m.group(1).strip()[:60] if m else "—"


def articole(r):
    return sorted(set(re.findall(r"[Aa]rt\.\s*\d+[^),.\n]*", r)))


def main():
    filtru = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
    repeta = 1
    if "--repeta" in sys.argv:
        repeta = int(sys.argv[sys.argv.index("--repeta") + 1])

    prompt = citeste_prompt()
    print(f"prompt: {len(prompt)} car. (~{round(len(prompt)/2.7)} tokeni) | model: {MODEL}\n")

    sc = json.load(open(AICI / "scenarii.json", encoding="utf-8"))["scenarii"]
    if filtru:
        sc = [s for s in sc if s["id"].startswith(filtru)]
        if not sc:
            sys.exit(f"Niciun scenariu care începe cu '{filtru}'")

    client = Anthropic(api_key=cheie)
    out = []

    for s in sc:
        for n in range(repeta):
            eticheta = f"{s['id']}" + (f" #{n+1}" if repeta > 1 else "")
            print(f"{eticheta:<30}", end="", flush=True)
            m = client.messages.create(
                model=MODEL, max_tokens=1500, system=prompt,
                messages=[{"role": "user", "content": s["text"]}],
            )
            r = m.content[0].text
            rec = {"id": s["id"], "rulare": n + 1, "scor": scor(r),
                   "asteptat": s["asteptat_scor"], "tipar": tipar(r),
                   "articole": articole(r), "cuvinte": len(r.split()),
                   "tokeni_in": m.usage.input_tokens,
                   "tokeni_out": m.usage.output_tokens, "raspuns": r}
            out.append(rec)
            ok = "" if rec["scor"] in rec["asteptat"] else "  ⚠ DIFERIT"
            print(f"{rec['scor']:<10}{rec['cuvinte']:>4} cuv.  "
                  f"{len(rec['articole'])} art.{ok}")

    (AICI / "rezultate").mkdir(exist_ok=True)
    nume = AICI / "rezultate" / f"local-{datetime.now():%Y-%m-%d-%H%M}.json"
    json.dump(out, open(nume, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ti = sum(r["tokeni_in"] for r in out)
    to = sum(r["tokeni_out"] for r in out)
    print(f"\n{len(out)} apeluri | {ti} tokeni intrare, {to} ieșire")
    print(f"salvat: {nume}")

    if repeta > 1:
        print("\n--- STABILITATE (ce e constant = tipar, ce variază = zgomot) ---")
        for sid in dict.fromkeys(r["id"] for r in out):
            g = [r for r in out if r["id"] == sid]
            scoruri = set(r["scor"] for r in g)
            arts = set(tuple(r["articole"]) for r in g)
            print(f"{sid}: scor {'STABIL ' + scoruri.pop() if len(scoruri)==1 else 'VARIAZĂ ' + str(scoruri)}"
                  f" | articole {'stabile' if len(arts)==1 else 'VARIAZĂ'}"
                  f" | lungime {min(r['cuvinte'] for r in g)}–{max(r['cuvinte'] for r in g)} cuv.")


if __name__ == "__main__":
    main()
