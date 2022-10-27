from typing import Any, Dict
from pymongo.cursor import Cursor

from db.main import get_database


def getTests(filters: Dict[str, Any] = {}) -> Cursor:
    return get_database()["tests"].find(filters)

def getResults(filters: Dict[str, Any] = {}) -> Cursor:
    return get_database()["results"].find(filters)