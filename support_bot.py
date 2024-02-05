import asyncio
import contextlib

from aiogram import Dispatcher, Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import Config


class AnswerState(StatesGroup):
    answer = State()


class SendQuestion(StatesGroup):
    question = State()


router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text="Здравствуйте! Напишите ваше сообщение, и в скором времени вам ответит Тех. Поддержка!")

    await state.set_state(SendQuestion.question)


@router.message(F.text, StateFilter(SendQuestion.question))
async def send_question(message: Message, state: FSMContext):
    user = message.from_user

    await message.answer(text="Вы успешно отправили сообщение! Ожидайте ответа...")

    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить", callback_data=f"otvet|{str(user.id)}")
    builder.adjust(1)

    await message.bot.send_message(chat_id=1282629807, text=message.text, reply_markup=builder.as_markup())

    await state.clear()


@router.callback_query(StateFilter(None))
async def send_answer(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('|')[1]
    await call.message.answer(text="Что написать?")

    await state.set_state(AnswerState.answer)
    await state.update_data(user_id=user_id)


@router.message(F.text, StateFilter(AnswerState.answer))
async def answer_user_question(message: Message, state: FSMContext):
    state_data = await state.get_data()

    user_id = state_data.get('user_id')
    answer_text = message.text

    await message.bot.send_message(chat_id=user_id, text=answer_text)
    await message.answer(text='Выслал')

    await state.clear()


async def main():
    bot = Bot(token=Config.SUPPORT_BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit, RuntimeError):
        asyncio.run(main())
