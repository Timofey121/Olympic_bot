# -*- coding: utf8 -*-
import pymorphy2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from additional_files.dictionary import lis_of_subjects, sub
from keyboards.default.del_subject_or_choice import keyboard_3
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import select_data_olimp_use_id, subscriber_exists, select_data_sub_info, \
    select_data_olimp_use_subject, del_data_in_olimpic, del_notif_in_olimpic


@dp.message_handler(Command("delete_notification"))
async def del_notification(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer('Выберите способ удаления уведомлений(cм.ниже).', reply_markup=keyboard_3)
        await Test.Q_for_delete_notification_1.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_delete_notification_1)
async def del_notification_1(message: types.Message, state: FSMContext):
    answer_1 = message.text
    await state.update_data(answer1=answer_1)
    if message.text == "Удалить уведомления определенного предмета!":
        try:
            if len(list(await select_data_olimp_use_id(telegram_id=message.from_user.id))) > 0:
                await message.answer(
                    "Введите предмет информацию о олимпиаде(ах) которого Вы хотите удалить(C большой буквы, через "
                    "запятую)!\n\nСписок доступных предметов, по которым мы предоставляем информацию о олимпиадах:\n",
                    reply_markup=ReplyKeyboardRemove())
                abc = []
                for i in range(len(lis_of_subjects)):
                    abc.append(f"{i + 1}) {lis_of_subjects[i]}")
                await message.answer(
                    f"{''.join(abc)}\n Пример ввода:\n"
                    "1) География\n"
                    "2) География, Математика")
            else:
                await message.answer(
                    "Перед тем, чтобы удалять уведомления, их надо подключить, для подключения уведомлений "
                    "напишите - '/notification'")
        except:
            await message.answer(
                "Перед тем, чтобы удалять уведомления, их надо подключить, для подключения уведомлений "
                "напишите - '/notification'")
    elif message.text == "Удалить выбранные уведомления(по номеру)!":
        await message.answer("Подождите немного! Начался поиск уведомлений!")
        a = list(await select_data_sub_info(telegram_id=message.from_user.id))
        c = [[]]
        t = 0
        if len(a) > 0:
            for i in range(len(a)):
                if a[i][1] in sub:
                    word_text = sub[a[i][1]]
                else:
                    morse = pymorphy2.MorphAnalyzer()
                    ji = morse.parse(a[i][1].strip())[0]
                    word_text = ji.inflect({'loct'}).word

                if len(str("\n".join(c[t]))) + len(str(f"{i + 1}) Уведомления подключены к {word_text}\n"
                                                       f"{str(''.join(a[i][2]))}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"{i + 1}) Уведомления подключены к {word_text.capitalize()}\n{str(''.join(a[i][2]))}")

            for i in range(len(c)):
                await message.answer("\n".join(c[i]))
        await message.answer("Введите номера тех олимпиад, уведомления которых Вы хотите удалить(через запятую)!",
                             reply_markup=ReplyKeyboardRemove())

    await Test.Q_for_delete_notification_2.set()


@dp.message_handler(state=Test.Q_for_delete_notification_2)
async def del_notification_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    telegram_id = message.from_user.id
    if answer1 == "Удалить уведомления определенного предмета!":
        sa = message.text.split(",")
        for i in range(len(sa)):
            sa[i] = str(sa[i]).lstrip().rstrip()
        for i in range(len(sa)):
            try:
                if f'{sa[i]}  \n' in lis_of_subjects:
                    htt = sa[i]
                    rgt = list(await select_data_olimp_use_subject(str(htt).lower().capitalize()))

                    if sa[i] in sub:
                        word_text = sub[sa[i]]
                    else:
                        morse = pymorphy2.MorphAnalyzer()
                        ji = morse.parse(sa[i].strip())[0]
                        word_text = ji.inflect({'datv'}).word

                    if rgt:
                        await message.answer(
                            hbold(f"Началось отключение уведомлений, подключенных к {word_text.capitalize()}!"))
                        rt = sa[i]
                        await del_data_in_olimpic(telegram_id=telegram_id, subject=rt)
                        await message.answer(hbold(f"Отключены уведомления, подключенные к {word_text.capitalize()}!"))
                    else:
                        await message.answer(hbold(f"Уведомления не подключены к {word_text.capitalize()}"))
                else:
                    await message.answer(f"Такого предмета не существует, проверьте правильность написания!")
            except Exception as ex:
                await message.answer("Проверьте правильность название предмета! Нашли ошибку, "
                                     "напишите нам в поддержку и мы обязательно ее решим.")

    elif answer1 == "Удалить выбранные уведомления(по номеру)!":
        try:
            sa = message.text.split(",")
            for i in range(len(sa)):
                sa[i] = str(sa[i]).lstrip().rstrip()
            a = list(await select_data_sub_info(telegram_id=message.from_user.id))
            for i in range(len(a)):
                if str(int(i + 1)) in sa:
                    await del_notif_in_olimpic(telegram_id=telegram_id, information=''.join(a[i][2]))
                    await message.answer("Уведомления отключены от")
                    await message.answer(f"{i + 1}) {str(''.join(a[i][2]))}")
        except Exception as ex:
            await message.answer(f"Проверьте правильность номеров уведомлений, для удаления!")
            pass

    await state.finish()
