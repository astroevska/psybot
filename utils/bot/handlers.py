from typing import List
from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery

from init.globals import globals
from utils.bot.keyboard import getButtons
from utils.bot.message import clearStartMessage, changeMessage
from utils.helpers import getTag, getResult, clearTestData, getHelpMessage

async def handleFirstQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:    
    await callback.message.answer(
        "\n".join([f"<b>{i})</b> {x}" for i, x in enumerate(globals.currentTest['content']['questions'][globals.currentQuestion])]),
        reply_markup=getButtons(callback.data, currentQuestion=globals.currentQuestion)
    )

    globals.data[callback.from_user.id]: List = [int(getTag(callback.data))]
    globals.currentStartMessage = callback.message
    globals.currentQuestion += 1

    return await callback.answer()

async def handleLastQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:    
    if globals.currentStartMessage:
        await clearStartMessage()

    globals.data[callback.from_user.id].append(int(getTag(callback.data)))

    globals.result = sum(globals.data[callback.from_user.id])
    globals.resultIndex = getResult(globals.currentTest['content']['interpretor'], globals.result)
    text: str = f"Вы прошли тест. Ваш результат: <b>{globals.result} баллов</b>.\nПо шкале Бека он соответствует следующему состоянию: <b>{globals.currentTest['content']['interpretor'][globals.resultIndex][2]}</b>.\n\n{globals.currentTest['content']['interpretor'][globals.resultIndex][3]}"

    await changeMessage(
        callback, 
        f"{text}\n\n{getHelpMessage()}" if globals.resultIndex > 1 else text,
        getButtons(callback.data, isEnd=True)
    )

    clearTestData(callback.from_user.id)

    return await callback.answer()