import { createContext, useContext, useState } from "react"
import translations from "../i18n/translations"

const LanguageContext = createContext(null)

const CYCLE = { en: "zh", zh: "es", es: "en" }
const LABELS = { en: "EN", zh: "中文", es: "ES" }

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem("lang") || "en")

  function toggleLang() {
    const next = CYCLE[lang]
    setLang(next)
    localStorage.setItem("lang", next)
  }

  const t = (key, ...args) => {
    const val = translations[lang]?.[key] ?? translations["en"]?.[key]
    if (typeof val === "function") return val(...args)
    return val ?? key
  }

  return (
    <LanguageContext.Provider value={{ lang, toggleLang, t, LABELS }}>
      {children}
    </LanguageContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useLang() {
  return useContext(LanguageContext)
}
