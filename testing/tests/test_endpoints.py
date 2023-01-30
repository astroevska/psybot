import pytest
from source.constants.types import TTest, TUser

from testing.fixtures.mongodb import *
from testing.fixtures.aiohttp import *
from testing.utils import mongo_check_update
from testing.handlers import get_endpoint_test_handler, post_endpoint_test_handler
from testing.mocks.constants import INITIAL_ID, INITIAL_RESULTS, INSERTED_TEST, TEST_FOR_UPDATE, INSERTED_USER, USER_FOR_UPDATE, INSERTED_RESULT


@pytest.mark.asyncio
async def test_get_tests(cli):
    """Is the /tests endpoint really return the tests list"""
    await get_endpoint_test_handler(cli, '/tests', INITIAL_TESTS, INITIAL_ID)


@pytest.mark.asyncio
async def test_add_test(cli, mongo_db):
    """Is the /tests/add endpoint really push a new test to database"""
    await post_endpoint_test_handler(cli, "/tests/add", json=INSERTED_TEST)
    mongo_check_update(mongo_db, INSERTED_TEST, 'tests')


@pytest.mark.asyncio
async def test_update_test(cli, mongo_db):
    """Is the /tests/update endpoint really update a test with new data in database"""
    updated_test: TTest = {**TEST_FOR_UPDATE, "name": "updated_test"}

    await post_endpoint_test_handler(cli, "/tests/update", json={**updated_test, "_id": str(INITIAL_ID)})
    mongo_check_update(mongo_db, updated_test, 'tests')


@pytest.mark.asyncio
async def test_get_users(cli):
    """Is the /users endpoint really return the users list"""
    await get_endpoint_test_handler(cli, '/users', INITIAL_USERS, INITIAL_ID)


@pytest.mark.asyncio
async def test_add_user(cli, mongo_db):
    """Is the /users/add endpoint really push a new user to database"""
    await post_endpoint_test_handler(cli, "/users/add", json=INSERTED_USER)
    mongo_check_update(mongo_db, INSERTED_USER, 'users')


@pytest.mark.asyncio
async def test_update_user(cli, mongo_db):
    """Is the /users/update endpoint really update a user with new data in database"""
    updated_user: TUser = {**USER_FOR_UPDATE, "name": "updated_user"}

    await post_endpoint_test_handler(cli, "/users/update", json={**updated_user, "_id": str(INITIAL_ID)})
    mongo_check_update(mongo_db, updated_user, 'users')


@pytest.mark.asyncio
async def test_get_results(cli):
    """Is the /results endpoint really return the results list"""
    await get_endpoint_test_handler(cli, '/results', INITIAL_RESULTS, INITIAL_ID)


@pytest.mark.asyncio
async def test_add_result(cli, mongo_db):
    """Is the /results/add endpoint really push a new result to database"""
    await post_endpoint_test_handler(cli, "/results/add", json=INSERTED_RESULT)
    mongo_check_update(mongo_db, INSERTED_RESULT, 'results')


@pytest.mark.asyncio
async def test_get_reminders(cli):
    """Is the /reminders endpoint really return the reminders list"""
    await get_endpoint_test_handler(cli, '/reminders', INITIAL_REMINDERS, INITIAL_ID)
