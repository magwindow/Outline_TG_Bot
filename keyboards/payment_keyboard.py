from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_payment_methods_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Оплата по СБП", callback_data="pay_sbp")],
        [InlineKeyboardButton(text="💳 Оплата по карте", callback_data="pay_card")],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="confirm_payment")]
    ])
