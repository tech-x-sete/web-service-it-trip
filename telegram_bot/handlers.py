from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from flask import request

from keyboards import get_list_button_keyboard
from db.requests import get_all_publications
from domain import Publication


router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=get_list_button_keyboard())


@router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


@router.callback_query(F.data == "get_events")
async def get_events(callback: CallbackQuery):
    publications = await get_all_publications()
    await callback.message.answer("\n".join([elem.title for elem in publications]))
