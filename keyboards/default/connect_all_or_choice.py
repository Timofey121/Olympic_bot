from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подключить ко всем!")
        ],
        [
            KeyboardButton(text="Подключить только к тем, которые помогут при поступлении в ВУЗ!")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)