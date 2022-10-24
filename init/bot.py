import logging
from typing import Coroutine

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from init.globals import globals
from utils.bot.keyboard import getButtons
from constants.config import API_TOKEN, TESTS_CONFIG
from utils.plot import savePlot, getPlot, editPlotFigure
from utils.bot.message import changeMessage, clearStartMessage
from utils.helpers import getStartMessage, getTag, clearTestData
from utils.bot.handlers import handleFirstQuestion, handleLastQuestion


# logging
logging.basicConfig(level=logging.INFO)
# bot object
bot = Bot(token=API_TOKEN, parse_mode="HTML")
# bot dispatcher
dp = Dispatcher()

# bot methods
@dp.message(commands=['start'])
async def startBot(message: Message):
    await message.reply(
        f"Привет, {message.from_user.first_name}!\n\nНе секрет, что многие разработчики сталкиваются с выгоранием, тревогой и депрессией. Этот бот призван помочь вам отслеживать свое психологическое состояние и предлагает несколько психологических тестов. Бот будет сохранять ваши результаты, и вы сможете отслеживать динамику изменения своего состояния на длительных промежутках. Это поможет вам вовремя заметить ухудшение или понять, какие факторы идут вам на пользу, а какие во вред.",
        reply_markup=getButtons('init')
    )

@dp.callback_query(text="start")
async def startBot(callback: CallbackQuery):
    await callback.message.reply(
        getStartMessage(),
        reply_markup=getButtons('start')
    )

    await callback.answer()

@dp.callback_query(Text(text_startswith="test_"))
async def chooseTest(callback: CallbackQuery) -> AnswerCallbackQuery:
    globals.currentTest = TESTS_CONFIG[int(getTag(callback.data))]
        
    await changeMessage(
        callback,
        f"<b>{globals.currentTest['name']}</b>\n\n{globals.currentTest['description']}",
        markup=getButtons(callback.data)
    )
    
    await callback.answer()

@dp.callback_query(Text(text_startswith="next_"))
async def setAnswer(callback: CallbackQuery) -> AnswerCallbackQuery:
    if globals.currentQuestion == 0:
        return await handleFirstQuestion(callback)

    if globals.currentQuestion == len(globals.currentTest['content']['questions']):
        return await handleLastQuestion(callback)

    globals.data[callback.from_user.id].append(int(getTag(callback.data)))

    await changeMessage(
        callback,
        "\n".join([f"<b>{i})</b> {x}" for i,x in enumerate(globals.currentTest['content']['questions'][globals.currentQuestion])]),
        getButtons(callback.data, currentQuestion=globals.currentQuestion)
    )

    globals.currentQuestion += 1

    await callback.answer()

@dp.callback_query(text="stat")
async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    await callback.message.answer_photo(
        savePlot(editPlotFigure(getPlot(globals.currentTest['content']['interpretor'], isStyled=True), align="center")),
        caption="Динамика вашего психологического состояния",
        reply_markup=getButtons(callback.data)
    )
    
    await callback.answer()

@dp.callback_query(Text(text_startswith="exit_"))
async def exitTest(callback: CallbackQuery) -> AnswerCallbackQuery:    
    markup: InlineKeyboardMarkup = getButtons(callback.data)
    
    if globals.currentStartMessage:
        await clearStartMessage()
        clearTestData(callback.from_user.id)

    if getTag(callback.data) == 'simple':
        await changeMessage(
            callback,
            "Вы закончили прохождение теста. Если захотите пройти заново, нажмите на кнопку <b>Пройти тест</b>.",
            markup=markup
        )

        return await callback.answer()

    await callback.message.reply(
        "Вы закончили прохождение теста. Если захотите пройти заново, нажмите на кнопку <b>Пройти тест</b>.",
        reply_markup=markup
    )
    
    await callback.answer()


async def main() -> Coroutine:
    await dp.start_polling(bot)
