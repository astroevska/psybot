from constants.types import TResult, TTest, TUser, TReminder

from db.main import get_database


async def insertTest(data: TTest):
    await get_database()["tests"].insert_one(data)

async def insertResult(data: TResult):
    await get_database()["results"].insert_one(data)

async def insertUser(data: TUser):
    await get_database()["users"].insert_one(data)

async def insertReminder(data: TReminder):
    await get_database()["reminders"].insert_one(data)