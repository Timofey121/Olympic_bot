# -*- coding: utf8 -*-
import datetime

import pymorphy2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from additional_files.dictionary import sub, lis_of_subjects, subjects_rsosh
from additional_files.parsing_olimpiads import select_sub_id
from handlers.users.notification import notification
from keyboards.default.all_or_choice import keyboard_1
from keyboards.default.connect_or_no import keyboard
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, information_about_olympiads, del_olympic, \
    del_olympic_in_olympiads_parsing


@dp.message_handler(Command("info"), state=None)
async def info(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer(
            f"{hbold('Введите предмет(ы)')} интересующих Вас олимпиады! (c большой буквы, через запятую)!\n \n"
            'Список доступных предметов, по которым мы предоставляем информацию об олимпиадах:\n',
            reply_markup=ReplyKeyboardRemove())
        abc = []
        for i in range(len(lis_of_subjects)):
            abc.append(f"{i + 1}) {lis_of_subjects[i]}")
        await message.answer(f"{''.join(abc)}\n"
                             f"{hbold('Пример ввода:')}\n"
                             "1) География\n"
                             "2) География, Математика")
        await Test.Q_for_info_1.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_info_1)
async def info_3(message: types.Message, state: FSMContext):
    answer_2 = message.text
    await state.update_data(answer2=answer_2)

    await message.answer('Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
                         reply_markup=keyboard_1)
    await Test.Q_for_info_2.set()


@dp.message_handler(state=Test.Q_for_info_2)
async def info_4(message: types.Message, state: FSMContext):
    global name_olimpiads, information_olimpiads, data_start, gen, e, a, count, count_1, sa, abc
    data = await state.get_data()
    answer2 = data.get("answer2")
    sa = answer2.split(",")
    for i in range(len(sa)):
        sa[i] = str(sa[i]).lstrip().rstrip()

    for i in range(len(sa)):
        try:
            if f'{sa[i]}  \n' in lis_of_subjects:
                if sa[i] in sub:
                    word_text = sub[sa[i]]
                else:
                    morse = pymorphy2.MorphAnalyzer()
                    ji = morse.parse(sa[i].strip())[0]
                    word_text = ji.inflect({'loct'}).word

                await message.answer(
                    hbold(f"Подождите немного!\nНачался поиск информации об {word_text.capitalize()}!\n"
                          f"Это займет около 2х минут"),
                    reply_markup=ReplyKeyboardRemove())

                sub_id = int(list(await select_sub_id(sub=str(sa[i]).lower().capitalize()))[0][0])
                gen = list(await information_about_olympiads(sub_id))

                name_olimpiads = []
                information_olimpiads = []
                stages, schedules, sites, rsochs, sub_ids = [], [], [], [], []
                dates = []

                for item in gen:
                    title, start, stage, schedule, site = item[0], item[1], item[2], item[3], item[4]
                    stages.append(title)
                    schedules.append(title)
                    sites.append(title)
                    rsochs.append(title)
                    sub_ids.append(title)
                    information_about_olimpiad = (f"{hunderline(title)}.  \n"
                                                  f"Этап олимпиады - {hbold(stage)} \n"
                                                  f"{start} \n"
                                                  f"Расписание можете посмотреть {hlink(title='ТУТ!', url=schedule)}\n"
                                                  f"Сайт этой олимпиады Вы можете посмотреть"
                                                  f"{hlink(title='ТУТ!', url=site)}\n")
                    information_olimpiads.append(information_about_olimpiad)
                    dates.append(start)

                count = 0
                count_1 = 0
                flag = False

                for k in range(len(name_olimpiads)):
                    f = False

                    if message.text == "Вывести все!":
                        f = True
                    elif message.text == "Вывести олимпиады, входящие в РСОШ!":
                        f = name_olimpiads[k].strip() in subjects_rsosh[sa[i].lower().capitalize()]
                        count_1 += 1

                    if f is True:
                        if datetime.datetime.strptime(''.join(dates[k].split("-")),
                                                      '%Y%m%d').date() <= datetime.datetime.strptime(
                            datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date():
                            await del_olympic(name_olimpiads[k], dates[k], stages[k], schedules[k], sites[k], rsochs[k],
                                              sub_ids[k])
                            await del_olympic_in_olympiads_parsing(name_olimpiads[k], dates[k], stages[k], schedules[k],
                                                                   sites[k], rsochs[k], sub_ids[k])
                        else:
                            count += 1
                            flag = True
                            await message.answer(f"{count}) {information_olimpiads[k]}")

                if flag is False:
                    if count_1 == 0:
                        await message.answer(
                            'К сожалению, все олимпиды по этому предмету в этом учебном году прошли!')
                    else:
                        await message.answer('К сожалению, все олимпиды по этому предмету в этом учебном году прошли!')
                else:
                    if i + 1 == len(sa):
                        await message.answer(
                            hbold("Олимпиады упрощают поступление в ВУЗ! Они позволяют "
                                  "поступить в ВУЗ без экзаменов или засчитать 100 баллов по ЕГЭ."))
                        await message.answer(
                            hbold("Не забывайте, что ЕГЭ — это всего одна попытка. Олимпиад много "
                                  "и количество раз, "
                                  "которое вы попробуете, зависит только от вас. Тут работает теория вероятностей"
                                  " — чем больше пробуешь, тем выше шансы на успех."))
                        await message.answer(
                            hbold("По статистике каждый школьник забывает примерно о 6 из 10 олимпиад, из-за этого"
                                  " снижается шанс поступления в ВУЗ. Поэтому мы предлагаем Вам, бесплатно "
                                  "подключить уведомления на "
                                  "разные олимпиады, хотите подключить уведомления?"), reply_markup=keyboard)
            else:
                await message.answer(f"Такого предмета не существует, проверьте правильность написания!",
                                     reply_markup=ReplyKeyboardRemove())

        except Exception as ex:
            await message.answer("Проверьте правильность название предмета! Нашли ошибку, "
                                 "напишите нам в поддержку и мы обязательно ее решим.")

    await state.finish()


@dp.message_handler(Text(equals=["Подключить!"]))
async def get(message: types.Message):
    await notification(message)


@dp.message_handler(Text(equals=["Не подключать!"]))
async def get_not(message: types.Message):
    await message.answer(
        "Не подключив уведомления, есть шанс, что Вы потеряете свой ключ на светлое будущее! В будущем, "
        "если Вы захотите подключить уведомления,просто напишите '/notification'", reply_markup=ReplyKeyboardRemove())
