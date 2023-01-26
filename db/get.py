from pymongo.cursor import Cursor

from db.main import get_database
from constants.types import TDBFilters


def getTests(filters: TDBFilters = {}) -> Cursor:
    return get_database()["tests"].find(filters)


def getResults(filters: TDBFilters = {}) -> Cursor:
    return get_database()["results"].find(filters)


def getUsers(filters: TDBFilters = {}) -> Cursor:
    return get_database()["users"].find(filters)


def getUser(filters: TDBFilters = {}) -> Cursor:
    return get_database()["users"].find_one(filters)


def getReminders(filters: TDBFilters = {}) -> Cursor:
    return get_database()["reminders"].find(filters)


def getUnfinished(filters: TDBFilters = {}) -> Cursor:
    return get_database()["unfinished_tests"].find_one(filters)


def getButtons(filters: TDBFilters = {}) -> Cursor:
    return get_database()["buttons"].find(filters)


def getTranslates(filters: TDBFilters = {}) -> Cursor:
    return get_database()["texts"].find(filters)
