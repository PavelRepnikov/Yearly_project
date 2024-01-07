import logging
import sys
import pandas as pd
from aiogram import Bot, Dispatcher, types
import asyncio
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile


TOKEN = 'secret'

bot = Bot(token=TOKEN)
dp = Dispatcher()

df = pd.read_csv('parsed_news_EDA.csv', sep=';')
df['date and time'] = pd.to_datetime(df['date and time'])
print("csv loaded")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Welcome! I am your news bot. Use /news to see the news(TBD), /popular to get top tags of the day, /random to get random news story, /guessadategame to play a game, /head to get head of the DataFrame.')


@dp.message(Command("head"))
async def display_head(message: types.Message):
    # Display the head of the DataFrame
    head_text = df.head(2).to_string(index=False)
    await message.answer(f"Head of the DataFrame:\n{head_text}")


@dp.message(Command("random"))
async def display_head(message: types.Message):
    random_row = df.sample().values[0]
    await message.answer(str(random_row))


@dp.message(Command("popular"))
async def cmd_popular(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы! Пример: /popular YYYY-MM-DD"
        )
        return
    try:
        datetime.strptime(command.args, '%Y-%m-%d')
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n /popular YYYY-MM-DD"
        )
        return
    input_date = pd.to_datetime(command.args)
    selected_data = df[df['date and time'].dt.date == input_date.date()]
    tags_series = pd.concat([selected_data['tag1'], selected_data['tag2'], selected_data['tag3']])
    tag_counts = tags_series.value_counts()
    popular_tags = tag_counts.head(20)

    await message.answer(str(popular_tags))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    user_data = {}
    scores = {}
    asyncio.run(main())



