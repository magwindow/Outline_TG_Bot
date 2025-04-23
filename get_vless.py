from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import async_session, VlessKey
from keyboards.inline_keyboard import vless_tariff_keyboard, main_keyboard
from vless_service import add_client
from sqlalchemy import select

vless_router = Router()

# 👇 сюда подставь твой inbound_id (или передавай его параметром, если он может меняться)
INBOUND_ID = 1
FLOW = "xtls-rprx-vision"


# === Триал на 3 дня ===
@vless_router.callback_query(F.data == "trial_vless")
async def send_trial_vless(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with async_session() as session:
        existing = await session.execute(select(VlessKey).where(VlessKey.chat_id == user_id))
        if existing.scalars().first():
            await callback.message.answer("❗️У вас уже есть активный VLESS ключ.", reply_markup=main_keyboard())
            return

    try:
        key = await add_client(
            inbound_id=INBOUND_ID,
            total_gb=5,
            expiry_days=3,
            flow=FLOW,
            chat_id=user_id,
            user_name=callback.from_user.username
        )

        await callback.message.answer(
            f"✅ Ваш пробный VLESS ключ на 3 дня:\n\n<code>{key.access_url}</code>\n"
            f"⏳ Действителен до: {key.expires_at.strftime('%Y-%m-%d')}", reply_markup=main_keyboard()
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {str(e)}")


# === Обработка платных тарифов ===
@vless_router.callback_query(F.data.in_(["vless_1", "vless_3", "vless_6", "vless_unlim"]))
async def send_paid_vless(callback: CallbackQuery):
    user_id = callback.from_user.id
    tariff = callback.data

    tariffs = {
        "vless_1": {"gb": 100, "days": 30},
        "vless_3": {"gb": 300, "days": 90},
        "vless_6": {"gb": 600, "days": 180},
        "vless_unlim": {"gb": 9999, "days": 365},
    }

    try:
        t = tariffs[tariff]
        key = await add_client(
            inbound_id=INBOUND_ID,
            total_gb=t["gb"],
            expiry_days=t["days"],
            flow=FLOW,
            chat_id=user_id,
            user_name=callback.from_user.username
        )

        await callback.message.answer(
            f"✅ Ваш VLESS ключ:\n\n<code>{key.access_url}</code>\n"
            f"📅 Срок: до {key.expires_at.strftime('%d-%m-%Y')}", reply_markup=await vless_tariff_keyboard()
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {str(e)}")


@vless_router.callback_query(F.data == "traffic_vless")
async def show_vless_tariffs(callback: CallbackQuery):
    keyboard = await vless_tariff_keyboard()
    await callback.message.edit_text(
        "💳 Выберите тариф для подключения VLESS:",
        reply_markup=keyboard
    )
