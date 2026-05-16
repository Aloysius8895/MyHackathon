from google.adk.agents import Agent

flashcard_agent = Agent(
    name="flashcard_agent",
    model="gemini-2.5-flash",
    description="Generates flashcards for active recall",
    instruction="""
You will receive a topic and must return 3 to 5 flashcards for review.

Each flashcard should be a key-value pair:
{
  "What is X?": "X is ...",
  "How does Y work?": "Y works by ..."
}

Respond only with a JSON object, where the keys are the questions and the values are the answers.
Do NOT include any text, commentary, or formatting outside the JSON.
"""
)
