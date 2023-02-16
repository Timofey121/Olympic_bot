# -*- coding: utf8 -*-

import pymorphy2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from additional_files.dictionary import sub, lis_of_subjects, subjects_rsosh
from handlers.users.notification import notification
from keyboards.default.all_or_choice import keyboard_1
from keyboards.default.connect_or_no import keyboard
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, information_about_olympiads


@dp.message_handler(Command("info"), state=None)
async def info(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer(
            f"{hbold('Введите предмет(ы)')} олимпиады(у) которого вы хотите найти! (c большой буквы, через запятую)!\n \n"
            'Список доступных предметов, по которым мы предоставляем информацию о олимпиадах:\n')
        abc = []
        for i in range(len(lis_of_subjects)):
            abc.append(f"{i + 1}) {lis_of_subjects[i]}")
        await message.answer(f"{''.join(abc)}"
                             f"{hbold('Пример ввода:')}\n"
                             "1) География\n"
                             "2) География, Математика")
        await Test.Q_for_info_1.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_info_1)
async def info_3(message: types.Message, state: FSMContext):
    global word_text, z, e, i
    answer_2 = message.text
    await state.update_data(answer2=answer_2)

    await message.answer('Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
                         reply_markup=keyboard_1)
    await Test.Q_for_info_2.set()


@dp.message_handler(state=Test.Q_for_info_2)
async def info_4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer2 = data.get("answer2")
    sa = answer2.split(",")
    for i in range(len(sa)):
        sa[i] = str(sa[i]).lstrip().rstrip()

    for i in range(len(sa)):
        ht = sa[i]
        yt = sa[i]
        try:
            if sa[i] in sub:
                word_text = sub[sa[i]]
            else:
                morse = pymorphy2.MorphAnalyzer()
                ji = morse.parse(sa[i].strip())[0]

                word_text = ji.inflect({'loct'}).word

            await message.answer(hbold(f"Подождите немного!\nНачался поиск информации о {word_text.capitalize()}!\n"
                                       f"Это займет около 2х минут"),
                                 reply_markup=ReplyKeyboardRemove())

            gen = list(await information_about_olympiads(str(ht).lower().capitalize()))

            name_olimpiads = []
            information_olimpiads = []

            for item in gen:
                name_olimpiads.append(item[0])
                information_olimpiads.append(item[1])

            count = 0
            count_1 = 0
            flag = False

            for k in range(len(name_olimpiads)):
                f = False

                if message.text == "Вывести все!":
                    f = True
                elif message.text == "Вывести олимпиады, входящие в РСОШ!":
                    f = name_olimpiads[k].strip() in subjects_rsosh[yt.lower().capitalize()]
                    count_1 += 1

                if f is True:
                    count += 1
                    flag = True
                    await message.answer(f"{count}) {information_olimpiads[k]}")

            if flag is False:
                if count_1 == 0:
                    await message.answer(
                        'К сожалению, нет таких олимпиад, которые помогут при поступлении в ВУЗ! '
                        'Или они все уже прошли.')
                else:
                    await message.answer('К сожалению, все олимпиады по этому предмету уже прошли')
            else:
                await message.answer(
                    hbold("Олимпиада — отличная штука! Она упрощает  поступление в ВУЗ – мечты! Олимпиада позволяет "
                          "поступить в ВУЗ без экзаменов  или засчитывается  100 баллов по ЕГЭ. "))
                await message.answer(
                    hbold("Не забывайте, что ЕГЭ — это всего одна попытка и многое зависит от воли случая. На "
                          "олимпиадах случайности тоже важны, но олимпиад много, соответственно количество раз, "
                          "которое вы попробуете, зависит только от вас. Тут работает теория вероятностей"
                          " — чем больше пробуешь, тем выше шансы на успех."))
                await message.answer(
                    hbold("По статистике каждый школьник забывает примерно 6 из 10 олимпиад, из-за этого появляются "
                          "сложности при поступлении в ВУЗ. Поэтому мы предлагаем Вам, подключить уведомления на "
                          "разные предметы, хотите подключить уведомления?"), reply_markup=keyboard)

        except Exception as ex:
            print(ex)
            await message.answer("Проверьте правильность название предмета! Если все правильно, "
                                 "проверьте синтаксис, или посмотрите примеры, которые есть под "
                                 "вопросами!")

    await state.finish()


@dp.message_handler(Text(equals=["Подключить!"]))
async def get(message: types.Message):
    await notification(message)


@dp.message_handler(Text(equals=["Не подключать!"]))
async def get_not(message: types.Message):
    await message.answer(
        "Не подключив уведомления, есть шанс, что Вы потеряете свой ключ на светлое будущее! В будущем, "
        "если Вы захотите подключить уведомления,просто напишите '/notification'", reply_markup=ReplyKeyboardRemove())
