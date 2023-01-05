import asyncio
import logging
from typing import Coroutine
from functools import reduce

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from datetime import datetime
from dateutil import parser

from db.insert import insertUser, insertReminder
from db.update import updateReminder
from db.remove import removeReminder
from db.get import getUsers, getReminders
from init.globals import globals
from constants.config import API_TOKEN
from constants.data import TESTS_CONFIG
from utils.bot.keyboard import getButtons
from utils.plot import savePlot, getPlot, editPlotFigure
from utils.bot.message import changeMessage, clearStartMessage
from utils.helpers import getStartMessage, getTag, clearTestData
from utils.bot.handlers import handleFirstQuestion, handleLastQuestion
from utils.datetime import nextDateByPeriod

# logging
logging.basicConfig(level=logging.INFO)
# bot object
bot = Bot(token=API_TOKEN, parse_mode="HTML")
# bot dispatcher
dp = Dispatcher()

# bot methods
@dp.message(Command(commands=['start']))
async def startBot(message: Message):
    try:
        user = list(getUsers({"telegram_id": message.from_user.id}))
        if len(user) == 0:
            insertUser({
                "telegram_id": message.from_user.id, 
                "name": message.from_user.first_name, 
                "telegram_username": message.from_user.username
            })
        else:
            globals.currentUser = user[0]["_id"]
    except: 
        print("Error")
        
    await message.reply(
        f"Привет, {message.from_user.first_name}!\n\nНе секрет, что многие разработчики сталкиваются с выгоранием, тревогой и депрессией. Этот бот призван помочь вам отслеживать свое психологическое состояние и предлагает несколько психологических тестов. Бот будет сохранять ваши результаты, и вы сможете отслеживать динамику изменения своего состояния на длительных промежутках. Это поможет вам вовремя заметить ухудшение или понять, какие факторы идут вам на пользу, а какие во вред.",
        reply_markup=getButtons('init')
    )

@dp.callback_query(Text(text="start"))
async def startBot(callback: CallbackQuery):
    await callback.message.reply(
        getStartMessage(),
        reply_markup=getButtons('start')
    )

    await callback.answer()

@dp.callback_query(Text(startswith="test_"))
async def chooseTest(callback: CallbackQuery) -> AnswerCallbackQuery:
    globals.currentTest = TESTS_CONFIG[int(getTag(callback.data))]
        
    await changeMessage(
        callback,
        f"<b>{globals.currentTest['name']}</b>\n\n{globals.currentTest['description']}",
        markup=getButtons(callback.data)
    )
    
    await callback.answer()

@dp.callback_query(Text(startswith="next_"))
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

@dp.callback_query(Text(text="stat"))
async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    await callback.message.answer_photo(
        savePlot(editPlotFigure(getPlot(globals.currentTest['content']['interpretor'], globals.currentTest["name"], callback.from_user.id, isCurrent=True, isResponsibleX=True), align="center")),
        caption="Динамика вашего психологического состояния",
        reply_markup=getButtons(callback.data)
    )
    
    await callback.answer()

@dp.callback_query(Text(text="stat_choice"))
async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    await callback.message.answer_photo(
        savePlot(editPlotFigure(getPlot(globals.currentTest['content']['interpretor'], globals.currentTest["name"], callback.from_user.id, isCurrent=False, isResponsibleX=True), align="center")),
        caption="Динамика вашего психологического состояния",
        reply_markup=getButtons(callback.data)
    )
    
    await callback.answer()

@dp.callback_query(Text(startswith="exit_"))
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
        "Посмотрите статистику, настройте уведомления или начните тест.",
        reply_markup=markup
    )
    
    await callback.answer()

@dp.callback_query(Text(text='reminder'))
async def getStatistics(callback: CallbackQuery) -> AnswerCallbackQuery:
    if globals.currentUser == '':
        globals.currentUser = getUsers({"telegram_id": callback.from_user.id})[0]["_id"]

    userReminders = reduce(lambda a, b: f"{a}\nПериод: {b['period']}\nСледующее напоминание: {b['next']}\n", list(getReminders({"user_id": globals.currentUser})), "")

    await changeMessage(
            callback,
            f"Вы можете настроить персональные напоминания о прохождении теста, чтобы регулярно отслеживать свое психологическое состояние. \n\n<b>Ваши напоминания:\n</b>{userReminders}\n Пожалуйста, выберите периодичность напоминаний: ",
            markup=getButtons(callback.data)
        )

    return await callback.answer()

@dp.callback_query(Text(text='remove_reminder'))
async def deleteReminder(callback: CallbackQuery) -> AnswerCallbackQuery:
    userReminders = list(getReminders({
        "chat_id": callback.from_user.id
    }))

    try:
        removeReminder()
    except:
        print("Remove error")
    
    await changeMessage(
            callback,
            f"Вы удалили напоминания.",
            markup=getButtons(callback.data)
        )

    return await callback.answer()
    

@dp.callback_query(Text(startswith="every_"))
async def setReminder(callback: CallbackQuery) -> AnswerCallbackQuery:  
    markup = getButtons("init")
    reminder_type = getTag(callback.data)

    if globals.currentUser == '':
        globals.currentUser = getUsers({"telegram_id": callback.from_user.id})[0]["_id"]

    try:
        insertReminder({
            "user_id": globals.currentUser, 
            "period": reminder_type, 
            "chat_id": callback.from_user.id, 
            "next": nextDateByPeriod(reminder_type)
        })
    except:
        print('Error')
    
    if reminder_type == 'day':
        await changeMessage(
            callback,
            "Вы установили напоминания на каждый день.",
            markup=markup
        )
    elif reminder_type == 'week':
        await changeMessage(
            callback,
            "Вы установили напоминания на каждую неделю.",
            markup=markup
        )
    elif reminder_type == '2weeks':
        await changeMessage(
            callback,
            "Вы установили напоминания два раза в месяц.",
            markup=markup
        )
    elif reminder_type == 'month':
        await changeMessage(
            callback,
            "Вы установили напоминания раз в месяц.",
            markup=markup
        )

    return await callback.answer()


async def sendMessage(chat_id: int, text: str):
    await bot.send_message(chat_id, text)


async def scheduleReminders() -> Coroutine: 
    now = datetime.utcnow()
    tomorrow = now + datetime.timedelta(days=1)
    start_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
    end_time = start_time + datetime.timedelta(days=1)

    currentReminders = list(getReminders({"next": {
        '$gte': start_time,
        '$lt': end_time
    }}))

    # TODO: plan next day reminders (parse time)
    # TODO: handle cases when we start this function today and today reminders is expired (maybe we need to get not today reminders but tomorrow), also be careful with date of time
    # TODO: insert to database new next datetime after task creating
    # TODO: add middleware state with list of current user reminders with buttons: create new reminder and remove reminder. 
    # Remove will be with buttons with each reminder. Pushing button will delete it from database.
    # Add will open current reminders state
    
    if len(currentReminders) != 0:
        for r in currentReminders:
            nextDateTime = parser.parse(r['next'])
            await asyncio.sleep(nextDateTime - now)
            
            try:
                updateReminder({"$set": {**r, "next": nextDateByPeriod(r['period'], nextDateTime)}}, {'_id': r['_id']})
            except:
                print('Update error.')
            
            asyncio.create_task(sendMessage(r['chat_id'], f"Время проверить свое психологическое состояние!\nСледующее напоминание будет {nextDateTime}"))
            


async def scheduleCheckReminders() -> Coroutine: 
    while True:
        await asyncio.sleep(86400)
        asyncio.create_task(scheduleReminders())


async def main() -> Coroutine:
    await dp.start_polling(bot)
    
