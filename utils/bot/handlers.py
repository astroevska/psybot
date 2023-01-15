from typing import List
from dateutil import parser
from functools import reduce
from datetime import datetime
from threading import Timer
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.plot import getPlotImg
from db.insert import insertResult
from db.remove import removeUnfinished 
from init.globals import globalsList
from utils.bot.keyboard import getButtons, getAnswersKeyboardFab
from utils.globals import getOrSetCurrentGlobal
from utils.bot.message import clearStartMessage, changeMessage
from utils.helpers import getTag, getResult, clearTestData, getHelpMessage, saveUnfinishedResults


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

    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']]: List = int(tag) if tag else []
    globalsList[globalsIdx].test_timeout = Timer(
        10, saveUnfinishedResults, args=[globalsIdx, callback.from_user, globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']]])
    globalsList[globalsIdx].test_timeout.start()
    
    globalsList[globalsIdx].currentStartMessage = callback.message
    globalsList[globalsIdx].currentQuestion += 1

    return await callback.answer()


async def handleLastQuestion(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']].append(int(getTag(callback.data)))
    globalsList[globalsIdx].result = sum(globalsList[globalsIdx].data[globalsList[globalsIdx].currentTest['name']])
    globalsList[globalsIdx].resultIndex = getResult(
        globalsList[globalsIdx].currentTest['content']['interpretor'], globalsList[globalsIdx].result)
    
    text: str = f"Вы прошли тест. Ваш результат: <b>{globalsList[globalsIdx].result} баллов</b>.\nПо шкале Бека он соответствует следующему состоянию: <b>{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][2]}</b>.\n\n{globalsList[globalsIdx].currentTest['content']['interpretor'][globalsList[globalsIdx].resultIndex][3]}"
    plot = await getPlotImg(callback.from_user, True)    

    await callback.message.answer_photo(
        plot,
        f"{text}\n\n{getHelpMessage()}" if globalsList[globalsIdx].resultIndex > 1 else text,
        reply_markup=getButtons('testStat', isEnd=True)
    )

    callback.message.delete()

    try:
        insertResult({
            "telegram_id": callback.from_user.id,
            "test_name": globalsList[globalsIdx].currentTest["name"],
            "result": globalsList[globalsIdx].result,
            "date": parser.parse(str(datetime.now()))
        })
    except Exception as e:
        print(e)

    try: 
        removeUnfinished({
            "chat_id": callback.from_user.id,
            "test_name": globalsList[globalsIdx].currentTest["name"]
        })
    except Exception as e:
        print(e)
        
    if globalsList[globalsIdx].currentStartMessage:
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