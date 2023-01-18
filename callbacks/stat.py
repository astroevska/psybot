from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils import i18n
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.helpers import getTag
from utils.plot import getPlotImg
from utils.bot.globals import getOrSetCurrentGlobal, setTest
from utils.bot.helpers import changeMessage, getStartMessage
from utils.bot.keyboard import getButtons, getTestKeyboardFab


async def getStatTest(callback: CallbackQuery):
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    await changeMessage(
        callback.message,
        getStartMessage(),
        markup=getTestKeyboardFab(builder, 'stat_', 'exit_full')
    )

    await callback.answer()


async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    setTest(globalsIdx, getTag(callback.data))

    plot = await getPlotImg(callback.from_user, False)
    await callback.message.answer_photo(
        plot,
        "Динамика вашего психологического состояния.",
        reply_markup=getButtons(callback.data),
    )

    await callback.message.delete()

    await callback.answer()
