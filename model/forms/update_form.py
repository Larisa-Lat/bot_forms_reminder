from model.data.subloader_mentor_menti import get_mentis_names
from datetime import datetime, timedelta

today = datetime.now()
weeks2_ago = today - timedelta(days=14)

START_DAY = weeks2_ago.strftime('%d/%m/%Y')
END_DAY = today.strftime('%d/%m/%Y')

title_page_break_item = f"Чек встреч с менти c {START_DAY} по {END_DAY}"

NEW_FORM = {
    "info": {
        "title": f"Встреча с менти c {START_DAY} по {END_DAY}"
    }
}

QUESTIONS = {
    "requests": [
        {
            "createItem": {
                "item": {
                    "itemId": "2ba3f212",
                    "title": title_page_break_item,
                    "pageBreakItem": {}
                },
                "location": {"index": 0}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "3320629d",
                    "title": "Комментарий",
                    "questionItem": {
                        "question": {
                            "questionId": "2add7b78",
                            "textQuestion": {
                                "paragraph": True}}}
                },
                "location": {"index": 1}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "3d77d9dd",
                    "title": title_page_break_item,
                    "pageBreakItem": {}
                },
                "location": {"index": 0}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "17855ccc",
                    "title": "Почему встреча не состоялась",
                    "questionItem": {
                        "question": {"questionId": "01f546ed",
                                     "required": True,
                                     "choiceQuestion": {
                                         "type": "RADIO",
                                         "options": [
                                             {"value": "По состоянию здоровья / По личным причинам",
                                              "goToSectionId": "2ba3f212"},
                                             {"value": "Не было выхода в интерне / Технические неполадки",
                                              "goToSectionId": "2ba3f212"},
                                             {"value": "Не выходит на связь", "goToSectionId": "2ba3f212"},
                                             {"value": "Не пришел на встречу", "goToSectionId": "2ba3f212"},
                                             {"isOther": True, "goToSectionId": "2ba3f212"}]}}}
                },
                "location": {"index": 1}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "698439c0",
                    "title": title_page_break_item,
                    "pageBreakItem": {}
                },
                "location": {"index": 0}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "6a6f6499",
                    "title": "Почему встреча с менти не состоялась",
                    "questionItem": {
                        "question": {
                            "questionId": "31bf842a",
                            "required": True,
                            "choiceQuestion": {"type": "RADIO",
                                               "options": [
                                                   {"value": "По состоянию здоровья / По личным причинам",
                                                    "goToSectionId": "2ba3f212"},
                                                   {"value": "Не было выхода в интерне / Технические неполадки",
                                                    "goToSectionId": "2ba3f212"},
                                                   {"value": "Нет нашлось времени", "goToSectionId": "2ba3f212"},
                                                   {"isOther": True, "goToSectionId": "2ba3f212"}]}
                        }
                    }
                },
                "location": {"index": 1}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "070e0565",
                    "title": title_page_break_item,
                    "pageBreakItem": {}
                },
                "location": {"index": 0}
            }
        },
        {
            "createItem": {
                "item": {
                    "itemId": "1ff8622f",
                    "title": "По чей инициативе (отсутствия инициативы) встреча не состоялась",
                    "questionItem": {
                        "question": {
                            "questionId": "315d213d",
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "Ментор", "goToSectionId": "698439c0"},
                                    {"value": "Менти", "goToSectionId": "3d77d9dd"}]}}}
                },
                "location": {"index": 1}
            }
        },
        {
            "createItem": {
                "item": {
                        "itemId": "054b7be3",
                        "title": "Кто твой менти?",
                        "questionItem": {
                            "question": {
                                "questionId": "40b7faa3",
                                "required": True,
                                "choiceQuestion": {"type": "DROP_DOWN",
                                                   "options": [{"value": menti_name} for menti_name in get_mentis_names()]}}}

                },
                "location": {"index": 0}
            }
        },
        {
            "createItem": {
                "item": {
                  "itemId": "6d0e4110",
                  "title": f"Сколько было встреч c менти c {START_DAY} по {END_DAY}",
                  "questionItem": {
                    "question": {
                      "questionId": "536547f5",
                      "required": True,
                      "choiceQuestion": {
                          "type": "RADIO",
                          "options": [
                              {"value": "0", "goToSectionId": "070e0565"},
                              {"value": "1", "goToSectionId": "2ba3f212"},
                              {"value": "2 or more", "goToSectionId": "2ba3f212"}]}}}
                },
                "location": {"index": 1}
            }
        }
    ]
}
