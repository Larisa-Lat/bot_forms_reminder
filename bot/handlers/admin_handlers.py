"""
- Получить файл json текущий
- Заменить json на новый
- получение всех задолжностей
"""

from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from datetime import timedelta, datetime

import os
from dotenv import load_dotenv
from config import PATH_ENV, PATH_MENTOR_MENTI

from model.updating import update

from bot.middlewares.is_admin import IsAdmin

from bot.utils.statesforms import ChangeAdmins

from main import bot

from model.data.subloader_mentor_menti import get_mentors_names

load_dotenv(PATH_ENV)

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

router = Router()

router.message.middleware(IsAdmin())
router.message.filter(
    F.chat.func(lambda chat: chat.type == "private")
)


@router.message(Command("admin"))
async def get_admin_commands(message: Message) -> None:
    """
    Выведет админу все доступные команды
    :param message:
    :return:
    """
    answer = "/get_forms - получение задолжностей\n" \
             "/get_mentor_menti - получение файла с менти и их ментором\n" \
             "/new_mentor_menti - изменение файла с менти и их ментором"
    await message.answer(answer)


@router.message(Command("get_forms"))
async def get_needed_forms(message: Message) -> None:
    """
    Выведет все формы, что не заполнены
    :param message:
    :return:
    """
    data = await update()

    mentors = get_mentors_names()
    for mentor in mentors:
        asking = ""
        for d in data:
            for m_m in d.menti_mentor:
                if m_m[0] == mentor:
                    if len(asking) == 0:
                        asking = f"@{mentor}\n\n"
                    start_date = (datetime.strptime(d.date, '%d/%m/%Y') - timedelta(days=14)).strftime('%d/%m/%Y')
                    asking += f"\t- менти {m_m[1]} ({start_date} - {d.date})\n" \
                              f"https://docs.google.com/forms/d/{d.form_id}\n\n"
        if len(asking) != 0:
            await message.answer(asking)
        else:
            await message.answer("Все формы заполнены ))")


@router.message(Command("get_mentor_menti"))
async def get_admins_info(message: Message) -> None:
    """
    Отправляет админу файл со списком ментор и менти
    :param message:
    :return:
    """
    await message.answer("с начало идет tg nickname ментора без @, потом Имя Фамилия менти")
    document = FSInputFile(path=PATH_MENTOR_MENTI)
    await message.answer_document(document=document)


@router.message(Command("new_mentor_menti"))
async def new_mentor_menti(message: Message, state: FSMContext) -> None:
    await message.answer("Файл должен быть json, формата:\n[[tg nickname mentora без @, Имя Фамилия менти], ...]")
    await message.answer("Пришли файл")
    await state.set_state(ChangeAdmins.GET_FILE)


@router.message(ChangeAdmins.GET_FILE)
async def set_mentor_menti(message: Message, state: FSMContext) -> None:
    """
    Получение файл с новыми ментором и менти
    :param message:
    :param state:
    :return:
    """
    try:
        if message.document and message.document.file_name.endswith(".json"):
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, PATH_MENTOR_MENTI)
            await message.answer("Файл успешно загружен")
        else:
            await message.answer("Это не файл json")

    except Exception:
        await message.answer("С файлом что то не то")
    finally:
        await state.clear()

