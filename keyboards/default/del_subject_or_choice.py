from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_3 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Удалить уведомления определенного предмета!")
        ],
        [
            KeyboardButton(text="Удалить выбранные уведомления!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
