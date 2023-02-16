from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подключить ко всем!")
        ],
        [
            KeyboardButton(text="Подключить к олимпиадам, входящим в РСОШ!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)