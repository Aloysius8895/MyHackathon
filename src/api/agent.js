import { COMPANIES, MENTORS, PAST_ENGAGEMENTS, MOCK_MATCHES } from "../data/mockData"

const USE_MOCK = true
const BACKEND_URL = "http://localhost:8000/api/match"
const MOCK_DELAY_MS = 2200

async function runMockAgent(onLog, companies, mentors, engagements) {
  const steps = [
    "Initialising Gemini 2.5 Pro agent...",
    `Loading ${companies.length} companies into knowledge graph...`,
    `Loading ${mentors.length} mentors...`,
    "Running match agent — scoring all company-mentor pairs...",
    `Querying ${engagements.length} past engagement records...`,
    "Generating reasoning and key unlocks...",
    `Match complete — ${Math.min(companies.length, mentors.length)} pairings generated`
  ]
  for (const step of steps) {
    onLog(step)
    await new Promise(r => setTimeout(r, MOCK_DELAY_MS / steps.length))
  }
  // Return mock matches but relabelled with real company/mentor names if custom data
  return MOCK_MATCHES.slice(0, Math.min(companies.length, mentors.length, MOCK_MATCHES.length))
}

async function runRealAgent(onLog, companies, mentors, engagements) {
  onLog("Connecting to EcoGraph backend...")
  const res = await fetch(BACKEND_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ companies, mentors, past_engagements: engagements })
  })
  if (!res.ok) throw new Error(`Backend error: ${res.status}`)
  onLog("Agent processing relationships...")
  const data = await res.json()
  onLog(`Match complete — ${data.matches.length} pairings generated`)
  return data.matches
}

export async function runAgent(onLog = () => {}, customData = null) {
  const companies = customData?.companies || COMPANIES
  const mentors = customData?.mentors || MENTORS
  const engagements = customData?.engagements || PAST_ENGAGEMENTS

  if (USE_MOCK) return runMockAgent(onLog, companies, mentors, engagements)
  return runRealAgent(onLog, companies, mentors, engagements)
}
