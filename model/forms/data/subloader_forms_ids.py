from json import load, dump
from typing import NamedTuple
from datetime import datetime
from model.data.subloader_mentor_menti import get_mentor_menti_s, MentorMenti

from config import PATH_FORMS_IDS


class NeedForm(NamedTuple):
    form_id: str
    date: str
    menti_mentor: list[list[str, str]]


def get_data() -> list[list]:
    with open(PATH_FORMS_IDS, encoding='utf-8') as json_file:
        forms = load(json_file)
    return forms


def get_forms() -> list[NeedForm]:
    """
    :return: NeedForm(form_id, date, menti_mentor = [mentor, menti])
    """
    forms = get_data()
    return [NeedForm(form_id=form[0], date=form[1], menti_mentor=form[2]) for form in forms]


def get_forms_set() -> set[NeedForm]:
    forms = get_data()
    return set(NeedForm(form_id=form[0], date=form[1], menti_mentor=form[2]) for form in forms)


def delete_form(form_id: str, menti_name: str):
    data = get_forms()
    for i in range(len(data)):
        if data[i].form_id == form_id and data[i].menti_mentor[0] == menti_name:
            data.pop(i)
            break
    dump_forms_id(data)


def add_form(form_id: str) -> None:
    data = get_forms()
    new_form = NeedForm(form_id=form_id,
                        date=str(datetime.now().strftime("%d/%m/%Y")),
                        menti_mentor=get_mentor_menti_s())
    data.append(new_form)
    dump_forms_id(data)


def dump_forms_id(data: list[NeedForm]) -> None:
    with open(PATH_FORMS_IDS, mode='w', encoding='utf-8') as json_file:
        dump(data, json_file, indent=4, ensure_ascii=False)
