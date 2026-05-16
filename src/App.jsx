import { useState } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Toaster } from "react-hot-toast"
import Navbar from "./components/Navbar"
import InputPage from "./pages/InputPage"
import MatchesPage from "./pages/MatchesPage"
import GraphPage from "./pages/GraphPage"
import UploadPage from "./pages/UploadPage"

export default function App() {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [customData, setCustomData] = useState(null)

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-grid relative overflow-x-hidden">
        <div className="orb orb-purple" />
        <div className="orb orb-teal" />
        <div className="relative z-10">
          <Toaster position="top-right" toastOptions={{
            style: {
              background: "rgba(15,23,42,0.9)",
              backdropFilter: "blur(16px)",
              color: "#e2e8f0",
              border: "1px solid rgba(124,58,237,0.3)",
              borderRadius: "12px",
              fontFamily: "'Space Grotesk', sans-serif"
            }
          }}/>
          <Navbar matchCount={matches.length} />
          <Routes>
            <Route path="/" element={
              <InputPage setMatches={setMatches} loading={loading}
                setLoading={setLoading} logs={logs} setLogs={setLogs}
                customData={customData} />
            }/>
            <Route path="/matches" element={<MatchesPage matches={matches} />}/>
            <Route path="/graph" element={<GraphPage matches={matches} />}/>
            <Route path="/upload" element={<UploadPage setCustomData={setCustomData} />}/>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}
