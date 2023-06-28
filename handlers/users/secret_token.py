from secrets import token_hex

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, secret_token_exists, add_token


@dp.message_handler(Command("secret_token"))
async def bot_help(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        if len(await secret_token_exists(message.from_user.id)) > 0:
            await message.answer(
                f"Ваш Секретный Токен для синхронизации с сайтом\n\n{list(await secret_token_exists(message.from_user.id))[0][-1]}")
        else:
            token = token_hex(32)
            await add_token(telegram_id=message.from_user.id, token=token)
            await message.answer(f"Ваш Секретный Токен для синхронизации с сайтом\n\n{token}")
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")
