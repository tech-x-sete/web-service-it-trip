from aiogram import Bot, Dispatcher
# from app.database.models import async_main
from db.models import init_models
from handlers import router
from dotenv import load_dotenv
import os
import logging
import asyncio

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    await init_models()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
