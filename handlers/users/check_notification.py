import pymorphy2
from aiogram import types
from aiogram.dispatcher.filters import Command

from additional_files.dictionary import sub
from loader import dp
from utils.db_api.PostgreSQL import select_data_sub_info, subscriber_exists


@dp.message_handler(Command("check_notification"))
async def check_notification(message: types.Message):
    if str(list(await subscriber_exists(message.from_user.id))[0][2]) != "Да":
        await message.answer("Подождите немного! Начался поиск Ваших уведомлений!")
        try:
            a = list(await select_data_sub_info(telegram_id=message.from_user.id))
            c = [[]]
            t = 0
            if len(a) > 0:
                for i in range(len(a)):
                    if len(str("\n".join(c[t]))) + len(str(f"{i + 1}) Уведомления подключены к \n"
                                                           f"{str(''.join(a[i][2]))}")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"{i + 1}) Уведомления подключены к \n{str(''.join(a[i][2]))}")

                for i in range(len(c)):
                    await message.answer("\n".join(c[i]))
            else:
                await message.answer(
                    "К сожалению, у Вас не подключены уведомления. Для подключения уведомлений напишите -"
                    " '/notification'")
        except Exception as ex:
            print(ex)
            await message.answer(
                "К сожалению, у Вас не подключены уведомления. Для подключения уведомлений напишите - '/notification'")
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")
