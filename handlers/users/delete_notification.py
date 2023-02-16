# -*- coding: utf8 -*-
from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists


@dp.message_handler(Command("delete_notification"))
async def del_notification(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer('YES')
