from db.main import get_database
from constants.types import TDBFilters, TReminder, TTest, TUser, TUnfinishedTest

def updateReminder(data: TReminder, filters: TDBFilters = {}):
    get_database()["reminders"].update_one(filters, data)

def updateTest(data: TTest, filters: TDBFilters = {}):
    get_database()["tests"].update_one(filters, data)

def updateUser(data: TUser, filters: TDBFilters = {}):
    get_database()["users"].update_one(filters, data)

def updateUnfinished(data: TUnfinishedTest, filters: TDBFilters = {}):
    get_database()["unfinished_tests"].update_one(filters, data, upsert=True)