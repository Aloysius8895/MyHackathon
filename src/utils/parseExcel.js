import * as XLSX from "xlsx"

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
          const json = XLSX.utils.sheet_to_json(sheet, { defval: "" })
          result[sheetName.toLowerCase()] = json
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
  return rows.map((row, i) => ({
    id: `co_${String(i + 1).padStart(3, "0")}`,
    name: row["Company Name"] || row["name"] || row["Company"] || `Company ${i + 1}`,
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
  }))
}

export function mapMentors(rows) {
  return rows.map((row, i) => ({
    id: `me_${String(i + 1).padStart(3, "0")}`,
    name: row["Mentor Name"] || row["name"] || row["Name"] || `Mentor ${i + 1}`,
    title: row["Title"] || row["title"] || row["Position"] || "",
    expertise: [
      row["Expertise 1"] || row["expertise_1"] || row["Skill 1"] || "",
      row["Expertise 2"] || row["expertise_2"] || row["Skill 2"] || "",
      row["Expertise 3"] || row["expertise_3"] || row["Skill 3"] || ""
    ].filter(Boolean),
    exits: [
      row["Exit 1"] || row["exit_1"] || "",
      row["Exit 2"] || row["exit_2"] || ""
    ].filter(Boolean),
    sector: row["Sector"] || row["sector"] || "",
    availability: row["Availability"] || row["availability"] || "Bi-weekly"
  }))
}

export function mapEngagements(rows) {
  return rows.map((row, i) => ({
    mentor_id: row["Mentor ID"] || row["mentor_id"] || `me_00${i + 1}`,
    company: row["Company"] || row["company"] || row["Company Name"] || "",
    outcome: row["Outcome"] || row["outcome"] || row["Result"] || "",
    score: parseFloat(row["Score"] || row["score"] || row["Engagement Score"] || 0.8)
  }))
}