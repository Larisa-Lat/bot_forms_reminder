from aiogram import Bot
from aiogram.types import BotCommand


async def show_commands(bot: Bot):
    commands = [
        BotCommand(
            command="info",
            description="В личке: инфа о формах, которых надо заполнить"
        ),
        BotCommand(
            command="admin",
            description="для админов"
        )
    ]
    await bot.set_my_commands(commands)