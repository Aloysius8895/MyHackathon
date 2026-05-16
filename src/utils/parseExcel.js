import * as XLSX from "xlsx"

const COMPANY_KEYS = ["Company Name", "Company", "Startup", "Startup Name", "Company / Mentee"]
const MENTOR_NAME_KEYS = ["Mentor Name", "mentor_name", "Mentor", "Lecturer Name", "Lecturer", "Advisor Name", "Advisor", "Name"]

function firstValue(row, keys, fallback = "") {
  for (const key of keys) {
    const value = row[key]
    if (value !== undefined && value !== null && String(value).trim() !== "") {
      return value
    }
  }
  return fallback
}

function slugFrom(value, fallback) {
  const slug = String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
  return slug || fallback
}

export function toObjectsFromRows(rows) {
  if (!rows.length) return []
  const headerIndex = rows.findIndex(row => {
    const normalized = row.map(value => String(value).trim().toLowerCase())
    return normalized.some(value =>
      ["name", "mentor name", "lecturer name", "session id", "company name", "company / mentee"].includes(value)
    )
  })
  const header = (headerIndex >= 0 ? rows[headerIndex] : rows[0]).map((value, i) =>
    String(value || `Column ${i + 1}`).trim()
  )
  const dataRows = rows.slice((headerIndex >= 0 ? headerIndex : 0) + 1)
  return dataRows
    .map(row => Object.fromEntries(header.map((key, i) => [key, row[i] ?? ""])))
    .filter(row => Object.values(row).some(value => String(value).trim() !== ""))
}

export function parseExcelFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: "array" })
        const result = {}
        workbook.SheetNames.forEach(sheetName => {
          const sheet = workbook.Sheets[sheetName]
          const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: "" })
          result[sheetName.toLowerCase()] = toObjectsFromRows(rows)
        })
        resolve(result)
      } catch (err) {
        reject(new Error("Failed to parse Excel file: " + err.message))
      }
    }
    reader.onerror = () => reject(new Error("Failed to read file"))
    reader.readAsArrayBuffer(file)
  })
}

export function mapCompanies(rows) {
  return rows.map((row, i) => {
    const name = firstValue(row, COMPANY_KEYS, `Company ${i + 1}`)
    return {
    id: `co_${String(i + 1).padStart(3, "0")}`,
    name,
    sector: row["Sector"] || row["sector"] || row["Industry"] || "General",
    stage: row["Stage"] || row["stage"] || row["Funding Stage"] || "Seed",
    asks: [
      row["Ask 1"] || row["ask_1"] || row["Challenge 1"] || "",
      row["Ask 2"] || row["ask_2"] || row["Challenge 2"] || "",
      row["Ask 3"] || row["ask_3"] || row["Challenge 3"] || ""
    ].filter(Boolean),
    revenue_mrr: row["MRR (USD)"] || row["mrr"] || 0,
    employees: row["Employees"] || row["employees"] || 0,
    founder: row["Founder"] || row["founder"] || "",
    description: row["Description"] || row["description"] || ""
  }})
}

export function mapMentors(rows) {
  return rows.map((row, i) => {
    const name = firstValue(row, MENTOR_NAME_KEYS, `Mentor ${i + 1}`)
    const sourceId = firstValue(row, ["Mentor ID", "Lecturer ID", "Advisor ID", "ID", "id"], "")
    return {
    id: sourceId ? `me_${slugFrom(sourceId, String(i + 1).padStart(3, "0"))}` : `me_${slugFrom(name, String(i + 1).padStart(3, "0"))}`,
    source_id: sourceId,
    name,
    title: row["Title"] || row["title"] || row["Position"] || row["Expertise Area"] || "",
    expertise: [
      row["Expertise 1"] || row["expertise_1"] || row["Skill 1"] || "",
      row["Expertise 2"] || row["expertise_2"] || row["Skill 2"] || "",
      row["Expertise 3"] || row["expertise_3"] || row["Skill 3"] || "",
      row["Expertise Area"] || "",
      row["Sub-specialty"] || ""
    ].filter(Boolean),
    exits: [
      row["Exit 1"] || row["exit_1"] || "",
      row["Exit 2"] || row["exit_2"] || ""
    ].filter(Boolean),
    sector: row["Sector"] || row["sector"] || "",
    industry: row["Industry"] || row["industry"] || row["Sector"] || "",
    availability: row["Availability"] || row["availability"] || "Bi-weekly",
    rating: row["Post-Session Rating (avg)"] || row["Rating"] || "",
    total_sessions: row["Total Sessions"] || "",
    mentees_handled: row["Mentees Handled"] || "",
    contact_email: row["Contact Email"] || row["Email"] || ""
  }})
}

export function mapEngagements(rows) {
  return rows.map((row, i) => {
    const mentorName = firstValue(row, MENTOR_NAME_KEYS)
    const company = firstValue(row, ["Company", "company", "Company Name", "Startup", "Startup Name"])
    const fallbackMentorId = mentorName ? `me_${slugFrom(mentorName, String(i + 1).padStart(3, "0"))}` : `me_00${i + 1}`
    return {
      session_id: firstValue(row, ["Session ID", "session_id", "Session Id", "ID"]),
      mentor_id: firstValue(row, ["Mentor ID", "mentor_id", "Mentor Id", "Lecturer ID", "Advisor ID"], fallbackMentorId),
      mentor_name: mentorName,
      company: company || firstValue(row, ["Company / Mentee"]),
      company_name: company || firstValue(row, ["Company / Mentee"]),
      outcome: firstValue(row, ["Outcome", "outcome", "Result", "Topic", "Session Topic", "Topic Covered"]),
      date: firstValue(row, ["Date", "Session Date", "date"]),
      programme: firstValue(row, ["Programme", "Program", "programme", "Programme Name"], "Uploaded Dataset"),
      pax: firstValue(row, ["Pax", "Participants", "Attendees"]),
      hours: firstValue(row, ["Hours", "Duration", "Session Hours", "Duration (hrs)"]),
      feedback: firstValue(row, ["Feedback Summary", "Feedback", "Comment"]),
      reengage: firstValue(row, ["Re-engagement Recommended", "Re-engage", "Reengage"]),
      match_type: firstValue(row, ["Match Type", "match_type", "Matched By"], "manual"),
      score: parseFloat(firstValue(row, ["Score", "score", "Engagement Score", "Rating", "Post-Session Rating"], 0.8))
    }
  })
}

export function deriveCompaniesFromEngagements(engagements) {
  const seen = new Set()
  return engagements
    .map((engagement, i) => {
      const name = firstValue(engagement, ["company_name", "company"], "")
      const key = name.trim().toLowerCase()
      if (!key || seen.has(key)) return null
      seen.add(key)
      return {
        id: `co_${slugFrom(name, String(i + 1).padStart(3, "0"))}`,
        name,
        sector: "History",
        stage: "Uploaded",
        asks: [],
        revenue_mrr: 0,
        employees: 0,
        founder: "",
        description: ""
      }
    })
    .filter(Boolean)
}
