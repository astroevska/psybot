from pymongo.results import InsertOneResult

from ..db.main import get_database
from ..constants.types import TResult, TTest, TUser, TReminder, TUnfinishedTest


def insertTest(data: TTest) -> InsertOneResult:
    return get_database()["tests"].insert_one(data)


def insertResult(data: TResult) -> InsertOneResult:
    return get_database()["results"].insert_one(data)


def insertUser(data: TUser) -> InsertOneResult:
    return get_database()["users"].insert_one(data).inserted_id


def insertReminder(data: TReminder) -> InsertOneResult:
    return get_database()["reminders"].insert_one(data)


def insertUnfinished(data: TUnfinishedTest) -> InsertOneResult:
    return get_database()["unfinished_tests"].insert_one(data)
