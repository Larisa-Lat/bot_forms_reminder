import logging

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

import os
from dotenv import load_dotenv

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers import user_handlers, admin_handlers
from bot.utils.menu_commands import show_commands

from bot.handlers.group_handlers import create_new_form, get_needed_forms

from config import PATH_ENV

dp = Dispatcher()

load_dotenv(PATH_ENV)

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

bot = Bot(TOKEN)

START_DATE_AUTUMN_WINTER_CREATE_FORM = datetime(2024, 9, 2, 13, 0, 0)
END_DATE_AUTUMN_WINTER_CREATE_FORM = datetime(2024, 12, 30, 13, 0, 0)

START_DATE_AUTUMN_WINTER_ANALYZE = datetime(2024, 9, 2, 12, 0, 0)
END_DATE_AUTUMN_WINTER_ANALYZE = datetime(2024, 12, 30, 12, 0, 0)

logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")

logger = logging.getLogger(__name__)

# START_DATE_WINTER_SPRING = datetime(2024, 9, 2, 13, 3, 0)
# END_DATE_WINTER_SPRING = datetime(2024, 9, 2, 13, 3, 0)


# @dp.message()
# async def get_chat_id(message: Message):
#     print(message.chat.id)


async def set_schedulers(scheduler: AsyncIOScheduler) -> None:
    """
    Создает два AsyncIOScheduler:
        Первый: каждый две недели создает форму начиная с 02.09.2024 в 13:00
        Второй: каждую 3 дня проверяет заполнение формы с 02.09.2024 в 12:00
    :param scheduler:
    :return: вывод в группу бота
    """

    scheduler.add_job(get_needed_forms,
                      trigger="interval",
                      days=3,
                      start_date=START_DATE_AUTUMN_WINTER_ANALYZE,
                      end_date=END_DATE_AUTUMN_WINTER_ANALYZE,
                      id="analyze_needed_forms",
                      args=[bot]
                      )

    scheduler.add_job(create_new_form,
                      trigger="interval",
                      seconds=5,
                      start_date=START_DATE_AUTUMN_WINTER_CREATE_FORM,
                      end_date=END_DATE_AUTUMN_WINTER_CREATE_FORM,
                      id="creating_form",
                      args=[bot]
                      )


async def start():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    await set_schedulers(scheduler)
    scheduler.start()

    try:
        dp.startup.register(show_commands)
        dp.include_routers(
            admin_handlers.router,
            user_handlers.router
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())

"""
aiogram.exceptions.TelegramRetryAfter: Telegram server says - Flood control exceeded on method 'SendMessage' in chat -4588010562. Retry in 36 seconds.
Original description: Too Many Requests: retry after 36
(background on this error at: https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this)

"""