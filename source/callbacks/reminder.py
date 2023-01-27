from dateutil import parser
from pymongo import ASCENDING
from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from source.db.get import getReminders
from source.db.remove import removeReminder
from source.db.insert import insertReminder

from source.utils.helpers import getTag
from source.init.globals import globalsList
from source.utils.datetime import nextDateByPeriod
from source.utils.bot.handlers import remindersHandler
from source.utils.bot.globals import getOrSetCurrentGlobal
from source.utils.bot.helpers import changeMessage, getReminderPeriodName
from source.utils.bot.keyboard import getButtons, getRemindersKeyboardFab


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
    text = getReminderPeriodName(reminder_type)

    await changeMessage(
        callback.message,
        text,
        markup=markup
    )

    return await callback.answer()
