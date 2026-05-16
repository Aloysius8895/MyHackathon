import { useNavigate } from "react-router-dom"
import MatchCard from "../components/MatchCard"

export default function MatchesPage({ matches }) {
  const navigate = useNavigate()

  if (matches.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <p className="text-slate-500 text-sm">No matches yet. Run the agent first.</p>
        <button onClick={() => navigate("/")}
          className="text-purple-400 hover:text-purple-300 text-sm transition-colors">
          ← Back to input
        </button>
      </div>
    )
  }

  const avg = Math.round(matches.reduce((a, m) => a + m.score, 0) / matches.length * 100)

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Agent match results</h1>
          <p className="text-slate-400 text-sm mt-1">{matches.length} pairings · all based on knowledge graph history</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-2xl font-bold text-emerald-400 font-mono">{avg}%</div>
            <div className="text-xs text-slate-500">avg match</div>
          </div>
          <button onClick={() => navigate("/graph")}
            className="px-4 py-2 border border-slate-700 hover:border-purple-600
              text-slate-300 hover:text-purple-300 rounded-xl text-sm font-medium transition-all">
            View graph →
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {matches.map((match, i) => (
          <MatchCard key={match.company_id} match={match} index={i} />
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
        <p className="text-sm font-medium text-slate-300">Cohort predicted outcomes</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Companies matched", value: matches.length },
            { label: "Avg match score", value: `${avg}%` },
            { label: "Graph records used", value: 6 },
            { label: "Est. funding milestones", value: "5 co." }
          ].map(s => (
            <div key={s.label} className="bg-slate-800 rounded-xl p-3 text-center">
              <div className="text-2xl font-bold text-white font-mono">{s.value}</div>
              <div className="text-xs text-slate-500 mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}