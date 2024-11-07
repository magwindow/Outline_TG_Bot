import asyncio
import os
from callback_query.callback import router_call
from heandlers.users import router_users

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


async def start():
    bot: Bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp: Dispatcher = Dispatcher()
    dp.include_router(router_users)
    dp.include_router(router_call)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
