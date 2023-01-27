# coding=utf-8           # -*- coding: utf-8 -*-
import asyncio
import tracemalloc

from source.init.bot import main
from source.init.server import start_server
from source.utils.asynchronous import scheduleCheckReminders


async def run_tasks():
    task = asyncio.create_task(main())
    asyncio.create_task(scheduleCheckReminders())
    await task

tracemalloc.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    loop.create_task(run_tasks())
    loop.run_forever()
