# SEO-SPEC-V2.md — Extindere: 7 pagini noi de tipar

Continuare a `SEO-SPEC.md`. Aceleași decizii de arhitectură, același template de
13 secțiuni, același CSS. Nu se schimbă nimic din specificația inițială.

Motivul extinderii: `SYSTEM_PROMPT` a ajuns la 19 tipare, iar paginile
statice acoperă 15 dintre ele. Dintre acestea, 4 tipare nu au încă pagină.

---

## Reguli obligatorii pentru toate paginile de mai jos

1. **Structura identică** cu paginile existente. Model de referință:
   `frontend/public/fraude/amenda-falsa-sms/index.html`. Copiază exact
   convențiile de markup: clasele CSS, headerul, footerul, blocul JSON-LD FAQPage,
   meta tags, favicon inline.
2. **Textul secțiunii „Ce spune legea" este dat verbatim mai jos pentru fiecare
   pagină. Se copiază exact, fără reformulare și fără completări.** Este
   INTERZIS să se adauge orice articol de lege care nu apare în acest fișier.
3. Unde scrie „principiu general, fără articole" — asta nu e o scăpare, e decizia
   corectă: entitatea invocată e o companie privată, nu o instituție publică.
4. Diacritice complete în text. Slug-uri fără diacritice.
5. Ton: română simplă, fără anglicisme. Termenii tehnici se explică în paranteză
   la prima apariție.
6. Fără judecată la adresa victimei, în special pe pagina de escrocherie
   sentimentală.

## Sarcini tehnice după generarea paginilor

- adaugă în `frontend/public/sitemap.xml` URL-ul paginii rămase de generat
- adaugă cardurile în `frontend/public/fraude/index.html`
- **linkuri reciproce**: fiecare pagină nouă trebuie să primească minimum 2
  linkuri interne de la alte pagini. Adaugă în secțiunea „Alte fraude active
  acum" de pe paginile vechi indicate la fiecare intrare de mai jos.
- commit-uri separate: pagini / fișiere tehnice

---

## Ordinea de lucru

După volumul estimat de căutări în română:

| # | Slug | Stare |
|---|------|-------|
| 1 | `colet-blocat-curier` | generat |
| 2 | `cazare-falsa-vacanta` | generat |
| 3 | `fals-suport-tehnic` | generat |
| 4 | `job-fals-sarcini-platite` | generat |
| 5 | `investitii-deepfake` | generat — vezi avertismentul de la secțiunea 5 |
| 6 | `escrocherie-sentimentala` | generat |
| 7 | `abonament-suspendat-plata-esuata` | generat |

---

## 1. `/fraude/colet-blocat-curier/`

**Title:** SMS despre un colet blocat care cere o taxă mică — e fraudă? | VerificăÎnainte
**Meta description:** Ai primit un SMS de la un curier despre un colet oprit, cu o taxă de câțiva lei? Vezi de ce suma mică este capcana și ce faci în primele minute.
**H1:** Ai primit un SMS despre un colet blocat care cere o taxă de câțiva lei?

**Exemplu de mesaj fals:**
> „Coletul dumneavoastră cu AWB 4092817 nu a putut fi livrat — adresă incompletă.
> Achitați taxa de redirecționare de 4,50 lei în 24h pentru reprogramarea livrării:
> curier-redirectionare-colet.com"

Paragraf de context: mesajul vine în numele unui curier cunoscut (Fan Courier,
DHL, Sameday, Poșta Română), invocă un colet oprit în vamă sau o adresă
incompletă, iar suma cerută e mereu între 2 și 15 lei.

**3 semne:**
1. **Suma mică este capcana, nu o scăpare.** Pentru 5 lei nimeni nu se oprește să
   verifice — exact pe asta se bazează. Ținta nu e suma, ci datele cardului.
2. Pagina cere numărul complet al cardului, data expirării și codul CVV. Un
   curier real nu încasează taxe printr-un link primit prin SMS.
3. Termen scurt și consecință: „24h", „coletul se returnează expeditorului".

**Ce faci ACUM:** nu accesa linkul / captură de ecran / caută AWB-ul direct pe
site-ul curierului scris manual în browser, iar dacă aștepți un colet real,
contactează magazinul de la care ai comandat.

**Ce NU faci:** nu introduce datele cardului / nu plăti taxa, oricât de mică /
nu suna numărul din mesaj / nu șterge mesajul — este dovadă pentru Poliție și DNSC.

**Ce spune legea (verbatim):**
> Curierii sunt companii private, nu instituții publice, deci aici nu se aplică
> regulile de comunicare oficială. Se aplică în schimb un principiu simplu: o
> companie legitimă nu cere datele cardului printr-un link nesolicitat, nu cere
> plata în afara canalelor sale oficiale și nu condiționează un serviciu de o
> taxă comunicată prin SMS.
>
> Dacă ai introdus datele cardului, fapta este o infracțiune și poate fi
> reclamată la Poliție. Păstrează mesajul și captura paginii de plată — fără ele,
> plângerea rămâne fără probe.

**FAQ:**
1. Am plătit deja taxa. Ce fac acum? → sună banca, cere blocarea cardului; suma
   plătită nu e problema, datele cardului sunt; plângere la Poliție cu dovezile.
2. Cum verific dacă am într-adevăr un colet în așteptare? → AWB direct pe site-ul
   oficial, scris manual; dacă aștepți colet real, contactează magazinul.
3. Am introdus datele cardului, dar nu văd nicio plată. Sunt în siguranță? → nu;
   datele pot fi folosite peste săptămâni sau pentru abonamente recurente cu sume
   mici, greu de observat pe extras; sună banca oricum.

**Linkuri interne de pe pagina asta:** `amenda-falsa-sms`, `apel-fals-banca-politie`, `/fraude/`
**Linkuri reciproce de adăugat:** din `amenda-falsa-sms` și `apel-fals-banca-politie`

---

## 2. `/fraude/cazare-falsa-vacanta/`

**Title:** Anunț de cazare la preț foarte mic — e fraudă? | VerificăÎnainte
**Meta description:** Gazda îți cere plata în afara platformei, „ca să evitați comisionul"? Vezi de ce asta este semnalul decisiv și cum verifici un anunț de cazare.
**H1:** Ai găsit o cazare foarte ieftină, iar gazda îți cere plata direct în cont?

**Exemplu de mesaj fals:**
> „Bună ziua! Da, apartamentul e liber în perioada aceea. Ca să evităm comisionul
> platformei, vă rog să trimiteți avansul de 40% direct în cont sau prin aplicația
> de plăți. Mai am o singură rezervare disponibilă și am și alte solicitări."

Paragraf de context: anunțul apare pe rețele sociale, în grupuri sau pe site-uri
care imită platforme cunoscute. Fotografiile pot fi furate de pe un anunț real,
iar proprietatea chiar există — doar că nu are nicio legătură cu persoana care
cere banii.

**3 semne:**
1. **Plata în afara platformei oficiale este semnalul decisiv.** Motivul e mereu
   același — „evităm comisionul", „e mai simplu". În afara platformei nu există
   protecție și nici posibilitate reală de recuperare a banilor.
2. Preț vizibil sub piață pentru zonă și perioadă, combinat cu presiune de timp:
   „mai am o singură rezervare".
3. Gazda evită apelul video, refuză un contract și nu poate da detalii verificabile
   despre imobil.

**Ce faci ACUM:** nu trimite avansul / caută adresa și fotografiile în căutarea
inversă de imagini, ca să vezi dacă apar pe alt anunț / dacă anunțul e pe o
platformă, comunică și plătește exclusiv prin platformă.

**Ce NU faci:** nu plăti prin transfer direct, aplicație de plăți sau card
cadou / nu trimite copie după buletin unei persoane necunoscute / nu continua
discuția pe alt canal decât cel al platformei / nu șterge conversația — este
dovadă pentru Poliție.

**Ce spune legea (verbatim):**
> O gazdă sau o agenție de cazare este o entitate privată, deci aici nu se aplică
> regulile de comunicare ale instituțiilor publice. Principiul care se aplică este
> altul: o ofertă legitimă nu te scoate din canalul oficial al platformei ca să
> încaseze banii. Comisionul platformei este exact prețul protecției pe care o
> pierzi când plătești pe lângă ea.
>
> Dacă ai trimis deja banii, fapta este o infracțiune și poate fi reclamată la
> Poliție. Păstrează conversația, anunțul și dovada transferului.

**FAQ:**
1. Am trimis deja avansul. Mai pot recupera banii? → contactează imediat banca și
   cere retragerea plății; depune plângere la Poliție cu dovezile; șansele scad cu
   fiecare oră, deci nu amâna.
2. Cum verific dacă anunțul e real? → caută adresa și fotografiile în căutarea
   inversă de imagini; cere un apel video în care gazda să arate imobilul; verifică
   dacă anunțul există și pe platforma oficială, cu același preț.
3. Gazda pare foarte serioasă și are recenzii. E în regulă? → recenziile pot fi
   copiate odată cu fotografiile. Ce contează nu e cât de convingător pare
   profilul, ci dacă plata rămâne în platformă.

**Linkuri interne:** `colet-blocat-curier`, `apel-fals-banca-politie`, `/fraude/`
**Linkuri reciproce de adăugat:** din `colet-blocat-curier` și `investitii-crypto-false`

---

## 3. `/fraude/fals-suport-tehnic/`

**Title:** Te-a sunat cineva de la „Microsoft" că ai un virus — e fraudă? | VerificăÎnainte
**Meta description:** Ți se cere să instalezi o aplicație ca să-ți repare calculatorul de la distanță? Vezi de ce companiile reale nu sună niciodată și ce faci dacă ai instalat deja.
**H1:** Te-a sunat cineva care spune că dispozitivul tău e infectat?

**Exemplu de mesaj fals:**
> „Bună ziua, sunt de la departamentul tehnic Microsoft. Am detectat activitate
> suspectă pe calculatorul dumneavoastră — cineva încearcă să vă acceseze conturile.
> Ca să pot verifica și repara, vă rog să instalați aplicația pe care v-o indic eu
> acum. Durează două minute."

Paragraf de context: poate veni ca apel neașteptat sau ca fereastră care apare în
browser și anunță că dispozitivul e blocat. Uneori numărul afișat pare românesc
sau oficial — se poate falsifica (spoofing: falsificarea numărului afișat pe ecran).

**3 semne:**
1. **Nu tu ai cerut ajutorul.** Microsoft, Google și furnizorii de internet nu sună
   niciodată utilizatorii pentru probleme pe care aceștia nu le-au semnalat.
2. Ți se cere să instalezi o aplicație de acces la distanță — TeamViewer, AnyDesk
   sau altele (programe care dau altcuiva control complet asupra ecranului tău).
3. Discuția alunecă spre bancă: ți se cere să deschizi aplicația bancară „ca să
   verificăm dacă ai fost afectat".

**Ce faci ACUM:** închide apelul, fără explicații / dacă ai instalat deja
aplicația, deconectează dispozitivul de la internet imediat / schimbă parolele de
pe ALT dispozitiv și anunță banca.

**Ce NU faci:** nu instala nicio aplicație cerută la telefon / nu deschide
aplicația bancară în timpul apelului / nu comunica coduri primite prin SMS /
nu suna înapoi numărul afișat / nu șterge istoricul apelului — este dovadă.

**Ce spune legea (verbatim):**
> Furnizorii de servicii tehnice sunt companii private, deci aici nu se aplică
> regulile de comunicare ale instituțiilor publice. Principiul care se aplică este
> simplu: o companie legitimă nu te sună pentru o problemă pe care nu ai
> semnalat-o și nu îți cere niciodată acces la distanță la dispozitiv în urma unui
> apel pe care nu l-ai solicitat.
>
> Dacă ai oferit acces la dispozitiv sau ai comunicat coduri, fapta este o
> infracțiune și poate fi reclamată la Poliție. Incidentul poate fi raportat și la
> DNSC, care emite alerte naționale pe baza sesizărilor primite.

**FAQ:**
1. Am instalat deja aplicația. Ce fac? → deconectează de la internet, dezinstalează
   aplicația, schimbă parolele de pe alt dispozitiv, sună banca și cere verificarea
   contului; nu folosi dispozitivul pentru operațiuni bancare până nu e verificat.
2. Numărul afișat părea al unei firme reale. Cum e posibil? → numărul afișat se
   poate falsifica; ecranul telefonului nu este o dovadă de identitate.
3. Am deschis aplicația bancară în timp ce erau conectați. Ce urmează? → sună
   imediat banca pe numărul de pe card, cere blocarea accesului și verificarea
   tranzacțiilor; păstrează dovezile pentru plângerea la Poliție.

**Linkuri interne:** `dispozitiv-blocat`, `apel-fals-banca-politie`, `/fraude/`
**Linkuri reciproce de adăugat:** din `dispozitiv-blocat` și `voce-ai-telefon`

---

## 4. `/fraude/job-fals-sarcini-platite/`

**Title:** Ofertă de job pe Telegram cu sarcini plătite — e fraudă? | VerificăÎnainte
**Meta description:** Ai primit primele plăți mici, iar acum ți se cere o depunere ca să continui? Vezi cum funcționează capcana și ce riști dacă primești bani în cont pentru altcineva.
**H1:** Ai primit o ofertă de job cu sarcini simple plătite pe Telegram sau WhatsApp?

**Exemplu de mesaj fals:**
> „Felicitări, ați finalizat 3 sarcini și ați primit 87 lei. Pentru a debloca
> sarcinile din nivelul următor, cu plată de 5 ori mai mare, contul dumneavoastră
> trebuie activat cu un depozit de 500 lei. Depozitul se returnează integral odată
> cu primul câștig."

Paragraf de context: recrutarea vine prin mesaj privat, cu promisiunea unui venit
ușor pentru sarcini banale — like-uri, recenzii, „optimizare de produse".

**3 semne:**
1. **Primele sume chiar se plătesc.** Exact asta construiește încrederea și e
   partea care derutează — dacă ai primit bani reali, pare imposibil să fie fraudă.
   Sumele mici sunt investiția lor, nu câștigul tău.
2. Apare cererea unei depuneri proprii ca să „deblochezi" sarcini mai bine plătite.
   Din acel moment banii nu mai pot fi retrași.
3. Varianta mai gravă: ți se cere să primești bani în contul tău și să-i trimiți
   mai departe, contra unui comision.

**Ce faci ACUM:** nu depune nimic și oprește orice transfer / fă captură de ecran a
întregii conversații, inclusiv a plăților primite / dacă ai primit deja bani în
cont pentru altcineva, anunță banca și mergi din proprie inițiativă la Poliție.

**Ce NU faci:** nu depune banii ceruți / nu trimite copie după buletin sau date de
card / nu accepta să primești bani în cont și să-i trimiți mai departe / nu șterge
conversația — este dovadă.

**Ce spune legea (verbatim):**
> Un angajator legitim nu cere niciodată bani de la angajat pentru a-i da de lucru
> — plata circulă într-un singur sens.
>
> Partea gravă apare dacă accepți să primești bani în cont și să-i trimiți mai
> departe. Transferul de bunuri despre care știai că provin din infracțiuni, în
> scopul ascunderii originii lor, se pedepsește cu închisoare de la 3 la 10 ani
> (Art. 49 alin. (1) lit. a) din Legea 129/2019). Legea nu pedepsește pe cine a
> fost înșelat fără nicio urmă de suspiciune — infracțiunea cere cunoașterea
> provenienței banilor. Dar „nu am știut" nu funcționează automat ca scut: Art. 49
> alin. (4) prevede că această cunoaștere se stabilește din circumstanțele faptice
> obiective, adică din cât de vizibile erau semnalele.
>
> În plus, banca are obligația să raporteze tranzacțiile suspecte înainte de a le
> efectua (Art. 6 și Art. 8 din aceeași lege) și nu are voie să îți spună că a
> făcut o raportare (Art. 38 alin. (2)) — de aceea blocarea contului vine fără
> niciun avertisment.

**FAQ:**
1. Am depus deja banii. Îi mai pot recupera? → contactează imediat banca și cere
   retragerea plății; depune plângere la Poliție cu toate dovezile; nu trimite
   niciun ban în plus pentru „deblocarea retragerii" — e aceeași capcană.
2. Am primit bani în cont și i-am trimis mai departe. Ce fac? → oprește orice
   transfer următor, anunță imediat banca, și mergi din proprie inițiativă la
   Poliție cu toate dovezile. A te prezenta singur, cu dovezi, este cea mai bună
   poziție posibilă.
3. Dar chiar am primit bani la început — cum poate fi fraudă? → sumele mici plătite
   real sunt costul lor de recrutare. Testul nu e dacă ai primit ceva, ci dacă ți
   se cere să pui bani ca să continui.

**Linkuri interne:** `investitii-deepfake`, `whatsapp-cont-spart`, `/fraude/`
**Linkuri reciproce de adăugat:** din `investitii-crypto-false` și `whatsapp-cont-spart`

---

## 5. `/fraude/investitii-deepfake/`

> **⚠️ Atenție la suprapunere.** Există deja `/fraude/investitii-crypto-false/`,
> care acoperă tiparul cu apeluri insistente, spoofing și revictimizare prin
> „recuperare de fonduri". Pagina nouă acoperă un canal de intrare DIFERIT:
> reclama video pe rețele sociale, cu chip generat artificial. Cele două nu trebuie
> să repete același conținut, altfel concurează între ele în Google. Diferența se
> menține explicit în H1, în exemplul de mesaj și în primul semn. Cele două pagini
> se leagă reciproc.

**Title:** Reclamă cu o persoană publică ce recomandă investiții — e fraudă? | VerificăÎnainte
**Meta description:** Ai văzut un videoclip în care un guvernator sau un ministru recomandă o platformă de investiții? Vezi de ce un videoclip nu mai este o dovadă.
**H1:** Ai văzut o reclamă video în care o persoană publică recomandă o platformă de investiții?

**Exemplu de mesaj fals:**
> Reclamă sponsorizată pe Facebook sau YouTube: un videoclip în care guvernatorul
> BNR, un ministru sau un prezentator TV cunoscut explică, cu vocea și chipul lui,
> că statul sprijină o nouă platformă de investiții și că primii înscriși primesc
> un capital garantat. Urmează un formular și, în câteva ore, un apel de la un
> „consultant" care te ghidează la prima depunere.

**3 semne:**
1. **Un videoclip nu mai este o dovadă.** Chipul și vocea se pot genera artificial
   (deepfake: material video sau audio fals, creat de calculator, în care o
   persoană reală pare să spună lucruri pe care nu le-a spus niciodată).
2. Nicio persoană publică și nicio instituție a statului nu recomandă platforme
   private de investiții. Nu e o chestiune de etică, e o imposibilitate legală.
3. Primele „câștiguri" apar pe ecran și cresc, dar retragerea se blochează mereu de
   o „taxă" — un impozit, un comision de verificare, o garanție.

**Ce faci ACUM:** nu completa formularul și nu depune nimic / verifică dacă
platforma figurează printre entitățile autorizate de ASF, pe asfromania.ro scris
manual în browser / raportează reclama pe platforma unde ai văzut-o.

**Ce NU faci:** nu depune bani nici măcar „ca test" / nu instala aplicații cerute de
consultant / nu trimite copie după buletin sau selfie cu actul / nu plăti nicio
taxă ca să „deblochezi" o retragere / nu șterge reclama sau conversația — sunt dovezi.

**Ce spune legea (verbatim):**
> Banca Națională a României comunică exclusiv prin Monitorul Oficial, rapoarte și
> comunicate de presă (Art. 56 din Legea 312/2004), iar atribuțiile ei sunt strict
> politica monetară, supravegherea băncilor, emisiunea monetară, regimul valutar și
> rezervele internaționale (Art. 2). Un videoclip în care conducerea BNR recomandă o
> platformă privată de investiții este imposibil, indiferent cât de convingător arată.
>
> Autoritatea de Supraveghere Financiară acordă, suspendă și retrage autorizațiile
> entităților de pe piața de capital (Art. 3 alin. (1) lit. a) din OUG 93/2012). O
> platformă care nu figurează ca autorizată la ASF nu are dreptul legal să atragă
> bani de la public în România. Aceasta este singura verificare care contează —
> nu recenziile, nu videoclipul, nu insistența consultantului.

**FAQ:**
1. Am depus deja bani. Îi mai pot recupera? → contactează imediat banca și cere
   retragerea plății; depune plângere la Poliție cu toate dovezile; nu plăti nicio
   sumă suplimentară pentru „deblocarea retragerii".
2. M-a contactat cineva care spune că îmi recuperează banii pierduți. E real? →
   aproape sigur nu. Recontactarea victimelor este o a doua fraudă, făcută adesea
   de același grup, folosind lista celor care au plătit deja o dată.
3. Cum verific dacă o platformă de investiții e legală în România? → caută-o în
   lista entităților autorizate de ASF, pe asfromania.ro scris manual în browser.
   Dacă nu apare acolo, nu are dreptul să îți ceară bani.

**Linkuri interne:** `investitii-crypto-false`, `job-fals-sarcini-platite`, `/fraude/`
**Linkuri reciproce de adăugat:** din `investitii-crypto-false` (obligatoriu) și `anaf-fals-firme`

---

## 6. `/fraude/escrocherie-sentimentala/`

**Title:** Persoana cunoscută online îți cere bani — e fraudă? | VerificăÎnainte
**Meta description:** Relație online de luni de zile, dar nicio întâlnire reală și acum o urgență financiară? Vezi care este singurul semnal care contează cu adevărat.
**H1:** Persoana pe care ai cunoscut-o online îți cere bani pentru o urgență?

**Exemplu de mesaj fals:**
> „Iubito, nu știu cui altcuiva să-i cer. Coletul cu documentele și inelul a fost
> oprit la vamă și îmi cer 2.400 de euro taxă ca să-l elibereze. Sunt pe platformă,
> nu am acces la bani până luna viitoare. Îți dau înapoi tot, imediat ce ajung.
> Te rog să nu spui nimănui, mi-e rușine că am ajuns să-ți cer asta."

Paragraf de context: relația se construiește săptămâni sau luni, cu comunicare
intensă și afecțiune reală din partea ta. Persoana pare să existe: are fotografii,
o poveste coerentă, un program de lucru. Doar întâlnirea nu se produce niciodată.

**3 semne:**
1. **Combinația care contează: nicio întâlnire reală plus cerere de bani.** Nu cât
   de credibilă e povestea — poveștile sunt construite tocmai ca să fie credibile.
2. Apelul video e mereu amânat, cu o scuză nouă de fiecare dată: conexiune proastă,
   camera stricată, program imposibil, misiune militară, platformă petrolieră.
3. Cererea de discreție: „nu spune nimănui". Izolarea de familie și prieteni e
   parte din metodă, pentru că o a doua opinie ar opri totul.

**Ce faci ACUM:** nu trimite banii / caută fotografiile persoanei în căutarea
inversă de imagini, ca să vezi dacă aparțin altcuiva / spune-i unei persoane
apropiate în care ai încredere, chiar dacă ți-e greu.

**Ce NU faci:** nu trimite bani, carduri cadou sau criptomonede / nu accepta să
primești bani în cont pentru această persoană / nu trimite fotografii intime, care
pot fi folosite ulterior pentru șantaj / nu șterge conversația — este dovadă.

**Ce spune legea (verbatim):**
> Înșelăciunea prin folosirea de calități mincinoase — o identitate inventată, o
> profesie sau o situație care nu există — se pedepsește cu închisoare de la 1 la 5
> ani (Art. 244 Cod Penal). Faptul că ai trimis banii de bunăvoie nu schimbă
> încadrarea: consimțământul obținut prin inducere în eroare nu este un
> consimțământ valabil.
>
> Dacă ți s-a cerut să primești bani în cont și să-i trimiți mai departe, situația
> este mai gravă și intră sub Legea 129/2019 privind spălarea banilor. Oprește orice
> transfer, anunță banca și mergi din proprie inițiativă la Poliție.

**FAQ:**
1. Am trimis deja bani. Ce fac? → contactează banca și cere retragerea plății;
   depune plângere la Poliție cu toate conversațiile și dovezile de transfer.
   Nu trimite alți bani, indiferent ce urgență apare.
2. Dar poate e o persoană reală și chiar are nevoie de ajutor. Cum știu? → cere un
   apel video neanunțat, acum. O persoană reală care te apreciază înțelege
   verificarea. Un refuz repetat, cu scuze noi, este răspunsul.
3. Mi-e rușine să spun cuiva. Chiar trebuie? → da, și e cel mai greu pas.
   Escrocheriile sentimentale funcționează exact pentru că victima nu cere o a doua
   opinie. Rușinea aparține celui care a mințit, nu celui care a avut încredere.

**Linkuri interne:** `whatsapp-cont-spart`, `investitii-deepfake`, `/fraude/`
**Linkuri reciproce de adăugat:** din `whatsapp-cont-spart` și `voce-ai-telefon`

---

## 7. `/fraude/abonament-suspendat-plata-esuata/`

**Title:** SMS că abonamentul Netflix va fi suspendat — e fraudă? | VerificăÎnainte
**Meta description:** Ai primit un SMS că plata pentru Netflix a eșuat și contul va fi suspendat? Vezi de ce mesajul pare credibil chiar dacă ai o problemă reală de plată.
**H1:** Ai primit un SMS că abonamentul va fi suspendat pentru că plata a eșuat?

**Exemplu de mesaj fals:**
> „NETFLIX: Plata a esuat. Accesul dvs. va fi suspendat daca nu va actualizati
> datele aici: [link]"

Paragraf de context: mesajul vine în numele unui serviciu de abonament folosit
zilnic (Netflix, HBO Max, Spotify, YouTube Premium, Disney+), anunță o plată eșuată
și cere actualizarea datelor printr-un link. Poate ajunge și pe email, cu aceeași
structură.

**3 semne:**
1. **Plauzibilitatea este capcana, nu o coincidență.** Plățile eșuate există în
   realitate — card expirat, tranzacție refuzată de bancă. Mesajul nu cere nimic
   neobișnuit; cere un lucru normal, într-un loc greșit. Dacă ai chiar o problemă de
   plată, potrivirea nu confirmă mesajul: cardurile expiră lunar la mii de oameni,
   iar mesajele se trimit în masă.
2. Amenințarea cu suspendarea nu produce suspiciune, produce grabă. Un serviciu real
   nu îți taie accesul printr-un mesaj cu termen scurt.
3. Linkul duce pe o pagină clonă, identică vizual, găzduită pe un domeniu construit
   să semene cu numele brandului prin litere lipsă sau cuvinte adăugate. Diferența e
   de câteva caractere și nu se observă pe ecranul telefonului.

**Ce faci ACUM:** nu deschide linkul / deschide aplicația oficială instalată pe
telefon sau tastează adresa brandului direct în browser / verifică starea
abonamentului acolo / actualizează cardul doar din aplicație sau din contul oficial.

**Ce NU faci:** nu deschide linkul din mesaj / nu introduce datele cardului pe pagina
din link / nu răspunde la mesaj / nu șterge mesajul — este dovadă.

**Ce spune legea (verbatim):**
> Serviciile de abonament sunt companii private, nu instituții publice, deci aici nu
> se aplică regulile de comunicare oficială. Se aplică în schimb un principiu simplu:
> o companie legitimă nu îți cere datele cardului printr-un link primit nesolicitat
> și nu rezolvă o problemă de plată în afara aplicației sau a contului tău. Locul în
> care se actualizează un card este contul, nu un mesaj.
>
> Dacă ai introdus datele cardului, fapta este o infracțiune și poate fi reclamată la
> Poliție. Păstrează mesajul și captura paginii — fără ele, plângerea rămâne fără
> probe. Sună banca și cere blocarea cardului: datele permit plăți recurente, nu doar
> o singură tranzacție.

**FAQ:**
1. Am introdus datele cardului. Ce fac acum? → sună imediat banca și cere blocarea
   cardului; datele complete permit plăți repetate, nu una singură; depune plângere la
   Poliție cu mesajul și captura paginii.
2. Cum verific dacă plata mea a eșuat într-adevăr? → deschizi aplicația oficială sau
   contul de pe site-ul brandului, tastat de tine în browser; dacă există o problemă
   reală, o vezi acolo; dacă aplicația nu spune nimic, mesajul e fals.
3. Cardul meu a expirat chiar luna asta. Nu înseamnă că mesajul e real? → nu.
   Cardurile expiră în fiecare lună la mii de oameni, iar mesajele se trimit în masă.
   Coincidența e motivul pentru care tiparul funcționează, nu o confirmare.
4. Linkul arăta ca adresa oficială. Cum e posibil? → domeniile false sunt construite
   să semene cu numele brandului, prin litere lipsă sau cuvinte adăugate. Diferența e
   de câteva caractere și nu se observă pe ecranul telefonului.

**Linkuri interne de pe pagina asta:** `colet-blocat-curier`, `whatsapp-cont-spart`, `/fraude/`
**Linkuri reciproce de adăugat:** din `colet-blocat-curier` și `whatsapp-cont-spart`
