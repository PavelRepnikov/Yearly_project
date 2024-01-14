import logging
import sys
import pandas as pd
from aiogram import Bot, Dispatcher, types, Router
import asyncio
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile
import matplotlib.pyplot as plt

from main import df

#import requests
#from bs4 import BeautifulSoup

router = Router()

# Парсер текущих новостей (не доделан)
@router.message(Command("news"))
async def get_news(message: types.Message):
    await message.answer("TBD")
#     news = parse_news()
#     for article in news:
#         await message.answer(html.escape(article['title']))
#
#
# def parse_news():
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text, 'html')
#     news = []
#     for link in soup.find_all('a'):
#         news.append({
#             'title': link.text,
#             'url': link.get('href')
#         })
#     return news
#
# # Заглушка (для предложения тегов по тексту статьи)
# @router.message(Command("predict_tags"))
# async def predict_tags(message: types.Message):
#     article_text = message.text.split('/predict_tags ')[1]  # Извлечь текст статьи из аргумента команды
#     # Предобработка и извлечение признаков из текста статьи
#     features = preprocess(article_text)
#     # Подача признаков в модель для предсказания тегов
#     predicted_tags = model.predict(features)
#     # Отправка предсказанных тегов пользователю
#     await message.answer(f"Предсказанные теги для данной статьи: {predicted_tags}")
