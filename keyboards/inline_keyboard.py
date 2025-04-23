from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Получить ключ Outline', callback_data='trial_outline')
    keyboard_builder.button(text='Получить ключ Vless', callback_data='trial_vless')
    keyboard_builder.button(text='Тарифы Outline', callback_data='traffic')
    keyboard_builder.button(text='Тарифы Vless', callback_data='traffic_vless')
    keyboard_builder.button(text='Мои ключи Outline', callback_data='my_keys')
    keyboard_builder.button(text='Мои ключи Vless', callback_data='my_keys_vless')

    keyboard_builder.adjust(1, 1, 2)
    return keyboard_builder.as_markup()


async def get_traffic_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='349₽ | 100ГБ/мес.', callback_data='month')
    keyboard_builder.button(text='999₽ | 300ГБ/3 мес.', callback_data='three_month')
    keyboard_builder.button(text='1999₽ | 600ГБ/6 мес.', callback_data='six_month')
    keyboard_builder.button(text='3399₽ | Безлимит/год', callback_data='year')
    keyboard_builder.button(text='➕Пригласить друга', callback_data='invite_friend')
    keyboard_builder.button(text='🔙 В главное меню', callback_data='back_main')
    keyboard_builder.adjust(2, 2)
    return keyboard_builder.as_markup()


async def vless_tariff_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🇷🇺 349₽/мес", callback_data="vless_1")
    kb.button(text="🌍 999₽/3 мес", callback_data="vless_3")
    kb.button(text="🧿 1999₽/6 мес", callback_data="vless_6")
    kb.button(text="♾️ 3399₽/год", callback_data="vless_unlim")
    kb.button(text='➕Пригласить друга', callback_data='invite_friend')
    kb.button(text='🔙 В главное меню', callback_data='back_main')
    kb.adjust(2, 2)
    return kb.as_markup()


