import { useNavigate } from "react-router-dom"
import GraphView from "../components/GraphView"

export default function GraphPage({ matches }) {
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

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Living knowledge graph</h1>
        <p className="text-slate-400 text-sm mt-1">Every programme adds to this graph. Matching gets smarter each cycle.</p>
      </div>

      <GraphView matches={matches} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { title: "Reusable relationships", desc: "Mentor-company pairings stored as graph entities, reused across programmes automatically." },
          { title: "Self-improving matching", desc: "Each cohort's engagement scores feed back into the graph. Next match is always better." },
          { title: "Zero admin overhead", desc: "Admin enters profiles once. Agent handles verification, matching, scheduling, and tracking." }
        ].map(c => (
          <div key={c.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
            <p className="text-sm font-semibold text-purple-300">{c.title}</p>
            <p className="text-xs text-slate-400 leading-relaxed">{c.desc}</p>
          </div>
        ))}
      </div>

      <button onClick={() => navigate("/matches")}
        className="text-sm text-slate-500 hover:text-slate-300 transition-colors">
        ← Back to match cards
      </button>
    </div>
  )
}