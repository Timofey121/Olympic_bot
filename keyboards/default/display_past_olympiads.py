from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вывести!")
        ],
        [
            KeyboardButton(text="Не выводить!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)