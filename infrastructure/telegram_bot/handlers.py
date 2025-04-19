from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from infrastructure.db.models import async_session

from keyboards import get_list_button_keyboard
# from infrastructure.db.requests import get_all_publications
from infrastructure.db.repositories.publication_repository import PublicationRepository

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=get_list_button_keyboard())


@router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


@router.callback_query(F.data == "get_events")
async def get_events(callback: CallbackQuery):
    async with async_session() as session:
        repo = PublicationRepository(session)
        publications = await repo.get_all_publications()

        # Преобразуем в строки внутри контекста сессии
        publications_list = [
            f"{pub.title} (опубликовано: {pub.publish_date})"
            for pub in publications
        ]

        if not publications_list:
            await callback.message.answer("Нет мероприятий")
            return

        await callback.message.answer("\n".join(publications_list))
