# -*- coding: utf8 -*-
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import add_user_tech, subscriber_exists


@dp.message_handler(Command("technical_support"), state=None)
async def technical_support(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        if message.from_user.username is None:
            await message.answer(f"Привет, к сожалению, мы не сможем ответить Вам, т.к. у Вас нет имени пользователя!"
                                 f"Укажите пожалуйста его в настройках, чтобы мы смогли с Вами связаться!")
            photo = open('handlers/users/img.png', 'rb')
            await message.answer_photo(photo)
        else:
            await message.answer("Привет ещё раз, расскажи в чем проблема? Мы ответим Вам, как только закончим"
                                 " с предыдущем вопросом!")
            await Test.Q_for_tech_support.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_tech_support)
async def technical_support_1(message: types.Message, state: FSMContext):
    answer = message.text
    await add_user_tech(telegram_id=str(message.from_user.id), help=answer)
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin,
                                      f"Сообщение о технической поддержки для админов:\n"
                                      f"Full_name = {message.from_user.full_name}\n"
                                      f"is_bot = {'Не бот!' if message.from_user.is_bot is False else 'Бот!'}\n"
                                      f"User_name = @{'Нет значения' if message.from_user.username is None else message.from_user.username}\n"
                                      f"id = {message.from_user.id}\n"
                                      f"Language = {message.from_user.language_code}\n\n"
                                      f"Его просьба:\n"
                                      f"{answer}")
        except Exception as err:
            logging.exception(err)
    await state.finish()
