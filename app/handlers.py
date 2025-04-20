from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from main import Publication
from keyboards import get_list_button_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Получить список мероприятий", reply_markup=get_list_button_keyboard())


@router.callback_query(F.data == "get_events")
async def get_events(callback: CallbackQuery):
    publications = Publication.query.all()
    result = []
    for pub in publications:
        result.append({
            'id': pub.id,
            'title': pub.title,
            'location': pub.location,
            'organization': {
                'name': pub.organization.name,
                'logo_url': pub.organization.logo_url
            },
            'tags': [tag.name for tag in pub.tags]
        })

    await callback.message.answer(*result)
