# 📘 Edu.AI — Multi-Agent Educational System for ENEM

> 🇧🇷 _Quality education for all, powered by autonomous agents._

**Edu.AI** is an intelligent multi-agent platform designed to democratize access to high-quality ENEM preparation in Brazil. Built using Google’s **Agent Development Kit (ADK)**, Edu.AI offers personalized essay correction, simulated exams, study plans, and content generation — simulating the experience of an elite preparatory course, but powered entirely by AI.

---

## 🚀 Features

- ✍️ **AI-powered Essay Correction**
  Corrects essays according to ENEM's 5 official competencies, with scores and detailed feedback.

- 📚 **ENEM-style Prompt Generation**
  Creates contextualized essay prompts with motivational texts.

- 🧪 **Simulated Exams by Area & Theme**
  Builds customized tests with answer keys and explanations.

- 🧩 **Interdisciplinary Question Generation**
  Combines areas like History + Physics, or Chemistry + Sociology.

- 🎓 **Personalized Study Paths**
  Analyzes performance and suggests targeted learning strategies.

- 🎥 **Didactic Content Generation**
  Produces summaries, flashcards, slides, and visuals.

- 🗣️ **AI Rewriting Assistant**
  Helps students rewrite and improve their essays.

- 📈 **Progress Tracking Dashboard**
  Tracks scores over time and gives actionable recommendations.

- 📤 **Seamless Frontend Delivery**
  Clean UI powered by Next.js and deployed via Vercel.

---

## 🧠 Multi-Agent System Overview

| Agent                    | Role                                                   |
| ------------------------ | ------------------------------------------------------ |
| `EssayEvaluatorAgent`    | Evaluates essays with official rubric and feedback     |
| `PromptBuilderAgent`     | Generates contextual ENEM-style essay prompts          |
| `SimulatedExamAgent`     | Produces realistic exams with grading and explanations |
| `InterdisciplinaryAgent` | Creates cross-disciplinary questions                   |
| `ContentGeneratorAgent`  | Builds content: summaries, flashcards, slides          |
| `RephraserAgent`         | Suggests improved phrasing for essays or short answers |
| `ProgressTrackerAgent`   | Tracks performance and calculates averages             |
| `PersonalTutorAgent`     | Recommends study paths based on user history           |

---

## 🗺️ Architecture

> 🧭 Agents work collaboratively via an orchestrator and shared state.

![Architecture Diagram](./docs/Architecture.pdf)

- **Frontend:** Next.js + Tailwind (Vercel)
- **Backend:** FastAPI with ADK agents
- **Storage:** Google Cloud Storage, SQLite
- **OCR:** Cloud Vision for extracting essays from images
- **LLMs:** Gemini 2.5-flash

---

### 🏃‍♀️ Installation

To run the agents, clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Then, start the FastAPI server:

```bash
uvicorn main:app --reload --port 8080
```

The frontend is available at [https://edu-ai-adk.vercel.app/](https://edu-ai-adk.vercel.app/).

---

## 🏆 What We’re Proud Of

- Built a truly modular and scalable multi-agent architecture with 8+ intelligent agents.
- Delivered a full-stack AI product with a clean and functional UI.
- Created a solution with **real potential to impact education** at scale in Brazil.

---

Built by Giovanna Moeller.
