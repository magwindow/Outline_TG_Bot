from keyboards.inline_keyboard import main_keyboard, get_traffic_keyboard

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

outline_download_link = 'https://getoutline.org/ru/get-started/'

router_users: Router = Router()


@router_users.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text='Привет! Добро пожаловать в бота, который поможет вам выбрать лучший VPN',
                         reply_markup=main_keyboard())








