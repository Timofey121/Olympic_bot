from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_buttons_choose_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вывести все!", callback_data="Уведомления-Вывести-все")
        ],
        [
            InlineKeyboardButton(text="Вывести олимпиады, входящие в РСОШ!", callback_data="Уведомления-Вывести-РСОШ")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
