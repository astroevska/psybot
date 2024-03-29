from pymongo.cursor import Cursor

from ..db.main import get_database
from ..constants.types import TDBFilters


def getTests(filters: TDBFilters = {}) -> Cursor:
    return get_database()["tests"].find(filters)


def getTest(filters: TDBFilters = {}) -> Cursor:
    return get_database()["tests"].find_one(filters)


def getResults(filters: TDBFilters = {}) -> Cursor:
    return get_database()["results"].find(filters)

def getResult(filters: TDBFilters = {}) -> Cursor:
    return get_database()["results"].find_one(filters)


def getUsers(filters: TDBFilters = {}) -> Cursor:
    return get_database()["users"].find(filters)


def getUser(filters: TDBFilters = {}) -> Cursor:
    return get_database()["users"].find_one(filters)


def getReminders(filters: TDBFilters = {}) -> Cursor:
    return get_database()["reminders"].find(filters)


def getReminder(filters: TDBFilters = {}) -> Cursor:
    return get_database()["reminders"].find_one(filters)


def getUnfinished(filters: TDBFilters = {}) -> Cursor:
    return get_database()["unfinished_tests"].find_one(filters)


def getButtons(filters: TDBFilters = {}) -> Cursor:
    return get_database()["buttons"].find(filters)


def getButton(filters: TDBFilters = {}) -> Cursor:
    return get_database()["buttons"].find_one(filters)
