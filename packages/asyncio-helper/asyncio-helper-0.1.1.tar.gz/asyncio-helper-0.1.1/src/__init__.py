import asyncio
from datetime import timedelta
from typing import Coroutine

__author__ = "Noah Hummel"


def schedule_with_timeout(coro: Coroutine, t: timedelta) -> asyncio.Task:
    """Schedule a Coroutine to run concurrently, cancels after a timeout.

    Args:
        coro: The coroutine to schedule.
        t: The timeout.

    Returns:
        The handle of the scheduled task, may be used to await or cancel the
        coroutine.
    """
    task = asyncio.create_task(coro)

    async def _timeout():
        await asyncio.sleep(t.seconds)
        task.cancel()

    _ = asyncio.create_task(_timeout())
    return task
