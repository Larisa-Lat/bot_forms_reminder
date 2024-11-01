from aiogram import Bot

from datetime import timedelta, datetime

import os
from dotenv import load_dotenv

from config import PATH_ENV

from model.updating import update
from model.forms.google_form import Form

from model.data.subloader_mentor_menti import get_mentors_names

load_dotenv(PATH_ENV)
GROUP_ID = os.getenv("GROUP_ID")


async def get_needed_forms(bot: Bot) -> None:
    """
    Уведомляет пользователей о тех формах, что ментор забыл заполнить
    :param bot:
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
                        asking = f"@{mentor} заполни пожалуйста формы: \n\n"
                    start_date = (datetime.strptime(d.date, '%d/%m/%Y') - timedelta(days=14)).strftime('%d/%m/%Y')
                    asking += f"\t- менти {m_m[1]} ({start_date} - {d.date})\n" \
                              f"https://docs.google.com/forms/d/{d.form_id}\n\n"
        if len(asking) != 0:
            await bot.send_message(chat_id=GROUP_ID, text=asking)


async def create_new_form(bot: Bot) -> None:
    """
    Уведомляет пользователей об новой форме
    :param bot:
    :return:
    """
    new_form_id = await Form().create_form()
    answer = "Error"
    if new_form_id is not None:
        answer = f"Пожалуста заполните форму по вашим менти\n" \
                 f"https://docs.google.com/forms/d/{new_form_id}"

    await bot.send_message(chat_id=GROUP_ID, text=answer)
