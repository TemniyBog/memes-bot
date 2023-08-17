from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from memes_bot.db.commands import save_meme
from memes_bot.filters.chat_type import ChatTypeFilter
from memes_bot.kb.kb_for_all import main_menu, approved
from memes_bot.states.states_for_all import UserState

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type='private'),
    F.from_user.id == 5079687466
)


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserState.wait_for)
    await message.answer('Чё надо?', reply_markup=main_menu())



@router.message(UserState.wait_for, Text(text="Добавить мем", ignore_case=True))
async def download_meme(message: Message, state: FSMContext):
    await state.set_state(UserState.wait_for_pic)
    await message.answer('Загрузите картинку', reply_markup=ReplyKeyboardRemove())



@router.message(UserState.wait_for_pic, F.photo)
async def write_tags(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(meme_hash=message.photo[-1].file_id)
    await state.set_state(UserState.wait_for_tags)
    await bot.send_photo(message.from_user.id, str(message.photo[-1].file_id))
    await message.answer('Напишите теги через запятую')


@router.message(UserState.wait_for_tags, F.text)
async def add_confirm(message: Message, state: FSMContext):
    text = message.text.split(',')
    tags = list()
    for each in text:
        tags.append(each.strip())
    tags_set = set(tags)
    tags_list = list(tags_set)
    await state.update_data(tags_list=tags_list)
    await state.set_state(UserState.wait_for_approve)
    await message.answer(f'Проверьте теги: {tags_set}', reply_markup=approved())


@router.callback_query(UserState.wait_for_approve, Text('save_meme_db'))
async def add_in_db(callback_query: types.CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    hash_meme = context_data['meme_hash']
    tags_list = context_data['tags_list']
    await save_meme(hash_meme, tags_list)
    await state.clear()


@router.callback_query(UserState.wait_for_approve, Text('return'))
async def add_in_db(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    return await cmd_start(callback_query.message, state)



@router.message(Text(text="Найти мем", ignore_case=True))
async def text_find_meme(message: Message):
    pass
