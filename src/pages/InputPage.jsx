import { useNavigate } from "react-router-dom"
import toast from "react-hot-toast"
import { motion } from "framer-motion"
import { COMPANIES, MENTORS, PAST_ENGAGEMENTS, SECTOR_COLORS } from "../data/mockData"
import { runAgent } from "../api/agent"
import AgentLog from "../components/AgentLog"
import { useLang } from "../context/LanguageContext"

export default function InputPage({ setMatches, loading, setLoading, logs, setLogs, customData }) {
  const navigate = useNavigate()
  const { t } = useLang()

  function addLog(msg) {
    setLogs(prev => [...prev, { msg, time: new Date().toLocaleTimeString() }])
  }

  async function handleRun() {
    setLoading(true)
    setLogs([])
    setMatches([])
    try {
      const results = await runAgent(addLog, customData)
      setMatches(results)
      toast.success(t("toast_pairings", results.length))
      navigate("/matches")
    } catch (e) {
      addLog("Error: " + e.message)
      toast.error(t("toast_agent_failed"))
    }
    setLoading(false)
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-16 space-y-16">

      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }} className="space-y-6">
        <div className="inline-flex items-center gap-2 bg-purple-950/40 border border-purple-800/30 px-4 py-2 rounded-full">
          <span className="w-2 h-2 rounded-full bg-purple-400 pulse-dot"/>
          <span className="text-sm text-purple-300 font-medium">{t("badge_agentic")}</span>
        </div>
        <h1 className="font-display text-6xl font-black leading-none tracking-tight">
          <span className="text-white">{t("hero_title_1")}</span><br/>
          <span className="text-gradient">{t("hero_title_2")}</span>
        </h1>
        <p className="text-slate-400 text-xl max-w-xl leading-relaxed">
          {t("hero_desc")}
        </p>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="grid grid-cols-3 gap-6">
        {[
          { value: COMPANIES.length, label: t("stat_companies"), color: "text-purple-400" },
          { value: MENTORS.length, label: t("stat_mentors"), color: "text-teal-400" },
          { value: PAST_ENGAGEMENTS.length, label: t("stat_graph"), color: "text-amber-400" }
        ].map((s, i) => (
          <div key={i} className="glass rounded-2xl p-6 text-center">
            <div className={`stat-number ${s.color}`}>{s.value}</div>
            <div className="text-slate-500 text-sm mt-2">{s.label}</div>
          </div>
        ))}
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4">

        <div className="glass rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500 uppercase tracking-widest font-medium">{t("label_companies")}</p>
            <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800/40 px-2 py-0.5 rounded-full">{COMPANIES.length}</span>
          </div>
          {COMPANIES.map(c => {
            const sc = SECTOR_COLORS[c.sector] || { bg: "bg-slate-800", text: "text-slate-300" }
            return (
              <div key={c.id} className="flex items-center justify-between gap-2">
                <div>
                  <p className="text-sm text-slate-200 font-medium">{c.name}</p>
                  <p className="text-xs text-slate-600">{c.stage}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full shrink-0 ${sc.bg} ${sc.text}`}>{c.sector}</span>
              </div>
            )
          })}
        </div>

        <div className="glass rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500 uppercase tracking-widest font-medium">{t("label_mentors")}</p>
            <span className="text-xs bg-teal-950 text-teal-300 border border-teal-800/40 px-2 py-0.5 rounded-full">{MENTORS.length}</span>
          </div>
          {MENTORS.map(m => (
            <div key={m.id} className="flex items-start gap-3">
              <div className="w-7 h-7 rounded-lg bg-teal-950 border border-teal-800/30 flex items-center justify-center shrink-0 mt-0.5">
                <span className="text-xs text-teal-400 font-bold">{m.name[0]}</span>
              </div>
              <div>
                <p className="text-sm text-slate-200 font-medium leading-tight">{m.name}</p>
                <p className="text-xs text-slate-500">{m.expertise[0]}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="glass rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500 uppercase tracking-widest font-medium">{t("label_graph_memory")}</p>
            <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800/40 px-2 py-0.5 rounded-full">{t("label_past", PAST_ENGAGEMENTS.length)}</span>
          </div>
          {PAST_ENGAGEMENTS.map((p, i) => (
            <div key={i} className="flex items-start justify-between gap-2">
              <div>
                <p className="text-xs text-slate-300 font-medium">{p.company}</p>
                <p className="text-xs text-slate-600 leading-tight mt-0.5">{p.outcome}</p>
              </div>
              <span className="text-xs font-mono text-emerald-400 shrink-0">{Math.round(p.score * 100)}%</span>
            </div>
          ))}
        </div>
      </motion.div>

      <AgentLog logs={logs} loading={loading} />

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }} className="space-y-4">
        <button onClick={handleRun} disabled={loading}
          className="w-full py-5 rounded-2xl font-display text-lg font-bold tracking-wide
            transition-all duration-300 relative overflow-hidden group
            disabled:opacity-50 disabled:cursor-not-allowed"
          style={{
            background: loading ? "rgba(109,40,217,0.3)" : "linear-gradient(135deg, #7c3aed, #6d28d9)",
            boxShadow: loading ? "none" : "0 0 40px rgba(124,58,237,0.4), inset 0 1px 0 rgba(255,255,255,0.1)"
          }}>
          <span className="relative z-10">
            {loading ? t("btn_running") : t("btn_run")}
          </span>
          {!loading && (
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-violet-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"/>
          )}
        </button>
        <p className="text-center text-xs text-slate-700">
          {t("run_note")}
        </p>
      </motion.div>
    </div>
  )
}
