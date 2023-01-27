from typing import Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from ..constants.config import MONGODB_CONNECTION


def get_database() -> Database[Any]:
    client: MongoClient = MongoClient(MONGODB_CONNECTION)

    return client['psybot']


if __name__ == "__main__":
    dbname = get_database()
