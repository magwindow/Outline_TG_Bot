import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from callback_query.callback import router_call
from heandlers.users import router_users
from database.models import init_models
from middlewares.trial_access import TrialAccessMiddleware
from apshed import start_scheduler
from payments.admin_panel import admin_router
from payments.fake_payment import fake_payment_router
from tasks import cleanup_expired_keys

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Создание бота
bot: Bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def startup(dispatcher: Dispatcher):
    await init_models()  # Инициализация моделей БД
    start_scheduler(bot)  # Запуск планировщика
    asyncio.create_task(cleanup_expired_keys())
    print('Bot is started!')


async def shutdown(dispatcher: Dispatcher):
    print('Bot is shutting down...')


async def main():
    dp = Dispatcher()

    # Подключаем middleware ДО роутеров
    dp.callback_query.middleware(TrialAccessMiddleware())

    # Подключаем роутеры
    dp.include_router(router_users)
    dp.include_router(router_call)
    dp.include_router(fake_payment_router)
    dp.include_router(admin_router)

    # Подключаем события старта/остановки
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
