import logging

from dateutil import parser
from threading import Timer
from typing import Coroutine
from pymongo import ASCENDING

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from db.get import getReminders
from db.remove import removeReminder
from db.insert import insertReminder

from init.globals import globalsList
from constants.config import API_TOKEN
from constants.data import TESTS_CONFIG
from constants.types import TSendMessage

from utils.plot import getPlotImg
from utils.bot.keyboard import getButtons
from utils.datetime import nextDateByPeriod
from utils.globals import getOrSetCurrentGlobal
from utils.bot.message import changeMessage, clearStartMessage
from utils.bot.handlers import handleFirstQuestion, handleLastQuestion, remindersHandler
from utils.helpers import getStartMessage, getTag, clearTestData, insertUnfinishedResults


# logging
logging.basicConfig(level=logging.INFO)
# bot object
bot = Bot(token=API_TOKEN, parse_mode="HTML")
# bot dispatcher
dp = Dispatcher()


# bot methods
@dp.message(Command(commands=['start']))
async def startBot(message: Message):
    await getOrSetCurrentGlobal(message.from_user)

    await message.reply(
        f"Привет, {message.from_user.first_name}!\n\nНе секрет, что многие разработчики сталкиваются с выгоранием, тревогой и депрессией. Этот бот призван помочь вам отслеживать свое психологическое состояние и предлагает несколько психологических тестов. Бот будет сохранять ваши результаты, и вы сможете отслеживать динамику изменения своего состояния на длительных промежутках. Это поможет вам вовремя заметить ухудшение или понять, какие факторы идут вам на пользу, а какие во вред.",
        reply_markup=getButtons('init')
    )


@dp.callback_query(Text(text="start"))
async def startBot(callback: CallbackQuery):
    await changeMessage(
        callback.message,
        getStartMessage(),
        markup=getButtons('start') if callback.message.photo else getButtons('start')
    )

    await callback.answer()


@dp.callback_query(Text(startswith="test_"))
async def chooseTest(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    globalsList[globalsIdx].currentTest = TESTS_CONFIG[int(getTag(callback.data))]

    await changeMessage(
        callback.message,
        f"<b>{globalsList[globalsIdx].currentTest['name']}</b>\n\n{globalsList[globalsIdx].currentTest['description']}",
        markup=getButtons(callback.data)
    )

    await callback.answer()


@dp.callback_query(Text(startswith="next_"))
async def setAnswer(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    if globalsList[globalsIdx].test_timeout:
        globalsList[globalsIdx].test_timeout.cancel()
        globalsList[globalsIdx].test_timeout = None

    if globalsList[globalsIdx].currentQuestion == None or globalsList[globalsIdx].currentQuestion == 0:
        return await handleFirstQuestion(callback)

    if globalsList[globalsIdx].currentQuestion == len(globalsList[globalsIdx].currentTest['content']['questions']):
        return await handleLastQuestion(callback)

    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']].append(
        int(getTag(callback.data)))

    globalsList[globalsIdx].test_timeout = Timer(
        10, insertUnfinishedResults, args=[globalsIdx, callback.from_user, globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']]])
    globalsList[globalsIdx].test_timeout.start()

    try:
        await changeMessage(
            callback.message,
            "\n".join([f"<b>{i})</b> {x}" for i, x in enumerate(globalsList[globalsIdx].currentTest['content']
                                                                ['questions'][globalsList[globalsIdx].currentQuestion])]),
            getButtons(callback.data, currentTest=globalsList[globalsIdx].currentTest,
                       currentQuestion=globalsList[globalsIdx].currentQuestion)
        )
    except Exception as e:
        print(e)

    globalsList[globalsIdx].currentQuestion += 1

    await callback.answer()


@dp.callback_query(Text(text="stat"))
async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    plot = await getPlotImg(callback.from_user, False)

    await callback.message.answer_photo(
        plot,
        "Динамика вашего психологического состояния.",
        reply_markup=getButtons(callback.data),
    )

    await callback.message.delete()

    await callback.answer()


@dp.callback_query(Text(startswith="exit_"))
async def exitTest(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    tag = getTag(callback.data)
    markup: InlineKeyboardMarkup = getButtons(tag)

    if globalsList[globalsIdx].currentStartMessage:
        await clearStartMessage(globalsIdx)
        await clearTestData(callback.from_user)

    if tag == 'simple':
        await changeMessage(
            callback.message,
            "Вы закончили прохождение теста. Если захотите пройти заново, нажмите на кнопку <b>Пройти тест</b>.",
            markup=markup
        )

        return await callback.answer()

    if tag == 'fullPhoto':
        await callback.message.answer(
            "Вы посмотрели статистику. Если хотите пройти один из наших психологических тестов, нажмите на кнопку <b>Выбрать тест</b>.\n\nЕсли хотите, чтобы бот напоминал вам проходить тесты раз в определенный период, выберите кнопку <b>Напоминания</b>.",
            reply_markup=markup
        )

        await callback.message.delete()

        return await callback.answer()

    if tag == 'photo':
        await callback.message.answer(
            "Вы закончили прохождение теста. Если хотите отслеживать свое состояние регулярно, вы можете попросить бота присылать вам уведомления раз в определенный период. Для этого нажмите кнопку <b>Напоминания</b>.\nТакже вы можете ознакомиться с другими нашими тестами.",
            reply_markup=markup
        )

        return await callback.answer()

    await changeMessage(
        callback.message,
        "Если хотите пройти один из наших психологических тестов, нажмите на кнопку <b>Выбрать тест</b>.\n\nЕсли хотите, чтобы бот напоминал вам проходить тесты раз в определенный период, выберите кнопку <b>Напоминания</b>.\n\nВы также можете посмотреть статистику всех пройденных тестов, чтобы оценить динамику собственного психологического состояния.",
        markup=markup
    )

    await callback.answer()


@dp.callback_query(Text(text='reminder'))
async def showReminders(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    userReminders = list(getReminders({
        "user_id": globalsList[globalsIdx].currentUser
    }).sort([("next", ASCENDING)]))

    return await remindersHandler(callback, userReminders)


@dp.callback_query(Text(startswith='removeReminder'))
async def deleteReminder(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    reminder = getTag(callback.data)

    if (reminder):
        removeReminder({"next": parser.parse(reminder)})

    userReminders = list(getReminders({
        "user_id": globalsList[globalsIdx].currentUser
    }).sort([("next", ASCENDING)]))

    hasReminders = len(userReminders) > 0

    if hasReminders:
        await changeMessage(
            callback.message,
            callback.message.text if reminder else 'Выберите, какой ремайндер вы хотите удалить.',
            markup=getButtons('removeReminder', reminders=userReminders)
        )

    return await remindersHandler(callback, userReminders, not hasReminders)


@dp.callback_query(Text(startswith="every_"))
async def setReminder(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    reminder_type = getTag(callback.data)

    try:
        await insertReminder({
            "user_id": globalsList[globalsIdx].currentUser,
            "period": reminder_type,
            "chat_id": callback.from_user.id,
            "next": nextDateByPeriod(reminder_type)
        })
    except Exception as e:
        print(e)

    markup = getButtons("init")
    text = "Вы установили напоминание "

    if reminder_type == 'day':
        text += "на каждый день"
    elif reminder_type == 'week':
        text += "на каждую неделю"
    elif reminder_type == '2weeks':
        text += "два раза в месяц"
    elif reminder_type == 'month':
        text += "раз в месяц"

    await changeMessage(
        callback.message,
        text,
        markup=markup
    )

    return await callback.answer()


async def sendMessage(data: TSendMessage):
    await bot.send_message(data["chat_id"], data["text"])


async def main() -> Coroutine:
    await dp.start_polling(bot)
