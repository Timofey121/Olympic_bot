from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default.admin_commands import keyboard_4
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import select_all_users, select_data_olimp_use_id, count_users, select_blocked_users, \
    update_blocked_users, subscriber_exists


@dp.message_handler(Command("admin"))
async def notification(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Выберите нужную команду (cм.ниже).', reply_markup=keyboard_4)
        await Test.Q_for_admin_1.set()
    else:
        text = ("ТАКОЙ КОМАНДЫ НЕТ!",
                "Список команд: ",
                "/start - Начать диалог",
                "/info - Вывести информацию о нужной олимпиаде",
                "/notification - Подключение уведомлений",
                "/check_notification - Подключение уведомлений",
                "/delete_notification - Удаление уведомлений",
                "/feedback - Оставить отзыв",
                "/technical_support - Написать в тех поддержку!",
                "/help - Получить справку",
                )

        await message.answer("\n".join(text))


@dp.message_handler(state=Test.Q_for_admin_1)
async def answer(message: types.Message, state: FSMContext):
    try:
        if message.text == "Показать уведомления пользователей!":
            dat = list(await select_all_users())
            for i in range(len(dat)):
                await message.answer(
                    f"У пользователя {dat[i][1]} подключено {len(await select_data_olimp_use_id(dat[i][0]))} "
                    f"уведомления к олимпиадам.", reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text == "Показать полный список пользователей!":
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text == "Показать кол-во пользователей!":
            await message.answer(f"Привет админ! В боте - {list(await count_users())[0][0]} пользователей!",
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text == "Заблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=ReplyKeyboardRemove())
            await Test.Q_for_admin_2.set()
        elif message.text == "Разблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_blocked_users())
            await message.answer(f"Полный заблокированных список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][1]} -> ID = {dat[i][0]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=ReplyKeyboardRemove())
            await Test.Q_for_admin_3.set()
        elif message.text == "Отправить пользователям сообщение!":
            await message.answer(f"Введите сообщение для пользователей!", reply_markup=ReplyKeyboardRemove())
            await Test.Q_for_admin_4.set()
    except Exception as ex:
        print(ex)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_2)
async def block(message: types.Message, state: FSMContext):
    try:
        await update_blocked_users(message.text, 'Да')
        await message.answer(
            f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - ЗАБЛОКИРОВАН")
    except Exception as ex:
        print(ex)
        await message.answer("Такого пользователя не существует!")
    await state.finish()


@dp.message_handler(state=Test.Q_for_admin_3)
async def block(message: types.Message, state: FSMContext):
    try:
        await update_blocked_users(message.text, 'Нет')
        await message.answer(
            f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - РАЗБЛОКИРОВАН")
    except:
        await message.answer("Такого пользователя не существует!")
    await state.finish()


@dp.message_handler(state=Test.Q_for_admin_4)
async def block(message: types.Message, state: FSMContext):
    dat = list(await select_all_users())
    for i in range(len(dat)):
        await dp.bot.send_message(dat[i][0], message.text)
    await state.finish()
