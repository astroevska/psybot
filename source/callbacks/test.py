from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..utils.helpers import getTag
from ..init.globals import globalsList
from ..constants.data import TESTS_CONFIG
from ..utils.bot.helpers import changeMessage
from ..utils.bot.keyboard import getButtons, getAnswersKeyboardFab
from ..utils.bot.handlers import handleFirstQuestion, handleLastQuestion
from ..utils.bot.globals import appendAnswer, backToUnfinishedTest, getOrSetCurrentGlobal, clearTestData, clearUnfinishedTimeout, startUnfinishedTimeout


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

    backToUnfinishedTest(globalsIdx, callback.from_user)
    clearUnfinishedTimeout(globalsIdx)

    if globalsList[globalsIdx].currentQuestion == 0 and not globalsList[globalsIdx].currentStartMessage:
        return await handleFirstQuestion(callback)
    elif globalsList[globalsIdx].currentQuestion == len(globalsList[globalsIdx].currentTest['content']['questions']):
        return await handleLastQuestion(callback)

    appendAnswer(globalsIdx, tag)

    startUnfinishedTimeout(globalsIdx, callback.from_user)

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
