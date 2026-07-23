# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

VerificăÎnainte (verificainainte.ro) is a Romanian-language web app that helps users detect financial
fraud/scam scenarios (phishing, vishing, smishing, impersonated institutions like ANAF/BNR/Poliție,
WhatsApp account compromise, etc.) before they act on them. A user describes a suspicious situation in
free text; the backend sends it to Claude with a detailed system prompt and returns a structured risk
analysis (SCOR: SCĂZUT/MEDIU/RIDICAT/CRITIC + recommended actions + legal basis).

Two independent halves, no shared package/build:
- `frontend/` — React 19 + Vite SPA (single-page form + result view)
- `verificainainte/` — Python FastAPI backend that calls the Anthropic API

The frontend is deployed separately (calls a hardcoded production API URL) and the backend is deployed
to Railway (see `DB_PATH` fallback logic in `main.py`).

## Commands

### Frontend (`frontend/`)
```
npm install       # install deps
npm run dev       # start Vite dev server
npm run build     # production build to dist/
npm run lint      # eslint .
npm run preview   # preview production build
```

### Backend (`verificainainte/`)
```
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
uvicorn main:app --reload         # run dev server (default http://127.0.0.1:8000)
```
Requires a `.env` file in `verificainainte/` with `ANTHROPIC_API_KEY=...`.

There is no test suite or lint config for the backend, and no CI configuration in the repo.

## Architecture

### Backend (`verificainainte/main.py`)
Single-file FastAPI app. Key things to know before editing it:

- **`SYSTEM_PROMPT`** is the entire "brain" of the app — a long Romanian-language prompt encoding: the
  legal basis for why each institution (ANAF, BNR, banks, Poliție, ASF, DNSC) cannot legally contact
  people the way scammers claim to, a catalog of active fraud patterns in Romania, scoring criteria for
  SCĂZUT/MEDIU/RIDICAT/CRITIC, and an exact required response format (with worked examples). When asked
  to change detection behavior, response tone, or scoring, this prompt is almost always the place to
  edit — not application code. Keep edits self-consistent with the existing structure (legal framework →
  fraud patterns → scoring rules → response format → examples) since the model is instructed to follow
  it literally.
- `POST /analyze` — the only real endpoint. Rate-limited to 10 requests/minute per IP via `slowapi`
  (`Limiter`/`get_remote_address`). Calls `client.messages.create` with model `claude-haiku-4-5`,
  `max_tokens=1024`, the system prompt above, and the user's raw text as the single user message.
  Returns `{"rezultat": <model text>}` directly to the frontend — no parsing/validation of the model's
  output shape.
- Every successful `/analyze` call also inserts a row into a `verificari` SQLite table purely as a
  usage counter (no content is stored, just a timestamp). Counting failures are swallowed
  (`except Exception: pass`) so they never break the actual API response.
- `DB_PATH` picks `/data/stats.db` if `/data` exists (Railway volume, persists across redeploys) or
  falls back to a local `stats.db` next to `main.py` (e.g. when testing on Windows).
- `GET /` is a bare health check; `GET /stats` exposes `{"total": ..., "azi": ...}` (today's count) from
  the same table.
- CORS is wide open (`allow_origins=["*"]`) since the frontend is a separately hosted static SPA.
- `check.py` is a standalone throwaway script (direct `anthropic` call with an older/simpler system
  prompt and a hardcoded test scenario) used for prompt experimentation — it is not imported by
  `main.py` and not part of the served app. Don't assume the two system prompts are in sync; `main.py`'s
  is the current/authoritative one.

### Frontend (`frontend/src/App.jsx`)
Single-component app, no router, no state management library:

- Holds `text` (textarea input), `rezultat` (raw markdown string from the backend), `loading`, `eroare`.
- `analizeaza()` POSTs `{ text }` to a **hardcoded production URL**
  (`https://verificainainte-production.up.railway.app/analyze`) — not an env var. If working against a
  local backend, this URL needs to be changed manually (or made configurable) rather than assuming
  `npm run dev` talks to `localhost`.
- `detecteazaScor()` derives the risk banner (color/emoji) by naively checking whether the response text
  *contains* one of the four Romanian score labels (`SCĂZUT`, `MEDIU`, `RIDICAT`, `CRITIC`) — it does not
  parse structured JSON. This means the banner logic is coupled to the backend's `SYSTEM_PROMPT` always
  emitting the literal line `SCOR: <label>`; changing those labels in the backend prompt requires
  updating `SCORURI` in `App.jsx` too.
- The result body itself is rendered with `react-markdown` since the model returns markdown-ish text
  following the prompt's required section format (SCOR / TIPAR DETECTAT / CE FACI ACUM / CE NU FACI /
  TEMEI JURIDIC / VERIFICĂ OFICIAL LA).
- Uses `@vercel/analytics` (`<Analytics />`) for pageview tracking.

## Notes

- All user-facing copy and the model's output are Romanian-only by design (the system prompt explicitly
  instructs the model to respond only in Romanian).
- The backend's legal citations (ANAF/BNR/bank/Poliție/ASF/DNSC articles) are deliberately restricted —
  the prompt tells the model to cite *exclusively* from the laws/articles listed in `SYSTEM_PROMPT` and
  never invent others. If asked to add a new institution or fraud pattern, follow that same pattern:
  give it a legal-basis section (or explicitly note when none applies) and a fraud-pattern entry, don't
  just add scoring logic.

  ## Operational constraints

- Railway is on the FREE plan: $1/month credit, ~$0.80 currently used.
  Memory is 96% of the bill (~77 MB average). Do NOT add background
  workers, schedulers, in-memory caches, or extra uvicorn workers
  without flagging the memory cost first.
- Do NOT implement Anthropic prompt caching. Traffic is ~2 requests/day,
  far below the ~2/hour break-even; caching would increase cost.
- /analyze is public, unauthenticated and calls a paid API. Any change
  that could increase per-call token count or call volume must be
  flagged explicitly. Input length caps and rate limits are cost
  controls, not UX preferences — do not relax them.
- Legal citations in SYSTEM_PROMPT are verified against original
  legislative PDFs. Never edit article numbers or add citations
  without explicit instruction.

## Audience
85% mobile, 53% Android, 85% Romania, 67% arriving from Threads.
Mobile-first is not optional.
