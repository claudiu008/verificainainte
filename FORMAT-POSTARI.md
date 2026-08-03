# FORMAT-POSTĂRI — VerificăÎnainte

Tiparul stabilit pentru conținutul de social media. Orice postare nouă respectă
structura de mai jos, fără excepții nediscutate.

---

## Principii de bază

- **Model reactiv, nu calendar.** Se postează când apare o alertă reală (DNSC,
  Poliția Română, bănci, presă). Nu se inventează conținut ca să se umple un
  program de publicare.
- **Ordinea de postare: Threads primul**, apoi Facebook + Instagram. Threads e
  canalul principal (raport de trafic ~6:1 față de Facebook).
- **Un singur grafic 1080×1080** servește toate cele trei platforme.
- **Zero afirmații noi neverificate.** Tot ce apare în postare e fie preluat din
  alerta oficială, fie deja verificat în prompt-ul aplicației.
- **Fără citări legale inventate.** Dacă instituția invocată nu are temei în
  CADRUL JURIDIC din `main.py`, se folosește principiul general de rezervă:
  nicio instituție publică nu cere date sau plăți prin SMS/link.
  Exemplu aplicat: taxele de parcare sunt administrate local, nu de Poliția
  Rutieră — deci NU se citează OG 2/2001 acolo.

---

## Structura postării pe Threads

Text scurt, fără emoji, fără hashtag-uri. Ordinea:

1. **Cârlig de o linie** — o observație sau un contrast, nu un titlu de știre.
   Exemplu: „Nu de data asta amenințare. De data asta, un compliment."
2. **Mesajul fals, citat exact**, între ghilimele, cu contextul lui.
3. **Mecanismul psihologic, numit explicit** — de ce funcționează pe cine
   funcționează. Asta e partea care diferențiază postarea de o știre.
4. **Restul mecanicii, pe scurt** — link fals, pagină clonă, cere card.
5. **Regula reală** — ce face sau nu face instituția în realitate.
6. **verificainainte.ro** pe rând separat, la final.

## Structura postării pe Facebook + Instagram

Aceeași substanță, format mai explicit:

1. **🚨 + etichetă** — „Tipar nou:", „Alertă:", urmată de rezumatul în o linie.
2. **Mesajul fals**, prezentat vizibil.
3. **Explicația mecanismului**, cu 2–4 puncte.
4. **Ce faci / Ce nu faci** — instrucțiuni scurte, imperative.
5. **Unde verifici oficial** — domeniul corect, scris complet.
6. **Link + invitație la distribuire** („trimite asta părinților tăi" —
   funcționează ca motor de distribuire pe tiparele care vizează vârstnici).

---

## Ton

- Română simplă, fără anglicisme („escroci", nu „scammeri").
- Termenii tehnici se explică imediat în paranteză, la prima utilizare.
- Fără judecată la adresa victimei. Niciodată „cum ai putut să crezi asta".
- Fără dramatizare — mecanismul explicat calm e mai convingător decât alarma.

---

## Grafice

- 1080×1080 PNG, generate din SVG.
- Două formate folosite până acum:
  - **Mockup de mesaj** — reproducerea capcanei (WhatsApp/SMS) cu ștampilă
    „CAPCANĂ / NU TRANSFERA" peste el.
  - **Fișă de recunoaștere** — format de referință, gândit să fie salvat și
    retrimis, nu doar citit o dată.
- Bulletele poartă mereu perechea acțiune-negativă + acțiune-pozitivă
  (ex: NU transfera + SUNĂ pe numărul vechi din agendă).

---

## Verificare înainte de postare

- [ ] Alerta e reală și recentă (sursă oficială sau presă care citează sursa)
- [ ] Tiparul nu a fost deja acoperit de trei ori
- [ ] Nicio citare legală care să nu existe în `main.py`
- [ ] Domeniul oficial scris complet și corect
- [ ] Textul Threads și textul FB/IG sunt separate, nu identice
