from typing import List, Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.globals import getKeyList
from constants.data import TESTS_CONFIG, BUTTONS_CONFIG


def getTestKeyboardFab(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    for i in range(len(TESTS_CONFIG)):
        builder.add(
            InlineKeyboardButton(
                text=TESTS_CONFIG[i]['name'],
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
    targetList = getKeyList(BUTTONS_CONFIG, "name")

    try:
        targetIdx = targetList.index(target)
    except ValueError:
        targetIdx = targetList.index(f"{target.split('_')[0]}_")

    if targetIdx != -1 and (all(c in args for c in BUTTONS_CONFIG[targetIdx]["conditions"]) if "conditions" in BUTTONS_CONFIG[targetIdx] and len(BUTTONS_CONFIG[targetIdx]["conditions"]) != 0 else True):
        if "message_actions" in BUTTONS_CONFIG and len(BUTTONS_CONFIG[targetIdx]["message_actions"]) != 0 and "message" in args and args["message"]:
            for a in BUTTONS_CONFIG["message_actions"]:
                args["message"][a]()

        for b in BUTTONS_CONFIG[targetIdx]["buttons"]:
            if b["condition"] not in args or not args[b["condition"]] if "condition" in b else False:
                continue
            builder.add(
                InlineKeyboardButton(
                    text=b["text"],
                    callback_data=b["callback_data"]
                )
            )
            
        builder.adjust(BUTTONS_CONFIG[targetIdx]["adjust"])
        
    elif any(target.startswith(k) for k in targetList.index(target)):
        if 'message' in args:
            return args['message'].reply_markup
        
    else:
            builder.add(
                InlineKeyboardButton(
                    text="Продолжить",
                    callback_data="next_0"
                )
            )
            builder.add(
                InlineKeyboardButton(
                    text="Выход",
                    callback_data="exit_full"
                )
            )
            
        
    return builder.as_markup()