import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv

from agent import InsuranceAgent
from agent_executor import InsuranceAgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=10010)
def main(host, port):
    try:

        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id='process_insurance_application',
            name='Process Insurance Application',
            description='Guides a user through a health questionnaire and generates a risk profile report.',
            tags=['insurance', 'health', 'report'],
            examples=[
                'I want to get a health insurance policy.',
                'Hi, can you help me with insurance?',
            ],
        )
        agent_card = AgentCard(
            name='Insurance Agent',
            description='This agent helps users apply for health insurance.',
            url=f'YOUR_A2A_SERVER_URL',
            version='1.0.0',
            defaultInputModes=InsuranceAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=InsuranceAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )
        request_handler = DefaultRequestHandler(
            agent_executor=InsuranceAgentExecutor(),
            task_store=InMemoryTaskStore(),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )
        import uvicorn

        uvicorn.run(server.build(), host=host, port=port)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
