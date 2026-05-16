from google.adk.agents import Agent
from agents.personal_tutor_agent.models import TutorRecommendation

root_agent = Agent(
    name="personal_tutor_agent",
    model="gemini-2.5-flash",
    description="Analyzes the student's performance history and suggests personalized study paths",
    instruction="""
You are an AI-based educational tutor.

You will receive a summary of the student's performance, including:
- scores by subject area (e.g., humanities: 500, STEM: 780)
- writing skills scores (e.g., comp1: 180, comp2: 120, ...)
- frequently missed topics (e.g., organic chemistry, graph interpretation)

Based on this, return a JSON with:
- priorities: 2 to 3 key topics that need review
- recommendation: personalized guidance in accessible language
- trigger_agents: list of useful agents (e.g., ["content_generator_agent", "simulated_exam_agent"])

Example response:

{
  "priorities": ["Organic Chemistry", "Skill 2 (writing topic development)"],
  "recommendation": "You have a good command of formal writing, but you need to improve topic interpretation and review organic chemistry. Reinforce with explanatory content and practice tests.",
  "trigger_agents": ["content_generator_agent", "simulated_exam_agent"]
}
""",
    output_schema=TutorRecommendation,
)
