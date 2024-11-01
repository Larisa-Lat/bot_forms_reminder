import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gspread.exceptions import SpreadsheetNotFound

from os import getenv
from dotenv import load_dotenv
from config import PATH_ENV, PATH_CREDENTIALS


load_dotenv(PATH_ENV)
SHEET_ID = getenv("SHEET_ID")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
HEAD = ["form_id", "form_date", "response_id",	"menti_name", "amount_meetings",
        "who",	"reason",	"comment"]


class MainSheet:
    """
    Класс MainSheet предназначенный для работы с таблицей куда сливаются все данные
    Функции:
        get_sheet_data: получение всех данных таблицы в [[], [], ...]
        update_sheet: изменение данных талицы, перед изменением происходит сортировка по дате создание формы
    """
    worksheet = None

    def __init__(self):
        try:
            creds = Credentials.from_service_account_file(PATH_CREDENTIALS,
                                                          scopes=SCOPES)
            sheets = gspread.authorize(creds).open_by_key(SHEET_ID)  # получение доступ к конкретной таблицы
            self.worksheet = sheets.sheet1

        except SpreadsheetNotFound as err:
            print("SpreadsheetNotFound")

        # except Exception as err:
        #     print("Exception")

    async def get_sheet_data(self):
        """
        Получение всех данных (кроме шапки) таблицы в виде [[], [], ...]
        :return:
        """
        return self.worksheet.get_all_values()[1:]

    async def update_sheet(self, data):
        """
        Изменет данные таблицы, перед этим сортирует их по дате создания формы
        :param data:
        :return:
        """
        data = sorted(data, key=lambda x: datetime.strptime(x[1], "%d/%m/%Y"), reverse=True)
        data.insert(0, HEAD)
        self.worksheet.update(data)


if __name__ == "__main__":
    pass
