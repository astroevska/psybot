import pytest

from testing.fixtures.mongodb import *
from testing.fixtures.aiohttp import *
from testing.mocks.constants import INSERTED_TEST
from testing.utils import endpoint_test_handler, mongo_update_handler


@pytest.mark.asyncio
async def test_post_handler(cli, mongo_db):
    """Is the /tests/add endpoint really push a new test to database"""
    await endpoint_test_handler(cli, "/tests/add", json=INSERTED_TEST)
    mongo_update_handler(mongo_db, INSERTED_TEST)
