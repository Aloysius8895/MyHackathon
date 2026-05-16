import { useNavigate } from "react-router-dom"
import MatchCard from "../components/MatchCard"
import { useLang } from "../context/LanguageContext"

export default function MatchesPage({ matches }) {
  const navigate = useNavigate()
  const { t } = useLang()

  if (matches.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <p className="text-slate-500 text-sm">{t("no_matches")}</p>
        <button onClick={() => navigate("/")}
          className="text-purple-400 hover:text-purple-300 text-sm transition-colors">
          {t("back_input")}
        </button>
      </div>
    )
  }

  const avg = Math.round(matches.reduce((a, m) => a + m.score, 0) / matches.length * 100)

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">{t("matches_title")}</h1>
          <p className="text-slate-400 text-sm mt-1">{t("matches_subtitle", matches.length)}</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-2xl font-bold text-emerald-400 font-mono">{avg}%</div>
            <div className="text-xs text-slate-500">{t("avg_match")}</div>
          </div>
          <button onClick={() => navigate("/history")}
            className="px-4 py-2 border border-slate-700 hover:border-purple-600
              text-slate-300 hover:text-purple-300 rounded-xl text-sm font-medium transition-all">
            {t("btn_view_history")}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {matches.map((match, i) => (
          <MatchCard key={match.company_id} match={match} index={i} />
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
        <p className="text-sm font-medium text-slate-300">{t("cohort_title")}</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: t("stat_matched"), value: matches.length },
            { label: t("stat_avg_score"), value: `${avg}%` },
            { label: t("stat_graph_used"), value: 6 },
            { label: t("stat_funding"), value: "5 co." }
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
