# Teste de regresie pentru SYSTEM_PROMPT

Se rulează după **fiecare** modificare a promptului din `verificainainte/main.py`.

## De ce există

Riscul unui prompt care crește nu e că tiparul nou nu merge — pe acela îl testezi
oricum, imediat ce îl adaugi. Riscul e că un tipar vechi, de la mijlocul listei,
începe să fie ignorat, iar tu nu afli, pentru că nimeni nu-l mai testează.

Se numește **regresie**: ceva care funcționa se strică fără să fi atins acea parte.
Antidotul e un set fix de scenarii, rulate identic de fiecare dată. Contează mai
puțin rezultatul absolut, mai mult **diferența față de rularea anterioară**.

## Ce testează cele 8 scenarii

| ID | Ce verifică |
|----|-------------|
| 01 | tipar de la **începutul** listei — mai e văzut? |
| 02 | tipar de la **mijlocul** listei — poziția cea mai vulnerabilă |
| 03 | tiparul cel mai **nou** + limita medicală |
| 04 | tipar V4.2, mecanism inversat |
| 05 | **fals pozitiv** — mesaj legitim; CRITIC aici = model stricat |
| 06 | **nuanță** — situație ambiguă; nu trebuie CRITIC |
| 07 | **fallback juridic** — instituție din afara cadrului; fără articole inventate |
| 08 | **limita medicală** izolată — nu se pronunță pe eficacitate |

Scenariul 05 e cel mai ușor de uitat și cel mai important. Un model care vede
fraudă peste tot e la fel de inutil ca unul care nu vede niciuna — doar că eșecul
lui e invizibil, pentru că „CRITIC" pare mereu răspunsul prudent.

## Cum se rulează

### `local.py` — implicit, pentru orice test de prompt

```bash
pip install anthropic python-dotenv
python tests/local.py                 # toate scenariile
python tests/local.py 03              # doar unul
python tests/local.py 03 --repeta 5   # de 5 ori
```

Citește `SYSTEM_PROMPT` direct din `main.py` și cheamă API-ul Anthropic cu cheia
de **dev**. Nu atinge producția: fără rate limit, fără înregistrări în contorul
SQLite, fără consum pe cheia de producție.

Necesită `ANTHROPIC_API_KEY_DEV` în `.env`.

### `ruleaza.py` — doar pentru verificare end-to-end

```bash
python tests/ruleaza.py
python tests/ruleaza.py --compara rezultate/2026-08-04-1622.json
```

Cheamă backendul live. Folosește-l **doar** când vrei să verifici că lanțul
complet funcționează (rețea + backend + prompt), nu pentru teste de prompt.
Fiecare rulare consumă din cheia de producție și adaugă 8 înregistrări false în
statistici.

## Reguli de interpretare

**O observație nu e o constatare.** Modelele sunt nedeterministe: același prompt,
aceeași intrare, răspunsuri diferite. Înainte să schimbi ceva pe baza unui
comportament ciudat, rulează cu `--repeta 5` și vezi dacă se repetă. Un defect
apărut o dată din șase e zgomot; unul care apare de trei ori din cinci e tipar.

**Separă ce se repară prin prompt de ce se repară prin model.** Detectarea greșită
a unui tipar, un articol de lege inventat, o secțiune lipsă — astea sunt probleme
de prompt. Greșelile de gramatică românească și frazele incoerente izolate sunt
limite ale modelului; niciun prompt nu le rezolvă.

**Verifică testul înainte să verifici codul.** Un test care raportează probleme
inexistente e mai periculos decât unul care ratează probleme reale — te învață să
ignori alertele.

## Rezultate de referință

Rulare 2026-08-04, prompt V4.3 (~11.150 tokeni), Haiku 4.5:

- 8/8 scenarii cu scorul așteptat
- fără regresie pe tiparele vechi (01, 02 corecte, cu sfatul specific potrivit)
- fără fals pozitiv (05 → SCĂZUT), fără alarmism (06 → MEDIU)
- fallback juridic funcțional (07 → zero articole inventate)
- scenariul 03 rulat de 5 ori: SCOR stabil CRITIC 5/5, zero articole inventate 5/5
- persistent la toate rulările: greșeli de gramatică românească (limită de model)
