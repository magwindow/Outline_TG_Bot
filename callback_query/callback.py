from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from sqlalchemy import select

from outline_service import handle_invite
from keyboards.inline_keyboard import get_traffic_keyboard
from outline_service import create_new_key_trial, get_key_traffic_async
from keyboards.inline_keyboard import main_keyboard
from database.models import async_session, OutlineKey
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

router_call = Router()
outline_download_link = 'https://getoutline.org/ru/get-started/'

FREE_KEY_GENERATORS = {'trial_outline': (create_new_key_trial, get_traffic_keyboard)}


@router_call.callback_query(F.data.in_(FREE_KEY_GENERATORS.keys()))
async def handle_key_generation(call: CallbackQuery, bot: Bot):
    user_name = call.from_user.username
    chat = call.from_user
    create_func, keyboard_func = FREE_KEY_GENERATORS[call.data]

    # Открываем сессию БД
    async with async_session() as session:
        key = await create_func(chat, user_name, session)  # Передаем сессию в функцию создания ключа
        if callable(keyboard_func):
            if keyboard_func.__name__ == "main_keyboard":
                keyboard = await keyboard_func(call.from_user.id)
            else:
                keyboard = await keyboard_func()
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


@router_call.callback_query(F.data == "back_main")
async def back_to_main_menu(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 Главное меню:",
        reply_markup=main_keyboard()
    )


@router_call.callback_query(F.data == 'invite_friend')
async def invite_friend_callback(call: CallbackQuery):
    await call.answer()  # убирает "часики"
    await handle_invite(call.message)


@router_call.callback_query(F.data == "my_keys")
async def show_user_keys(call: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(OutlineKey).where(OutlineKey.chat_id == call.from_user.id)
        )
        keys = result.scalars().all()

        if not keys:
            await call.message.answer("У вас пока нет активных ключей.")
            return

        response = "🔑 <b>Ваши ключи:</b>\n\n"
        for k in keys:
            used_gb = await get_key_traffic_async(k.key_id)
            left_gb = k.total_limit_gb - used_gb if k.total_limit_gb else float('inf')
            expire = k.expires_at.strftime("%d.%m.%Y") if k.expires_at else "∞"
            response += (
                f"<b>🧩 Ключ:</b> <code>{k.access_url}</code>\n"
                f"📊 Использовано: {used_gb} / {k.total_limit_gb:.0f} ГБ\n"
                f"⏳ Осталось: {left_gb}\n"
                f"📅 Действует до: {expire}\n\n"
            )

        await call.message.answer(response, reply_markup=main_keyboard())
