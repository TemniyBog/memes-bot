from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    wait_for = State()
###
    # загрузить картинку
    wait_for_pic = State()
    wait_for_tags = State()
    wait_for_approve = State()
    approved = State()