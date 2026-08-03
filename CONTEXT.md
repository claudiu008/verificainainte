# CONTEXT — VerificăÎnainte

Stare la 3 august 2026. De actualizat când se schimbă ceva structural.

---

## Ce este

Aplicație web gratuită, în română, care analizează contacte suspecte (apeluri,
SMS, email, mesaje WhatsApp) și returnează scor de risc, tiparul de fraudă
detectat, acțiuni de protecție și temeiul juridic. Conceput ca „buton de pauză
înainte de un transfer bancar". Public țintă: cetățeni obișnuiți, inclusiv
vârstnici și diaspora.

Proiect solo, construit în concediu de creștere a copilului.

---

## Stack

| Componentă | Detaliu |
|---|---|
| Backend | Python/FastAPI pe Railway — `verificainainte/main.py` |
| Frontend | React/Vite pe Vercel — `frontend/` |
| Model | Claude Haiku 4.5 (upgrade la Sonnet după decizia Startup Program) |
| Repo | `claudiu008/verificainainte` (public, SSH) |
| Domeniu | verificainainte.ro — rotld.ro, DNS Cloudflare |
| Tracking | SQLite pe volum Railway, `/data/stats.db` |
| Analytics | Vercel Analytics (blocat de Brave Shields) + Google Search Console |

Mediu local: PowerShell 7 pe Windows cu WSL2. `Select-String`, nu `grep`.
Virtualenv-ul e `.venv`.

---

## Prompt-ul aplicației

`SYSTEM_PROMPT` în `main.py`, versiunea V4.1 (~10.000 tokeni).

Conține: cadrul juridic pentru șase instituții plus Legea 129/2019, 14 tipare
de fraudă active, criterii explicite de SCOR (CRITIC/RIDICAT/MEDIU/SCĂZUT),
șase secțiuni de răspuns în ordine fixă, cinci exemple few-shot.

**Regula absolută:** nicio citare legală care nu a fost verificată în PDF-ul
oficial de pe legislatie.just.ro. Când instituția invocată nu are temei în
prompt, se folosește principiul general, fără articole.

---

## Stare distribuție

- SEO: 9 pagini statice în `frontend/public/fraude/`, indexate în GSC
- Social: Facebook, Instagram, Threads (`@verificainainte`)
- Threads e canalul dominant, raport ~6:1 față de Facebook
- Corelație confirmată: zilele fără postare = zile cu ~0 verificări.
  Traficul nu curge de la sine, curge când împingi conținut în feed.

---

## Diagnostic principal

Produs solid tehnic, cu problemă de distribuție și măsurare, nu de tehnologie.
Decalaj mare între reach pe social (mii de vizualizări) și utilizări reale.

Cauza structurală: unealta e „pull", nu „push" — omul trebuie să-și amintească
de ea exact în momentul de panică.

---

## Ce urmează

1. Articole SEO pe tipare concrete de scam (lista de 10 subiecte stabilită)
2. RAG pe legislația română
3. Upgrade la Sonnet după creditele Startup Program
4. Monetizare — doar după clarificarea constrângerii legale legate de rolul
   profesional. Direcția: B2B/B2B2C (rapoarte PDF pentru avocați, API pentru
   instituții financiare, sponsorizări CSR, granturi), nu B2C.

---

## Mod de lucru

- Modificările de cod se fac în Claude Code, nu aici. Chat-ul ăsta e pentru
  strategie, acuratețe juridică și planificare.
- Verificarea codului se face prin pull din GitHub:
  `curl -sL https://codeload.github.com/claudiu008/verificainainte/tar.gz/refs/heads/main`
  Se șterge întâi extragerea anterioară, ca să nu se citească fișiere vechi.
- O singură temă odată, cu scopul discutat înainte de a construi ceva.
