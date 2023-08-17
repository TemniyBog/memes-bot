import asyncio
# from loguru import logger
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis

from config import TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB
from handlers import for_all
from memes_bot.db.create_db import create_tables

logging.basicConfig(level=logging.DEBUG)


# logger.add('logs/my_log.log', level='DEBUG')
# logger.debug('Error')
# logger.info('Information message')
# logger.warning('Warning')


async def main():
    bot = Bot(token=TOKEN)

    redis = Redis()

    # storage = RedisStorage.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    # job_stores = {
    #     "default": RedisJobStore(
    #         jobs_key="trips_jobs",
    #         run_times_key="trips_running",
    #         host=REDIS_HOST,
    #         db=REDIS_DB,
    #         port=REDIS_PORT
    #     )
    # }

    dp.include_router(for_all.router)
    create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
