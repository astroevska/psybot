from threading import Timer
from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from init.globals import globalsList
from constants.data import TESTS_CONFIG
from utils.bot.message import changeMessage
from utils.globals import getOrSetCurrentGlobal
from utils.bot.keyboard import getButtons, getAnswersKeyboardFab
from utils.bot.handlers import handleFirstQuestion, handleLastQuestion
from utils.helpers import getTag, insertUnfinishedResults, clearTestData


async def chooseTest(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    await clearTestData(callback.from_user)

    globalsList[globalsIdx].currentTest = TESTS_CONFIG[int(getTag(callback.data))]

    await changeMessage(
        callback.message,
        f"<b>{globalsList[globalsIdx].currentTest['name']}</b>\n\n{globalsList[globalsIdx].currentTest['description']}",
        markup=getButtons(callback.data, message=callback.message)
    )

    await callback.answer()


async def setAnswer(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    tag = getTag(callback.data)

    if globalsList[globalsIdx].test_timeout:
        globalsList[globalsIdx].test_timeout.cancel()
        globalsList[globalsIdx].test_timeout = None

    if globalsList[globalsIdx].currentQuestion == 0 and not globalsList[globalsIdx].currentStartMessage:
        return await handleFirstQuestion(callback)
    elif globalsList[globalsIdx].currentQuestion == len(globalsList[globalsIdx].currentTest['content']['questions']):
        return await handleLastQuestion(callback)

    if tag:
        globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']].append(int(tag))

    globalsList[globalsIdx].test_timeout = Timer(
        10, insertUnfinishedResults, args=[globalsIdx, callback.from_user, globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']]])
    globalsList[globalsIdx].test_timeout.start()

    try:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        await changeMessage(
            callback.message,
            "\n".join([f"<b>{i})</b> {x}" for i, x in enumerate(globalsList[globalsIdx].currentTest['content']
                                                                ['questions'][globalsList[globalsIdx].currentQuestion])]),
            getAnswersKeyboardFab(builder, len(globalsList[globalsIdx]['currentTest']['content']['questions'][globalsList[globalsIdx].currentQuestion]))
        )
    except Exception as e:
        print(e)

    globalsList[globalsIdx].currentQuestion += 1

    await callback.answer()