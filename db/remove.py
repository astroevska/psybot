from typing import Any, Dict
from constants.types import TReminder

from db.main import get_database

def removeReminder(filters: Dict[str, Any] = {}):
    get_database()["reminders"].delete_one(filters)