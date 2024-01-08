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
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

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


# Парсер текущих новостей (не доделан)
@dp.message(Command("news"))
async def get_news(message: types.Message):
    news = parse_news()
    for article in news:
        await message.answer(html.escape(article['title']))


def parse_news():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html')
    news = []
    for link in soup.find_all('a'):
        news.append({
            'title': link.text,
            'url': link.get('href')
        })
    return news


# График популярности тегов по годам
@dp.message(Command('popularity', prefixes=['/', '!']))
async def cmd_popularity(message: types.Message):
    if message.get_args() != 'graph':
        await message.answer("Ошибка: неправильный формат команды. Введите /tag popularity graph.")
        return
    df['date and time'] = pd.to_datetime(df['date and time'])
    df['year'] = df['date and time'].dt.year
    tag_counts = df.groupby(df['year'])['tag1', 'tag2', 'tag3'].agg(lambda x: x.value_counts().sum()).sum(axis=1)
    plt.figure(figsize=(10, 6))
    plt.plot(tag_counts.index, tag_counts.values)
    plt.xlabel('Год')
    plt.ylabel('Количество тегов')
    plt.title('Популярность тегов')
    plt.xticks(rotation=45)
    plt.savefig('popular_tags.png')
    plt.close()
    with open('popular_tags.png', 'rb') as file:
        await message.reply_photo(file)


# Заглушка (для предложения тегов по тексту статьи)
@dp.message(Command("predict_tags"))
async def predict_tags(message: types.Message):
    article_text = message.text.split('/predict_tags ')[1]  # Извлечь текст статьи из аргумента команды
    # Предобработка и извлечение признаков из текста статьи
    features = preprocess(article_text)
    # Подача признаков в модель для предсказания тегов
    predicted_tags = model.predict(features)
    # Отправка предсказанных тегов пользователю
    await message.answer(f"Предсказанные теги для данной статьи: {predicted_tags}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    user_data = {}
    scores = {}
    asyncio.run(main())
