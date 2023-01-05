import asyncio
from init.bot import main, scheduleCheckReminders

async def run_tasks():
    task = asyncio.create_task(main())
    asyncio.create_task(scheduleCheckReminders())
    await task

if __name__ == "__main__":
    asyncio.run(run_tasks())