from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Получить ключ', callback_data='get_key')
    keyboard_builder.button(text='Профиль', callback_data='profile')
    keyboard_builder.button(text='Поменять ключ', callback_data='rename_key')
    keyboard_builder.button(text='Тариф', callback_data='traffic')

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()
