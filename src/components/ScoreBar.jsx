import { useEffect, useState } from "react"

export default function ScoreBar({ score, animate = true }) {
  const [animatedWidth, setAnimatedWidth] = useState(() => (animate ? 0 : score * 100))

  useEffect(() => {
    if (!animate) return
    const t = setTimeout(() => setAnimatedWidth(score * 100), 300)
    return () => clearTimeout(t)
  }, [animate, score])

  const width = animate ? animatedWidth : score * 100

  const color =
    score >= 0.93 ? "bg-emerald-400"
    : score >= 0.85 ? "bg-amber-400"
    : "bg-red-400"

  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-500">
        <span>Match strength</span>
        <span className="font-mono text-slate-300">{Math.round(score * 100)}%</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full transition-all duration-1000 ease-out`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  )
}
