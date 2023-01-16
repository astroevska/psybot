from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.plot import getPlotImg
from init.globals import globalsList
from constants.data import TESTS_CONFIG
from utils.bot.message import changeMessage
from utils.globals import getOrSetCurrentGlobal
from utils.helpers import getStartMessage, getTag
from utils.bot.keyboard import getButtons, getTestKeyboardFab


async def getStatTest(callback: CallbackQuery):
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    print(callback.data)
    
    await changeMessage(
        callback.message,
        getStartMessage(),
        markup=getTestKeyboardFab(builder, 'stat_', 'exit_full')
    )

    await callback.answer()


async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    tag = getTag(callback.data)

    if tag:
        globalsList[globalsIdx].currentTest = TESTS_CONFIG[int(tag)]

    plot = await getPlotImg(callback.from_user, False)
    await callback.message.answer_photo(
        plot,
        "Динамика вашего психологического состояния.",
        reply_markup=getButtons(callback.data),
    )

    await callback.message.delete()

    await callback.answer()