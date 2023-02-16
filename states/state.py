from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q_for_feedback = State()
    Q_for_tech_support = State()
    Q_for_info_1 = State()
    Q_for_info_2 = State()

