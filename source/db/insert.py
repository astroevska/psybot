from source.db.main import get_database
from source.constants.types import TResult, TTest, TUser, TReminder, TUnfinishedTest


def insertTest(data: TTest):
    get_database()["tests"].insert_one(data)


def insertResult(data: TResult):
    return get_database()["results"].insert_one(data)


def insertUser(data: TUser):
    return get_database()["users"].insert_one(data).inserted_id


def insertReminder(data: TReminder):
    get_database()["reminders"].insert_one(data)


def insertUnfinished(data: TUnfinishedTest):
    get_database()["unfinished_tests"].insert_one(data)
