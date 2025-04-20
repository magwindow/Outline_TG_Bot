from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from outline_service import handle_invite
from keyboards.inline_keyboard import main_keyboard, get_traffic_keyboard
from outline_service import (create_new_key_trial, create_new_key_100, create_new_key_300,
                             create_new_key_600, create_new_key_no_limit)
from database.models import async_session

router_call = Router()
outline_download_link = 'https://getoutline.org/ru/get-started/'

# Словарь соответствия callback.data -> функция создания ключа и клавиатура
KEY_GENERATORS = {
    'new_key': (create_new_key_trial, main_keyboard),
    'trial': (create_new_key_trial, get_traffic_keyboard),
    'month': (create_new_key_100, get_traffic_keyboard),
    'three_month': (create_new_key_300, get_traffic_keyboard),
    'six_month': (create_new_key_600, get_traffic_keyboard),
    'year': (create_new_key_no_limit, get_traffic_keyboard)
}


@router_call.callback_query(F.data.in_(KEY_GENERATORS.keys()))
async def handle_key_generation(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    chat = call.from_user
    create_func, keyboard_func = KEY_GENERATORS[call.data]

    # Открываем сессию БД
    async with async_session() as session:
        key = await create_func(chat, user_name, session)  # Передаем сессию в функцию создания ключа
        # keyboard = await keyboard_func(call.from_user.id) if callable(keyboard_func) else keyboard_func
        if callable(keyboard_func):
            if keyboard_func.__name__ == "main_keyboard":
                keyboard = await keyboard_func(call.from_user.id)
            else:
                keyboard = keyboard_func()
        else:
            keyboard = keyboard_func

    await bot.send_message(
        call.from_user.id,
        f"Ваш ключ:\n\n<code>{key.access_url}</code>\n\n"
        f"Нажмите на него, чтобы скопировать\n"
        f"Скачать Outline Client вы можете по ссылке: {outline_download_link}",
        reply_markup=keyboard
    )


@router_call.callback_query(F.data == 'traffic')
async def get_traffic(call: CallbackQuery):
    await call.answer('Вы выбрали тариф')
    await call.message.edit_text(
        'Нажмите на кнопку, чтобы получить трафик',
        reply_markup=await get_traffic_keyboard()
    )


@router_call.callback_query(F.data == 'invite_friend')
async def invite_friend_callback(call: CallbackQuery):
    await call.answer()  # убирает "часики"
    await handle_invite(call.message)
