import re
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
import pandas as pd
from main import df


class Form(StatesGroup):
    currently_in_game = State()
    guess = State()
    answer = State()


router = Router()

@router.message(Command("guessadategame"))
async def start_guessadategame(message: Message, state: FSMContext):
    random_row = df.sample(n=1)
    text = random_row['text'].values[0]
    correct_date = random_row['date and time'].values[0]

    await message.answer(str(text))
    await state.set_state(Form.currently_in_game)
    await state.update_data(answer=correct_date)
    await message.answer("Guess a date: (YYYY-MM-DD)")


@router.message(Form.currently_in_game)
async def guess_guessadategame(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(
            "Ошибка: не переданы аргументы! Пример: YYYY-MM-DD"
        )
        return
    try:
        datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n YYYY-MM-DD"
        )
        return

    await state.update_data(guess=message.answer)
    data = await state.get_data()
    await state.clear()

    datastr = data['guess']
    datastr = re.search(r"text='(.*?)'", str(datastr))
    data['guess'] = (datetime.strptime(str(datastr.group(1)), '%Y-%m-%d'))

    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    matches = pattern.findall(str(data['answer']))
    print(matches)
    data['answer'] = (datetime.strptime(str(matches[0]),  '%Y-%m-%d'))

    # if data['guess'] == data['answer']:
    #     await message.answer("Вы угадали!")
    # else:
    #     await message.answer("Вы не угадали! Правильный ответ: " + str(data['answer']))

    if data['guess'] == data['answer']:
        await message.answer("Вы угадали точно!")
    elif data['guess'].year == data['answer'].year and data['guess'].month == data['answer'].month:
        await message.answer("Вы угадали месяц и год. Правильный ответ: " + str(data['answer']))
    elif data['guess'].year == data['answer'].year:
        await message.answer("Вы угадали год. Правильный ответ: " + str(data['answer']))
    else:
        await message.answer("Вы не угадали. Правильный ответ: " + str(data['answer']))
    await state.clear()
