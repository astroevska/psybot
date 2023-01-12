from typing import List
from dateutil import parser
from functools import reduce
from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery

from db.insert import insertResult
from init.globals import globalsList
from utils.bot.keyboard import getButtons
from utils.globals import getOrSetCurrentGlobal
from utils.bot.message import clearStartMessage, changeMessage
from utils.helpers import getTag, getResult, clearTestData, getHelpMessage


async def handleFirstQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    try:
        await changeMessage(
            callback.message,
            "\n".join([f"<b>{i})</b> {x}" for i, x in enumerate(globalsList[globalsIdx].currentTest['content']
                    ['questions'][globalsList[globalsIdx].currentQuestion])]),
            markup=getButtons(
                callback.data, currentQuestion=globalsList[globalsIdx].currentQuestion, currentTest=globalsList[globalsIdx].currentTest)
        )
    except Exception as e:
        print(e)

    globalsList[globalsIdx].data[callback.from_user.id]: List = [int(getTag(callback.data))]
    globalsList[globalsIdx].currentStartMessage = callback.message
    globalsList[globalsIdx].currentQuestion += 1

    return await callback.answer()


async def handleLastQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    if globalsList[globalsIdx].currentStartMessage:
        await clearStartMessage(globalsIdx)

    globalsList[globalsIdx].data[callback.from_user.id].append(int(getTag(callback.data)))

    globalsList[globalsIdx].result = sum(globalsList[globalsIdx].data[callback.from_user.id])
    globalsList[globalsIdx].resultIndex = getResult(
        globalsList[globalsIdx].currentTest['content']['interpretor'], globalsList[globalsIdx].result)
    text: str = f"Вы прошли тест. Ваш результат: <b>{globalsList[globalsIdx].result} баллов</b>.\nПо шкале Бека он соответствует следующему состоянию: <b>{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][2]}</b>.\n\n{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][3]}"

    try:
        await insertResult({
            "telegram_id": callback.from_user.id,
            "test_name": globalsList[globalsIdx].currentTest["name"],
            "result": globalsList[globalsIdx].result,
            "date": parser.parse(str(datetime.now()))
        })
    except:
        print('Insert Error')

    await changeMessage(
        callback.message,
        f"{text}\n\n{getHelpMessage()}" if globalsList[globalsIdx].resultIndex > 1 else text,
        getButtons(callback.data, isEnd=True)
    )

    await clearTestData(callback.from_user.id)

    return await callback.answer()


async def remindersHandler(callback: CallbackQuery, userReminders: list, condition = True):
    if condition:
        reminders = reduce(lambda acc, item: f"{acc}\n\n{item[0] + 1}) Период: <b>{item[1]['period']}</b>\n🔔Следующее напоминание вас ожидает {item[1]['next'].strftime('<b>%d-%m-%Y</b> в <b>%H:%M:%S</b>')}",
            enumerate(userReminders), "")

        remindersText = "<b>У вас пока нет напоминаний. Хотите добавить?</b>" if len(reminders) == 0 else f"<b>Ваши напоминания:</b>{reminders}"

        await changeMessage(
            callback.message,
            f"Вы можете настроить персональные напоминания о прохождении теста, чтобы регулярно отслеживать свое психологическое состояние. \n\n{remindersText}\n\nПожалуйста, выберите периодичность напоминаний: ",
            markup=getButtons('reminder', hasReminders=bool(len(userReminders)))
        )

    return await callback.answer()