from aiogram import Router, F, Bot
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from memes_bot.config import USERS
from memes_bot.db.create_db import Meme, Tag
from memes_bot.filters.chat_type import ChatTypeFilter
from memes_bot.kb.kb_for_all import main_menu
from memes_bot.states.states_for_all import UserState

router = Router()
router.message.filter(ChatTypeFilter(chat_type='private'),
                      F.from_user.id.in_(USERS))


@router.message(UserState.wait_for, Text(text="Найти мем", ignore_case=True))
async def download_meme(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(UserState.wait_for_user_tag)
    await message.answer('Напишите слово, по которому будем искать', reply_markup=ReplyKeyboardRemove())


@router.message(UserState.wait_for_user_tag, F.text)
async def add_confirm(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    key_word = message.text.rstrip().lower()
    tags = await session.execute(select(Tag).filter_by(title=key_word))
    if len(tags.all()) > 0:
        tags = await session.execute(select(Tag).filter_by(title=key_word))
        tags_result = tags.scalars()
        for x in tags_result:
            db_query = await session.execute(select(Meme).filter_by(id=x.meme_id))
            hash = db_query.scalar_one()
            if hash:
                await bot.send_photo(chat_id=message.from_user.id, photo=hash.hash)
        await state.set_state(UserState.wait_for)
        await bot.send_message(chat_id=message.from_user.id, text='Успешно!\nНайти ещё мем?',
                               reply_markup=main_menu())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='По данному слову ничего не найдено, введите другое слово')
        return await download_meme(message, state, session)
