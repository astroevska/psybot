from threading import Timer
from datetime import datetime
from aiogram.types import User
from pymongo import DESCENDING

from ...db.insert import insertUser
from ...init.globals import globalsList
from ...db.update import updateUnfinished
from ...constants.data import TESTS_CONFIG
from ...utils.helpers import getKeyList, getResult
from ...constants.types import TGlobals, TResultData
from ...constants.config import UNFINISHED_SAVE_DELAY
from ...db.get import getResults, getUnfinished, getUser


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


async def clearTestData(user: User):
    globalsIdx = await getOrSetCurrentGlobal(user)

    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']] = []
    globalsList[globalsIdx].currentQuestion = 0
    globalsList[globalsIdx].test_timeout = None


def saveUnfinishedResults(globalsIdx: int, user: User, data: TResultData):
    try:
        updateUnfinished({
            "$set": {
                "datetime": datetime.now(),
                "userId": globalsList[globalsIdx].currentUser,
                "chat_id": user.id,
                "data": data
            }
        }, {
            "chat_id": user.id,
            "test_id": globalsList[globalsIdx].currentTest["_id"]
        })
    except Exception as e:
        print(e)

    clearUnfinishedTimeout(globalsIdx)


def clearUnfinishedTimeout(globalsIdx: int):
    if globalsList[globalsIdx].test_timeout:
        globalsList[globalsIdx].test_timeout.cancel()
        globalsList[globalsIdx].test_timeout = None


def startUnfinishedTimeout(globalsIdx: int, user: User):
    globalsList[globalsIdx].test_timeout = Timer(
        UNFINISHED_SAVE_DELAY, saveUnfinishedResults, args=[globalsIdx, user, globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']]])
    globalsList[globalsIdx].test_timeout.start()


def backToUnfinishedTest(globalsIdx: int, user: User):
    if globalsList[globalsIdx].currentTest['_id'] not in globalsList[globalsIdx].data:
        unfinishedResult = getUnfinished({"chat_id": user.id, "test_id": globalsList[globalsIdx].currentTest["_id"]})

        if unfinishedResult:
            globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']] = unfinishedResult['data']
            globalsList[globalsIdx].currentQuestion = len(unfinishedResult['data']) - 1


def appendAnswer(globalsIdx: int, tag: str):
    if tag:
        globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']].append(int(tag))


def setTest(globalsIdx: int, tag: str):
    if tag:
        globalsList[globalsIdx].currentTest = TESTS_CONFIG[int(tag)]


def setResult(globalsIdx: int):
    globalsList[globalsIdx].result = sum(globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']])
    globalsList[globalsIdx].resultIndex = getResult(
        globalsList[globalsIdx].currentTest['content']['interpretor'], globalsList[globalsIdx].result)


def getPreviousResult(globalsIdx: int, userId: int, testName: str):
    globalsList[globalsIdx].result = getResults({"telegram_id": userId, "test_name": testName}).sort(
            'date', DESCENDING).limit(1)[0]['result']
