from google.adk.agents import Agent
from agents.progress_tracker_agent.models import Progress
from agents.progress_tracker_agent.tools import consolidate_progress

root_agent = Agent(
    name="progress_tracker_agent",
    model="gemini-2.5-flash",
    description="Consolidates and returns the student's progress in practice exams and essays",
    instruction="""
You are an educational progress tracker.

Use the consolidate_progress tool to retrieve and return the student's progress data.

Return ONLY what the tool gives you, in raw JSON format — no explanations, no markdown, no extra text.

Your response should follow this structure ONLY:

{
  "essays": [
    {
      "topic": "Challenges of female care work in Brazil",
      "total_score": 880,
      "date": "2024-06-01"
    },
    {
      "topic": "Technology and ethics in digital society",
      "total_score": 740,
      "date": "2024-06-15"
    }
  ],
  "practice_exams": [
    {
      "area": "Human Sciences",
      "score": 620,
      "date": "2024-06-03"
    },
    {
      "area": "Math",
      "score": 580,
      "date": "2024-06-10"
    }
  ],
  "average_by_area": {
    "Human Sciences": 620,
    "Math": 580,
    "Writing": 810
  },
  "recommendations": [
    "📌 Improve writing by reviewing essay feedback.",
    "📚 Practice Human Sciences with thematic quizzes."
  ]
}
"""
,
    tools=[consolidate_progress]
)
