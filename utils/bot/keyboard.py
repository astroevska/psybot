from typing import List, Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from init.globals import globals
from constants.types import TTest
from constants.config import TESTS_CONFIG


def getTestKeyboardFab(builder: InlineKeyboardBuilder, tests: List[TTest]) -> InlineKeyboardMarkup:
    for i in range(len(tests)):
        builder.add(
            InlineKeyboardButton(
                text=tests[i]['name'],
                callback_data=f"test_{i}"
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

def getButtons(target: str, **args: Any) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if target == 'init':
        builder.add(
            InlineKeyboardButton(
                text="Выбрать тест",
                callback_data="start"
            )
        )
        return builder.as_markup()

    if target == 'start':
        return getTestKeyboardFab(builder, TESTS_CONFIG)
    
    if target == 'stat':
        builder.add(
            InlineKeyboardButton(
                text="Выход",
                callback_data="exit_photo"
            )
        )
        return builder.as_markup()

    if target.startswith('exit_'):
        builder.add(
            InlineKeyboardButton(
                text="Начать тест заново",
                callback_data="next_0"
            ),
            InlineKeyboardButton(
                text="Выбрать другой тест",
                callback_data="start"
            )
        )
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

    if target.startswith('next_') and "currentQuestion" in args:
        return getAnswersKeyboardFab(builder, len(globals.currentTest['content']['questions'][args['currentQuestion']]))

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