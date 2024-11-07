import asyncio
import os
from inline_keyboard import get_keyboard

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text='Привет! Добро пожаловать в бота, который поможет вам выбрать лучший VPN',
                         reply_markup=get_keyboard())


async def start():
    bot: Bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
