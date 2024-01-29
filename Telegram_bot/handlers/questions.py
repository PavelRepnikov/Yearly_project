from datetime import datetime
import pandas as pd
from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from main import df
from aiogram import types
from aiogram.filters import Command


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="/news"),
            types.KeyboardButton(text="/popular"),
            types.KeyboardButton(text="/random"),
            types.KeyboardButton(text="/guessadategame"),
            types.KeyboardButton(text="/plot")
        ]
    ]
    main_keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
    )
    await message.answer('Welcome! I am your news bot. Use /news to see the news(TBD), /popular YYYY-MM-DD to get top tags of the chosen day, /random to get random news story, /guessadategame to play a game, /plot to plot some data.',
                         reply_markup=main_keyboard)


@router.message(Command("head"))
async def display_head(message: Message):
    # Display the head of the DataFrame
    head_text = df.head(2).to_string(index=False)
    await message.answer(f"Head of the DataFrame:\n{head_text}")


@router.message(Command("random"))
async def display_head(message: Message):
    random_row = df.sample().values[0]
    await message.answer(str(random_row))





