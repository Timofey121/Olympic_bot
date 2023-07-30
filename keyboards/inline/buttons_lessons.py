from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='Информация-Предмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='Информация-Предмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='Информация-Предмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='Информация-Предмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='Информация-Предмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='Информация-Предмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='Информация-Предмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='Информация-Предмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='Информация-Предмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='Информация-Предмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='Информация-Предмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='Информация-Предмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='Информация-Предмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='Информация-Предмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='Информация-Предмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='Информация-Предмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='Информация-Предмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='Информация-Предмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='Информация-Предмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='Информация-Предмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='Информация-Предмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='Информация-Предмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='Информация-Предмет-Психология'),
        ],
    ],
)
