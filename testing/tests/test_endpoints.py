import pytest
from source.constants.types import TTest

from testing.fixtures.mongodb import *
from testing.fixtures.aiohttp import *
from testing.mocks.constants import INITIAL_ID, INSERTED_TEST, TEST_FOR_UPDATE
from testing.utils import endpoint_test_handler, mongo_update_handler


@pytest.mark.asyncio
async def test_add_test(cli, mongo_db):
    """Is the /tests/add endpoint really push a new test to database"""
    await endpoint_test_handler(cli, "/tests/add", json=INSERTED_TEST)
    mongo_update_handler(mongo_db, INSERTED_TEST)


@pytest.mark.asyncio
async def test_update_test(cli, mongo_db):
    """Is the /tests/update endpoint really update a test with new data in database"""
    updated_test: TTest = {**TEST_FOR_UPDATE, "_id": str(INITIAL_ID), "name": "updated_test"}

    await endpoint_test_handler(cli, "/tests/update", json=updated_test)
    mongo_update_handler(mongo_db, {**TEST_FOR_UPDATE, "name": "updated_test"})
