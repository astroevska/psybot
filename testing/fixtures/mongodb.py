import pytest
from mongomock import MongoClient

from testing.mocks.constants import INITIAL_TEST


@pytest.fixture
def mongo_uri():
    return "mongodb://localhost:27017/test_db"


@pytest.fixture
def mongo_db(mongo_uri):
    client = MongoClient(mongo_uri)
    yield client.test_db
    client.close()


@pytest.fixture(autouse=True)
def setup_test_data(mongo_db):
    mongo_db.tests.insert_one(INITIAL_TEST)


@pytest.fixture(autouse=True)
def teardown_test_data(mongo_db):
    mongo_db.tests.delete_many({})
