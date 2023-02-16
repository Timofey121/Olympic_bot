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
from utils.db_api.PostgreSQL import subscriber_exists, data_olympiads, add_notification_dates, select_data_infor_id


@dp.message_handler(Command("notification"))
async def notification(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer(
            f"{hbold('Введите предмет(ы)')} информацию о олимпиаде(ах) Вы хотите знать(C большой буквы, через запятую)!\n \n"
            'Список доступных предметов, по которым мы предоставляем информацию о олимпиадах:\n',
            reply_markup=ReplyKeyboardRemove())
        abc = []
        for i in range(len(lis_of_subjects)):
            abc.append(f"{i + 1}) {lis_of_subjects[i]}")
        await message.answer(f"{''.join(abc)}"
                             f"{hbold('Пример ввода:')}\n"
                             "1) География\n"
                             "2) География, Математика")
        await Test.Q_for_notification.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.message_handler(state=Test.Q_for_notification)
async def notification_3(message: types.Message, state: FSMContext):
    global dat, all, sa, titles, word_text, z, e, i
    answer_6 = message.text
    await state.update_data(answer6=answer_6)

    await message.answer('Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
                         reply_markup=keyboard_1)
    await Test.Q_for_notification_2.set()


@dp.message_handler(state=Test.Q_for_notification_2)
async def notification_4(message: types.Message, state: FSMContext):
    global dat, all, titles, answer7, frt
    data = await state.get_data()
    answer6 = data.get("answer6")
    answer7 = message.from_user.id

    sa = answer6.split(",")
    for i in range(len(sa)):
        sa[i] = str(sa[i]).lstrip().rstrip()

    for i in range(len(sa)):
        ht = sa[i]
        yt = sa[i]
        rt = sa[i]
        dat = []
        titles = []
        j = 0
        j += 1
        try:
            if sa[i] in sub:
                word_text_1 = sub[sa[i]]
            else:
                morse = pymorphy2.MorphAnalyzer()
                ji = morse.parse(sa[i].strip())[0]
                word_text_1 = ji.inflect({'datv'}).word
            await message.answer(hbold(f"Началось подключение уведомлений к {word_text_1.capitalize()}!\n"
                                       f"Это займет около 2х минут"),
                                 reply_markup=ReplyKeyboardRemove())

            gen = list(await data_olympiads(str(ht).lower().capitalize()))

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
                elif message.text == "Подключить к олимпиадам, входящим в РСОШ!":
                    if name_olimpiads[k] in subjects_rsosh[yt.lower().capitalize()]:
                        f = True

                if f is True:
                    e += 1
                    flag = True
                    await add_notification_dates(telegram_id=answer7, data_olymp=data_start[k], subject=rt,
                                                 information=information_olimpiads[k])
            if flag is False:
                await message.answer("К сожалению, все олимпиады по этому предмету прошли. Уведомления  "
                                     "возможно подключить после  утверждения графика проведения олимпиад "
                                     "школьников и их уровней на 2021/22 учебный год по профилям! Ориентировочно "
                                     "сентябрь-октябрь 2022г!")
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

        except Exception as ex:
            print(ex)
            await message.answer(
                "Проверьте правильность название города, предметов или класса! Если все правильно, "
                "проверьте пожайлуйста синтаксис, или посмотрите примеры, которые есть под каждым "
                "вопросом!")
            break

    await state.finish()


async def check(dp):
    dat = list(await select_data_infor_id())
    for i in range(len(dat)):
        data = datetime.datetime.strptime(''.join(dat[i][1].split("-")), '%Y%m%d').date()
        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date()

        flag = ((data - now) <= datetime.timedelta(days=1))
        flag1 = ((data - now) > datetime.timedelta(days=0))

        if flag is True and flag1 is True:
            await dp.bot.send_message(dat[i][0], f"Не забудьте\n"
                                                 f"{dat[i][2]}")


@dp.message_handler(Text(equals=["ДА!"]))
async def get_yes(message: types.Message):
    await notification(message)


@dp.message_handler(Text(equals=["НЕТ!"]))
async def get_yes(message: types.Message):
    await message.answer("Не подключив уведомления, есть шанс, что Вы потеряете свой ключ на "
                         "светлое будущее!!! В будущем, если Вы захотите подключить "
                         "уведомления,просто напишите '/notification'", reply_markup=ReplyKeyboardRemove())


