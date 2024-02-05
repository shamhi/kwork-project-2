from aiogram.fsm.state import State, StatesGroup


class BuyCurrency(StatesGroup):
    buy = State()
