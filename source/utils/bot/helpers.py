from aiogram.types import InlineKeyboardMarkup, Message

from ...init.globals import globalsList
from ...constants.data import TESTS_CONFIG


async def clearStartMessage(globalsIdx: int):
    if globalsList[globalsIdx].currentStartMessage:
        await globalsList[globalsIdx].currentStartMessage.delete()

        globalsList[globalsIdx].currentStartMessage = None


async def changeMessage(message: Message, text: str, markup: InlineKeyboardMarkup, photo = None):
    if message.photo:
        await message.answer(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)


def getStartMessage() -> str:
    startText = f"На данный момент в боте доступны следующие тесты:\n\n"
    for i in range(len(TESTS_CONFIG)):
        startText += f"<b>{i + 1}. {TESTS_CONFIG[i]['name']}</b>\n"

    startText += "\nВы можете выбрать любой из них, пройти его, а в дальнейшем отслеживать динамику изменений своего психологического состояния. Тесты постоянно дополняются."
    return startText


def getHelpMessage() -> str:
    return "Ваше состояние вызывает озабоченность. Вам стоит продолжить за ним наблюдать, а также по возможности обратиться к специалисту."


def getReminderPeriodName(reminder_type: str) -> str:
    text = "Вы установили напоминание "

    if reminder_type == 'day':
        text += "на каждый день"
    elif reminder_type == 'week':
        text += "на каждую неделю"
    elif reminder_type == '2weeks':
        text += "два раза в месяц"
    elif reminder_type == 'month':
        text += "раз в месяц"

    return text
