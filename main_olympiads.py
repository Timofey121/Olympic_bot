import asyncio

from data.config import ADMINS
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def main():
    for item in ADMINS:
        await dp.bot.send_message(item, 'Бот запущен!')
    await dp.start_polling(on_startup(dp))


if __name__ == '__main__':
    asyncio.run(main())
