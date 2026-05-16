import asyncio
from google.adk.agents import LlmAgent, Agent, BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.genai import types
from pydantic import BaseModel, Field

from a2a_to_adk_adapter import AdkToA2AClientAdapter

async def save_report_in_state(callback_context: CallbackContext):
    """
    An after_agent_callback that saves the output of the information_collector
    agent as an artifact.
    """
    if callback_context.agent_name == 'health_insurance_agent':
        last_event = callback_context._invocation_context.session.events[-1]
        if last_event and last_event.author == 'information_collector' and "report" in last_event.content.parts[0].text:
            report_content_part = last_event.content.parts[0].text
            callback_context.state["medical_report"] = report_content_part
            print("\n--- CALLBACK: Saved medical report to state. ---")

def orch_before_model_callback(callback_context: CallbackContext, llm_request):
        contents=llm_request.contents
        new_contents=[]
        for content in contents:
            if content.role=='user':
                for part in content.parts:
                    if part.text and "form_data" in part.text:
                        to_be_appended = types.Content(parts=[types.Part.from_text(text="Form submited by User. Please transfer it the information collector.")],role='user')
                    else:
                        to_be_appended = content
            else:
                to_be_appended = content
            new_contents.append(to_be_appended)

        llm_request.contents = new_contents

def before_model_callback(callback_context: CallbackContext, llm_request):
        contents=llm_request.contents
        new_contents=[]
        for content in contents:
            if content.role=='user':
                for part in content.parts:
                    if part.text and "form_data" in part.text:
                        to_be_appended = types.Content(parts=[types.Part.from_text(text="Form submited by User which was summarized by the information collector.")],role='user')
                    else:
                        to_be_appended = content
            else:
                to_be_appended = content
            new_contents.append(to_be_appended)

        llm_request.contents = new_contents

# Agent Definitions

information_collector = AdkToA2AClientAdapter(
    name='information_collector',
    description='This agent collects user information via a chat and generates a medical summary report.',
    a2a_server_url='YOUR_A2A_SERVER_URL',
)

doctor_agent = Agent(
    name='doctor_agent',
    model='gemini-2.5-flash',
    description='Agent to analyse the medical summary report and create a risk profile for the user.',
    instruction='''You are a doctor agent. Analyze the provided medical summary report to create a risk profile for the user.
    Explain the risk profile clearly, how it might affect their insurance application, and any extra medical documents they might need.
    Ignore if user says something like ok or awesome or great and get on with your task of giving the risk profile.

    MEDICAL SUMMARY REPORT:
    {medical_report?}
    ''',
    before_model_callback=before_model_callback,
)

policy_agent = Agent(
    name='policy_agent',
    model='gemini-2.5-flash',
    description='Agent to select the best insurance plan for the user based on their needs and medical report.',
    instruction='''You are a policy agent. Your job is to find the best insurance plan.
    First, understand the user's requirements from the given medical summary report.
    Use their medcial summary report to create a detailed query for the get_insurance_plan tool.
    Finally, present the recommended plans to the user in a clear format.

    USER'S MEDICAL SUMMARY REPORT:
    {medical_report?}

    ''',
    tools=[MCPToolset(connection_params=StreamableHTTPServerParams(url="YOUR_MCP_SERVER_URL"))],
    before_model_callback=before_model_callback,
)

root_agent = Agent(
    model='gemini-2.5-pro',
    name='health_insurance_agent',
    description='Master agent which helps the user assess his risk profile before applying for health insurance and choose the best health insurance.',
    instruction='''You are master agent who does the flow. You have three agents to do your work.
1.information_collector = An agent which collects details from user via forms and also gives an annonymized medical report.
2.doctor_agent - which gives risk profile based on the summary.
3.policy_agent - which recommends the best insurance plan.

Make sure to follow this process:
First, Call the information collector, information collector gives the form.
User fills the form, MAKE SURE to send it back to information collector.
Then information collector responds back to you with the summary. User might respond with ok or anything just call the doctor agent.
Call the Doctor agent, Doctor agent will respond with risk analysis. then
Call the policy agent, policy agent will respond with the best insurance plan.
''',
    sub_agents=[information_collector, doctor_agent, policy_agent],
    after_agent_callback=save_report_in_state,
    before_model_callback=orch_before_model_callback
)