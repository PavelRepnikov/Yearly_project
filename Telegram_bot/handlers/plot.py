import matplotlib.pyplot as plt
from aiogram import Router
from main import df
import re
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
import pandas as pd
from aiogram.types import BufferedInputFile

class Form(StatesGroup):
    currently_in_plot = State()


router = Router()


@router.message(Command("plot"))
async def start_plot(message: Message, state: FSMContext):

    await state.set_state(Form.currently_in_plot)
    await message.answer("Choose a tag to plot it")


@router.message(Form.currently_in_plot)
async def plot(message: Message, state: FSMContext):

    tag_found = df.map(lambda x: message.text in str(x)).any().any()

    if tag_found:
        await message.answer("Сейчас будет построен граф!")
    else:
        await message.answer("Ошибка: нет такого тега!")
        return

    desired_tag = message.text

    df['date and time'] = pd.to_datetime(df['date and time'])
    df['month'] = df['date and time'].dt.to_period('M').astype(str)
    tag_counts = []

    for month, group in df.groupby('month'):
        tag_count = group[['tag1', 'tag2', 'tag3']].eq(desired_tag).sum().sum()
        tag_counts.append(tag_count)

    # plt.bar(df['month'].dt.year.unique(), tag_counts, color='purple')
    # plt.bar(df['month'].unique(), tag_counts, color='green')

    # df['month'] = pd.to_datetime(df['month'], format='%Y-%m')

    plt.figure(figsize=(10, 6))
    plt.plot(df['month'].unique(), tag_counts, color='green', linestyle='-')

    plt.title(f'Total occurrences of tag "{desired_tag}" per month')
    plt.xlabel('Month')
    plt.ylabel('Total occurrences')

    plt.xticks(rotation=45, ha='right')
    plt.xticks(df['month'].unique()[::10], visible=True)

    output_file_name = desired_tag + '.png'
    plt.savefig(output_file_name, dpi=300)
    image_from_pc = FSInputFile(output_file_name)

    await message.answer_photo(image_from_pc)

    await state.clear()
