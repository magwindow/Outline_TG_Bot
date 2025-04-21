from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from keyboards.inline_keyboard import get_traffic_keyboard
from keyboards.payment_keyboard import get_payment_methods_keyboard
from payments.admin_panel import ADMIN_IDS
from payments.data_storage import pending_users, waiting_for_payment, user_tariff_selection
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

fake_payment_router = Router()


# Создаем инлайн-кнопки для подтверждения
def get_admin_confirmation_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{user_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")]
    ])


TARIFFS = {
    "month": 349,
    "three_month": 999,
    "six_month": 1999,
    "year": 3399
}


@fake_payment_router.callback_query(F.data == "month")
async def handle_fake_payment(call: CallbackQuery):
    user_tariff_selection[call.from_user.id] = "month"
    await call.message.edit_text(
        "💳 Для оплаты тарифа *100 ГБ (1 месяц)* выберите способ ниже:",
        reply_markup=get_payment_methods_keyboard(back_callback="traffic")
    )


@fake_payment_router.callback_query(F.data == "three_month")
async def handle_three_month(call: CallbackQuery):
    user_tariff_selection[call.from_user.id] = "three_month"
    await call.message.edit_text(
        "💳 Для оплаты тарифа *300 ГБ (3 месяца)* выберите способ ниже:",
        reply_markup=get_payment_methods_keyboard(back_callback="traffic")
    )


@fake_payment_router.callback_query(F.data == "six_month")
async def handle_six_month(call: CallbackQuery):
    user_tariff_selection[call.from_user.id] = "six_month"
    await call.message.edit_text(
        "💳 Для оплаты тарифа *600 ГБ (6 месяцев)* выберите способ ниже:",
        reply_markup=get_payment_methods_keyboard(back_callback="traffic")
    )


@fake_payment_router.callback_query(F.data == "year")
async def handle_year(call: CallbackQuery):
    user_tariff_selection[call.from_user.id] = "year"
    await call.message.edit_text(
        "💳 Для оплаты тарифа *Безлимит (1 год)* выберите способ ниже:",
        reply_markup=get_payment_methods_keyboard(back_callback="traffic")
    )


@fake_payment_router.callback_query(F.data == "pay_card")
async def pay_card(call: CallbackQuery):
    tariff = user_tariff_selection.get(call.from_user.id, "month")
    price = TARIFFS.get(tariff, 349)
    await call.message.answer(
        f"💳 Переведите {price}₽ на карту и пришлите скриншот платежа:\n\n<b>2200 4528 3654 2122</b>\n"
        "После перевода нажмите «Я оплатил»"
    )


@fake_payment_router.callback_query(F.data == "pay_sbp")
async def pay_sbp(call: CallbackQuery):
    tariff = user_tariff_selection.get(call.from_user.id, "month")
    price = TARIFFS.get(tariff, 349)
    await call.message.answer(
        f"📲 Переведите {price}₽ по СБП на номер:\n\n<b>+7 999 111 25 25</b>\n"
        "После перевода нажмите «Я оплатил»"
    )


@fake_payment_router.callback_query(F.data == "traffic")
async def back_to_tariffs(call: CallbackQuery):
    await call.message.edit_text(
        "Выберите тариф:",
        reply_markup=await get_traffic_keyboard()
    )


@fake_payment_router.callback_query(F.data == "confirm_payment")
async def confirm_payment(call: CallbackQuery):
    pending_users.add(call.from_user.id)
    await call.message.answer("⌛ Заявка на оплату отправлена. Ожидайте подтверждения от администратора.")


# Обработка отправки скриншота
@fake_payment_router.message(F.photo)
async def handle_payment_screenshot(message: Message):
    # Добавляем пользователя в список ожидания и сохраняем фото
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    pending_users.add(user_id)
    waiting_for_payment[user_id] = file_id

    # Сохраняем фото
    file_id = message.photo[-1].file_id  # Берём самую большую версию фото

    # Сохраняем путь к фото в список
    waiting_for_payment[user_id] = file_id

    await message.answer("✅ Ваш скриншот принят. Ожидайте подтверждения от администратора.")

    # Уведомление админам
    for admin_id in ADMIN_IDS:
        await message.bot.send_photo(
            admin_id,
            file_id,
            caption=f"📸 Скрин от <b>{message.from_user.full_name}</b> (ID: <code>{user_id}</code>)",
            reply_markup=get_admin_confirmation_keyboard(user_id)
        )
