import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from additional_files.dictionary import lis_of_subjects
from keyboards.default.connect_all_or_choice import keyboard_1
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, data_olympiads, add_notification_dates, select_data_infor_id, \
    del_olympic, del_olympic_in_olympiads_parsing, select_yes_or_no_in_notifications, select_sub_id, select_tg_or_site, \
    select_sub, select_user


@dp.message_handler(Command("notification"))
async def notification(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
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
                word_text_1 = sa[i]

                await message.answer(hbold(f"Началось подключение уведомлений к {word_text_1.capitalize()}!\n"
                                           f"Это займет около 2х минут"),
                                     reply_markup=ReplyKeyboardRemove())

                sub_id = int(list(await select_sub_id(sub=str(sa[i]).lower().capitalize()))[0][0])
                gen = list(await data_olympiads(sub_id))

                name_olimpiads = []
                stages, schedules, sites, rsochs, sub_ids = [], [], [], [], []
                dates = []

                for item in gen:
                    title, start, stage, schedule, site, rsoch = item[0], item[1], item[2], item[3], item[4], item[5]
                    stages.append(stage)
                    schedules.append(schedule)
                    sites.append(site)
                    sub_ids.append(sub_id)
                    name_olimpiads.append(title)
                    rsochs.append(rsoch)
                    dates.append(start)

                e = 0
                flag = False

                for k in range(len(name_olimpiads)):
                    f = False
                    if message.text == "Подключить ко всем!":
                        f = True
                    elif message.text == "Подключить к олимпиадам, входящим в РСОШ!":
                        if rsochs[k] == 1 or rsochs[k] is True:
                            f = True

                    if f is True:
                        data = datetime.datetime.strptime(''.join(dates[k].split("-")), '%d%m%Y').date()
                        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()
                        if data <= now:
                            await del_olympic(name_olimpiads[k], dates[k], stages[k], schedules[k], sites[k], rsochs[k],
                                              sub_ids[k])
                            await del_olympic_in_olympiads_parsing(name_olimpiads[k], dates[k], stages[k], schedules[k],
                                                                   sites[k], rsochs[k], sub_ids[k])
                        else:
                            e += 1
                            flag = True
                            if len(await select_yes_or_no_in_notifications(answer7, name_olimpiads[k], dates[k],
                                                                           stages[k], schedules[k], sites[k],
                                                                           rsochs[k], sub_ids[k])) == 0:
                                await add_notification_dates(answer7, name_olimpiads[k], dates[k],
                                                             stages[k], schedules[k], sites[k],
                                                             rsochs[k], sub_ids[k])
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
                await message.answer(f"Такого предмета не существует, проверьте правильность написания!",
                                     reply_markup=ReplyKeyboardRemove())
                await state.finish()

        except Exception as ex:
            print(ex)
            await message.answer("Проверьте правильность название предмета! Нашли ошибку, "
                                 "напишите нам в поддержку и мы обязательно ее решим.",
                                 reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def check(dp):
    dat = list(await select_data_infor_id())
    for i in range(len(dat)):
        if len(list(await select_tg_or_site(dat[i][0]))) > 0:
            tg = dat[i][0]
            subject = list(await select_sub(int(dat[i][7])))[0][0]
            information_about_olimpiad = (f"{str(subject).upper()}.  \n"
                                          f"{hunderline(dat[i][1])}.  \n"
                                          f"Начало олимпиады: {hbold(dat[i][2])} \n"
                                          f"Этап олимпиады: {hbold(dat[i][3])} \n"
                                          f"Расписание можете посмотреть {hlink(title='ТУТ!', url=dat[i][4])}\n"
                                          f"Сайт этой олимпиады Вы можете посмотреть"
                                          f"{hlink(title='ТУТ!', url=dat[i][5])}\n")

            data = datetime.datetime.strptime(''.join(dat[i][2].split("-")), '%d%m%Y').date()
            now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()

            flag = ((data - now) <= datetime.timedelta(days=2))
            flag1 = ((data - now) > datetime.timedelta(days=0))

            if flag is True and flag1 is True:
                await dp.bot.send_message(tg, f"{hbold('НЕ ЗАБУДЬТЕ!')}\n\n"
                                              f"{information_about_olimpiad}")
            else:
                if data < now:
                    await del_olympic(dat[i][1], dat[i][2], dat[i][3], dat[i][4], dat[i][5], dat[i][6], dat[i][7])
        else:
            usr = dat[i][0]
            if len(await select_user(telegram_id=usr)) > 0:
                tg = list(await select_user(telegram_id=usr))[0][0]
                subject = list(await select_sub(int(dat[i][7])))[0][0]
                information_about_olimpiad = (f"{str(subject).upper()}.  \n"
                                              f"{hunderline(dat[i][1])}.  \n"
                                              f"Начало олимпиады: {hbold(dat[i][2])} \n"
                                              f"Этап олимпиады: {hbold(dat[i][3])} \n"
                                              f"Расписание можете посмотреть {hlink(title='ТУТ!', url=dat[i][4])}\n"
                                              f"Сайт этой олимпиады Вы можете посмотреть"
                                              f"{hlink(title='ТУТ!', url=dat[i][5])}\n")

                data = datetime.datetime.strptime(''.join(dat[i][2].split("-")), '%d%m%Y').date()
                now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()

                flag = ((data - now) <= datetime.timedelta(days=2))
                flag1 = ((data - now) > datetime.timedelta(days=0))

                if flag is True and flag1 is True:
                    await dp.bot.send_message(tg, f"{hbold('НЕ ЗАБУДЬТЕ!')}\n\n"
                                                  f"{information_about_olimpiad}")
                else:
                    if data < now:
                        await del_olympic(dat[i][1], dat[i][2], dat[i][3], dat[i][4], dat[i][5], dat[i][6], dat[i][7])


@dp.message_handler(Text(equals=["ДА!"]))
async def get_yes(message: types.Message):
    await notification(message)


@dp.message_handler(Text(equals=["НЕТ!"]))
async def get_no(message: types.Message):
    await message.answer("Не подключив уведомления, есть шанс, что Вы потеряете свой ключ на "
                         "светлое будущее!!! В будущем, если Вы захотите подключить "
                         "уведомления,просто напишите '/notification'", reply_markup=ReplyKeyboardRemove())
