from init.globals import globals
from aiogram.types import InlineKeyboardMarkup, CallbackQuery


async def clearStartMessage():    
    await globals.currentStartMessage.delete()
    globals.currentStartMessage = None

async def changeMessage(callback: CallbackQuery, text: str, markup: InlineKeyboardMarkup):
    if callback.message.photo:
        await callback.message.edit_caption('')
    await callback.message.edit_text(text, reply_markup=markup)
