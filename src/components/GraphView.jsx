import { useRef, useEffect } from "react"
import ForceGraph2D from "react-force-graph-2d"
import { COMPANIES, MENTORS } from "../data/mockData"

export default function GraphView({ matches }) {
  const fgRef = useRef()

  const nodes = [
    ...COMPANIES.map(c => ({ id: c.id, name: c.name, type: "company", sector: c.sector })),
    ...MENTORS.map(m => ({ id: m.id, name: m.name.split(" ").slice(-1)[0], type: "mentor" }))
  ]

  const links = matches.map(m => ({
    source: m.company_id,
    target: m.mentor_id,
    score: m.score
  }))

  useEffect(() => {
    if (fgRef.current) {
      setTimeout(() => fgRef.current.zoomToFit(400), 500)
    }
  }, [matches])

  function nodeColor(node) {
    if (node.type === "mentor") return "#14b8a6"
    const colors = {
      Fintech: "#7c3aed", Agritech: "#16a34a", Healthtech: "#2563eb",
      Logistics: "#ea580c", Edtech: "#db2777", Cleantech: "#0891b2"
    }
    return colors[node.sector] || "#7c3aed"
  }

  function linkColor(link) {
    return link.score >= 0.93 ? "#34d399"
      : link.score >= 0.85 ? "#fbbf24" : "#f87171"
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-xs text-slate-500 uppercase tracking-widest font-medium">
          Living knowledge graph
        </p>
        <div className="flex items-center gap-4 text-xs text-slate-500">
          <span className="flex items-center gap-1.5"><span className="w-3 h-0.5 bg-emerald-400 inline-block rounded"/>≥93%</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-0.5 bg-amber-400 inline-block rounded"/>≥85%</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-0.5 bg-red-400 inline-block rounded"/>below</span>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden" style={{ height: "480px" }}>
        <ForceGraph2D
          ref={fgRef}
          graphData={{ nodes, links }}
          backgroundColor="#0f172a"
          nodeColor={nodeColor}
          nodeLabel={node => `${node.name} (${node.type})`}
          nodeRelSize={6}
          linkColor={linkColor}
          linkWidth={link => link.score * 4}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.005}
          linkDirectionalParticleColor={linkColor}
          cooldownTicks={100}
        />
      </div>

      <div className="flex gap-3 justify-center text-xs text-slate-500">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-purple-600 inline-block"/>Company</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-teal-500 inline-block"/>Mentor</span>
        <span className="text-slate-600">· Drag nodes · Scroll to zoom · Hover to inspect</span>
      </div>
    </div>
  )
}