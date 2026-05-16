const BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "")

function historyUrl(path) {
  return `${BASE}${path}`
}

export async function saveHistoryUpload(dataset) {
  const payload = {
    companies: dataset?.companies ?? [],
    mentors: dataset?.mentors ?? [],
    engagements: dataset?.engagements ?? [],
    source: "frontend-upload",
    uploadedAt: new Date().toISOString(),
  }

  try {
    const res = await fetch(historyUrl("/history/upload"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
    return res.ok
  } catch {
    // UI can still use the current upload even if the backend is offline.
    return false
  }
}

export async function loadHistorySessions() {
  try {
    const res = await fetch(historyUrl("/history/sessions"))
    if (!res.ok) return null
    const data = await res.json()
    return data?.engagements?.length ? data : null
  } catch {
    return null
  }
}
