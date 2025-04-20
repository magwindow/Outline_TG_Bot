import asyncio
import os
from callback_query.callback import router_call
from heandlers.users import router_users
from database.models import init_models
from apshed import start_scheduler
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
bot: Bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp: Dispatcher = Dispatcher()
    dp.include_router(router_users)
    dp.include_router(router_call)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def startup(dispatcher: Dispatcher):
    await init_models()
    start_scheduler(bot)
    print('Bot is started!')


async def shutdown(dispatcher: Dispatcher):
    print('Bot is shutting down...')


if __name__ == '__main__':
    asyncio.run(main())
