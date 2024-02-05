from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_panel_rkb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔗 Ссылки")
    builder.button(text="💰 Профит")
    builder.button(text="👤 Профиль")
    builder.button(text="💬 Наш чат")

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)
