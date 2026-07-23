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

function App() {
  const [text, setText] = useState("")
  const [rezultat, setRezultat] = useState(null)
  const [loading, setLoading] = useState(false)
  const [eroare, setEroare] = useState(null)

  const analizeaza = async () => {
    if (!text.trim()) return

    setLoading(true)
    setRezultat(null)
    setEroare(null)

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

  const scor = rezultat ? detecteazaScor(rezultat) : null
  const stilScor = scor ? SCORURI[scor] : null

  return (
    <div className="container">
      <Analytics />

      {/* Header */}
      <div className="header">
        <h1
          onClick={() => { setText(""); setRezultat(null); setEroare(null); }}
          style={{ cursor: "pointer" }}
        >
          🛡️ VerificăÎnainte
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
      </div>

      {/* Eroare */}
      {eroare && (
        <div className="eroare">
          ⚠️ {eroare}
        </div>
      )}

      {/* Rezultat */}
      {rezultat && (
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
            <ReactMarkdown>{rezultat}</ReactMarkdown>
          </div>
          <p className="disclaimer">
            ⚠️ Analiză generată automat, orientativă — nu e consultanță juridică.
            Verifică mereu la sursele oficiale de mai sus înainte să acționezi.
          </p>
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