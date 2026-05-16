import { useState, useMemo, useEffect } from "react"
import { motion } from "framer-motion"
import { HISTORY_SESSIONS, HISTORY_STATS } from "../data/historyData"
import { useLang } from "../context/LanguageContext"
import { loadHistorySessions } from "../api/history"

const FILTERS = ["all", "ai", "manual", "high_rating", "reengage"]

function normalizedKey(value) {
  return String(value ?? "").trim().toLowerCase()
}

function firstValue(...values) {
  return values.find(value => value !== undefined && value !== null && String(value).trim() !== "") ?? ""
}

function scoreToRating(score) {
  const numeric = Number.parseFloat(score)
  if (!Number.isFinite(numeric)) return 0
  const rating = numeric <= 1 ? numeric * 5 : numeric <= 5 ? numeric : numeric / 20
  return Number.parseFloat(Math.max(0, Math.min(5, rating)).toFixed(1))
}

function isReEngage(value, score) {
  const text = String(value ?? "").trim().toLowerCase()
  if (["yes", "y", "true", "recommended"].includes(text)) return true
  if (["no", "n", "false"].includes(text)) return false
  return (Number.parseFloat(score) || 0) >= 0.75
}

function normalizeMatchType(value) {
  const text = String(value ?? "").trim().toLowerCase()
  if (text.includes("ai") || text.includes("gemini")) return "ai"
  return "manual"
}

function mapUploadToSessions(data) {
  const engagements = data?.engagements ?? []
  const mentors = data?.mentors ?? []
  const mentorById = Object.fromEntries(
    mentors.flatMap(m => [m.id, m.source_id, m.history_id].filter(Boolean).map(id => [normalizedKey(id), m]))
  )
  const mentorByName = Object.fromEntries(
    mentors.flatMap(m => [m.name, m.mentor_name, m.lecturer].filter(Boolean).map(name => [normalizedKey(name), m]))
  )

  return engagements.map((eng, i) => {
    const uploadedMentorName = firstValue(eng.mentor_name, eng.mentorName, eng.lecturer, eng.mentor)
    const mentor = mentorById[normalizedKey(eng.mentor_id)] || mentorByName[normalizedKey(uploadedMentorName)]
    const mentorName = firstValue(uploadedMentorName, mentor?.name, eng.mentor_id, "Unknown mentor")
    const companyName = firstValue(eng.company_name, eng.companyName, eng.company, eng.startup, eng.startup_name)
    const rawScore = Number.parseFloat(eng.score) || 0
    const rating = scoreToRating(eng.score)
    return {
      id: firstValue(eng.session_id, eng.sessionId, eng.id, `SES-U${String(i + 1).padStart(3, "0")}`),
      lecturer: mentorName,
      mentorName,
      date: firstValue(eng.date, eng.session_date, data?.uploadedAt, "Uploaded data"),
      programme: firstValue(eng.programme, eng.program, "Uploaded Dataset"),
      pax: firstValue(eng.pax, eng.participants, eng.attendees) || null,
      hours: firstValue(eng.hours, eng.duration) || null,
      topic: eng.outcome || "—",
      rating,
      quote: eng.company ? `Mentored ${eng.company}` : "—",
      reEngage: rawScore >= 0.75,
      matchType: "manual",
      ...{
        topic: firstValue(eng.outcome, eng.topic, eng.result, "-"),
        quote: firstValue(eng.feedback, eng.comment, companyName ? `Mentored ${companyName}` : "-"),
        reEngage: isReEngage(eng.reengage ?? eng.reEngage, rawScore),
        matchType: normalizeMatchType(eng.match_type ?? eng.matchType),
      },
    }
  })
}

function deriveStats(sessions) {
  if (!sessions.length) return { totalSessions: 0, avgRating: 0, aiMatched: 0, reEngageRate: 0 }
  const avg = sessions.reduce((s, x) => s + x.rating, 0) / sessions.length
  return {
    totalSessions: sessions.length,
    avgRating: parseFloat(avg.toFixed(1)),
    aiMatched: sessions.filter(s => s.matchType === "ai").length,
    reEngageRate: Math.round((sessions.filter(s => s.reEngage).length / sessions.length) * 100),
  }
}

function StatCard({ label, value, sub, valueColor }) {
  return (
    <div className="rounded-2xl border border-slate-800/60 bg-[#161b27] p-5 space-y-1">
      <p className="text-xs text-slate-500 font-medium">{label}</p>
      <p className={`text-4xl font-black font-mono tracking-tight ${valueColor}`}>{value}</p>
      <p className="text-xs text-slate-600">{sub}</p>
    </div>
  )
}

function MatchBadge({ type, t }) {
  return type === "ai" ? (
    <span className="rounded-full bg-cyan-950/60 border border-cyan-500/30 px-3 py-1 text-xs font-semibold text-cyan-400">
      {t("hist_filter_ai")}
    </span>
  ) : (
    <span className="rounded-full bg-slate-800/60 border border-slate-600/30 px-3 py-1 text-xs font-semibold text-slate-400">
      {t("hist_filter_manual")}
    </span>
  )
}

function SessionCard({ session, index, showName, t }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.06 }}
      className="rounded-2xl border border-slate-800/50 bg-[#161b27] p-5 space-y-3"
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1.5">
          <p className="text-base font-bold text-white leading-tight">{session.lecturer}</p>
          {showName && session.mentorName && session.mentorName !== session.lecturer && (
            <span className="inline-flex items-center gap-1.5 rounded-full bg-teal-950/60 border border-teal-500/30 px-2.5 py-0.5 text-xs font-semibold text-teal-300">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-400" />
              {session.mentorName}
            </span>
          )}
          <p className="text-xs text-slate-500">{session.id} · {session.date}</p>
        </div>
        <MatchBadge type={session.matchType} t={t} />
      </div>

      {/* Meta row */}
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-purple-500/60" />
          {session.programme}
        </span>
        {session.pax != null && (
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600" />
            {t("hist_pax", session.pax)}
          </span>
        )}
        {session.hours != null && (
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600" />
            {t("hist_hrs", session.hours)}
          </span>
        )}
      </div>

      {/* Topic */}
      <div className="rounded-xl border border-slate-700/40 bg-slate-900/50 px-4 py-2.5">
        <p className="text-sm text-slate-300">{session.topic}</p>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between gap-3">
        <div className="space-y-1">
          <span className="flex items-center gap-1 text-sm font-semibold text-amber-400">
            <span>★</span>
            <span>{session.rating.toFixed(1)}</span>
            <span className="text-slate-600 font-normal">/ 5.0</span>
          </span>
          <p className="text-xs text-slate-500 italic">"{session.quote}"</p>
        </div>
        {session.reEngage && (
          <span className="shrink-0 rounded-full border border-violet-500/30 bg-violet-950/40 px-3 py-1 text-xs font-semibold text-violet-300">
            {t("hist_reengage_badge")}
          </span>
        )}
      </div>
    </motion.div>
  )
}

export default function HistoryPage({ customData }) {
  const { t } = useLang()
  const [search, setSearch] = useState("")
  const [activeFilter, setActiveFilter] = useState("all")
  const [savedData, setSavedData] = useState(undefined) // undefined = still loading

  useEffect(() => {
    loadHistorySessions().then(data => setSavedData(data ?? null))
  }, [])

  // Priority: savedData (from DB) > customData (current session upload) > default
  const uploadedData = savedData ?? customData ?? null
  const isUploaded = Boolean(uploadedData?.engagements?.length)

  const sessions = useMemo(
    () => isUploaded ? mapUploadToSessions(uploadedData) : HISTORY_SESSIONS,
    [uploadedData, isUploaded]
  )

  const stats = useMemo(
    () => isUploaded ? deriveStats(sessions) : HISTORY_STATS,
    [isUploaded, sessions]
  )

  const filterLabels = {
    all: t("hist_filter_all"),
    ai: t("hist_filter_ai"),
    manual: t("hist_filter_manual"),
    high_rating: t("hist_filter_rating"),
    reengage: t("hist_filter_reengage"),
  }

  const filtered = useMemo(() => {
    let list = sessions
    if (search.trim()) {
      const q = search.toLowerCase()
      list = list.filter(s =>
        s.lecturer.toLowerCase().includes(q) ||
        s.mentorName.toLowerCase().includes(q) ||
        s.topic.toLowerCase().includes(q) ||
        s.programme.toLowerCase().includes(q) ||
        s.quote.toLowerCase().includes(q)
      )
    }
    if (activeFilter === "ai") list = list.filter(s => s.matchType === "ai")
    if (activeFilter === "manual") list = list.filter(s => s.matchType === "manual")
    if (activeFilter === "high_rating") list = list.filter(s => s.rating >= 4.7)
    if (activeFilter === "reengage") list = list.filter(s => s.reEngage)
    return list
  }, [sessions, search, activeFilter])

  if (savedData === undefined) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 flex justify-center">
        <span className="text-slate-500 text-sm animate-pulse">Loading history...</span>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">

      {/* Title */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">{t("history_title")}</h1>
          <p className="text-slate-400 text-sm mt-1">{t("history_subtitle")}</p>
        </div>
        {isUploaded && (
          <span className="shrink-0 rounded-full border border-teal-500/40 bg-teal-950/40 px-3 py-1.5 text-xs font-semibold text-teal-300">
            {sessions.length} uploaded
          </span>
        )}
      </div>

      {/* Stats 2×2 */}
      <div className="grid grid-cols-2 gap-4">
        <StatCard label={t("hist_total")} value={stats.totalSessions}
          sub={isUploaded ? "Uploaded dataset" : t("hist_total_since")} valueColor="text-cyan-400" />
        <StatCard label={t("hist_avg_rating")} value={stats.avgRating.toFixed(1)}
          sub={t("hist_avg_out")} valueColor="text-violet-400" />
        <StatCard label={t("hist_ai_matched")} value={stats.aiMatched}
          sub={isUploaded ? "From your data" : t("hist_ai_from")} valueColor="text-pink-400" />
        <StatCard label={t("hist_reengage")} value={`${stats.reEngageRate}%`}
          sub={t("hist_reengage_label")} valueColor="text-amber-400" />
      </div>

      {/* Search */}
      <input
        type="text"
        value={search}
        onChange={e => setSearch(e.target.value)}
        placeholder={t("hist_search_placeholder")}
        className="w-full rounded-2xl border border-slate-700/50 bg-white/95 px-5 py-3.5 text-slate-900
          placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/50"
      />

      {/* Filter chips */}
      <div className="flex flex-wrap gap-2">
        {FILTERS.map(f => (
          <button
            key={f}
            onClick={() => setActiveFilter(f)}
            className={`rounded-full border px-4 py-1.5 text-sm font-medium transition-colors ${
              activeFilter === f
                ? "border-cyan-500 bg-cyan-950/60 text-cyan-300"
                : "border-slate-700 bg-transparent text-slate-400 hover:border-slate-500 hover:text-slate-300"
            }`}
          >
            {filterLabels[f]}
          </button>
        ))}
      </div>

      {/* Session list */}
      <div className="space-y-3">
        <p className="text-xs font-semibold tracking-widest text-slate-500">{t("hist_recent")}</p>
        {filtered.length === 0 ? (
          <p className="text-slate-500 text-sm py-8 text-center">{t("hist_no_results")}</p>
        ) : (
          filtered.map((session, i) => (
            <SessionCard key={session.id} session={session} index={i} showName={isUploaded} t={t} />
          ))
        )}
      </div>
    </div>
  )
}
