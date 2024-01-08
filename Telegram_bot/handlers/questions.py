from datetime import datetime
import pandas as pd
from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from main import df

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Welcome! I am your news bot. Use /news to see the news(TBD), /popular to get top tags of the day, /random to get random news story, /guessadategame to play a game, /head to get head of the DataFrame.')


@router.message(Command("head"))
async def display_head(message: Message):
    # Display the head of the DataFrame
    head_text = df.head(2).to_string(index=False)
    await message.answer(f"Head of the DataFrame:\n{head_text}")


@router.message(Command("random"))
async def display_head(message: Message):
    random_row = df.sample().values[0]
    await message.answer(str(random_row))


@router.message(Command("popular"))
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


