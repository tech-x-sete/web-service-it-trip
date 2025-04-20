from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_list_button_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить список мероприятий", callback_data='get_events')]
    ])

    return keyboard
