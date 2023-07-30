from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_buttons_choose_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подключить ко всем!", callback_data="Уведомления-Вывести-все")
        ],
        [
            InlineKeyboardButton(text="Подключить к олимпиадам, входящим в РСОШ!",
                                 callback_data="Уведомления-Вывести-РСОШ")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
