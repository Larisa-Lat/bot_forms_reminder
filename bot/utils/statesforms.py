from aiogram.fsm.state import StatesGroup, State


class ChangeAdmins(StatesGroup):
    GET_FILE = State()
