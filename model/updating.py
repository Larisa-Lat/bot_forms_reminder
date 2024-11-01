from datetime import datetime
from model.forms.data.subloader_forms_ids import NeedForm
from model.forms.google_form import Form
from model.forms.data.subloader_forms_ids import get_forms, dump_forms_id
from model.sheet.google_sheet import MainSheet


async def update() -> list[NeedForm]:
    needed_forms = get_forms()

    sheet = MainSheet()
    sheet_data = await sheet.get_sheet_data()
    form = Form()

    for need_form in needed_forms:
        responses = await form.get_responses(need_form.form_id)
        if len(responses) != 0:
            amount_menti_mentor = len(need_form.menti_mentor)
            amount_responses = len(responses["responses"])
            for i_response in range(amount_responses):
                menti_name = responses["responses"][i_response]["answers"]["40b7faa3"]["textAnswers"]["answers"][0]["value"]
                for mentor_menti in need_form.menti_mentor.copy():
                    if mentor_menti[1] == menti_name:
                        need_form.menti_mentor.remove(mentor_menti)
                        new_line = await get_info(need_form.form_id, need_form.date, responses["responses"][i_response])
                        sheet_data.append(new_line)
                        break

    await sheet.update_sheet(sheet_data)
    dump_forms_id(needed_forms)
    return needed_forms


async def get_info(form_id, form_date, data: dict) -> list:
    """
    Расшифровка ответов из формы
    :param form_id:
    :param form_date:
    :param data:
    :return:
    """
    response_id = data["responseId"]
    menti_name = data["answers"]["40b7faa3"]["textAnswers"]["answers"][0]["value"]
    amount_meetings = data["answers"]["536547f5"]["textAnswers"]["answers"][0]["value"]

    if amount_meetings == "0":
        who = data["answers"]["315d213d"]["textAnswers"]["answers"][0]["value"]
        reason = data["answers"]["31bf842a"]["textAnswers"]["answers"][0]["value"]
    else:
        who = "-"
        reason = "-"

    if "2add7b78" in data["answers"]:
        comment = data["answers"]["2add7b78"]["textAnswers"]["answers"][0]["value"]
    else:
        comment = "-"

    return [form_id, form_date, response_id, menti_name, amount_meetings, who, reason, comment]
