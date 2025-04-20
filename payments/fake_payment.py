from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards.payment_keyboard import get_payment_methods_keyboard
from payments.admin_panel import ADMIN_IDS
from payments.data_storage import pending_users, waiting_for_payment
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

fake_payment_router = Router()


# Создаем инлайн-кнопки для подтверждения
def get_admin_confirmation_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{user_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")]
    ])


@fake_payment_router.callback_query(F.data == "month")
async def handle_fake_payment(call: CallbackQuery):
    await call.message.edit_text(
        "💳 Для оплаты тарифа *100 ГБ* выберите способ ниже:",
        reply_markup=get_payment_methods_keyboard()
    )


@fake_payment_router.callback_query(F.data == "pay_sbp")
async def pay_sbp(call: CallbackQuery):
    await call.message.answer(
        "📲 Переведите 200₽ по СБП на номер:\n\n<b>+7 999 111 25 25</b>\n"
        "После перевода нажмите «Я оплатил»"
    )


@fake_payment_router.callback_query(F.data == "pay_card")
async def pay_card(call: CallbackQuery):
    await call.message.answer(
        "💳 Переведите 200₽ на карту:\n\n<b>2200 4528 3654 2122</b>\n"
        "После перевода нажмите «Я оплатил»"
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
