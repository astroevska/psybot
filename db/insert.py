from constants.types import TResult, TTest

from db.main import get_database


def insertTest(data: TTest):
    get_database()["tests"].insert_one(data)

def insertResult(data: TResult):
    get_database()["results"].insert_one(data)