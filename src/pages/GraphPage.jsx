import { useNavigate } from "react-router-dom"
import GraphView from "../components/GraphView"
import { useLang } from "../context/LanguageContext"

export default function GraphPage({ matches }) {
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

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">{t("graph_title")}</h1>
        <p className="text-slate-400 text-sm mt-1">{t("graph_subtitle")}</p>
      </div>

      <GraphView matches={matches} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { title: t("graph_card1_title"), desc: t("graph_card1_desc") },
          { title: t("graph_card2_title"), desc: t("graph_card2_desc") },
          { title: t("graph_card3_title"), desc: t("graph_card3_desc") },
        ].map(c => (
          <div key={c.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
            <p className="text-sm font-semibold text-purple-300">{c.title}</p>
            <p className="text-xs text-slate-400 leading-relaxed">{c.desc}</p>
          </div>
        ))}
      </div>

      <button onClick={() => navigate("/matches")}
        className="text-sm text-slate-500 hover:text-slate-300 transition-colors">
        {t("back_matches")}
      </button>
    </div>
  )
}
