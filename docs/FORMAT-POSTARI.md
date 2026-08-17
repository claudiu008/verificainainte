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
- **Un singur grafic 1080×1080** servește toate cele trei platforme, Threads
  inclusiv. Postările doar-text performează cel mai slab pe Threads, în ciuda
  reputației de platformă text-first — textul se însoțește mereu de imagine.
- **Primele 60–90 de minute după publicare contează mai mult decât orice
  optimizare.** Algoritmul Threads cântărește greu răspunsurile și viteza cu care
  o postare strânge interacțiune. Se postează când ești disponibil să răspunzi,
  nu în ore moarte.
- **Zero afirmații noi neverificate.** Tot ce apare în postare e fie preluat din
  alerta oficială, fie deja verificat în prompt-ul aplicației.
- **Fără citări legale inventate.** Dacă instituția invocată nu are temei în
  CADRUL JURIDIC din `main.py`, se folosește principiul general de rezervă:
  nicio instituție publică nu cere date sau plăți prin SMS/link.
  Exemplu aplicat: taxele de parcare sunt administrate local, nu de Poliția
  Rutieră — deci NU se citează OG 2/2001 acolo.
- **Fără dată pe grafic.** Nici în antet, nici în pilulă, nici în subtitlu. O dată
  vizibilă scurtează viața utilă a imaginii: postările vechi continuă să aducă
  trafic pe Threads, iar un grafic datat pare expirat chiar când tiparul e încă
  activ. Perisabilitatea indicatorilor concreți (domenii, numere) se gestionează
  prin text, nu prin ștampilarea imaginii.
- **Nicio altă entitate menționată, nici în grafic, nici în text.** Nu se atribuie
  sursa semnalului și nu se citează firme de securitate, instituții sau publicații.
  Singura entitate care apare este brandul sau instituția impersonată de escroci,
  pentru că e subiectul capcanei. Regula privește CONȚINUTUL publicat, nu
  declanșatorul: alertele oficiale rămân sursa care justifică postarea, doar nu se
  numesc în ea.

---

## Structura postării pe Threads

Text scurt, fără emoji. Ordinea:

1. **Cârlig de o linie** — o observație sau un contrast, nu un titlu de știre.
   Exemplu: „Nu de data asta amenințare. De data asta, un compliment."
2. **Mesajul fals, citat exact**, între ghilimele, cu contextul lui.
3. **Mecanismul psihologic, numit explicit** — de ce funcționează pe cine
   funcționează. Asta e partea care diferențiază postarea de o știre.
4. **Restul mecanicii, pe scurt** — link fals, pagină clonă, cere card.
5. **Regula reală** — ce face sau nu face instituția în realitate.
6. **verificainainte.ro** pe rând separat, la final.

**Topic tag pe Threads:** Threads NU are hashtag-uri ca Instagram. Are topic tags
și permite **o singură etichetă per postare**, aleasă din câmpul dedicat. Un `#`
scris în corpul textului rămâne text simplu — nu te bagă în niciun flux.

Reguli:
- Verifică întâi dacă eticheta EXISTĂ. Dacă apare „+ Tag new topic", înseamnă că e
  nouă, are zero postări și nu face nimic. Încearcă fără diacritice.
- O etichetă irelevantă e mai rea decât niciuna — dezinformează algoritmul.
- Eticheta e un departajator, nu un multiplicator. Nu petrece pe ea mai mult de
  câteva secunde.
- `#verificainainte` e un candidat prost pe Threads (flux gol). Brandul se scrie
  natural în text.
- Orice cuvânt din postare e oricum căutabil. Mai eficient decât o etichetă:
  strecoară cuvintele-cheie natural în text („frauda asta", nu doar „escrocheria").

## Structura postării pe Facebook + Instagram

Aceeași substanță, format mai explicit:

1. **🚨 + etichetă** — „Tipar nou:", „Alertă:", urmată de rezumatul în o linie.
2. **Mesajul fals**, prezentat vizibil.
3. **Explicația mecanismului**, cu 2–4 puncte.
4. **Ce faci / Ce nu faci** — instrucțiuni scurte, imperative.
5. **Unde verifici oficial** — domeniul corect, scris complet.
6. **Link + invitație la distribuire** („trimite asta părinților tăi" —
   funcționează ca motor de distribuire pe tiparele care vizează vârstnici).

**Hashtag-uri pe Facebook și Instagram:** aici merg mai multe, spre deosebire de
Threads.

- **Instagram:** în primul comentariu, nu în descriere. Între 5 și 10; peste 15 nu
  mai adaugă nimic.
- **Facebook:** contează puțin. Două-trei, ca semnal de temă.
- **Fără diacritice** — se caută mai mult „escrocherie" decât varianta cu ș și ț,
  iar diacriticele fragmentează eticheta în variante separate.
- **`#verificainainte` pe fiecare postare, pe ambele platforme.** Nu aduce oameni
  noi, dar adună postările într-un loc: cine vede una le găsește pe toate. Se
  construiește doar dacă e pus de la început.

Set de bază, de adaptat la subiect:
`#verificainainte #escrocherie #fraudaonline #phishing #securitatecibernetica
#romania #sfaturiutile` plus 2–3 specifice tiparului (ex. `#crypto`, `#kucoin`
pentru fraudele cu platforme de criptomonede).

---

## Ton

- Română simplă, fără anglicisme („escroci", nu „scammeri").
- Termenii tehnici se explică imediat în paranteză, la prima utilizare.
- Fără judecată la adresa victimei. Niciodată „cum ai putut să crezi asta".
- Fără dramatizare — mecanismul explicat calm e mai convingător decât alarma.

---

## Grafice

1080×1080 PNG, generate din SVG, randate cu Playwright/Chromium headless.

### Format curent: card pe fundal navy

Formatele pe fundal gri deschis (`#F5F5F5`, antet cu scut și titlu verde centrat)
sunt istorice. Rămân în postările deja publicate, nu se mai generează.

Implementarea se află în `docs/grafice/grafic.html`, randată cu
`docs/grafice/randeaza.py`. Template-ul este sursa de adevăr pentru culoare și
geometrie; tabelul de mai jos îl documentează. Dacă cele două diverg, template-ul
are dreptate.

Paletă. Tokenuri Tailwind, citite din graficele publicate.

| Rol | Hex | Token |
|---|---|---|
| Fundal, sus | `#0F172A` | slate-900 |
| Fundal, jos | `#1E293B` | slate-800 |
| Pilulă, buton de formular, bulină numerotată | `#DC2626` | red-600 |
| Ștampilă, buline de listă | `#EF4444` | red-500 |
| Link fals în card, termenii ofertei | `#B91C1C` | red-700 |
| Panou de escaladare (ultimul pas) | `#450A0A` | red-950 |
| Titlu, rândul 1 | `#F8FAFC` | slate-50 |
| Titlu, rândul 2 | `#FCA5A5` | red-300 |
| Subtitlu, placeholder de formular | `#94A3B8` | slate-400 |
| Titlu de secțiune | `#FFFFFF` | — |
| Text bullet | `#E2E8F0` | slate-200 |
| Card mesaj (fundal) | `#F1F5F9` | slate-100 |
| Text în card | `#0F172A` | slate-900 |
| Metadate în card, URL jos-dreapta | `#64748B` | slate-500 |
| Bordură de câmp de formular | `#CDD7E2` | — |
| Rând de pas numerotat | `#1E293B` | slate-800 |
| Banner concluzie | `#064E3B` | emerald-900 |

**Fundalul este gradient vertical, nu culoare plată.** Un fundal uniform se observă
imediat lângă graficele publicate.

**Roșul nu este unul, sunt patru**, cu roluri care nu se amestecă.

Structura verticală, de sus în jos:

1. **Pilulă roșie**, colț stânga-sus, text alb bold cu spațiere între litere.
2. **Titlu pe două rânduri** — rândul 1 alb, rândul 2 somon. Cele două rânduri
   formează un contrast sau o răsturnare, nu o propoziție tăiată în două.
   Exemplu: „Nu capsulele" / „sunt produsul."
3. **Subtitlu de o linie**, gri, care spune concret despre ce tipar e vorba.
4. **Card deschis** cu reproducerea capcanei: expeditor + metadate sus, apoi
   mesajul pe rânduri scurte, rupte manual ca în original. Nu se reformatează
   textul fraudei ca paragraf curgător — rândurile scurte fac mesajul să arate ca
   pe telefon.
5. **Ștampila „CAPCANĂ"** — contur roșu rotunjit, rotit ~9°, suprapus pe marginea
   dreaptă a cardului. Se pune DOAR când cardul reproduce capcana.
6. **Titlu de secțiune** alb bold, care întreabă sau afirmă ceva despre mecanism
   („De ce prinde la oamenii prudenți", „Reclama caută pe cine merită sunat").
7. **Trei buline** — descriu mecanismul, nu instrucțiuni. Câte una pe rând, scurte.
8. **Banner verde**, lățime completă între margini, cu concluzia acționabilă.
   Jumătatea finală, bold: acolo stă regula pe care omul o duce cu el.
9. **verificainainte.ro** jos-dreapta, gri, discret.

Marginile stânga/dreapta: 72 px / 1008 px. Cardul nu se întinde până la marginea
dreaptă — se oprește în jur de 812 px, ca ștampila să aibă unde ieși din el.

### Eticheta din pilulă

- **TIPAR NOU** — mecanism nou, explicat prima dată (tiparul medical în două
  etape, codul de verificare nesolicitat).
- **ALERTĂ NOUĂ** — mecanism deja cunoscut, dar campanie activă acum, cu
  indicatori concreți (domenii, formulări). Aici indicatorul concret se pune în
  card, sub mesaj, în font monospațiat roșu.

Distincția e reală și se respectă: dacă orice campanie primește „TIPAR NOU",
eticheta nu mai transmite nimic.

### Perechea acțiune-negativă / acțiune-pozitivă

Regula se păstrează, dar și-a schimbat locul. În formatul vechi stătea în buline.
În formatul navy, bulinele explică mecanismul, iar perechea completă stă în
bannerul verde: partea nebold spune ce faci, partea bold spune ce nu faci
niciodată. Exemplu: „Deschide aplicația oficială direct. **Niciodată linkul din
mesaj.**"

### Al doilea format: fișă de recunoaștere

Aceeași paletă și aceeași structură, dar cardul reproduce mesajul integral cu
elementele care îl trădează evidențiate în roșu în text, iar secțiunea de jos
listează indiciile numerotate („CELE 4 INDICII"). Gândită să fie salvată și
retrimisă, nu citită o dată. Fără ștampilă — aici mesajul se demontează, nu se
anulează.

---

## Verificare înainte de postare

- [ ] Alerta e reală și recentă (sursă oficială sau presă care citează sursa)
- [ ] Tiparul nu a fost deja acoperit de trei ori
- [ ] Nicio citare legală care să nu existe în `main.py`
- [ ] Domeniul oficial scris complet și corect
- [ ] Textul Threads și textul FB/IG sunt separate, nu identice
- [ ] Graficul nu conține nicio dată
- [ ] Nicio entitate menționată în afara brandului impersonat
