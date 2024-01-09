import sys
import pandas as pd
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


TOKEN = 'secret'

df = pd.read_csv('parsed_news_EDA.csv', sep=';')
df['date and time'] = pd.to_datetime(df['date and time'])
print("csv loaded")

from handlers import questions, FSM


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(questions.router, FSM.router, plot.router, handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    user_data = {}
    asyncio.run(main())



