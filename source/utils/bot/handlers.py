from typing import List
from dateutil import parser
from functools import reduce
from datetime import datetime
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from source.utils.helpers import getTag
from source.utils.plot import getPlotImg
from source.db.insert import insertResult
from source.init.globals import globalsList
from source.db.remove import removeUnfinished
from source.utils.bot.keyboard import getButtons, getAnswersKeyboardFab
from source.utils.bot.helpers import clearStartMessage, changeMessage, getHelpMessage
from source.utils.bot.globals import appendAnswer, getOrSetCurrentGlobal, clearTestData, clearUnfinishedTimeout, setResult, startUnfinishedTimeout


async def handleFirstQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    tag = getTag(callback.data)

    await callback.message.delete_reply_markup()

    try:
        await callback.message.answer(
            "\n".join([f"<b>{i})</b> {x}" for i, x in enumerate(globalsList[globalsIdx].currentTest['content']
                    ['questions'][globalsList[globalsIdx].currentQuestion])]),
            reply_markup=getAnswersKeyboardFab(builder, len(globalsList[globalsIdx].currentTest['content']
                    ['questions'][globalsList[globalsIdx].currentQuestion])))

    except Exception as e:
        print(e)

    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['_id']]: List = int(tag) if tag else []
    startUnfinishedTimeout(globalsIdx, callback.from_user)

    globalsList[globalsIdx].currentStartMessage = callback.message
    globalsList[globalsIdx].currentQuestion += 1

    return await callback.answer()


async def handleLastQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)

    appendAnswer(globalsIdx, getTag(callback.data))
    setResult(globalsIdx)

    text: str = f"Вы прошли тест. Ваш результат: <b>{globalsList[globalsIdx].result} баллов</b>.\nПо шкале Бека он соответствует следующему состоянию: <b>{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][2]}</b>.\n\n{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][3]}"
    plot = await getPlotImg(callback.from_user, True)

    clearUnfinishedTimeout(globalsIdx)

    await callback.message.answer_photo(
        plot,
        f"{text}\n\n{getHelpMessage()}" if globalsList[globalsIdx].resultIndex > 1 else text,
        reply_markup=getButtons('testStat', isEnd=True)
    )

    await callback.message.delete()

    try:
        insertResult({
            "telegram_id": callback.from_user.id,
            "test_name": globalsList[globalsIdx].currentTest["name"],
            "test_id": globalsList[globalsIdx].currentTest["_id"],
            "result": globalsList[globalsIdx].result,
            "date": parser.parse(str(datetime.now()))
        })
    except Exception as e:
        print(e)

    try:
        removeUnfinished({
            "chat_id": callback.from_user.id,
            "test_id": globalsList[globalsIdx].currentTest["_id"]
        })
    except Exception as e:
        print(e)

    await clearStartMessage(globalsIdx)
    await clearTestData(callback.from_user)

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


async def startBot(message: Message):
    await getOrSetCurrentGlobal(message.from_user)

    await message.reply(
        f"Привет, {message.from_user.first_name}!\n\nНе секрет, что многие разработчики сталкиваются с выгоранием, тревогой и депрессией. Этот бот призван помочь вам отслеживать свое психологическое состояние и предлагает несколько психологических тестов. Бот будет сохранять ваши результаты, и вы сможете отслеживать динамику изменения своего состояния на длительных промежутках. Это поможет вам вовремя заметить ухудшение или понять, какие факторы идут вам на пользу, а какие во вред.",
        reply_markup=getButtons('init')
    )
