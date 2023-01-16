from aiogram.types import User

from db.get import getUser
from db.insert import insertUser
from init.globals import globalsList
from constants.types import TGlobals
from utils.helpers import getKeyList
from constants.data import TESTS_CONFIG


def addNewGlobal() -> TGlobals:
    return TGlobals(**{
        'currentTest': TESTS_CONFIG[0],
        'data': dict(),
        'currentUser': "",
        'currentStartMessage': None,
        'test_timeout': None,
        'currentChatId': 0,
        'currentQuestion': 0,
        'result': 0,
        'resultIndex': 0
    })


async def getOrSetUser(telegramUser: User) -> str:
    try:
        user = getUser({"telegram_id": telegramUser.id})
    except Exception as e:
        print(e)

    if not user:
        userId = insertUser({
            "telegram_id": telegramUser.id,
            "name": telegramUser.first_name,
            "telegram_username": telegramUser.username
        })
    else:
        userId = user['_id']

    userId = str(userId)

    return userId


async def getOrSetCurrentGlobal(telegramUser: User) -> str:
    users = getKeyList(globalsList, 'currentChatId')
    userPosition = None

    if telegramUser.id not in users:
        userId = await getOrSetUser(telegramUser)

        userGlobal = addNewGlobal()
        userGlobal.currentUser = userId
        userGlobal.currentChatId = telegramUser.id
        userPosition = len(globalsList)
        globalsList.append(userGlobal)
    else:
        userPosition = users.index(telegramUser.id)

    return userPosition
