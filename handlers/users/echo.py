from aiogram import types  # подключение модуля для работы с сообщениями

from loader import dp  # подключение Dispatcher, подключенного к Telegram боту


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    text = ("ТАКОЙ КОМАНДЫ НЕТ!",
            "Список команд: ",
            "/start - Начать диалог",
            "/info - Вывести информацию о нужной олимпиаде",
            "/notification - Подключение уведомлений",
            "/check_notification - Просмотр подключенных уведомлений",
            "/delete_notification - Удаление уведомлений",
            "/feedback - Оставить отзыв",
            "/technical_support - Написать в тех поддержку!",
            )

    await message.answer("\n".join(text))  # вывод текст - ответ на команду
