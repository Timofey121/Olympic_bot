from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons_delete_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='Удаление-Уведомления-Предмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='Удаление-Уведомления-Предмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='Удаление-Уведомления-Предмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='Удаление-Уведомления-Предмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='Удаление-Уведомления-Предмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='Удаление-Уведомления-Предмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='Удаление-Уведомления-Предмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='Удаление-Уведомления-Предмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='Удаление-Уведомления-Предмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='Удаление-Уведомления-Предмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='Удаление-Уведомления-Предмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='Удаление-Уведомления-Предмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='Удаление-Уведомления-Предмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='Удаление-Уведомления-Предмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='Удаление-Уведомления-Предмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='Удаление-Уведомления-Предмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='Удаление-Уведомления-Предмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='Удаление-Уведомления-Предмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='Удаление-Уведомления-Предмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='Удаление-Уведомления-Предмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='Удаление-Уведомления-Предмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='Удаление-Уведомления-Предмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='Удаление-Уведомления-Предмет-Психология'),
        ],
    ],
)
