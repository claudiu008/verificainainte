# Teste de regresie pentru SYSTEM_PROMPT

Se rulează după **fiecare** modificare a promptului din `verificainainte/main.py`.

## De ce există

Riscul unui prompt care crește nu e că tiparul nou nu merge — pe acela îl testezi
oricum, imediat ce îl adaugi. Riscul e că un tipar vechi, de la mijlocul listei,
începe să fie ignorat, iar tu nu afli, pentru că nimeni nu-l mai testează.

Se numește **regresie**: ceva care funcționa se strică fără să fi atins acea parte.
Antidotul e un set fix de scenarii, rulate identic de fiecare dată. Contează mai
puțin rezultatul absolut, mai mult **diferența față de rularea anterioară**.

## Ce testează cele 11 scenarii

| ID | Ce verifică | Scor așteptat |
|----|-------------|---------------|
| 01 | tipar de la **începutul** listei — mai e văzut? | CRITIC |
| 02 | tipar de la **mijlocul** listei — poziția cea mai vulnerabilă | CRITIC |
| 03 | tipar medical, **etapa 1** (reclama) + limita medicală | RIDICAT |
| 03b | tipar medical, **etapa 2** — apelul „medicului"; profilare, nu vânzare | CRITIC |
| 04 | tipar V4.2, mecanism inversat | CRITIC |
| 04b | **abonament suspendat** — rămâne ferm când o coincidență reală face mesajul plauzibil | RIDICAT |
| 05 | **fals pozitiv** — mesaj legitim; CRITIC aici = model stricat | SCĂZUT |
| 06 | **nuanță** — situație ambiguă; nu trebuie CRITIC | MEDIU sau SCĂZUT |
| 07 | **fallback juridic** — instituție din afara cadrului; fără articole inventate | CRITIC sau RIDICAT |
| 08 | **limita medicală** izolată — nu se pronunță pe eficacitate, dar rămâne în format | SCĂZUT |
| 09 | **ieșirea din format** — mesaj chiar în afara sferei; perechea lui 08 | — (fără SCOR) |

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

Necesită `ANTHROPIC_API_KEY_DEV` în `.env` (se acceptă și numele vechi, `dev`).

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

Rulare 2026-08-19, prompt V4.7 (~15.000 tokeni, 40.466 caractere), Haiku 4.5
(`rezultate/local-2026-08-19-1827.json`):

- **11/11 scenarii cu scorul așteptat** — prima rulare completă fără nicio abatere
- fără regresie pe tiparele vechi (01, 02 corecte, cu sfatul specific potrivit),
  deși promptul a crescut cu ~6.500 de caractere față de V4.5
- fără fals pozitiv (05 → SCĂZUT), fără alarmism (06 → MEDIU)
- fallback juridic funcțional (07 → zero articole inventate, stabil pe 3 rulări)
- 08 emite acum formatul complet cu SCOR: SCĂZUT, stabil 5 din 5, păstrând
  limita medicală — vezi mai jos
- 09 confirmă că ieșirea din format încă funcționează unde trebuie, stabil 3 din 3
- corecțiile juridice se văd în ieșire: 02 spune „electronic prin contul de pe
  spv.anaf.ro în care tu intri singur", fără „doar dacă ai optat"; trimiterile la
  Codul penal ies cu alineat, „art. 244 alin. (2)"
- persistent la toate rulările: greșeli de gramatică românească (limită de model)

### Abaterea rămasă

**03 variază între RIDICAT și CRITIC.** Istoric: RIDICAT de 8 ori, CRITIC de 5 ori.
Nu e regresie, e nedeterminism — vezi regula de interpretare de mai sus. Merită
totuși revizuit dacă așteptarea `RIDICAT` din `scenarii.json` mai e corectă:
criteriul CRITIC (g) din prompt descrie literal acest scenariu, deci CRITIC e
apărabil.

**01 variază și el, între CRITIC și RIDICAT**, dar CRITIC rămâne dominant
(4 din 5 la `--repeta 5` pe V4.6, 3 din 5 pe V4.5). Verificat explicit după
creșterea promptului, fiindcă scenariul 01 există tocmai ca să prindă diluarea
tiparelor vechi într-un prompt lung. Nu s-a produs.

### 08 — ce era și cum s-a reparat (V4.7)

Scorul ieșea „—" în *fiecare* rulare completă din istoric (4, 17 și 19 august):
răspunsul era bun pe fond, dar fără linia `SCOR:`, deci `detecteazaScor()` din
`App.jsx` nu colora bannerul de risc.

Cauza nu era neascultare a modelului, ci o regulă din prompt: „dacă mesajul nu
descrie deloc un risc financiar, răspunde fără SCOR și fără formatul standard".
Modelul citea „am cumpărat un supliment, chiar funcționează?" ca fiind în afara
sferei și ieșea corect din format, conform instrucțiunii.

Reparat în două mișcări, fiindcă prima singură nu a fost suficientă — regula
rescrisă (ieșirea din format e permisă doar când nu există bani, produs sau
contact primit; „nu e fraudă" e rezultat al analizei, nu motiv să nu o faci) a
lăsat modelul tot pe „—" în 5 din 5. Abia adăugarea unui exemplu few-shot cu
formatul complet pentru o achiziție benignă din farmacie a mutat rezultatul, la
5 din 5 SCĂZUT.

**Exemplul din prompt folosește intenționat alt produs decât scenariul 08** (spray
nazal, nu colagen). Prima variantă reproducea textul scenariului cuvânt cu cuvânt,
ceea ce ar fi făcut testul să se valideze singur. Cu inputuri diferite, 08
măsoară generalizare, nu memorare.

Scenariul **09 e perechea lui 08** și a fost adăugat odată cu reparația: 08
verifică să NU se iasă din format când e vorba de o cheltuială, 09 verifică să SE
iasă când chiar nu e nimic de analizat. Fără 09, îngustarea regulii ar fi putut
transforma orice întrebare off-topic într-o analiză de risc, iar suita nu ar fi
prins-o.
