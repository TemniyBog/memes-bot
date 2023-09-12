from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from memes_bot.filters.chat_type import ChatTypeFilter
from memes_bot.kb.kb_for_all import main_menu
from memes_bot.states.states_for_all import UserState

router = Router()
router.message.filter(ChatTypeFilter(chat_type='private'),
                      F.from_user.id == 5079687466)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserState.wait_for)
    await message.answer('Чё надо?', reply_markup=main_menu())
