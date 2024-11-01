"""
/info - выдает информации по менти котрый ментор должен заполнить
Выдавать: имя менти и даты и ссылка на форму

"""

from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command

from datetime import timedelta, datetime

from model.updating import update


router = Router()
router.message.filter(
    F.chat.func(lambda chat: chat.type == "private")
)


@router.message(Command("info"))
async def get_info(message: Message) -> None:
    """
    Дает список не заполненных форм по менти по конкретному человеку
    :param message:
    :return:
    """
    data = await update()
    asking = None

    for d in data:
        start_date = (datetime.strptime(d.date, '%d/%m/%Y') - timedelta(days=14)).strftime('%d/%m/%Y')
        for m_m in d.menti_mentor:
            if m_m[1] == message.from_user.username or m_m[1] == message.from_user.id:
                asking = f"{message.from_user.username} \nЗаполни, пожалуйста, форму:" \
                          f"\n о встрече с менти {m_m[0]} с {start_date} по {d.date}\n" \
                         f"https://docs.google.com/forms/d/{d.form_id}"
                await message.answer(asking)

    if asking is None:
        await message.answer("Все формы заполнены ))")
