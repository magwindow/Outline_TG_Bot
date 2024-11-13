from keyboards.inline_keyboard import main_keyboard, get_traffic_keyboard
from outline_service import *

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import Bot, F

outline_download_link = 'https://getoutline.org/ru/get-started/'

router_call = Router()


@router_call.callback_query(F.data == 'new_key')
async def make_new_key(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'trial')
async def get_key_trial(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key_trial(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'month')
async def get_key_trial(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key_100(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'three_month')
async def get_key_trial(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key_300(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'six_month')
async def get_key_trial(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key_600(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'year')
async def get_key_trial(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    key = create_new_key_no_limit(user_name)
    await bot.send_message(call.from_user.id,
                           "Ваш ключ:\n\n" + "<code>" + key.access_url + "</code>" + "\n\n" +
                           "Нажмите на него, чтобы скопировать\n" + "Скачать Outline Client вы можете по ссылке: "
                           + outline_download_link, reply_markup=main_keyboard())


@router_call.callback_query(F.data == 'traffic')
async def get_traffic(call: CallbackQuery):
    await call.answer('Вы выбрали тариф')
    await call.message.edit_text('Нажмите на кнопку, чтобы получить трафик',
                                 reply_markup=await get_traffic_keyboard())
