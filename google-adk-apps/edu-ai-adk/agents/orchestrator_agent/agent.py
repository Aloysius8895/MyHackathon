from google.adk.agents import Agent
from agents.essay_evaluator_agent.agent import root_agent as essay_agent
from agents.simulated_exam_agent.agent import root_agent as exam_agent
from agents.prompt_builder_agent.agent import root_agent as prompt_agent
from agents.interdisciplinary_agent.agent import root_agent as inter_agent
from agents.personal_tutor_agent.agent import root_agent as tutor_agent
from agents.content_generator_agent.agent import root_agent as content_agent
from agents.rephraser_agent.agent import root_agent as rephraser_agent
from agents.progress_tracker_agent.agent import root_agent as tracker_agent
from agents.image_to_essay_agent.agent import root_agent as image_to_essay_agent
from agents.essay_memory_agent.agent import root_agent as memory_agent


root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-flash",
    description="Edu.AI orchestrator that decides which specialized agent to activate.",
    instruction="""
You are an intelligent orchestrator. Your job is to understand the student's intent
and delegate the task to the most appropriate specialized agent.
Delegate tasks as follows:
- Essay correction from text → essay_evaluator_agent
- Essay correction from image → image_to_essay_agent (after OCR, you must send the essay to essay_evaluator_agent)
- Simulated exam generation → simulated_exam_agent
- Essay prompt generation → prompt_builder_agent
- Interdisciplinary question generation → interdisciplinary_agent
- Personalized performance analysis and recommendations → personal_tutor_agent
- Didactic content generation → content_generator_agent
- Assisted rewriting → rephraser_agent
- Progress tracking and queries → progress_tracker_agent
- To retrieve or manage past essay evaluations → essay_memory_agent

You must NEVER attempt to answer the user yourself.
""",
    sub_agents=[
        image_to_essay_agent,
        essay_agent,
        exam_agent,
        prompt_agent,
        inter_agent,
        tutor_agent,
        content_agent,
        rephraser_agent,
        tracker_agent,
        memory_agent
    ]
)
