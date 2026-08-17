# docs/

Specificațiile care guvernează output-ul proiectului. Sunt versionate aici pentru
istoric și recuperare, dar sunt folosite prin încărcare în project knowledge în
Claude (proiectul VerificăÎnainte).

## Regula de sincronizare

Repo-ul este sursa de adevăr. Orice modificare se face aici, se comite, apoi
fișierul modificat se reîncarcă în project knowledge, înlocuind versiunea veche.
Niciodată invers: nu se editează direct în project knowledge, pentru că acea copie
nu are istoric și nu se poate recupera.

## Fișiere

- `FORMAT-POSTARI.md` — structura conținutului de social media: principii, format
  per platformă, paleta și structura graficelor, checklist înainte de postare.
- `SEO-SPEC.md` — decizia de arhitectură pentru paginile statice de tipar și
  template-ul de 13 secțiuni. Rămâne referința de bază pentru markup.
- `SEO-SPEC-V2.md` — extinderea cu 6 pagini noi. Depinde de `SEO-SPEC.md` pentru
  template și arhitectură; cele două nu se consolidează într-un fișier unic, pentru
  că ambele conțin texte legale verbatim care nu suportă rescriere.

## De adăugat

- `LOGGING-SPEC.md` — specificația logării cererilor de verificare
