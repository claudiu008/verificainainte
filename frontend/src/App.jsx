import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { Analytics, track } from '@vercel/analytics/react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || "https://verificainainte-production.up.railway.app"

const SCORURI = {
  'SCĂZUT': { culoare: '#2e7d32', fundal: '#f1f8e9', emoji: '🟢' },
  'MEDIU': { culoare: '#f57c00', fundal: '#fff8e1', emoji: '🟡' },
  'RIDICAT': { culoare: '#c62828', fundal: '#fff3e0', emoji: '🟠' },
  'CRITIC': { culoare: '#b71c1c', fundal: '#ffebee', emoji: '🔴' },
}

function detecteazaScor(text) {
  for (const scor of Object.keys(SCORURI)) {
    if (text.includes(scor)) return scor
  }
  return null
}

const EXEMPLU_SMS = "Ministerul Transporturilor: Aveti o amenda de circulatie neplatita de 145 RON. Pentru a evita majorarea cu 100% si transferul la executare silita, achitati in maxim 24h pe ghiseul-ro-plati.com. Introduceti numarul cardului si codul CVV pentru confirmare."

const EXEMPLU_REZULTAT = `STOP

SCOR: CRITIC

TIPAR DETECTAT: Amendă falsă de circulație prin SMS (link-clonă „Ghișeul.ro", cerere date card)

CE FACI ACUM: Fă o captură de ecran a SMS-ului acum. Nu accesa linkul din mesaj. Nu introduce nicio dată pe pagina la care ajungi din el.

CE NU FACI: Nu accesa linkul. Nu introduce numărul cardului, data expirării sau codul CVV. Nu suna niciun număr din SMS. Nu șterge mesajul — e dovadă.

TEMEI JURIDIC: Amenzile de circulație se comunică exclusiv prin poștă cu aviz de primire sau prin afișare la domiciliu, niciodată prin SMS sau link (Art. 27 alin. (1) OG 2/2001) — mesajul e imposibil legal.

VERIFICĂ OFICIAL LA: politiaromana.ro`

function App() {
  const [text, setText] = useState("")
  const [rezultat, setRezultat] = useState(null)
  const [loading, setLoading] = useState(false)
  const [eroare, setEroare] = useState(null)
  const [exemplu, setExemplu] = useState(false)

  const arataExemplu = () => {
    setExemplu(true)
    setRezultat(null)
    setEroare(null)
  }

  const ascundeExemplu = () => {
    setExemplu(false)
  }

  const analizeaza = async () => {
    if (!text.trim()) return

    setLoading(true)
    setRezultat(null)
    setEroare(null)
    setExemplu(false)

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      })

      const data = await response.json()

      if (!response.ok) {
        setEroare(data.detail || "A apărut o eroare. Încearcă din nou.")
        return
      }

      setRezultat(data.rezultat)
      track('verification_submitted')

    } catch {
      setEroare("Nu am putut contacta serverul. Verifică conexiunea la internet și încearcă din nou.")
    } finally {
      setLoading(false)
    }
  }

  const continutAfisat = exemplu ? EXEMPLU_REZULTAT : rezultat
  const scor = continutAfisat ? detecteazaScor(continutAfisat) : null
  const stilScor = scor ? SCORURI[scor] : null

  return (
    <div className="container">
      <Analytics />

      {/* Header */}
      <div className="header">
        <h1
          onClick={() => { setText(""); setRezultat(null); setEroare(null); setExemplu(false); }}
          style={{ cursor: "pointer" }}
        >
          <span className="shield-icon">🛡️</span> VerificăÎnainte
        </h1>
        <p>Ai fost sunat, ai primit un SMS, email sau mesaj pe WhatsApp de la Bancă, ANAF, Poliție sau o platformă de investiții?</p>
        <p className="stop-text">STOP. Nu face transferul încă.</p>
      </div>

      {/* Input */}
      <div className="input-section">
        <label className="label">
          Descrie situația în câteva propoziții:
        </label>
        <textarea
          className="textarea"
          placeholder="Ex: Am primit un SMS de la Bancă cu un link, m-a sunat cineva de la ANAF, am primit un email cu solicitare de actualizare date bancare..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
        />
        <button
          className="buton"
          onClick={analizeaza}
          disabled={loading || !text.trim()}
        >
          {loading ? (
            <span className="loading">
              <span className="spinner" /> Analizez situația...
            </span>
          ) : (
            "Verifică situația →"
          )}
        </button>
        <button
          className="buton-secundar"
          onClick={arataExemplu}
          disabled={loading}
        >
          🔎 Vezi un exemplu
        </button>
      </div>

      {/* Eroare */}
      {eroare && (
        <div className="eroare">
          ⚠️ {eroare}
        </div>
      )}

      {/* Exemplu — mesaj de intrare afișat deasupra rezultatului, doar în modul exemplu */}
      {exemplu && (
        <div className="exemplu-sms">
          <span className="exemplu-eticheta">EXEMPLU · SMS primit</span>
          <p>{EXEMPLU_SMS}</p>
        </div>
      )}

      {/* Rezultat */}
      {continutAfisat && (
        <div className="rezultat">

          {/* Banner scor — doar dacă există */}
          {stilScor && (
            <div
              className="scor-banner"
              style={{
                backgroundColor: stilScor.fundal,
                borderColor: stilScor.culoare,
                color: stilScor.culoare
              }}
            >
              <span className="scor-emoji">{stilScor.emoji}</span>
              <span className="scor-text">RISC {scor}</span>
            </div>
          )}

          {/* Conținut markdown — apare întotdeauna */}
          <div className="continut">
            <ReactMarkdown>{continutAfisat}</ReactMarkdown>
          </div>
          <p className="disclaimer">
            ⚠️ Analiză generată automat, orientativă — nu e consultanță juridică.
            Verifică mereu la sursele oficiale de mai sus înainte să acționezi.
          </p>
          {exemplu && (
            <button className="buton-inchide-exemplu" onClick={ascundeExemplu}>
              ✕ Ascunde exemplul
            </button>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="footer">
        <p>
          VerificăÎnainte oferă informații orientative, generate automat, nu consultanță
          juridică. Pentru situații serioase, verifică independent la sursele oficiale
          sau consultă un avocat/autoritatea competentă.
        </p>
        <p>Ai întrebări? Scrie-ne la <a href="mailto:contact@verificainainte.ro">contact@verificainainte.ro</a></p>
      </div>

    </div>
  )
}

export default App