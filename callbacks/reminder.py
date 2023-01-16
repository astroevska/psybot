from dateutil import parser
from pymongo import ASCENDING
from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.get import getReminders
from db.remove import removeReminder
from db.insert import insertReminder

from utils.helpers import getTag
from init.globals import globalsList
from utils.datetime import nextDateByPeriod
from utils.bot.helpers import changeMessage
from utils.bot.handlers import remindersHandler
from utils.globals import getOrSetCurrentGlobal
from utils.bot.keyboard import getButtons, getRemindersKeyboardFab


async def showReminders(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    userReminders = list(getReminders({
        "user_id": globalsList[globalsIdx].currentUser
    }).sort([("next", ASCENDING)]))

    return await remindersHandler(callback, userReminders)


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
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        
        await changeMessage(
            callback.message,
            callback.message.text if reminder else 'Выберите, какой ремайндер вы хотите удалить.',
            markup=getRemindersKeyboardFab(builder, userReminders)
        )

    return await remindersHandler(callback, userReminders, not hasReminders)


async def setReminder(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    reminder_type = getTag(callback.data)

    try:
        insertReminder({
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