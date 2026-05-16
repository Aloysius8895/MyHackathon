from google.adk.agents import Agent
from ..models import PromptOutput

composer_agent = Agent(
    name="composer_agent",
    model="gemini-2.5-flash",
    description="Generates structured JSON with ENEM essay topic, source texts, and writing instructions",
    instruction="""
You will receive three texts with data, quotes, and context about an essay topic.

Based on this content, generate the following JSON:

{
  "topic": "...",
  "source_texts": [
    "Text 1...",
    "Text 2...",
    "Text 3..."
  ],
  "instructions": "..."
}

⚠️ Respond with JSON only.
""",
    output_schema=PromptOutput,
)
