import { useEffect, useRef } from "react"

export default function AgentLog({ logs, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [logs])

  if (logs.length === 0 && !loading) return null

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2 font-mono text-xs max-h-48 overflow-y-auto">
      <p className="text-slate-500 uppercase tracking-widest text-xs mb-3">Agent log</p>
      {logs.map((log, i) => (
        <div key={i} className="flex gap-3 items-start">
          <span className="text-slate-600 shrink-0">{log.time}</span>
          <span className={i === logs.length - 1 ? "text-emerald-400" : "text-slate-400"}>
            {log.msg}
          </span>
        </div>
      ))}
      {loading && (
        <div className="flex items-center gap-2 pt-1">
          <span className="inline-flex gap-1">
            {[0,1,2].map(i => (
              <span key={i} className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}/>
            ))}
          </span>
          <span className="text-slate-500">Processing...</span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  )
}