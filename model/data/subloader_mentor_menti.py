from json import load
from typing import NamedTuple
from config import PATH_MENTOR_MENTI


class MentorMenti(NamedTuple):
    menti_name: str
    mentor_tg: str


def get_mentor_menti_s() -> list[list[str, str]]:
    with open(PATH_MENTOR_MENTI, encoding='utf-8') as json_file:
        mentor_menti_s = load(json_file)
    return mentor_menti_s


def get_mentis_names() -> set:
    mentor_menti_s = get_mentor_menti_s()
    return set(m_m[1] for m_m in mentor_menti_s)


def get_mentors_names() -> list[str]:
    mentor_menti_s = get_mentor_menti_s()
    return sorted(set(m_m[0] for m_m in mentor_menti_s))


if __name__ == "__main__":
    print(get_mentis_names())
    print(get_mentors_names())