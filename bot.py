import asyncio
import os
import outline_service
from keyboards.inline_keyboard import get_keyboard

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

router: Router = Router()

outline_download_link = 'https://getoutline.org/ru/get-started/'


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text='Привет! Добро пожаловать в бота, который поможет вам выбрать лучший VPN',
                         reply_markup=get_keyboard())


@router.message(Command(commands=['new_key']))
async def make_new_key(message: Message):
    user_name = message.text[7:]
    key = outline_service.create_new_key(user_name)
    await message.answer("Ваш ключ:\n" + key + "\n" + "Скачать Outline Client вы можете по ссылке: " +
                         outline_download_link, reply_markup=get_keyboard())


@router.callback_query(F.data == 'new_key')
async def make_new_key(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = outline_service.create_new_key(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n" + key + "\n" + "Скачать Outline Client вы можете по ссылке: " +
                           outline_download_link, reply_markup=get_keyboard())


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
