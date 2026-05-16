import { useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Upload, FileSpreadsheet, CheckCircle, AlertTriangle, X, ChevronRight } from "lucide-react"
import { parseExcelFile, mapCompanies, mapMentors, mapEngagements } from "../utils/parseExcel"
import { COMPANIES, MENTORS, PAST_ENGAGEMENTS } from "../data/mockData"
import toast from "react-hot-toast"

export default function UploadPage({ setCustomData }) {
  const navigate = useNavigate()
  const fileRef = useRef()
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [parsing, setParsing] = useState(false)
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState("")

  async function handleFile(f) {
    if (!f) return
    const ext = f.name.split(".").pop().toLowerCase()
    if (!["xlsx", "xls", "csv"].includes(ext)) {
      setError("Please upload an Excel (.xlsx, .xls) or CSV file")
      return
    }
    setFile(f)
    setError("")
    setParsing(true)
    try {
      const sheets = await parseExcelFile(f)
      const sheetNames = Object.keys(sheets)
      const companySheet = sheets["companies"] || sheets["company"] ||
        sheets[sheetNames.find(s => s.includes("compan"))] || sheets[sheetNames[0]]
      const mentorSheet = sheets["mentors"] || sheets["mentor"] ||
        sheets[sheetNames.find(s => s.includes("mentor"))] || sheets[sheetNames[1]]
      const engagementSheet = sheets["engagements"] || sheets["past"] ||
        sheets[sheetNames.find(s => s.includes("engag") || s.includes("past"))] || sheets[sheetNames[2]]
      const companies = companySheet ? mapCompanies(companySheet) : COMPANIES
      const mentors = mentorSheet ? mapMentors(mentorSheet) : MENTORS
      const engagements = engagementSheet ? mapEngagements(engagementSheet) : PAST_ENGAGEMENTS
      setPreview({ companies, mentors, engagements, sheetNames })
      setParsing(false)
    } catch (e) {
      setError(e.message)
      setParsing(false)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  function handleConfirm() {
    if (!preview) return
    setCustomData(preview)
    toast.success("Dataset loaded — agent will use your data!")
    navigate("/")
  }

  function handleUseMock() {
    setCustomData(null)
    toast("Using default demo dataset")
    navigate("/")
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-16 space-y-10">

      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }} className="space-y-4">
        <div className="inline-flex items-center gap-2 bg-teal-950/40 border border-teal-800/30 px-4 py-2 rounded-full">
          <FileSpreadsheet size={14} className="text-teal-400" />
          <span className="text-sm text-teal-300 font-medium">Excel / CSV import</span>
        </div>
        <h1 className="font-display text-5xl font-black leading-none tracking-tight">
          <span className="text-white">Upload your</span><br/>
          <span className="text-gradient">ecosystem data</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-xl leading-relaxed">
          Upload your Excel file with company and mentor data.
          The agent matches relationships based on your real data.
        </p>
      </motion.div>

      {/* Format guide */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
        className="glass rounded-2xl p-5 space-y-3">
        <p className="text-sm font-medium text-slate-300">Expected Excel column names</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          {[
            { sheet: "Sheet 1: Companies", color: "text-purple-400",
              cols: ["Company Name", "Sector", "Stage", "Ask 1", "Ask 2", "Ask 3", "Founder"] },
            { sheet: "Sheet 2: Mentors", color: "text-teal-400",
              cols: ["Mentor Name", "Title", "Expertise 1", "Expertise 2", "Sector", "Exit 1"] },
            { sheet: "Sheet 3: Engagements", color: "text-amber-400",
              cols: ["Mentor ID", "Company", "Outcome", "Score"] }
          ].map(s => (
            <div key={s.sheet} className="space-y-2">
              <p className={`font-medium ${s.color}`}>{s.sheet}</p>
              {s.cols.map(c => (
                <div key={c} className="flex items-center gap-2">
                  <span className="w-1 h-1 rounded-full bg-slate-600 shrink-0"/>
                  <span className="text-slate-500 font-mono">{c}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Drop zone */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <div
          onDragOver={e => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileRef.current?.click()}
          className={`relative rounded-2xl border-2 border-dashed p-16 text-center cursor-pointer
            transition-all duration-300
            ${dragging ? "border-purple-500 bg-purple-950/20" : "border-slate-800 hover:border-purple-700 hover:bg-purple-950/10"}`}
        >
          <input ref={fileRef} type="file" accept=".xlsx,.xls,.csv"
            className="hidden" onChange={e => handleFile(e.target.files[0])} />
          <div className="space-y-4">
            <div className={`w-16 h-16 rounded-2xl mx-auto flex items-center justify-center transition-all
              ${dragging ? "bg-purple-700" : "bg-slate-800"}`}>
              <Upload size={28} className={dragging ? "text-white" : "text-slate-400"} />
            </div>
            <div>
              <p className="text-white font-medium text-lg">
                {dragging ? "Drop to upload" : "Drop your Excel file here"}
              </p>
              <p className="text-slate-500 text-sm mt-1">or click to browse · .xlsx .xls .csv</p>
            </div>
            {parsing && (
              <div className="inline-flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-full">
                <span className="flex gap-1">
                  {[0,1,2].map(i => (
                    <span key={i} className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce"
                      style={{ animationDelay: `${i*0.15}s` }}/>
                  ))}
                </span>
                <span className="text-sm text-slate-400">Parsing file...</span>
              </div>
            )}
          </div>
        </div>
      </motion.div>

      {error && (
        <div className="flex items-start gap-3 bg-red-950/40 border border-red-800/40 rounded-2xl p-4">
          <AlertTriangle size={16} className="text-red-400 shrink-0 mt-0.5" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      <AnimatePresence>
        {preview && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }} className="space-y-6">
            <div className="flex items-center gap-3 bg-emerald-950/40 border border-emerald-800/40 rounded-2xl p-4">
              <CheckCircle size={20} className="text-emerald-400 shrink-0" />
              <div>
                <p className="text-sm font-medium text-emerald-300">File parsed successfully</p>
                <p className="text-xs text-emerald-600 mt-0.5">
                  {preview.companies.length} companies · {preview.mentors.length} mentors · {preview.engagements.length} engagements
                </p>
              </div>
              <button onClick={() => { setPreview(null); setFile(null) }}
                className="ml-auto text-slate-500 hover:text-slate-300 transition-colors">
                <X size={16} />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="glass rounded-2xl p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <p className="text-xs text-slate-500 uppercase tracking-widest">Companies</p>
                  <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800/40 px-2 py-0.5 rounded-full">
                    {preview.companies.length}
                  </span>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {preview.companies.map((c, i) => (
                    <div key={i} className="flex items-center justify-between py-1 border-b border-slate-800/60">
                      <div>
                        <p className="text-sm text-slate-200 font-medium">{c.name}</p>
                        <p className="text-xs text-slate-500">{c.stage} · {c.asks.length} asks</p>
                      </div>
                      <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full">{c.sector}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="glass rounded-2xl p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <p className="text-xs text-slate-500 uppercase tracking-widest">Mentors</p>
                  <span className="text-xs bg-teal-950 text-teal-300 border border-teal-800/40 px-2 py-0.5 rounded-full">
                    {preview.mentors.length}
                  </span>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {preview.mentors.map((m, i) => (
                    <div key={i} className="flex items-start gap-3 py-1 border-b border-slate-800/60">
                      <div className="w-6 h-6 rounded-lg bg-teal-950 border border-teal-800/30 flex items-center justify-center shrink-0">
                        <span className="text-xs text-teal-400 font-bold">{m.name[0]}</span>
                      </div>
                      <div>
                        <p className="text-sm text-slate-200 font-medium">{m.name}</p>
                        <p className="text-xs text-slate-500">{m.expertise.slice(0,2).join(", ")}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <button onClick={handleConfirm}
              className="w-full py-5 rounded-2xl font-display text-lg font-bold tracking-wide
                transition-all duration-300 flex items-center justify-center gap-3 text-white"
              style={{
                background: "linear-gradient(135deg, #0d9488, #0f766e)",
                boxShadow: "0 0 40px rgba(20,184,166,0.3)"
              }}>
              <CheckCircle size={20} />
              Use this data for matching
              <ChevronRight size={20} />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex items-center gap-4">
        <div className="flex-1 h-px bg-slate-800"/>
        <span className="text-xs text-slate-600">or</span>
        <div className="flex-1 h-px bg-slate-800"/>
      </div>

      <button onClick={handleUseMock}
        className="w-full py-4 rounded-2xl font-medium text-sm text-slate-400
          hover:text-slate-200 transition-all border border-slate-800 hover:border-slate-600">
        Use demo dataset instead
      </button>
    </div>
  )
}