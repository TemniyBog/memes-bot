from loguru import logger

from memes_bot.db.create_db import Meme, Tag
from memes_bot.db.db_connect import session


async def save_meme(hash_meme, tags_list):
    meme = Meme(hash=hash_meme)
    session.add(meme)
    try:
        await session.commit()
        await session.refresh(meme)
        logger.info(f'__________________\n{meme.id}')
        meme = await session.query(Meme).filter(hash=hash_meme).first()
        logger.info(f'Сохранили хэш {meme.id} в базе')
        for each in tags_list:
            tag = Tag(title=each, meme_id=meme.id)
            session.add(tag)
        await session.commit()
        logger.info(f'Сохранили теги {tags_list} в базе')
    except Exception as err:
        await session.rollback()  # откатываем
        logger.info(f'ERROR\n{err}')