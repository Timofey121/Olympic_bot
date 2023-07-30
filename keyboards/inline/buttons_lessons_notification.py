from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='Уведомления-Предмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='Уведомления-Предмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='Уведомления-Предмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='Уведомления-Предмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='Уведомления-Предмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='Уведомления-Предмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='Уведомления-Предмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='Уведомления-Предмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='Уведомления-Предмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='Уведомления-Предмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='Уведомления-Предмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='Уведомления-Предмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='Уведомления-Предмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='Уведомления-Предмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='Уведомления-Предмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='Уведомления-Предмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='Уведомления-Предмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='Уведомления-Предмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='Уведомления-Предмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='Уведомления-Предмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='Уведомления-Предмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='Уведомления-Предмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='Уведомления-Предмет-Психология'),
        ],
    ],
)
