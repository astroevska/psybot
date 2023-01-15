import logging
from typing import Coroutine
from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command

from constants.config import API_TOKEN
from constants.types import TSendMessage
from utils.bot.callbacks.test import chooseTest, setAnswer
from utils.bot.callbacks.main import getStatistics, handleExit, start, startBot
from utils.bot.callbacks.reminder import deleteReminder, setReminder, showReminders


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher()


async def sendMessage(data: TSendMessage):
    await bot.send_message(data["chat_id"], data["text"])


# bot callbacks
dp.callback_query(Text(text="start"))(start)
dp.message(Command(commands=['start']))(startBot)
dp.callback_query(Text(text="stat"))(getStatistics)
dp.callback_query(Text(startswith="exit_"))(handleExit)

dp.callback_query(Text(text='reminder'))(showReminders)
dp.callback_query(Text(startswith='removeReminder'))(deleteReminder)
dp.callback_query(Text(startswith="every_"))(setReminder)

dp.callback_query(Text(startswith="test_"))(chooseTest)
dp.callback_query(Text(startswith="next_"))(setAnswer)


async def main() -> Coroutine:
    await dp.start_polling(bot)
