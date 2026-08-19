"""
Citește scorul de risc din răspunsul modelului, ca formatul să fie o cifră.

De ce există: `detecteazaScor()` din `frontend/src/App.jsx` colorează bannerul de
risc căutând una dintre cele patru etichete în textul răspunsului. Dacă modelul
iese din format și nu scrie linia `SCOR:`, bannerul dispare — răspunsul rămâne
bun pe fond, dar utilizatorul nu mai vede culoarea, adică exact informația pentru
care a intrat pe site.

Nu e ipotetic: scenariul 08 a ieșit fără `SCOR:` în TOATE rulările complete din
4, 17 și 19 august, iar defectul a fost prins abia când cineva s-a uitat la
răspuns cu ochii. Un număr l-ar fi arătat din prima zi.

Ce NU face: nu repară nimic. Absența liniei e uneori corectă — promptul permite
ieșirea din format când mesajul nu descrie deloc un risc financiar (scenariul 09).
Un răspuns fără scor nu e o eroare, e o rată care trebuie privită: dacă sare după
o modificare de prompt, regula de ieșire din format a devenit prea largă.
"""
import re

# Ordinea și forma exactă din `SCORURI` (App.jsx). Orice etichetă adăugată acolo
# trebuie adăugată și aici, altfel răspunsurile care o folosesc vor fi numărate
# ca fiind fără scor.
ETICHETE = ("SCĂZUT", "MEDIU", "RIDICAT", "CRITIC")

# „SCOR: CRITIC", dar și „**SCOR:** CRITIC", „SCOR: **CRITIC**" ori „## SCOR: ..."
# — modelul scrie markdown, iar frontendul îl randează cu react-markdown.
LINIA_SCOR = re.compile(
    r"^\s*#*\s*\**\s*SCOR\s*\**\s*:\s*\**\s*([A-ZĂÂÎȘȚ]+)",
    re.MULTILINE,
)


def extrage_scor(text):
    """Eticheta de pe linia `SCOR:`, sau None dacă răspunsul nu are una validă."""
    if not text:
        return None
    for m in LINIA_SCOR.finditer(text):
        if m.group(1) in ETICHETE:
            return m.group(1)
    return None
