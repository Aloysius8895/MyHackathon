import { NavLink } from "react-router-dom"

const links = [
  { to: "/upload", label: "Upload Data" },
  { to: "/", label: "Run Agent" },
  { to: "/matches", label: "Matches" },
  { to: "/graph", label: "Graph" }
]

export default function Navbar({ matchCount = 0 }) {
  return (
    <nav className="sticky top-0 z-30 border-b border-slate-800/70 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
        <NavLink to="/" className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-teal-400 to-violet-500 font-display text-lg font-black text-white">
            E
          </div>
          <div>
            <p className="font-display text-lg font-bold text-white">EcoGraph</p>
            <p className="text-xs text-slate-500">AI ecosystem matching</p>
          </div>
        </NavLink>

        <div className="flex items-center gap-2">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-white text-slate-950"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>

        <div className="rounded-full border border-teal-500/30 bg-teal-950/40 px-4 py-2 text-sm font-semibold text-teal-200">
          {matchCount} matches
        </div>
      </div>
    </nav>
  )
}
