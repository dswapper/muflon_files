from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


game_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="О муфлоне", callback_data="about_muflon"),
    ],
    [
        InlineKeyboardButton(text="О чате", callback_data="about_chat"),
    ]
])
