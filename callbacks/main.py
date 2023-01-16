from aiogram.methods import AnswerCallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from init.globals import globalsList
from utils.globals import getOrSetCurrentGlobal
from utils.bot.keyboard import getButtons, getTestKeyboardFab
from utils.bot.message import changeMessage, clearStartMessage
from utils.helpers import getStartMessage, getTag, clearTestData


async def startBot(message: Message):
    await getOrSetCurrentGlobal(message.from_user)

    await message.reply(
        f"Привет, {message.from_user.first_name}!\n\nНе секрет, что многие разработчики сталкиваются с выгоранием, тревогой и депрессией. Этот бот призван помочь вам отслеживать свое психологическое состояние и предлагает несколько психологических тестов. Бот будет сохранять ваши результаты, и вы сможете отслеживать динамику изменения своего состояния на длительных промежутках. Это поможет вам вовремя заметить ухудшение или понять, какие факторы идут вам на пользу, а какие во вред.",
        reply_markup=getButtons('init')
    )


async def start(callback: CallbackQuery):
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    
    await changeMessage(
        callback.message,
        getStartMessage(),
        markup=getTestKeyboardFab(builder, 'test', 'exit_full')
    )

    await callback.answer()


async def handleExit(callback: CallbackQuery) -> AnswerCallbackQuery:
    globalsIdx = await getOrSetCurrentGlobal(callback.from_user)
    tag = getTag(callback.data)
    markup: InlineKeyboardMarkup = getButtons(callback.data)

    if globalsList[globalsIdx].currentStartMessage and tag != "simple":
        await clearStartMessage(globalsIdx)
        await clearTestData(callback.from_user)

    if tag == 'fullPhoto':
        await callback.message.answer(
            "Вы посмотрели статистику. Если хотите пройти один из наших психологических тестов, нажмите на кнопку <b>Выбрать тест</b>.\n\nЕсли хотите, чтобы бот напоминал вам проходить тесты раз в определенный период, выберите кнопку <b>Напоминания</b>.",
            reply_markup=markup
        )

        await callback.message.delete()

        return await callback.answer()

    if tag == 'photo':
        await callback.message.answer(
            "Вы закончили прохождение теста. Если хотите отслеживать свое состояние регулярно, вы можете попросить бота присылать вам уведомления раз в определенный период. Для этого нажмите кнопку <b>Напоминания</b>.\nТакже вы можете ознакомиться с другими нашими тестами.",
            reply_markup=markup
        )

        await callback.message.delete_reply_markup()

        return await callback.answer()

    if tag == 'simple':
        await changeMessage(
            callback.message,
            f"На данный момент вы проходите тест <b>{globalsList[globalsIdx].currentTest['name']}</b>.\nВы на {len(globalsList[globalsIdx].data)}/{len(globalsList[globalsIdx].currentTest['content']['questions'])} вопросе.\n\nХотите продолжить?",
            markup=markup
        )

        globalsList[globalsIdx].currentQuestion -= 1

        return await callback.answer()

    await changeMessage(
        callback.message,
        "Если хотите пройти один из наших психологических тестов, нажмите на кнопку <b>Выбрать тест</b>.\n\nЕсли хотите, чтобы бот напоминал вам проходить тесты раз в определенный период, выберите кнопку <b>Напоминания</b>.\n\nВы также можете посмотреть статистику всех пройденных тестов, чтобы оценить динамику собственного психологического состояния.",
        markup=markup
    )

    await callback.answer()