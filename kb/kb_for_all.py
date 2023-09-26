from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить мем")
    kb.button(text="Найти мем")
    kb.button(text="Случайный мем")
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def approved() -> InlineKeyboardMarkup:
    btn1: InlineKeyboardButton = InlineKeyboardButton(
        text="Сохранить мем и теги в базе",
        callback_data="save_meme_db")
    btn2: InlineKeyboardButton = InlineKeyboardButton(
        text="Перезаписать теги",
        callback_data="return")
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[btn1, btn2]])
    return keyboard
