import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, Optional, Any
from uuid import uuid4

import httpx
from pydantic import Field

# A2A Python SDK Imports
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    DataPart,
    JSONRPCErrorResponse,
    Message,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task,
    TaskState,
    TextPart,
)

# Google ADK Imports
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event
from google.genai import types as genai_types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdkToA2AClientAdapter(BaseAgent):
    """
    An ADK BaseAgent that acts as a client to an external A2A server.

    This version includes the required 'name' and 'description' fields for
    BaseAgent and creates a new httpx.AsyncClient for each request to ensure

    connection stability and prevent async lifecycle errors.
    """

    # Pydantic Field Declarations
    # Fields required by the BaseAgent superclass
    name: str
    description: str

    # Custom fields for this adapter
    a2a_server_url: str
    session_map: Dict[str, Dict[str, str]] = Field(default_factory=dict)

    def _init_(self, **data: Any):
        """
        Initializes the agent.

        This explicit _init_ is included for clarity. It passes all arguments
        (like name, description, a2a_server_url) to the parent BaseAgent
        (a Pydantic model) for validation and assignment.
        """
        super()._init_(**data)
        logger.info(
            f"Agent '{self.name}' instance created. Description: '{self.description}'."
            f" Targeting A2A server: {self.a2a_server_url}"
        )


    async def _run_async_impl(
        self,
        context: InvocationContext,
    ) -> AsyncGenerator[Event, None]:
        """
        The core logic for the agent, required by BaseAgent.

        For each invocation, this method creates, uses, and discards a new client.
        """
        # Create a new, short-lived client for this specific request
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                # Initialize the A2A client using the new httpx client
                logger.info(f"[{self.name}] Creating new A2A client for request.")
                resolver = A2AClient.get_client_from_agent_card_url(
                    httpx_client=client, base_url=self.a2a_server_url
                )
                a2a_client = await resolver
                logger.info(f"[{self.name}] New A2A client created successfully.")

                async for event in self._handle_request(context, a2a_client):
                    yield event

        except httpx.RequestError as e:
            logger.error(f"[{self.name}] HTTP request failed: {e}")
            error_text = f"Failed to connect to the remote agent at {self.a2a_server_url}."
            yield Event(
                invocation_id=context.invocation_id,
                author=self.name,
                branch=context.branch,
                content=genai_types.Content(parts=[genai_types.Part.from_text(text=error_text)])
            )
        except Exception as e:
            logger.error(
                f"[{self.name}] An unexpected error occurred during client "
                f"initialization or request handling: {e}",
                exc_info=True
            )
            error_text = "An unexpected error occurred while processing your request."
            yield Event(
                invocation_id=context.invocation_id,
                author=self.name,
                branch=context.branch,
                content=genai_types.Content(parts=[genai_types.Part.from_text(text=error_text)])
            )

    async def _handle_request(
        self,
        context: InvocationContext,
        a2a_client: A2AClient
    ) -> AsyncGenerator[Event, None]:
        """
        Handles the logic of a single request using the provided A2A client.
        This has been separated from _run_async_impl for clarity.
        """
        # Message Conversion: ADK -> A2A
        adk_message = context.user_content
        if not adk_message or not adk_message.parts:
            yield Event(
                invocation_id=context.invocation_id,
                author=self.name,
                branch=context.branch,
                is_final_response=True,
            )
            return

        session_id = context.session.id
        a2a_session_info = self.session_map.get(session_id, {})
        task_id = a2a_session_info.get("taskId")
        context_id = a2a_session_info.get("contextId")

        a2a_parts = [
            TextPart(kind="text", text=part.text)
            for part in adk_message.parts
            if part.text
        ]

        if not a2a_parts:
            logger.warning(f"[{self.name}] No text parts found in user message for session {session_id}.")
            return

        a2a_message_to_send = Message(
            role="user",
            parts=a2a_parts,
            messageId=uuid4().hex,
            taskId=task_id,
            contextId=context_id,
            kind="message",
        )

        params = MessageSendParams(message=a2a_message_to_send)
        request = SendMessageRequest(
            id=uuid4().hex, method="message/send", params=params
        )

        logger.info(
            f"[{self.name}] Sending A2A request for session {session_id}:\n"
            f"{request.model_dump_json(indent=2, exclude_none=True)}"
        )

        # A2A Interaction
        response_wrapper = await a2a_client.send_message(request)

        logger.info(
            f"[{self.name}] Received A2A response for session {session_id}:\n"
            f"{response_wrapper.model_dump_json(indent=2, exclude_none=True)}"
        )

        content_to_yield: Optional[genai_types.Content] = None

        if isinstance(response_wrapper.root, SendMessageSuccessResponse):
            result = response_wrapper.root.result
            if isinstance(result, Task):
                # Update session mapping with new task/context IDs
                self.session_map[session_id] = {
                    "taskId": result.id,
                    "contextId": result.contextId,
                }
                if result.status.state == TaskState.input_required:
                    content_to_yield = self._a2a_message_to_adk_content(
                        result.status.message
                    )
                elif result.artifacts:
                    content_to_yield = self._a2a_task_to_adk_content(result)

            elif isinstance(result, Message):
                content_to_yield = self._a2a_message_to_adk_content(result)

        elif isinstance(response_wrapper.root, JSONRPCErrorResponse):
            error = response_wrapper.root.error
            logger.error(
                f"[{self.name}] A2A server returned an error: "
                f"Code={error.code}, Message='{error.message}'"
            )
            error_text = f"Error communicating with remote agent: {error.message}"
            content_to_yield = genai_types.Content(parts=[genai_types.Part.from_text(text=error_text)])

        # Yield Final Event to ADK Runner
        yield Event(
            invocation_id=context.invocation_id,
            author=self.name,
            branch=context.branch,
            content=content_to_yield,
        )

    def _a2a_message_to_adk_content(
        self, a2a_msg: Optional[Message]
    ) -> Optional[genai_types.Content]:
        if not a2a_msg or not a2a_msg.parts:
            return None

        adk_parts = []
        for part_wrapper in a2a_msg.parts:
            part = part_wrapper.root
            if isinstance(part, DataPart):
                adk_parts.append(genai_types.Part.from_text(text=json.dumps(part.data)))
            elif isinstance(part, TextPart) and part.text:
                adk_parts.append(genai_types.Part.from_text(text=part.text))

        return genai_types.Content(parts=adk_parts) if adk_parts else None

    def _a2a_task_to_adk_content(
        self, task: Task
    ) -> Optional[genai_types.Content]:
        if not task.artifacts:
            return None

        all_parts = []
        for artifact in task.artifacts:
            for part_wrapper in artifact.parts:
                part = part_wrapper.root
                if isinstance(part, DataPart):
                    all_parts.append(genai_types.Part.from_text(text=json.dumps(part.data)))
                elif isinstance(part, TextPart) and part.text:
                    all_parts.append(genai_types.Part.from_text(text=part.text))

        return genai_types.Content(parts=all_parts) if all_parts else None