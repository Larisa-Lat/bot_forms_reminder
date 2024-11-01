import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from model.forms.data import subloader_forms_ids
from model.forms.update_form import QUESTIONS, NEW_FORM
from config import PATH_CREDENTIALS

logger = logging.getLogger(__name__)


class Form:
    """
    Класс Form предназнчаченный для работы с google forms

    Функции:
        create_form: создает форму, согласно шаблону в update_form
        get_responses: получение ответа по форме
    """
    form_service = None

    def __init__(self):
        try:
            credentials = Credentials.from_service_account_file(PATH_CREDENTIALS)
            self.form_service = build('forms', 'v1', credentials=credentials)

        except Exception as e:
            logger.exception("Преблема с credentials")

    async def create_form(self) -> str | None:
        try:
            # Creates the initial form
            result = self.form_service.forms().create(body=NEW_FORM).execute()

            # Adds the question to the form
            questions = (
                self.form_service.forms()
                .batchUpdate(formId=result["formId"], body=QUESTIONS)
                .execute()
            )

        except Exception as e:
            logger.exception("Проблема с созданием формы")
            return None

        else:
            subloader_forms_ids.add_form(result["formId"])
            return result["formId"]

    async def get_responses(self, form_id: str):
        return self.form_service.forms().responses().list(formId=form_id).execute()


if __name__ == "__main__":
    id = Form().create_form()
    print(f"https://docs.google.com/forms/d/{id}")
    # ans = Form().get_responses("1TV0jtYU1eWw86JpKpYJ3sXPGB0qeLPQ_IctQvfVvqNA")
    # print(ans)


