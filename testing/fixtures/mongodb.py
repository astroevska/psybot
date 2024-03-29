import pytest
from mongomock import MongoClient

from testing.mocks.constants import INITIAL_BUTTONS, INITIAL_REMINDERS, INITIAL_RESULTS, INITIAL_TESTS, INITIAL_UNFINISHED_TESTS, INITIAL_USERS


@pytest.fixture
def mongo_uri():
    return "mongodb://localhost:27017/test_db"


@pytest.fixture
def mongo_db(mongo_uri):
    client = MongoClient(mongo_uri)
    yield client.test_db
    client.close()


@pytest.fixture(autouse=True)
def print_test_docstring(request):
    print(f"\n\033[1m\033[34mDESCRIPTION:\033[0m \033[33m\033[1m{request.function.__doc__}\033[0m")


@pytest.fixture(autouse=True)
def setup_test_data(mongo_db):
    for t in INITIAL_TESTS:
        mongo_db.tests.insert_one(t)
    for u in INITIAL_USERS:
        mongo_db.users.insert_one(u)
    for r in INITIAL_RESULTS:
        mongo_db.results.insert_one(r)
    for e in INITIAL_REMINDERS:
        mongo_db.reminders.insert_one(e)
    for n in INITIAL_UNFINISHED_TESTS:
        mongo_db.unfinished_tests.insert_one(n)
    for b in INITIAL_BUTTONS:
        mongo_db.buttons.insert_one(b)
