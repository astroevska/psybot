from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from init.globals import globals
from db.get import getUsers

class UserDataMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        user_exists = globals.user == event.from_user.id
        print(user_exists)
        print(globals.user)
        
        if globals.currentUser == '':
            userData = getUsers({"telegram_id": event.from_user.id})[0]
            globals.user = userData["telegram_id"] or ""
            globals.currentUser = userData["_id"] or ""
        # user_exists = any(user.currentUser == event.from_user.id for user in globals)
        # if not user_exists: 
        #     globals.append(event.from_user.id)
        return await handler(event, data)