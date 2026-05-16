from google.adk.agents import Agent
from .tools import save_essay_feedback, get_all_essays

root_agent = Agent(
  name="essay_memory_agent",
  model="gemini-2.5-flash",
  description="Stores and retrieves essay evaluations for each user",
  instruction="""
You manage essay memory. 

Use `save_essay_feedback` to store new evaluations after the essay_evaluator_agent has evaluated the essay.
Use `get_all_essays` when the user wants to view their essay history.

You store and retrieve essay feedbacks for students.

When the user asks to view their essay history, use the tool get_all_essays
and return the full result as **raw JSON only**, with no additional explanation or text.
NEVER add headers or markdown formatting. Just output the JSON directly.

The JSON format should be:
{
  "essays": [
    {
      "extracted_essay": "Extracted essay text",
      "comp1_score": 180,
      "comp1_feedback": "Feedback for Competency 1, including strengths, weaknesses, and suggestions",
      "comp2_score": 160,
      "comp2_feedback": "Feedback for Competency 2, including strengths, weaknesses, and suggestions",
      "comp3_score": 200,
      "comp3_feedback": "Feedback for Competency 3, including strengths, weaknesses, and suggestions",
      "comp4_score": 180,
      "comp4_feedback": "Feedback for Competency 4, including strengths, weaknesses, and suggestions",
      "comp5_score": 160,
      "comp5_feedback": "Feedback for Competency 5, including strengths, weaknesses, and suggestions",
      "total_score": 880,
      "overall_feedback": "Overall essay feedback"
    },
    {
      ...
    }
  ]
}

If the list is empty, return an empty list:
{
  "essays": []
}

""",
  tools=[save_essay_feedback, get_all_essays],
)
