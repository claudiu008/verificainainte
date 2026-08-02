# SEO-SPEC.md — Pagini statice per tipar de fraudă
Spec pentru Claude Code. Proiect: VerificăÎnainte. Obiectiv: capturarea căutărilor Google
de tip „am primit [mesajul X], e real?" prin pagini statice indexabile, fără a atinge SPA-ul.

---

## 1. Decizie de arhitectură

**Pagini HTML statice pure în `frontend/public/fraude/`**, servite ca fișiere de Vercel.

- NU migrăm la Next/Astro (risc mare, câștig zero la 9 pagini).
- NU folosim rute React (SPA-ul nu e indexabil fiabil fără prerender).
- Vite copiază `public/` în `dist/` la build → Vercel le servește direct.
- Un singur CSS comun: `frontend/public/fraude/fraude.css`. Zero JavaScript pe aceste pagini.
- Refolosește variabilele CSS existente din `index.css` (`--text`, `--bg`, `--border`,
  `--text-h`, `--accent-bg`, `--accent-border`) copiate în `fraude.css` cu
  `color-scheme: light dark` — dark mode trebuie să funcționeze identic cu SPA-ul.

**⚠️ De verificat la prima pagină:** dacă există un rewrite catch-all spre `index.html`
(vercel.json sau setări Vercel), fișierele statice au prioritate („filesystem first"),
dar testează manual `https://verificainainte.ro/fraude/whatsapp-cont-spart/` după deploy
înainte de a genera restul paginilor.

---

## 2. Structura URL (9 pagini)

Slug-uri fără diacritice, cu cratime. Fiecare pagină = `index.html` în folderul ei.

| # | URL | Tipar (exact ca în SYSTEM_PROMPT) | Căutări țintă (exemple) |
|---|-----|-----------------------------------|--------------------------|
| 0 | `/fraude/` | Index — lista tuturor tiparelor | „tipuri de fraude online romania 2026" |
| 1 | `/fraude/whatsapp-cont-spart/` | Cont WhatsApp/Telegram compromis | „mesaj whatsapp prieten cere bani imprumut", „cont whatsapp spart ce fac" |
| 2 | `/fraude/amenda-falsa-sms/` | Amendă falsă de circulație prin SMS | „sms amenda neplatita link plata", „am primit sms amenda e real", „sms raspunde cu 1 amenda" |
| 3 | `/fraude/apel-fals-banca-politie/` | Vishing instituțional clasic | „m-a sunat banca cont blocat transfer", „apel politie procuror bani cont sigur" |
| 4 | `/fraude/voce-ai-telefon/` | Vishing cu voce generată AI | „voce clonata ai telefon frauda", „m-a sunat ruda voce ciudata cere bani" |
| 5 | `/fraude/investitii-crypto-false/` | Spoofing + investiții cripto false | „platforma investitii suna insistent", „recuperare bani crypto frauda apel" |
| 6 | `/fraude/anaf-fals-firme/` | Falși agenți ANAF (vizează firme) | „email anaf actualizare date bancare firma", „apel anaf urgent e adevarat" |
| 7 | `/fraude/dispozitiv-blocat/` | „Dispozitiv blocat" (Poliție/DNSC falși) | „ecran blocat politia romana amenda", „mesaj dnsc calculator blocat plata" |
| 8 | `/fraude/date-scurse-ancpi/` | Fraudă post-breșă de date | „ancpi date furate ce fac", „m-a sunat cineva stie cnp adresa" |

Căutările sunt ipoteze de pornire — se validează după 4 săptămâni cu datele reale din
Google Search Console (secțiunea 7) și cu Google Autocomplete.

---

## 3. Template de pagină (secțiuni fixe, în această ordine)

Fiecare pagină respectă exact structura de mai jos. Ton: română simplă, fără anglicisme,
orice termen tehnic explicat în paranteză la prima apariție (regulă existentă a proiectului).

1. **`<head>`**
   - `<html lang="ro">`
   - `<title>`: întrebarea căutată + brand. Ex: „Mesaj WhatsApp de la un prieten care cere bani — e fraudă? | VerificăÎnainte"
   - `<meta name="description">`: 150–160 caractere, include semnalul principal + promisiunea („Cum recunoști... și ce faci în primele 5 minute.")
   - `<link rel="canonical" href="https://verificainainte.ro/fraude/[slug]/">`
   - OG tags: `og:title`, `og:description`, `og:image` (refolosește `og-image.png` existent), `og:url`, `og:type=article`
   - favicon existent

2. **Header** — logo/titlu VerificăÎnainte, link spre `/` (consistent cu SPA-ul)

3. **H1** = formularea căutării, ca întrebare. Ex: „Ai primit un mesaj pe WhatsApp de la un prieten care îți cere bani?"

4. **„Așa arată mesajul"** — box vizual cu un exemplu realist de mesaj fraudulos,
   marcat clar cu eticheta **EXEMPLU DE MESAJ FALS** (stil consistent cu ștampila roșie
   din graficele social media). Exemplele se scriu pe baza descrierii tiparului din
   `SYSTEM_PROMPT` (main.py) — nu se inventează detalii noi de mecanism.

5. **„3 semne că e fraudă"** — H2 + trei puncte scurte, derivate din tiparul respectiv
   plus semnalele de alarmă universale din prompt.

6. **„Ce faci ACUM"** — H2 + maximum 3 pași, aceeași ordine și filosofie ca secțiunea
   CE FACI ACUM din aplicație.

7. **„Ce NU faci"** — H2 + listă scurtă. Obligatoriu pe fiecare pagină:
   „Nu șterge mesajul/emailul — este dovadă pentru Poliție și DNSC."

8. **„Ce spune legea"** — H2 + 1–2 propoziții. **Sursa unică de adevăr: citările deja
   verificate din `SYSTEM_PROMPT` în `verificainainte/main.py`.** Este INTERZIS să se
   adauge articole de lege care nu există deja acolo. Dacă tiparul nu are temei specific,
   se folosește principiul general existent în prompt.

9. **FAQ** — H2 + 3 întrebări/răspunsuri scurte per pagină (variații ale căutării:
   „Ce fac dacă am dat deja click?", „Ce fac dacă am transferat deja banii?",
   „Unde reclam?"). Răspunsurile la „am transferat deja" includ: banca (cerere de
   retragere a plății), Poliția (plângere), păstrarea dovezilor.

10. **CTA principal** — banner teal (stil consistent cu graficele existente):
    „Ai primit un mesaj asemănător? Verifică-l gratuit, în 30 de secunde →"
    Link: `https://verificainainte.ro/?utm_source=seo&utm_medium=organic&utm_campaign=[slug]`

11. **„Alte fraude active acum"** — 2–3 linkuri interne spre tiparele înrudite
    + link spre `/fraude/` (index). Fiecare pagină primește minimum 2 linkuri interne
    de la alte pagini.

12. **Footer** — identic în conținut cu footerul SPA: contact@verificainainte.ro,
    butoane sociale (Facebook, Instagram, Threads), disclaimer (secțiunea 5).

13. **JSON-LD** (în `<head>` sau înainte de `</body>`):
    - `FAQPage` cu cele 3 întrebări (pe fiecare pagină de tipar)
    - `Organization` (doar pe `/fraude/` index): nume, URL, logo, sameAs cu profilurile sociale

---

## 4. Pagina index `/fraude/`

- H1: „Fraude active în România — ghid de recunoaștere"
- Un paragraf introductiv (ce este VerificăÎnainte, gratuit, fără cont)
- Card per tipar: titlu + o propoziție + link
- CTA identic cu paginile de tipar
- JSON-LD Organization

---

## 5. Disclaimer (obligatoriu, pe toate paginile + în SPA dacă lipsește)

Text fix, în footer:
> „VerificăÎnainte oferă informații generale de prevenție, generate cu ajutorul
> inteligenței artificiale. Nu constituie consultanță juridică. Pentru situații
> în desfășurare, contactează instituțiile oficiale."

**Verifică dacă SPA-ul are deja acest disclaimer. Dacă nu, se adaugă și acolo, în footer.**

---

## 6. Fișiere tehnice SEO

- `frontend/public/sitemap.xml` — static, cu toate cele 9 URL-uri + `https://verificainainte.ro/`
- `frontend/public/robots.txt`:
  ```
  User-agent: *
  Allow: /
  Sitemap: https://verificainainte.ro/sitemap.xml
  ```
- Performanță: zero JS, imagini doar dacă au valoare (exemplele de mesaj sunt HTML/CSS, nu PNG)

---

## 7. Sarcini manuale (NU pentru Claude Code — le face Claudiu)

1. Google Search Console: verificare domeniu prin înregistrare TXT în Cloudflare DNS
2. Trimite `sitemap.xml` în GSC
3. „Request indexing" manual pentru fiecare din cele 9 URL-uri
4. După 4 săptămâni: exportă interogările reale din GSC → ajustăm titlurile/H1
   pe formulările pe care oamenii chiar le caută

---

## 8. Ordinea de lucru în Claude Code

1. **Pagina pilot**: `/fraude/whatsapp-cont-spart/` (tiparul cel mai răspândit) + `fraude.css`
2. Deploy → test manual: URL accesibil, dark mode ok, mobil ok, view-source arată conținutul
3. Abia apoi: restul de 7 pagini + index + sitemap + robots
4. Commit-uri separate: pilot / restul paginilor / fișiere tehnice

## 9. Criterii de succes (la 6 săptămâni)

- GSC: impresii pe minimum 5 din 9 pagini
- Primele click-uri organice (orice > 0 e semnal valid)
- Vercel Analytics: sesiuni cu `utm_source=seo` care ajung la o verificare
- Dacă o pagină primește impresii dar zero click-uri → rescriem title/description, nu pagina
