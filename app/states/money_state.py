from aiogram.fsm.state import State, StatesGroup


class MoneyOperation(StatesGroup):
    add = State()
    minus = State()
