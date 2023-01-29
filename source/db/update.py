from ..db.main import get_database
from ..constants.types import TDBFilters, TReminder, TTest, TUser, TUnfinishedTest


def updateReminder(filters: TDBFilters, data: TReminder):
    get_database()["reminders"].update_one(filters, data)


def updateTest(filters: TDBFilters, data: TTest):
    get_database()["tests"].update_one(filters, data)


def updateUser(filters: TDBFilters, data: TUser):
    get_database()["users"].update_one(filters, data)


def updateUnfinished(filters: TDBFilters, data: TUnfinishedTest):
    get_database()["unfinished_tests"].update_one(filters, data, upsert=True)
