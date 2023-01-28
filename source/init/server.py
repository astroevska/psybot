from aiohttp import web

from ..init.bot import sendMessage
from ..db.update import updateTest, updateUser
from ..db.insert import insertResult, insertTest, insertUser
from ..utils.server.helpers import getHandlerFactory, postHandlerFactory
from ..db.get import getTests, getTest, getReminders, getResults, getUsers, getUser


async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

app = web.Application()

app.router.add_get('/tests', getHandlerFactory(getTests, ['name']))
app.router.add_post('/tests/add', postHandlerFactory(insertTest, ["name", "description", "content", ["questions", "interpretor"]]))
app.router.add_post('/tests/update', postHandlerFactory(updateTest, ["name", "description", "content", ["questions", "interpretor"]], False, getTest))

app.router.add_get('/users', getHandlerFactory(getUsers, ['id', 'name', 'telegram_id', 'telegram_username']))
app.router.add_post('/users/add', postHandlerFactory(insertUser, ["name"]))
app.router.add_post('/users/update', postHandlerFactory(updateUser, ["name"], False, getUser))
app.router.add_post('/users/notify', postHandlerFactory(sendMessage, ["chat_id", "text"]))

app.router.add_get('/results', getHandlerFactory(getResults, ['test_name', 'result', 'telegram_id']))
app.router.add_post('/results/add', postHandlerFactory(insertResult, ["userId", "test_name", "result"], True))

app.router.add_get('/reminders', getHandlerFactory(getReminders, ['period']))
