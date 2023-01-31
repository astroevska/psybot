from aiohttp import web

from ..init.bot import sendMessage
from ..db.update import updateReminder, updateTest, updateUnfinished, updateUser
from ..db.insert import insertReminder, insertResult, insertTest, insertUnfinished, insertUser
from ..utils.server.helpers import getHandlerFactory, postHandlerFactory
from ..db.get import getButtons, getReminder, getTests, getTest, getReminders, getResults, getUnfinished, getUsers, getUser


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
app.router.add_post('/reminders/add', postHandlerFactory(insertReminder, ['period']))
app.router.add_post('/reminders/update', postHandlerFactory(updateReminder, ['period'], False, getReminder))


app.router.add_get('/unfinished_tests', getHandlerFactory(getUnfinished, ['chat_id', 'test_name', 'userId']))
app.router.add_post('/unfinished_tests/add', postHandlerFactory(insertUnfinished, ['chat_id', 'test_name', 'userId']))
app.router.add_post('/unfinished_tests/update', postHandlerFactory(updateUnfinished, ['chat_id', 'test_name', 'userId'], False, getUnfinished))

app.router.add_get('/buttons', getHandlerFactory(getButtons, ['name', 'buttons', 'userId']))
