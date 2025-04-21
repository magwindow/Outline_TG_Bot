from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import async_session
from outline_service import (
    create_new_key_100,
    create_new_key_300,
    create_new_key_600,
    create_new_key_no_limit
)

from payments.data_storage import pending_users, waiting_for_payment, user_tariff_selection
from keyboards.inline_keyboard import get_traffic_keyboard

admin_router = Router()
ADMIN_IDS = [804741082]  # Telegram ID

key_generators = {
    "month": create_new_key_100,
    "three_month": create_new_key_300,
    "six_month": create_new_key_600,
    "year": create_new_key_no_limit
}


# Временный класс-пустышка, имитирующий пользователя
class DummyUser:
    def __init__(self, user_id):
        self.id = user_id
        self.username = f"user_{user_id}"


@admin_router.callback_query(F.data.startswith("confirm_"))
async def confirm_user_payment(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    if user_id not in pending_users:
        await call.message.answer("❌ Пользователь не ожидает подтверждения.")
        return

    # Получаем выбранный пользователем тариф
    tariff = user_tariff_selection.get(user_id, "month")
    create_key_func = key_generators.get(tariff, create_new_key_100)

    async with async_session() as session:
        # key = await create_new_key_100(call.from_user, f"user_{user_id}", session)
        key = await create_key_func(DummyUser(user_id), f"user_{user_id}", session)
    await call.bot.send_message(
        user_id,
        f"✅ Оплата подтверждена!\nВот ваш ключ:\n\n<code>{key.access_url}</code>",
        reply_markup=await get_traffic_keyboard()
    )

    await call.message.edit_caption(f"✅ Оплата от пользователя {user_id} подтверждена. Ключ выдан.")

    pending_users.remove(user_id)
    waiting_for_payment.pop(user_id, None)
    user_tariff_selection.pop(user_id, None)
