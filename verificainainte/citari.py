"""
Verificare deterministă a trimiterilor la lege din răspunsul modelului.

De ce există: promptul cere modelului să citeze EXCLUSIV articolele din secțiunea
CADRUL JURIDIC și să reproducă alineatul. O instrucțiune din prompt e o rugăminte
respectată probabilistic de un model mic, iar fiecare gardă negativă adăugată
(„este INTERZIS să citezi art. X pentru…") crește promptul definitiv și nu iese
niciodată. Lista de mai jos e o garanție, costă zero tokeni și zero apeluri.

Patru acțiuni, în ordinea încrederii:
  - articol cunoscut, formă completă              -> trece neatins
  - articol cunoscut, fără alineatul obligatoriu  -> se completează
                                                     („art. 244" -> „art. 244 alin. (2)")
  - articol cunoscut, cu alt alineat decât cel din CADRUL JURIDIC
    („art. 244 alin. (1)")                        -> se corectează la forma din prompt
  - număr care nu apare în niciun act din catalog, sau pereche lege/articol
    imposibilă („art. 5 din Legea 207/2015")      -> trimiterea se elimină din text

Corectarea alineatului se aplică DOAR articolelor pentru care catalogul dă un
alineat unic — adică acelea pe care promptul le descrie cu un singur alineat.
Unde promptul citează mai multe (art. 47 Legea 207/2015, art. 49 Legea 129/2019),
valoarea din catalog e None și orice alineat scris rămâne neatins.

Ce NU face: nu judecă dacă articolul e potrivit pentru afirmația din propoziție.
Aia rămâne treaba promptului (ex: art. 113 OUG 99/2006 se adresează angajaților
băncii, nu escrocului) — astfel de cazuri se marchează doar în jurnal, textul nu
se atinge. La fel când articolul e real, dar contextul nu spune din ce lege e:
se lasă neatins și se notează. Ștergerea din greșeală a unei citări corecte e mai
rea decât păstrarea uneia ambigue.
"""
import logging
import re

log = logging.getLogger("citari")

# ── Catalogul de articole permise ───────────────────────────────────────────
# Sursa e secțiunea CADRUL JURIDIC din SYSTEM_PROMPT (main.py). Orice articol
# adăugat acolo trebuie adăugat și aici, altfel citarea lui va fi eliminată.
# Valoarea = alineatul obligatoriu: se completează când modelul scrie articolul
# gol și se corectează când modelul scrie alt alineat. Pune aici o valoare DOAR
# dacă promptul citează articolul cu un singur alineat — altfel corectarea ar
# rescrie o trimitere corectă. None = mai multe alineate în prompt, deci forma
# scurtă e legitimă și orice alineat scris rămâne neatins.
CATALOG = {
    "Legea 207/2015": {"11": "alin. (1)", "46": None, "47": None, "48": "alin. (2)"},
    "Legea 312/2004": {"2": None, "21": "alin. (1)", "51": "alin. (2)", "52": None,
                       "56": None},
    "OUG 99/2006": {"111": None, "112": None, "113": None},
    "Codul de procedură penală": {"257": None, "258": None, "265": None},
    "Legea 218/2002": {"31": "alin. (1) lit. c)"},
    "Legea 360/2002": {"43": "lit. e)"},
    "Codul penal": {"244": "alin. (2)", "348": None},
    "OG 2/2001": {"16": None, "27": "alin. (1)"},
    "OUG 93/2012": {"2": "alin. (1)", "3": None, "6": "alin. (3)", "17^3": None,
                    "21^2": None, "21^5": None},
    "Legea 126/2018": {"10": "alin. (1)", "262": None},
    "OUG 104/2021": {"1": None, "3": "alin. (4) lit. f)", "5": "lit. g)", "7": None},
    "Legea 129/2019": {"6": "alin. (1) lit. a)", "8": None, "38": "alin. (2)",
                       "49": None, "50": None},
}

# Citări reale, dar cu istoric de folosire greșită. Pentru articolele cu alineat
# unic în catalog (art. 27 OG 2/2001) textul de aici explică de ce s-a corectat;
# pentru celelalte (art. 113 OUG 99/2006, art. 3 OUG 93/2012) rămâne o simplă
# notă în jurnal — misuse-ul e semantic, iar verificatorul nu judecă semantica.
# Fiecare intrare vine dintr-o constatare a auditului juridic.
DE_REVIZUIT = {
    ("OUG 99/2006", "113", "alin. (4)"):
        "art. 113 alin. (4) se adresează angajaților băncii, nu escrocului",
    ("OUG 93/2012", "3", "alin. (1) lit. a)"):
        "art. 3 alin. (1) lit. a) descrie doar modul de supraveghere; "
        "pentru autorizare se citează Legea 126/2018",
    ("OG 2/2001", "27", "alin. (2)"):
        "alin. (2) privește martorul la afișare, nu modalitatea de comunicare",
}

# Cum e numit fiecare act în text. Numărul actului e cel mai sigur indiciu;
# codurile n-au număr, deci se recunosc după denumire.
ALIASE = {
    "Legea 207/2015": [r"207\s*/\s*2015", r"cod(?:ul)?\s+de\s+procedur[ăa]\s+fiscal[ăa]"],
    "Legea 312/2004": [r"312\s*/\s*2004"],
    "OUG 99/2006": [r"99\s*/\s*2006"],
    "Codul de procedură penală": [r"\bc\.?p\.?p\.?\b",
                                  r"cod(?:ul)?\s+de\s+procedur[ăa]\s+penal[ăa]"],
    "Legea 218/2002": [r"218\s*/\s*2002"],
    "Legea 360/2002": [r"360\s*/\s*2002"],
    "Codul penal": [r"cod(?:ul)?\s+penal"],
    "OG 2/2001": [r"(?<!\d)2\s*/\s*2001"],
    "OUG 93/2012": [r"93\s*/\s*2012"],
    "Legea 126/2018": [r"126\s*/\s*2018"],
    "OUG 104/2021": [r"104\s*/\s*2021"],
    "Legea 129/2019": [r"129\s*/\s*2019"],
}

# „art. 21^5 alin. (1) lit. c)" — numărul, apoi partea opțională de detaliu.
# Parantezele alineatului sunt opționale în tipar: modelul scrie și „alin. 2".
CITARE = re.compile(
    r"\bart\.\s*(?P<nr>\d+(?:\s*\^\s*\d+)?)"
    r"(?P<detaliu>"
    # paranteza se închide doar dacă s-a și deschis — altfel „(art. 11 alin. 1)"
    # ar înghiți paranteza frazei
    r"(?:\s*alin\.\s*(?:\(\s*\d+(?:\^\d+)?\s*\)(?:\s*[-–]\s*\(\s*\d+\s*\))?"
    r"|\d+(?:\^\d+)?))?"
    r"(?:\s*lit\.\s*[a-zăâîșț]\)?)?"
    r")",
    re.IGNORECASE,
)

# „art. 6, 38" — enumerare de articole; nu se completează automat, s-ar insera
# alineatul primului articol în mijlocul listei.
ENUMERARE = re.compile(r"\s*(?:,|și|si)\s*\d")

FEREASTRA = 200  # câte caractere în jurul citării se caută numele legii


def _normalizeaza_nr(nr):
    return re.sub(r"\s+", "", nr)


def _formateaza(detaliu):
    """Forma din prompt: „alin. 2" -> „alin. (2)", „lit. c" -> „lit. c)"."""
    detaliu = re.sub(r"alin\.\s*\(?\s*(\d+(?:\^\d+)?)\s*\)?", r"alin. (\1)", detaliu,
                     flags=re.IGNORECASE)
    detaliu = re.sub(r"lit\.\s*([a-zăâîșț])\)?", r"lit. \1)", detaliu, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", detaliu).strip()


def _lege_din_context(text, start, end):
    """Ce act normativ e numit cel mai aproape de citare. None dacă niciunul."""
    de_la = max(0, start - FEREASTRA)
    pana_la = min(len(text), end + FEREASTRA)
    fereastra = text[de_la:pana_la]
    pozitie = start - de_la
    gasite = []
    for lege, tipare in ALIASE.items():
        for tipar in tipare:
            for m in re.finditer(tipar, fereastra, re.IGNORECASE):
                gasite.append((abs(m.start() - pozitie), lege))
    return min(gasite)[1] if gasite else None


def _span_eliminare(text, start, end):
    """Extinde spanul citării ca ștergerea să nu lase o frază ciuntită."""
    s, e = start, end
    dupa = re.match(
        r"\s*(?:din\s+|,\s*)?(?:"
        r"(?:Legea|Legii|OUG|O\.U\.G\.|OG|O\.G\.|Ordonanța|Ordinul)\s*(?:nr\.\s*)?"
        r"\d+(?:\^\d+)?\s*/\s*\d{4}"
        r"|Cod(?:ul)?\s+(?:penal|de\s+procedur[ăa]\s+(?:penal[ăa]|fiscal[ăa]))"
        r"|C\.?P\.?P\.?"
        r")",
        text[e:], re.IGNORECASE)
    if dupa and dupa.end() > 0:
        e += dupa.end()
    inainte = re.search(r"(?:,\s*)?\b(?:conform|potrivit|[îi]n baza|[îi]n temeiul|cf\.|de|din|la)"
                        r"\s+$", text[:s], re.IGNORECASE)
    if inainte:
        s = inainte.start()
    # dacă paranteza nu mai conține aproape nimic fără citare, cade toată
    st = text.rfind("(", 0, s)
    dr = text.find(")", e)
    if st != -1 and dr != -1 and ")" not in text[st:s] and "(" not in text[e:dr]:
        rest = (text[st + 1:s] + text[e:dr]).strip(" ,;–-")
        if len(rest) <= 25:
            s, e = st, dr + 1
            if s > 0 and text[s - 1] == " ":
                s -= 1
    return s, e


def _curata(text):
    """Repară urmele lăsate de ștergere: paranteze goale, spații duble, virgule."""
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"[ \t]+([,.;:])", r"\1", text)
    text = re.sub(r",\s*([,.;])", r"\1", text)
    text = re.sub(r"[ \t]+\)", ")", text)
    text = re.sub(r"\([ \t]+", "(", text)
    return text


def verifica_citari(text):
    """
    Întoarce (text_verificat, jurnal).

    Jurnalul e o listă de dicționare cu 'actiune' (completat / eliminat / ambiguu
    / de_revizuit), 'citare' și 'motiv'. Textul se modifică doar la 'completat'
    și 'eliminat'.
    """
    if not text:
        return text, []

    jurnal = []
    modificari = []  # (start, end, înlocuitor)

    for m in CITARE.finditer(text):
        nr = _normalizeaza_nr(m.group("nr"))
        detaliu = re.sub(r"\s+", " ", (m.group("detaliu") or "").strip())
        citare = re.sub(r"\s+", " ", m.group(0).strip())
        lege = _lege_din_context(text, m.start(), m.end())
        candidati = [l for l in CATALOG if nr in CATALOG[l]]

        if not candidati or (lege is not None and lege not in candidati):
            motiv = (f"art. {nr} nu figurează în {lege} în CADRUL JURIDIC"
                     if candidati else
                     f"art. {nr} nu figurează în niciun act din CADRUL JURIDIC")
            s, e = _span_eliminare(text, m.start(), m.end())
            modificari.append((s, e, ""))
            jurnal.append({"actiune": "eliminat", "citare": citare, "motiv": motiv})
            continue

        if lege is None:
            potriviri = [l for l in candidati
                         if CATALOG[l][nr] and detaliu
                         and CATALOG[l][nr].lower().startswith(detaliu.lower()[:8])]
            if len(potriviri) == 1:
                lege = potriviri[0]
            elif len(candidati) == 1:
                lege = candidati[0]
            else:
                jurnal.append({
                    "actiune": "ambiguu", "citare": citare,
                    "motiv": f"art. {nr} apare în {len(candidati)} acte, "
                             "iar textul nu spune în care",
                })
                continue

        cerut = CATALOG[lege][nr]
        scris = _formateaza(detaliu) if detaliu else ""

        if not scris and not cerut:
            continue  # promptul descrie articolul cu mai multe alineate
        if not scris and ENUMERARE.match(text, m.end()):
            jurnal.append({
                "actiune": "ambiguu", "citare": citare,
                "motiv": f"art. {nr} apare într-o enumerare de articole — "
                         "alineatul nu se completează automat",
            })
            continue

        final, actiune, motiv = scris, None, ""
        if not scris:
            final, actiune = cerut, "completat"
            motiv = f"art. {nr} -> art. {nr} {cerut} ({lege})"
        elif cerut and scris != cerut and not scris.startswith(cerut):
            final = cerut
            if cerut.startswith(scris):
                # „art. 31 alin. (1)" când catalogul cere „alin. (1) lit. c)":
                # nu e greșit, e incomplet — se duce până la forma din prompt
                actiune = "precizat"
                motiv = f"art. {nr} {scris} -> art. {nr} {cerut} ({lege})"
            else:
                # alineat scris explicit, dar altul decât cel din CADRUL JURIDIC
                actiune = "corectat"
                motiv = (f"art. {nr} {scris} -> art. {nr} {cerut}: "
                         + (DE_REVIZUIT.get((lege, nr, scris))
                            or f"în {lege}, CADRUL JURIDIC citează art. {nr} {cerut}"))
        elif scris != detaliu:
            actiune = "normalizat"
            motiv = f"{citare} -> art. {nr} {scris}"

        if actiune:
            # „Art." la început de frază rămâne cu majusculă
            prefix = re.sub(r"\s+", " ", text[m.start():m.start("nr")])
            modificari.append((m.start(), m.end(), f"{prefix}{nr} {final}"))
            jurnal.append({"actiune": actiune, "citare": citare, "motiv": motiv})

        avertisment = DE_REVIZUIT.get((lege, nr, final))
        if avertisment:
            jurnal.append({"actiune": "de_revizuit", "citare": citare,
                           "motiv": avertisment})

    if not modificari:
        return text, jurnal

    rezultat = text
    for s, e, inlocuitor in sorted(modificari, reverse=True):
        rezultat = rezultat[:s] + inlocuitor + rezultat[e:]
    # curățenia atinge tot textul, deci se face doar când chiar s-a șters ceva —
    # o completare de alineat nu lasă spații duble sau paranteze goale în urmă
    if any(not inlocuitor for _, _, inlocuitor in modificari):
        rezultat = _curata(rezultat)
    return rezultat, jurnal


def jurnalizeaza(jurnal):
    """Scrie în log doar ce merită privit — un articol inventat sau eliminat."""
    for nota in jurnal:
        nivel = (log.warning if nota["actiune"] in ("eliminat", "ambiguu", "corectat")
                 else log.info)
        nivel("citare %s: %s (%s)", nota["actiune"], nota["citare"], nota["motiv"])
