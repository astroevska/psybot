from constants.types import TResult, TTest, TUser, TReminder

from db.main import get_database


def insertTest(data: TTest):
    get_database()["tests"].insert_one(data)

def insertResult(data: TResult):
    get_database()["results"].insert_one(data)

def insertUser(data: TUser):
    get_database()["users"].insert_one(data)

def insertReminder(data: TReminder):
    get_database()["reminders"].insert_one(data)