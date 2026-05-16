---
name: "cradle-ecosystem-data-ingestion"
description: "Transforms raw unstructured files into structured JSON tokens and generates 768-dimension mathematical coordinate arrays using text-embedding-004."
capabilities: ["Data Structuring", "Semantic Chunking", "Vector Matrix Generation"]
---

# Skill: Structure & Vector Embedding Pipeline

## 🏁 Boundary & Responsibility
This skill isolates data-preparation and vector generation math from live database queries and frontend dashboard components. It handles raw inputs, structures them into strict JSON arrays, and appends mathematical coordinates.

---

## ⚙️ Deterministic Pipeline Logic (The Workflow)

1. **Schema Extraction:** Parse text inputs exclusively into rigid string configurations for primary identifiers (`id`, `name`, `content`).
2. **Granular Slicing:** Isolate target profiles into unified semantic blocks so that distinct ecosystem tags (e.g., *Bank Negara Compliance*) are preserved.
3. **Vector Transformation:** Route formatted strings to the Google GenAI SDK utilizing the `text-embedding-004` engine to harvest vector coordinates.
4. **Staging Delivery:** Package the raw text data alongside the new numeric array field (`embedding: [...]`) for direct document landing.

---

## 🚫 Guardrails & Hard Rules
* **NEVER** pass structural objects down the pipeline without a successfully generated embedding matrix.
* **NEVER** expose the system `GEMINI_API_KEY` inline—all authorization protocols must process via native `.env` system boundaries.
* **MUST** isolate processing errors on a per-file basis so a single corrupt string profile does not halt the entire batch execution block.