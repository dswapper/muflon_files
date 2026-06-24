from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


game_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🍎 Покормить", callback_data="muflon_feed"),
        InlineKeyboardButton(text="🧼 Помыть", callback_data="muflon_wash"),
        InlineKeyboardButton(text="😴 Уложить спать", callback_data="muflon_sleep"),
    ],
    [
        InlineKeyboardButton(text="🥊 Вызвать игрока на бой", callback_data="muflon_pvp-start"),
        InlineKeyboardButton(text="🎲 Мини-игры", callback_data="muflon_mini-games"),
    ],
    [
        InlineKeyboardButton(text="🛒 Магазин", callback_data="muflon_pvp-start"),
        InlineKeyboardButton(text="🎒 Инвентарь", callback_data="muflon_mini-games"),
    ],
])
