from typing import Any, Dict
from constants.types import TReminder, TTest, TUser

from db.main import get_database

def updateReminder(data: TReminder, filters: Dict[str, Any] = {}):
    get_database()["reminders"].update_one(filters, data)

def updateTest(data: TTest, filters: Dict[str, Any] = {}):
    get_database()["tests"].update_one(filters, data)

def updateUser(data: TUser, filters: Dict[str, Any] = {}):
    get_database()["users"].update_one(filters, data)