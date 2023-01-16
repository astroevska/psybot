from db.main import get_database
from constants.types import TDBFilters

def removeReminder(filters: TDBFilters = {}):
    get_database()["reminders"].delete_one(filters)

def removeUnfinished(filters: TDBFilters = {}):
    get_database()["unfinished_tests"].delete_one(filters)