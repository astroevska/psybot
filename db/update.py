from typing import Any, Dict
from constants.types import TReminder

from db.main import get_database

def updateReminder(data: TReminder, filters: Dict[str, Any] = {}):
    get_database()["reminders"].update_one(filters, data)