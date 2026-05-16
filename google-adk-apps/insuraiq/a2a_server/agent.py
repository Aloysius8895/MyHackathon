import os
import json
from typing import Any, AsyncIterable

from google import genai
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types

def form_creator() -> dict[str, Any]:
    """Call this tool first to get the JSON schema for the insurance questionnaire form."""
    print("calling form_creator")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'my_dict1.json')
    with open(json_path, "r") as f:
        initial_form_dict = json.load(f)
    return initial_form_dict

def return_form_to_user(
    form_schema: dict[str, Any],
    tool_context: ToolContext,
) -> dict[str, Any]:
    """
    Use this tool to return a form to the user for them to fill out.
    The schema from the 'form_creator' tool must be passed as the 'form_schema' argument.
    """
    print(f"return_form_to_user was called with schema.")

    if not form_schema:
        return json.dumps({"error": "Form schema was not provided to the tool."})

    tool_context.actions.skip_summarization = True
    tool_context.actions.escalate = True
    form_dict = {
        'type': 'form',
        'form': form_schema,
        'form_data': {},
    }
    return json.dumps(form_dict)


class InsuranceAgent:
    """An agent that helps users get an insurance policy."""

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain', 'application/json']

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'insurance_seeker'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def get_processing_message(self) -> str:
        return 'Processing your insurance request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for the insurance agent."""
        return LlmAgent(
            model='gemini-2.5-flash',
            name='insurance_agent',
            description='This agent helps users with health insurance assessments.',
            instruction="""You are an information collector agent that collects user's medical history.
You do it via the given tools to you form_creator and return_form_to_user

FOLLOW THIS EXACT WORKFLOW:
1. First, call `form_creator` to get insurance questionnaire form.
2. Second, use `return_form_to_user` to respond back to the user. Pass the form_schema exactly how you recieve it from form_creator without changing the order.

If you see filled form with form data do as below:
*** Analyze the information and generate a concise risk assessment report with "Summary of Information" and "Identified Risk Factors" sections. 
Make sure it contains no Personally Identifiable Information. Output this report as your final text answer to the client agent. ***
""",

            tools=[
                form_creator,
                return_form_to_user,
            ],
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )

        try:
            data = json.loads(query)
            if isinstance(data, dict) and "form_data" in data:
                print("-----INSIDE FORM DATA-----")
                content = types.Content(
                    role='user', parts=[types.Part.from_text(text=json.dumps(data["form_data"]))]
                )
            else:
                print("-----INSIDE ELSE BLOCK-----")
                content = types.Content(
                    role='user', parts=[types.Part.from_text(text=query)]
                )
        except json.JSONDecodeError:
            content = types.Content(
                role='user', parts=[types.Part.from_text(text=query)]
            )

        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
        async for event in self._runner.run_async(
            user_id=self._user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                response = ''
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    response = '\n'.join(
                        [p.text for p in event.content.parts if p.text]
                    )
                elif (
                    event.content
                    and event.content.parts
                    and any(
                        [
                            True
                            for p in event.content.parts
                            if p.function_response
                        ]
                    )
                ):
                    response_part = next(
                        p.function_response
                        for p in event.content.parts if p.function_response
                    )
                    response = {'response': {'result': response_part.response['result']}}

                yield {
                    'is_task_complete': True,
                    'content': response,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }