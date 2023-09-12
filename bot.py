import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB, DB_PATH
from handlers import add
from memes_bot.db.create_db import Base
from memes_bot.handlers import commands, find
from memes_bot.middlewares.db import DbSessionMiddleware

logger.add('logs/my_log.log', level='DEBUG')
logger.debug('Error')
logger.info('Information message')
logger.warning('Warning')


async def main():
    bot = Bot(token=TOKEN)
    engine = create_async_engine(url=DB_PATH, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    storage = RedisStorage.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.callback_query.middleware(CallbackAnswerMiddleware())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    dp.include_router(commands.router)
    dp.include_router(find.router)
    dp.include_router(add.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
