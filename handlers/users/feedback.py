# -*- coding: utf8 -*-
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import add_user_feedback, subscriber_exists


@dp.message_handler(Command("feedback"), state=None)
async def feedback(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer("Привет ещё раз, мы очень рады, что Вы решили оставить отзыв! Напишите Ваш отзыв.")
        await Test.Q_for_feedback.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_feedback)
async def feedback_1(message: types.Message, state: FSMContext):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        answer = message.text
        await add_user_feedback(feedback=answer, telegram_id=message.from_user.id)
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin,
                                          f"Сообщение о отзыве для админов:\n"
                                          f"Full_name = {message.from_user.full_name}\n"
                                          f"is_bot = {'Не бот!' if message.from_user.is_bot is False else 'Бот!'}\n"
                                          f"User_name = @{'Нет значения' if message.from_user.username is None else message.from_user.username}\n"
                                          f"id = {message.from_user.id}\n"
                                          f"Language = {message.from_user.language_code}\n\n"
                                          f"Отзыв:\n"
                                          f"{answer}")
            except Exception as err:
                logging.exception(err)
        await state.finish()
