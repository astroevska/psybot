from datetime import datetime
from aiogram.types import User, InlineKeyboardMarkup,  Message

from init.globals import globalsList
from db.update import updateUnfinished
from constants.data import TESTS_CONFIG
from constants.types import TResultData
from utils.globals import getOrSetCurrentGlobal


async def clearStartMessage(globalsIdx: int):    
    await globalsList[globalsIdx].currentStartMessage.delete()
    
    globalsList[globalsIdx].currentStartMessage = None


async def changeMessage(message: Message, text: str, markup: InlineKeyboardMarkup, photo = None):
    if message.photo:
        await message.answer(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)


def getStartMessage() -> str:
    startText = f"На данный момент в боте доступны следующие тесты:\n\n"
    for i in range(len(TESTS_CONFIG)):
        startText += f"<b>{i + 1}. {TESTS_CONFIG[i]['name']}</b>\n"

    startText += "\nВы можете выбрать любой из них, пройти его, а в дальнейшем отслеживать динамику изменений своего психологического состояния. Тесты постоянно дополняются."
    return startText


def getHelpMessage() -> str:
    return "Ваше состояние вызывает озабоченность. Вам стоит продолжить за ним наблюдать, а также по возможности обратиться к специалисту."


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

    globalsList[globalsIdx].test_timeout.cancel()
    globalsList[globalsIdx].test_timeout = None


async def clearTestData(user: User):
    globalsIdx = await getOrSetCurrentGlobal(user)

    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']] = []
    globalsList[globalsIdx].currentQuestion = 0
    globalsList[globalsIdx].test_timeout = None