from aiogram import Bot, Dispatcher
# from app.database.models import async_main
from handlers import router
import os
import logging
import asyncio

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    # await async_main()
    ...
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
