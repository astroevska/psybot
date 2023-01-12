from typing import Union
from aiogram.types import InlineKeyboardMarkup, CallbackQuery,  Message
from init.globals import globalsList

async def clearStartMessage(globalsIdx: int):    
    await globalsList[globalsIdx].currentStartMessage.delete()
    
    globalsList[globalsIdx].currentStartMessage = None

async def changeMessage(message: Message, text: str, markup: InlineKeyboardMarkup, photo = None):
    if message.photo:
        await message.answer(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)
