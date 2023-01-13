import asyncio
from typing import Any, Coroutine
from datetime import datetime, timedelta

from db.get import getReminders
from init.bot import sendMessage
from db.update import updateReminder
from utils.datetime import nextDateByPeriod


async def sendRemind(chat_id: int, text: str, sleepTime: int, nextDateTime: datetime, r: Any):
    await asyncio.sleep(sleepTime)

    try:
        await updateReminder({"$set": {**r, "next": nextDateByPeriod(r['period'], nextDateTime)}}, {'_id': r['_id']})
    except Exception as e:
        print(e)
        
    await sendMessage(chat_id, text)


async def scheduleReminders() -> Coroutine: 
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
    end_time = start_time + timedelta(days=1)

    currentReminders = list(getReminders({"next": {
        '$gte': start_time,
        '$lt': end_time
    }}))

    if len(currentReminders) != 0:
        for r in currentReminders:
            nextDateTime = r['next']
            sleepTime = nextDateTime - now
            
            asyncio.create_task(sendMessage(
                r['chat_id'],
                f"Время проверить свое психологическое состояние!\nСледующее напоминание будет {nextDateTime.strftime('<b>%d-%m-%Y</b> в <b>%H:%M:%S</b>')}",
                sleepTime.total_seconds(),
                nextDateTime,
                r
            ))

async def scheduleCheckReminders() -> Coroutine: 
    while True:
        await asyncio.sleep(86400)
        asyncio.create_task(scheduleReminders())
