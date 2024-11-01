from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.methods.get_chat_administrators import GetChatAdministrators

from typing import Callable, Dict, Any, Awaitable

from main import bot
import os
from dotenv import load_dotenv

from config import PATH_ENV

load_dotenv(PATH_ENV)

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")


async def is_admin(user_id: int) -> bool:
    return user_id in set(admin.user.id for admin in await bot(GetChatAdministrators(chat_id=int(GROUP_ID))))


class IsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if await is_admin(event.from_user.id):
            return await handler(event, data)
