from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑🏻‍💻 Получить Секретный Токен для синхронизации сайта и Телеграмм бота"),
        ],
        [
            KeyboardButton(text="✍️ Вывести информацию о нужной олимпиаде"),
        ],
        [
            KeyboardButton(text="🔔 Просмотр подключенных уведомлений")
        ],
        [
            KeyboardButton(text="🔔 Подключение уведомлений"),
            KeyboardButton(text="🔔 Удаление уведомлений"),
        ],
        [
            KeyboardButton(text="📝 Оставить отзыв"),
            KeyboardButton(text="📝 Написать в тех поддержку"),
        ],
        [
            KeyboardButton(text="🧑🏻‍💻 Об авторе"),
        ],
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
