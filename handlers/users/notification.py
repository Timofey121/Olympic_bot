import datetime

import pymorphy2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from additional_files.dictionary import lis_of_subjects, sub, subjects_rsosh
from keyboards.default.connect_all_or_choice import keyboard_1
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, data_olympiads, add_notification_dates, select_data_infor_id, \
    del_olympic, del_olympic_in_olympiads_parsing, select_yes_or_no_in_notifications


@dp.message_handler(Command("notification"))
async def notification(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer(
            f"{hbold('Введите предмет(ы)')} информацию о олимпиаде(ах) Вы хотите знать"
            f"(C большой буквы, через запятую)!\n \n"
            'Список доступных предметов, по которым мы предоставляем информацию о олимпиадах:\n',
            reply_markup=ReplyKeyboardRemove())
        abc = []
        for i in range(len(lis_of_subjects)):
            abc.append(f"{i + 1}) {lis_of_subjects[i]}")
        await message.answer(f"{''.join(abc)}\n"
                             f"{hbold('Пример ввода:')}\n"
                             "1) География\n"
                             "2) География, Математика")
        abc = []
        await Test.Q_for_notification.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_notification)
async def notification_3(message: types.Message, state: FSMContext):
    answer_6 = message.text
    await state.update_data(answer6=answer_6)

    await message.answer('Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
                         reply_markup=keyboard_1)
    await Test.Q_for_notification_2.set()


@dp.message_handler(state=Test.Q_for_notification_2)
async def notification_4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer6 = data.get("answer6")
    answer7 = message.from_user.id

    sa = answer6.split(",")
    for i in range(len(sa)):
        sa[i] = str(sa[i]).lstrip().rstrip()

    for i in range(len(sa)):
        try:
            if f'{sa[i]}  \n' in lis_of_subjects:
                if sa[i] in sub:
                    word_text_1 = sub[sa[i]]
                else:
                    morse = pymorphy2.MorphAnalyzer()
                    ji = morse.parse(sa[i].strip())[0]
                    word_text_1 = ji.inflect({'datv'}).word
                await message.answer(hbold(f"Началось подключение уведомлений к {word_text_1.capitalize()}!\n"
                                           f"Это займет около 2х минут"),
                                     reply_markup=ReplyKeyboardRemove())

                gen = list(await data_olympiads(str(sa[i]).lower().capitalize()))

                name_olimpiads = []
                information_olimpiads = []
                data_start = []

                for item in gen:
                    name_olimpiads.append(item[0])
                    information_olimpiads.append(item[1])
                    data_start.append(item[2])

                e = 0
                flag = False
                for k in range(len(name_olimpiads)):
                    f = False
                    if message.text == "Подключить ко всем!":
                        f = True
                        a = 'no'
                    elif message.text == "Подключить к олимпиадам, входящим в РСОШ!":
                        if name_olimpiads[k] in subjects_rsosh[sa[i].lower().capitalize()]:
                            a = 'yes'
                            f = True

                    if f is True:
                        data = datetime.datetime.strptime(''.join(data_start[k].split("-")), '%Y%m%d').date()
                        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date()
                        if data <= now:
                            await del_olympic(information_olimpiads[k])
                            await del_olympic_in_olympiads_parsing(information_olimpiads[k])
                        else:
                            e += 1
                            flag = True
                            if len(await select_yes_or_no_in_notifications(answer7, information_olimpiads[k])) == 0:
                                await add_notification_dates(telegram_id=answer7, data_olymp=data_start[k],
                                                             subject=sa[i],
                                                             information=information_olimpiads[k], rsoch=a)
                if flag is False:
                    await message.answer(f"К сожалению, все олимпиады по этому предмету прошли. Уведомления  "
                                         "возможно подключить после  утверждения графика проведения олимпиад "
                                         f"школьников и их уровней "
                                         f"{datetime.datetime.now().year}/{datetime.datetime.now().year + 1} на "
                                         f"учебный год! Ориентировочно "
                                         "сентябрь-октябрь!")
                else:
                    if message.text == "Подключить к олимпиадам, входящим в РСОШ!":
                        if e == 0:
                            await message.answer(
                                hbold(f"К сожалению, нет таких олимпиад, которые помогут Вам при поступлении, "
                                      f"посмотрите весь список олимпиад по {str(word_text_1).capitalize()}:"))
                            break
                        else:
                            await message.answer(hbold(f"Уведомления подключены к {word_text_1.capitalize()}!"))
                    elif message.text == "Подключить ко всем!":
                        await message.answer(hbold(f"Подключены уведомления к {word_text_1.capitalize()}!"))
            else:
                await message.answer(f"Такого предмета не существует, проверьте правильность написания!")
                await state.finish()

        except Exception as ex:
            await message.answer("Проверьте правильность название предмета! Нашли ошибку, "
                                 "напишите нам в поддержку и мы обязательно ее решим.")
    await state.finish()


async def check(dp):
    dat = list(await select_data_infor_id())
    for i in range(len(dat)):
        data = datetime.datetime.strptime(''.join(dat[i][1].split("-")), '%Y%m%d').date()
        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date()

        flag = ((data - now) <= datetime.timedelta(days=2))
        flag1 = ((data - now) > datetime.timedelta(days=0))

        if flag is True and flag1 is True:
            await dp.bot.send_message(dat[i][0], f"{hbold('НЕ ЗАБУДЬТЕ!')}\n\n"
                                                 f"{dat[i][2]}")
        else:
            if data < now:
                await del_olympic(dat[i][2])
    dat = []


@dp.message_handler(Text(equals=["ДА!"]))
async def get_yes(message: types.Message):
    await notification(message)


@dp.message_handler(Text(equals=["НЕТ!"]))
async def get_no(message: types.Message):
    await message.answer("Не подключив уведомления, есть шанс, что Вы потеряете свой ключ на "
                         "светлое будущее!!! В будущем, если Вы захотите подключить "
                         "уведомления,просто напишите '/notification'", reply_markup=ReplyKeyboardRemove())
