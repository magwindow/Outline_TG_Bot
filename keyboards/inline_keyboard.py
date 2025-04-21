from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Получить ключ', callback_data='trial')
    keyboard_builder.button(text='Мои ключи', callback_data='my_keys')
    keyboard_builder.button(text='Тарифы', callback_data='traffic')

    keyboard_builder.adjust(1, 2)
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


