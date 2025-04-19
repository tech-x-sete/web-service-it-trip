from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("start")


@router.message(F.text)
async def echo(message: Message):
    await message.answer("Echo")
