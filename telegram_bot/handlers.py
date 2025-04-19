from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message

router = Router()


@router.message(Command("start", "get_list"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=...)


@router.message(F.text)
async def echo(message: Message):
    await message.answer("Echo")


@router.callback_query(...)
async def get_events(callback: CallbackData):
    await ...