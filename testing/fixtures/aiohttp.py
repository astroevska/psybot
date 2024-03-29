import pytest
from aiohttp import web

from testing.fixtures.mongodb import *
from source.utils.server.helpers import getHandlerFactory, postHandlerFactory


@pytest.fixture
def app(mongo_db):
    application = web.Application()

    application.router.add_get('/tests', getHandlerFactory(mongo_db.tests.find, ['name']))
    application.router.add_post('/tests/add', postHandlerFactory(mongo_db.tests.insert_one, ["name", "description", "content", ["questions", "interpretor"]]))
    application.router.add_post('/tests/update', postHandlerFactory(mongo_db.tests.update_one, ["name", "description", "content", ["questions", "interpretor"]], False, mongo_db.tests.find_one))

    application.router.add_get('/users', getHandlerFactory(mongo_db.users.find, ['id', 'name', 'telegram_id', 'telegram_username']))
    application.router.add_post('/users/add', postHandlerFactory(mongo_db.users.insert_one, ["name"]))
    application.router.add_post('/users/update', postHandlerFactory(mongo_db.users.update_one, ["name"], False, mongo_db.users.find_one))

    application.router.add_get('/results', getHandlerFactory(mongo_db.results.find, ['test_name', 'result', 'telegram_id']))
    application.router.add_post('/results/add', postHandlerFactory(mongo_db.results.insert_one, ["userId", "test_name", "result"], True))

    application.router.add_get('/reminders', getHandlerFactory(mongo_db.reminders.find, ['period']))
    application.router.add_post('/reminders/add', postHandlerFactory(mongo_db.reminders.insert_one, ['period']))
    application.router.add_post('/reminders/update', postHandlerFactory(mongo_db.reminders.update_one, ['period'], False, mongo_db.reminders.find_one))

    application.router.add_get('/unfinished_tests', getHandlerFactory(mongo_db.unfinished_tests.find, ['chat_id', 'test_name', 'userId']))
    application.router.add_post('/unfinished_tests/add', postHandlerFactory(mongo_db.unfinished_tests.insert_one, ['chat_id', 'test_name', 'userId']))
    application.router.add_post('/unfinished_tests/update', postHandlerFactory(mongo_db.unfinished_tests.update_one, ['chat_id', 'test_name', 'userId'], False, mongo_db.unfinished_tests.find_one))

    application.router.add_get('/buttons', getHandlerFactory(mongo_db.buttons.find, ['name', 'buttons', 'userId']))


    return application


@pytest.fixture
def cli(event_loop, app, aiohttp_client):
    return event_loop.run_until_complete(aiohttp_client(app))
