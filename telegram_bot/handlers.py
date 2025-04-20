from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards import get_list_button_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=get_list_button_keyboard())


@router.callback_query(F.data == "get_events")
async def get_events(callback: CallbackQuery):
    async with async_session() as session:
        ...
