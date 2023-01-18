from pymongo import MongoClient

from constants.config import MONGODB_CONNECTION


def get_database() -> MongoClient:
    client = MongoClient(MONGODB_CONNECTION)

    return client['psybot']


if __name__ == "__main__":
    dbname = get_database()
