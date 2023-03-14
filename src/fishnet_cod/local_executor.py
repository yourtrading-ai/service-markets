from typing import Optional
import time

from aars import AARS
from aleph_message.models import PostMessage, MessageType

from core.constants import FISHNET_MESSAGE_CHANNEL, EXECUTOR_MESSAGE_FILTER
from core.model import Execution
from core.execution import try_get_execution_from_message, run_execution

aars_client = AARS(channel=FISHNET_MESSAGE_CHANNEL)


async def handle_execution(event: PostMessage) -> Optional[Execution]:
    print(f"Received event: {event.content.type}")
    execution = await try_get_execution_from_message(event)
    if execution is not None:
        print(f"Running execution: {execution}")
        try:
            execution = await run_execution(execution)
        except Exception as e:
            print(f"Failed to run execution: {execution}")
            print(e)
    return None


async def listen():
    print(f"Listening for events on {EXECUTOR_MESSAGE_FILTER}")
    async for message in aars_client.session.watch_messages(
        start_date=time.time(),
        message_type=MessageType(EXECUTOR_MESSAGE_FILTER[0]["type"]),
        content_types=EXECUTOR_MESSAGE_FILTER[0]["post_type"],
        channels=[EXECUTOR_MESSAGE_FILTER[0]["channel"]],
    ):
        if isinstance(message, PostMessage):
            await handle_execution(message)
        else:
            print(f"Received invalid message: {message.type}")


async def main():
    await listen()


if __name__ == "__main__":
    import asyncio

    fut = asyncio.ensure_future(main())
    fut.add_done_callback(lambda fut: asyncio.get_event_loop().stop())
    asyncio.get_event_loop().run_forever()
