from keyboards.inline_keyboard import get_keyboard
import outline_service

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

outline_download_link = 'https://getoutline.org/ru/get-started/'

router_users: Router = Router()


@router_users.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text='Привет! Добро пожаловать в бота, который поможет вам выбрать лучший VPN',
                         reply_markup=get_keyboard())


@router_users.message(Command(commands=['new_key']))
async def make_new_key(message: Message):
    user_name = message.text[7:]
    key = outline_service.create_new_key(user_name)
    await message.answer("Ваш ключ:\n" + key + "\n" + "Скачать Outline Client вы можете по ссылке: " +
                         outline_download_link, reply_markup=get_keyboard())
