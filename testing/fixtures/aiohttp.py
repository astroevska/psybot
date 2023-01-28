import pytest
from aiohttp import web

from testing.fixtures.mongodb import *
from source.utils.server.helpers import postHandlerFactory


@pytest.fixture
def app(mongo_db):
    application = web.Application()
    application.router.add_post('/tests/add', postHandlerFactory(mongo_db.tests.insert_one, ["name", "description", "content", ["questions", "interpretor"]]))

    return application


@pytest.fixture
def cli(event_loop, app, aiohttp_client):
    return event_loop.run_until_complete(aiohttp_client(app))
