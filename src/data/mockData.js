export const COMPANIES = [
  { id: "co_001", name: "PayFlow MY", sector: "Fintech", stage: "Series A", asks: ["BNM e-money licence", "Enterprise sales", "Series A fundraising"] },
  { id: "co_002", name: "AgroSense", sector: "Agritech", stage: "Seed", asks: ["Hardware supply chain", "MAFI grant navigation", "Pilot scaling"] },
  { id: "co_003", name: "HealthBridge", sector: "Healthtech", stage: "Pre-Series A", asks: ["MOH partnerships", "Series A strategy", "Medical device licensing"] },
  { id: "co_004", name: "LogiChain", sector: "Logistics", stage: "Seed", asks: ["Enterprise pharma pilots", "NPRA compliance", "Series A narrative"] },
  { id: "co_005", name: "EduPath", sector: "Edtech", stage: "Series A", asks: ["MOE curriculum alignment", "Series B fundraising", "Indonesia expansion"] },
  { id: "co_006", name: "CarbonLedger", sector: "Cleantech", stage: "Seed", asks: ["Bursa ESG framework", "GLC enterprise sales", "Carbon credit access"] }
]

export const MENTORS = [
  { id: "me_001", name: "Dato' Farouk Mansur", title: "Ex-CEO, CIMB Ventures", expertise: ["Fintech", "BNM Regulatory", "VC", "SEA expansion"], exits: ["iPay88", "Revenue Monster"] },
  { id: "me_002", name: "Dr. Lim Mei Shan", title: "Managing Partner, AgriVentures Asia", expertise: ["Agritech", "IoT hardware", "Govt grants"], exits: ["FarmConnect", "NutriScan"] },
  { id: "me_003", name: "Hasniza Othman", title: "Ex-MOH Deputy Director", expertise: ["MOH/KKM partnerships", "Medical device regulation", "Telemedicine policy"], exits: [] },
  { id: "me_004", name: "James Ng Chin Wah", title: "Co-founder, ColdLink (exited)", expertise: ["Cold-chain logistics", "NPRA compliance", "Enterprise pharma sales"], exits: ["ColdLink → Zuellig Pharma"] },
  { id: "me_005", name: "Sharmini Rajasegaran", title: "Partner, Openspace Ventures", expertise: ["Edtech", "Series A/B fundraising", "SEA expansion"], exits: ["Teachable Asia", "SkillUp"] },
  { id: "me_006", name: "Ahmad Faris Zainudin", title: "ESG Lead, Bursa Malaysia", expertise: ["Bursa ESG framework", "Carbon markets", "GLC enterprise sales"], exits: [] }
]

export const PAST_ENGAGEMENTS = [
  { mentor_id: "me_001", company: "PayTech MY", outcome: "BNM licence + Series A RM5M", score: 0.91 },
  { mentor_id: "me_002", company: "AgriX Solutions", outcome: "MAFI grant RM800K + 200 farmer pilot", score: 0.95 },
  { mentor_id: "me_003", company: "MedFlow", outcome: "MOH pilot approved (3 clinics)", score: 0.82 },
  { mentor_id: "me_004", company: "DeliverCool", outcome: "NPRA cert + 2 pharma pilots", score: 0.93 },
  { mentor_id: "me_005", company: "LearnX Asia", outcome: "Series A USD3M + Indonesia launch", score: 0.98 },
  { mentor_id: "me_006", company: "GreenLedge", outcome: "Bursa MOU + 2 GLC pilots", score: 0.74 }
]

export const MOCK_MATCHES = [
  { company_id: "co_001", company: "PayFlow MY", sector: "Fintech", stage: "Series A", mentor_id: "me_001", mentor: "Dato' Farouk Mansur", mentor_title: "Ex-CEO, CIMB Ventures", score: 0.97, reasoning: "Dato' Farouk has direct BNM regulatory experience and two fintech exits in payments. PayFlow's top ask — BNM e-money licensing — maps directly to his expertise. Historical data mirrors CIP2024 PayTech MY pairing which secured both the licence and Series A.", key_unlock: "BNM e-money licence pathway", risk: null },
  { company_id: "co_002", company: "AgroSense", sector: "Agritech", stage: "Seed", mentor_id: "me_002", mentor: "Dr. Lim Mei Shan", mentor_title: "Managing Partner, AgriVentures Asia", score: 0.96, reasoning: "Dr. Lim has two agritech exits including an IoT hardware company. AgroSense's needs match her profile exactly. Near-identical to CIP2025 AgriX pairing, the strongest in that cohort.", key_unlock: "MAFI grant application + Agrobank intro", risk: null },
  { company_id: "co_003", company: "HealthBridge", sector: "Healthtech", stage: "Pre-Series A", mentor_id: "me_003", mentor: "Hasniza Othman", mentor_title: "Ex-MOH Deputy Director", score: 0.93, reasoning: "Hasniza's MOH network is HealthBridge's most critical unlock. As ex-Deputy Director she navigates KKM partnerships directly. Historical MedFlow pairing shows MOH pilot approval as outcome.", key_unlock: "MOH clinic pilot approval", risk: "Bi-weekly scheduling needed — buffer in calendar" },
  { company_id: "co_004", company: "LogiChain", sector: "Logistics", stage: "Seed", mentor_id: "me_004", mentor: "James Ng Chin Wah", mentor_title: "Co-founder, ColdLink (exited)", score: 0.95, reasoning: "James sold ColdLink to Zuellig Pharma — the exact sector LogiChain targets. DeliverCool pairing achieved NPRA cert and 2 enterprise pilots with identical profile.", key_unlock: "NPRA GDP cert + Zuellig/Duopharma intros", risk: null },
  { company_id: "co_005", company: "EduPath", sector: "Edtech", stage: "Series A", mentor_id: "me_005", mentor: "Sharmini Rajasegaran", mentor_title: "Partner, Openspace Ventures", score: 0.94, reasoning: "Sharmini is partner at the VC most likely to lead EduPath's Series B. LearnX Asia pairing directly led to Series A close — EduPath is at the same profile one stage later.", key_unlock: "Openspace Ventures Series B intro", risk: "Singapore-based — async communication critical" },
  { company_id: "co_006", company: "CarbonLedger", sector: "Cleantech", stage: "Seed", mentor_id: "me_006", mentor: "Ahmad Faris Zainudin", mentor_title: "ESG Lead, Bursa Malaysia", score: 0.91, reasoning: "Ahmad works inside Bursa Malaysia — CarbonLedger's primary regulatory environment. GreenLedge pairing showed strong outcome despite fewer sessions.", key_unlock: "Bursa ESG certification + GLC procurement", risk: null }
]

export const SECTOR_COLORS = {
  Fintech:    { bg: "bg-purple-900", text: "text-purple-300", dot: "#a78bfa" },
  Agritech:   { bg: "bg-green-900",  text: "text-green-300",  dot: "#86efac" },
  Healthtech: { bg: "bg-blue-900",   text: "text-blue-300",   dot: "#93c5fd" },
  Logistics:  { bg: "bg-orange-900", text: "text-orange-300", dot: "#fdba74" },
  Edtech:     { bg: "bg-pink-900",   text: "text-pink-300",   dot: "#f9a8d4" },
  Cleantech:  { bg: "bg-teal-900",   text: "text-teal-300",   dot: "#5eead4" }
}