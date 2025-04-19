from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(Command("start", "get_list"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=...)


@router.message(F.text)
async def echo(message: Message):
    await message.answer("Echo")


@router.callback_query(F.data == "get_events")
async def get_events(callback: CallbackQuery):
    await ...
