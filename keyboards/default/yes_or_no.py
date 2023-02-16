from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_5 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да!")
        ],
        [
            KeyboardButton(text="Нет, продолжить!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
