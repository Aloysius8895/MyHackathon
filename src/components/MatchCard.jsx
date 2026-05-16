import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { AlertTriangle, Unlock } from "lucide-react"
import ScoreBar from "./ScoreBar"
import { PAST_ENGAGEMENTS, SECTOR_COLORS } from "../data/mockData"

export default function MatchCard({ match, index }) {
  const [visible, setVisible] = useState(false)
  const past = PAST_ENGAGEMENTS.find(p => p.mentor_id === match.mentor_id)
  const sectorStyle = SECTOR_COLORS[match.sector] || { bg: "bg-slate-800", text: "text-slate-300" }

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), index * 120)
    return () => clearTimeout(t)
  }, [index])

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4
        hover:border-purple-700 hover:shadow-xl hover:shadow-purple-950/30 transition-all"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${sectorStyle.bg} ${sectorStyle.text}`}>
              {match.sector}
            </span>
            <span className="text-xs text-slate-500 border border-slate-700 px-2 py-0.5 rounded-full">
              {match.stage}
            </span>
          </div>
          <h3 className="font-semibold text-white text-base leading-tight">{match.company}</h3>
          <p className="text-sm text-purple-400 font-medium">{match.mentor}</p>
          <p className="text-xs text-slate-500">{match.mentor_title}</p>
        </div>
        <div className="text-right shrink-0">
          <div className="text-3xl font-bold text-emerald-400 font-mono leading-none">
            {Math.round(match.score * 100)}
            <span className="text-lg text-emerald-600">%</span>
          </div>
          <div className="text-xs text-slate-500 mt-0.5">match score</div>
        </div>
      </div>

      <ScoreBar score={match.score} animate={visible} />

      <div className="bg-slate-800/60 rounded-xl p-4 border-l-2 border-purple-600">
        <p className="text-sm text-slate-300 leading-relaxed">{match.reasoning}</p>
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        <span className="flex items-center gap-1 text-xs text-slate-500">
          <Unlock size={11}/> Key unlock:
        </span>
        <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-3 py-1 rounded-full font-medium">
          {match.key_unlock}
        </span>
      </div>

      {past && (
        <div className="border-t border-slate-800 pt-3">
          <p className="text-xs text-slate-500">
            <span className="text-slate-400 font-medium">Graph memory:</span>{" "}
            Similar to <span className="text-purple-400">{past.company}</span> pairing
            ({Math.round(past.score * 100)}%) — {past.outcome}
          </p>
        </div>
      )}

      {match.risk && (
        <div className="flex items-start gap-2 bg-amber-950/60 border border-amber-900/60 rounded-xl p-3">
          <AlertTriangle size={14} className="text-amber-400 shrink-0 mt-0.5" />
          <p className="text-xs text-amber-300">{match.risk}</p>
        </div>
      )}
    </motion.div>
  )
}