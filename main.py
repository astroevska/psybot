# coding=utf-8           # -*- coding: utf-8 -*-
import asyncio
import tracemalloc
from aiohttp import web

from init.bot import main, scheduleCheckReminders
from db.get import getTests, getReminders, getResults, getUsers
from utils.server.helpers import getHandlerFactory


async def handle_post(request):
    try:
        data = await request.json()
    except:
        return web.json_response({"message": "Invalid JSON"})
    
    if "name" not in data:
        return web.json_response({"message": "Missing 'name' field"})
    
    return web.Response({"message": f"Hello, {data['name']}!"}, charset='cp1251')


app = web.Application()
app.router.add_get('/tests', getHandlerFactory(getTests, ['name']))
app.router.add_get('/reminders', getHandlerFactory(getReminders, ['period']))
app.router.add_get('/results', getHandlerFactory(getResults, ['test_name', 'result', 'telegram_id']))
app.router.add_get('/users', getHandlerFactory(getUsers, ['name', 'telegram_id', 'telegram_username']))
app.router.add_post('/post', handle_post)

async def run_tasks():
    task = asyncio.create_task(main())
    asyncio.create_task(scheduleCheckReminders())
    await task

async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

tracemalloc.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    loop.create_task(run_tasks())
    loop.run_forever()