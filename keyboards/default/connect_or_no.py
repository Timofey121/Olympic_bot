from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подключить!")
        ],
        [
            KeyboardButton(text="Не подключать!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
