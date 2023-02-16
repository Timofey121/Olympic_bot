from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вывести все!")
        ],
        [
            KeyboardButton(text="Вывести олимпиады, входящие в РСОШ!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
