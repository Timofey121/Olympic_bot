from aiogram import types

from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists


@dp.message_handler(text="🧑🏻‍💻 Об авторе")
async def bot_help(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        text = ("Об авторе в Телеграмме -> @My_IT_RESUME_bot",
                "GitHub -> https://github.com/Timofey121"
                )
        await message.answer("\n".join(text))
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")
