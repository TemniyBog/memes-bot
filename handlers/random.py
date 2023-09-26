import random

from aiogram import Router, F, Bot
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from memes_bot.config import USERS
from memes_bot.db.create_db import Meme
from memes_bot.filters.chat_type import ChatTypeFilter
from memes_bot.kb.kb_for_all import main_menu
from memes_bot.states.states_for_all import UserState

router = Router()
router.message.filter(ChatTypeFilter(chat_type='private'),
                      F.from_user.id.in_(USERS))


@router.message(UserState.wait_for, Text(text="Случайный мем", ignore_case=True))
async def show_random_meme(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    db_query = await session.execute(select(Meme))
    memes = len(db_query.all())
    r = random.randint(1, memes)
    db_query1 = await session.execute(select(Meme).filter_by(id=r))
    nm: Meme = db_query1.scalar_one()
    hash = nm.hash
    await bot.send_photo(message.from_user.id, str(hash), reply_markup=main_menu())
    await state.set_state(UserState.wait_for)