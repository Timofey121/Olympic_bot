import asyncio

from additional_files.parsing_olimpiads import subject_to_bd
from data.config import ADMINS
from handlers.users.notification import check
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def test(dispatcher):
    while True:
        try:
            await check(dispatcher)
        except Exception as ex:
            pass
        await asyncio.sleep(43200)


async def test1():
    while True:
        await subject_to_bd()
        print('!')
        await asyncio.sleep(432000)


async def main():
    for item in ADMINS:
        await dp.bot.send_message(item, 'Бот запущен!')
    asyncio.create_task(test(dp))
    asyncio.create_task(test1())
    await dp.start_polling(on_startup(dp))


if __name__ == '__main__':
    asyncio.run(main())
