from google.adk.agents import Agent
from ..models import ContentOutput

content_composer_agent = Agent(
    name="content_composer_agent",
    model="gemini-2.5-flash",
    description="Combines sub-agent outputs into a structured content response",
    instruction="""
You will receive the following inputs:
- A textual explanation of the topic.
- A list of summarized bullet points (key concepts).
- A list of flashcards, where each flashcard includes a question and an answer.
- A list of video suggestions, where each suggestion includes a title, a link, and a description.

Return a JSON object in the following structure:

{
  "text_explanation": "A clear explanation of the topic...",
  "topics_summary": [
    "First key point...",
    "Second key point...",
    "Third key point..."
  ],
  "flashcards": [
    {
      "question": "What is...?",
      "answer": "It is..."
    },
    {
      "question": "Why...?",
      "answer": "Because..."
    }
  ],
  "video_suggestions": [
    {
      "title": "Video Title 1",
      "link": "https://www.youtube.com/watch?v=...",
      "description": "Short summary of video 1"
    },
    {
      "title": "Video Title 2",
      "link": "https://www.youtube.com/watch?v=...",
      "description": "Short summary of video 2"
    }
  ]
}

⚠️ Return only the final JSON. Do not include explanations, markdown, or any additional text.
""",
    output_schema=ContentOutput,
)
