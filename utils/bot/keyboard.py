from typing import List, Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from init.globals import globals
from dateutil import parser
from constants.types import TTest
from constants.data import TESTS_CONFIG


def getTestKeyboardFab(builder: InlineKeyboardBuilder, tests: List[TTest]) -> InlineKeyboardMarkup:
    for i in range(len(tests)):
        builder.add(
            InlineKeyboardButton(
                text=tests[i]['name'],
                callback_data=f"test_{i}"
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="Выход",
            callback_data="exit_full"
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def getAnswersKeyboardFab(builder: InlineKeyboardBuilder, length: int) -> InlineKeyboardMarkup:
    for i in range(length):
        builder.add(
            InlineKeyboardButton(
                text=str(i),
                callback_data=f"next_{i}"
            )
        )
    
    builder.add(
        InlineKeyboardButton(
            text="Выход",
            callback_data="exit_simple"
        )
    )
    
    builder.adjust(length)
    return builder.as_markup()

def getRemindersKeyboardFab(builder: InlineKeyboardBuilder, reminders: list) -> InlineKeyboardMarkup:
    for reminder in reminders:
        builder.add(
            InlineKeyboardButton(
                text=str(f"🔔 {reminder['next'].date()}  |  {reminder['period']} 🔄"),
                callback_data=f"removeReminder_{reminder['next']}"
            )
        )
    
    builder.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="reminder"
        )
    )
    
    builder.adjust(1)
    return builder.as_markup()

def getButtons(target: str, **args: Any) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if target == 'init':
        builder.add(
            InlineKeyboardButton(
                text="Выбрать тест",
                callback_data="start"
            ),
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stat_choice"
            ),
            InlineKeyboardButton(
                text = "Напоминания",
                callback_data="reminder"
            )
        )
        return builder.as_markup()

    if target == 'start':
        return getTestKeyboardFab(builder, TESTS_CONFIG)

    if target == 'stat_choice':
        builder.add(
            InlineKeyboardButton(
                text="Выход",
                callback_data="exit_full"
            )
        )
        return builder.as_markup()

    if target == 'reminder':
        builder.add(
            InlineKeyboardButton(
                text="Ежедневно",
                callback_data="every_day"
            ),
            InlineKeyboardButton(
                text="Каждую неделю",
                callback_data="every_week"
            ),
            InlineKeyboardButton(
                text="2 раза в месяц",
                callback_data="every_2weeks"
            ),
            InlineKeyboardButton(
                text="Каждый месяц",
                callback_data="every_month"
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data="removeReminder"
            ),
            InlineKeyboardButton(
                text="Выход",
                callback_data="exit_full"
            )
        )
        builder.adjust(2)
        return builder.as_markup()

    if target.startswith('removeReminder') and 'reminders' in args:
        return getRemindersKeyboardFab(builder, args['reminders'])
    
    if target == 'stat':
        builder.add(
            InlineKeyboardButton(
                text="Выход",
                callback_data="exit_photo"
            )
        )
        return builder.as_markup()

    if target == 'exit_simple':
        builder.add(
            InlineKeyboardButton(
                text="Начать тест заново",
                callback_data="next_0"
            ),
            InlineKeyboardButton(
                text="Выбрать другой тест",
                callback_data="start"
            ),
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stat_choice"
            )
        )
        builder.adjust(2)
        return builder.as_markup()

    if target == 'exit_full':
        builder.add(
            InlineKeyboardButton(
                text="Выбрать тест",
                callback_data="start"
            ),
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stat_choice"
            ),
            InlineKeyboardButton(
                text = "Напоминания",
                callback_data="reminder"
            )
        )
        builder.adjust(2)
        return builder.as_markup()

    if target.startswith('next_') and 'isEnd' in args:
        builder.add(
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stat"
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="Выход",
                callback_data="exit_full"
            )
        )
        return builder.as_markup()

    if target.startswith('next_') and "currentQuestion" in args and "currentTest" in args:
        return getAnswersKeyboardFab(builder, len(args['currentTest']['content']['questions'][args['currentQuestion']]))

    builder.add(
        InlineKeyboardButton(
            text="Продолжить",
            callback_data="next_0"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Выход",
            callback_data="exit_simple"
        )
    )
    return builder.as_markup()