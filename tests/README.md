# Teste de regresie pentru SYSTEM_PROMPT

Se rulează după **fiecare** modificare a promptului din `verificainainte/main.py`.

## De ce există

Riscul unui prompt care crește nu e că tiparul nou nu merge — pe acela îl testezi
oricum, imediat ce îl adaugi. Riscul e că un tipar vechi, de la mijlocul listei,
începe să fie ignorat, iar tu nu afli, pentru că nimeni nu-l mai testează.

Se numește **regresie**: ceva care funcționa se strică fără să fi atins acea parte.
Antidotul e un set fix de scenarii, rulate identic de fiecare dată. Contează mai
puțin rezultatul absolut, mai mult **diferența față de rularea anterioară**.

## Ce testează cele 10 scenarii

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
| 08 | **limita medicală** izolată — nu se pronunță pe eficacitate | SCĂZUT |

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

Rulare 2026-08-19, prompt V4.6 (~14.250 tokeni, 38.466 caractere), Haiku 4.5
(`rezultate/local-2026-08-19-1608.json`):

- 8/10 scenarii cu scorul așteptat — același raport ca înainte de corecțiile
  juridice din V4.6, deși promptul a crescut cu ~4.500 de caractere
- fără regresie pe tiparele vechi (01, 02 corecte, cu sfatul specific potrivit)
- fără fals pozitiv (05 → SCĂZUT), fără alarmism (06 → MEDIU)
- fallback juridic funcțional (07 → zero articole inventate, stabil pe 3 rulări)
- tiparul nou 04b → RIDICAT, cu TEMEI JURIDIC fără niciun articol, cum cere promptul
- corecțiile V4.6 se văd în ieșire: 02 spune „electronic prin contul de pe
  spv.anaf.ro în care tu intri singur", fără „doar dacă ai optat"; trimiterile la
  Codul penal ies cu alineat, „art. 244 alin. (2)"
- persistent la toate rulările: greșeli de gramatică românească (limită de model)

### Cele două abateri cunoscute

**03 variază între RIDICAT și CRITIC.** Istoric: RIDICAT de 7 ori, CRITIC de 5 ori.
Nu e regresie, e nedeterminism — vezi regula de interpretare de mai sus. Merită
totuși revizuit dacă așteptarea `RIDICAT` din `scenarii.json` mai e corectă:
criteriul CRITIC (g) din prompt descrie literal acest scenariu, deci CRITIC e
apărabil — iar de la 19 august încoace CRITIC e rezultatul dominant.

**01 variază și el, între CRITIC și RIDICAT**, dar CRITIC rămâne dominant
(4 din 5 la `--repeta 5` pe V4.6, 3 din 5 pe V4.5). Verificat explicit după
creșterea promptului, fiindcă scenariul 01 există tocmai ca să prindă diluarea
tiparelor vechi într-un prompt lung. Nu s-a produs.

**08 nu emite deloc formatul.** Scorul iese „—" în *fiecare* rulare completă din
istoric (4 august, 17 august, 19 august): răspunsul e bun pe fond — refuză să se
pronunțe pe eficacitate și trimite la medic sau farmacist — dar nu conține niciuna
dintre cele 5 secțiuni, deci nici linia `SCOR:`. Consecința e în frontend:
`detecteazaScor()` din `App.jsx` caută eticheta în text, deci pentru astfel de
întrebări bannerul de risc nu se colorează. Se repară din `SYSTEM_PROMPT`, nu din test.
