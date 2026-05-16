
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError

from agent import InsuranceAgent


class InsuranceAgentExecutor(AgentExecutor):
    """Insurance AgentExecutor Example."""

    def __init__(self):
        self.agent = InsuranceAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        task = context.current_task
        print("AGENT EXECUTOR QUERY------> ", query)
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.contextId)

        async for item in self.agent.stream(query, task.contextId):
            is_task_complete = item['is_task_complete']

            if not is_task_complete:
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(
                        item['updates'], task.contextId, task.id
                    ),
                )
                continue

            if isinstance(item['content'], dict):
                if (
                    'response' in item['content']
                    and 'result' in item['content']['response']
                ):
                    data = json.loads(item['content']['response']['result'])
                    await updater.update_status(
                        TaskState.input_required,
                        new_agent_parts_message(
                            [Part(root=DataPart(data=data))],
                            task.contextId,
                            task.id,
                        ),
                        final=True,
                    )
                    continue
                else: # Fallback for unexpected dict
                    await updater.update_status(
                        TaskState.failed,
                        new_agent_text_message(
                            f"Reaching an unexpected state with content: {item['content']}",
                            task.contextId,
                            task.id,
                        ),
                        final=True,
                    )
                    break
            else: # Its a final text response (the report)
                await updater.add_artifact(
                    [Part(root=TextPart(text=item['content']))], name='report'
                )
                await updater.complete()
                break

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
