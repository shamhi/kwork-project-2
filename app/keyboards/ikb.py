from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="👛 Кошелёк", callback_data="coshelec")
    builder.button(text="🍑 Подписки", callback_data="podpiski")
    builder.button(text="💎 P2P", callback_data="p2p")
    builder.button(text="🐬 Биржа", callback_data="birza")
    builder.button(text="🦋 Чеки", callback_data="cheki")
    builder.button(text="📩 Счета", callback_data="cheta")
    builder.button(text="⚙️ Настройки", callback_data="settings")

    builder.adjust(2)
    return builder.as_markup()


def get_help_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📈 Связаться с Тех. Поддержкой", url="https://t.me/CryptaSupport_bot")
    builder.button(text="< Назад", callback_data="bitcoin_buttons")

    builder.adjust(2)
    return builder.as_markup()


def get_p2p_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📈 Купить", callback_data="kupit")
    builder.button(text="📉 Продать", callback_data="prodat")
    builder.button(text="< Назад", callback_data="nazad_p2p")

    builder.adjust(2)
    return builder.as_markup()


def get_cryptocurrencies_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Tether (USDT) • 100₽ • 245", callback_data="valuta")
    builder.button(text="Gram(GRAM) • 0.28₽ • 32", callback_data="valuta")
    builder.button(text="Toncoin(TON) • 199₽ • 72", callback_data="valuta")
    builder.button(text="Bitcoin (BTC) • 3 980 000₽ • 53", callback_data="valuta")
    builder.button(text="LiteCoin (LTC) • 6 699₽ • 20", callback_data="valuta")
    builder.button(text="Ethereum (ETH) • 214 600₽ • 18", callback_data="valuta")
    builder.button(text="THRON • 11.19₽ • 28", callback_data="valuta")
    builder.button(text="USD Coin (USDC) • 134.65₽ • 2", callback_data="valuta")
    builder.button(text="Назад в P2P маркет", callback_data="nazad_v_p2p")

    builder.adjust(1)
    return builder.as_markup()


def get_subscriptions_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Подключить", callback_data="podcluchit")
    builder.button(text="< Назад", callback_data="nazad_p2p")

    builder.adjust(1)
    return builder.as_markup()


def get_stockmarket_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Войти на рынок", callback_data="rinok")
    builder.button(text="< Назад", callback_data="nazad_p2p")
    
    builder.adjust(1)
    return builder.as_markup()


def get_paychecks_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Создать чек", callback_data="add_check")
    builder.button(text="< Назад", callback_data="nazad_p2p")

    builder.adjust(1)
    return builder.as_markup()


def get_back_to_menu_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="В меню", callback_data="nazad_p2p")
    
    builder.adjust(1)
    return builder.as_markup()


def get_settings_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📈 Связаться с Тех. Поддержкой", url="https://t.me/CryptaSupport_bot")
    builder.button(text="Назад", callback_data="nazad_p2p")
    
    builder.adjust(1)
    return builder.as_markup()


def get_return_to_back_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="< Назад", callback_data="nazad_p2p")

    builder.adjust(1)
    return builder.as_markup()


def get_open_panel_ikb(user_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Открыть панель", callback_data=f"panel|{str(user_id)}")

    builder.adjust(1)
    return builder.as_markup()


def get_panel_ikb(mamont_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить баланс", callback_data=f"add_balance|{str(mamont_id)}")
    builder.button(text="➖ Забрать баланс", callback_data=f"minus_balance|{str(mamont_id)}")

    builder.adjust()
    return builder.as_markup()


def get_cancel_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Отменить", callback_data="cancel")

    builder.adjust(1)
    return builder.as_markup()


def get_chat_link_ikb(link):
    builder = InlineKeyboardBuilder()
    builder.button(text="📨 Присоединиться", url=link)

    builder.adjust(1)
    return builder.as_markup()
