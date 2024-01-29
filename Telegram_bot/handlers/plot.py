import matplotlib.pyplot as plt
import numpy as np
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
    await message.answer("Напишите тег для построения графика:")


@router.message(Form.currently_in_plot)
async def plot(message: Message, state: FSMContext):

    tag_found = df.map(lambda x1: message.text in str(x1)).any().any()

    if tag_found:
        await message.answer("Сейчас будет построен график!")
    else:
        await message.answer("Ошибка: нет такого тега!")
        return

    desired_tag = message.text

    df['date and time'] = pd.to_datetime(df['date and time'])
    df['month'] = df['date and time'].dt.to_period('M').astype(str)
    tag_counts = []
    months = []

    for month, group in df.groupby('month'):
        tag_count = group[['tag1', 'tag2', 'tag3']].eq(desired_tag).sum().sum()
        tag_counts.append(tag_count)
        months.append(month)

    result_df = pd.DataFrame({'months': months, 'tag_counts': tag_counts})

    x = np.asarray(df['month'].unique(), dtype='datetime64[s]')

    plt.figure(figsize=(10, 6))
    plt.plot(result_df['months'], result_df['tag_counts'], linestyle='-', color='purple', label='Tag Occurrences')

    plt.title(f'Total occurrences of tag "{desired_tag}" per month')
    plt.xlabel('Month')
    plt.ylabel('Total occurrences')
    plt.gca().get_xaxis().set_major_locator(plt.MaxNLocator(nbins=10))

    output_file_name = desired_tag + '.png'
    plt.savefig(output_file_name, dpi=300)
    image_from_pc = FSInputFile(output_file_name)

    await message.answer_photo(image_from_pc)

    await state.clear()
