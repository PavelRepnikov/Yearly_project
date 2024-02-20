from unittest.mock import AsyncMock
import pytest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from handlers.FSM import start_popular, cmd_popular
from handlers.handlers import get_news
from handlers.plot import start_plot, plot
from handlers.questions import command_start_handler, display_head, display_random
from main import df
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from handlers.plot import Form
from handlers.FSM import Form2


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await command_start_handler(message)
    message.answer.assert_called_with("""Welcome! I am your news bot. Use /news to see the news(TBD), /popular YYYY-MM-DD to get top tags of the chosen day, /random to get random news story, /guessadategame to play a game, /plot to plot some data.""",
                                      reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/news'),
                                                                                  KeyboardButton(text='/popular'),
                                                                                  KeyboardButton(text='/random'),
                                                                                  KeyboardButton(text='/guessadategame'),
                                                                                  KeyboardButton(text='/plot')]],
                                                                       is_persistent=None, resize_keyboard=True,
                                                                       one_time_keyboard=None,
                                                                       input_field_placeholder='Выберите действие',
                                                                       selective=None))


@pytest.mark.asyncio
async def test_news_handler():
    text_mock = '/news'
    message = AsyncMock(text=text_mock)
    await get_news(message)
    message.answer.assert_called_with("TBD")


@pytest.mark.asyncio
async def test_display_head_handler():
    text_mock = '/head'
    message = AsyncMock(text=text_mock)
    await display_head(message)
    head_text = df.head(2).to_string(index=False)
    message.answer.assert_called_with(f"Head of the DataFrame:\n{head_text}")


@pytest.mark.asyncio
async def test_display_random_handler():
    text_mock = '/random'
    message = AsyncMock(text=text_mock)
    await display_random(message)
    answer_string = str(message.answer)
    assert answer_string is not None


@pytest.mark.asyncio
async def test_handler_start_plot():
    requester = MockedBot(
        MessageHandler(
            start_plot, state=Form.currently_in_plot, state_data={"info": "False"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Напишите тег для построения графика:"


@pytest.mark.asyncio
async def test_handler_plot_f():
    requester = MockedBot(
        MessageHandler(
            start_plot, state=Form.currently_in_plot, state_data={"info": "True"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Напишите тег для построения графика:"

    requester = MockedBot(MessageHandler(plot))
    calls = await requester.query(MESSAGE.as_object(text="epasdfg"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Ошибка: нет такого тега!"


@pytest.mark.asyncio
async def test_handler_plot_t():
    requester = MockedBot(
        MessageHandler(
            start_plot, state=Form.currently_in_plot, state_data={"info": "True"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Напишите тег для построения графика:"

    requester = MockedBot(MessageHandler(plot))
    calls = await requester.query(MESSAGE.as_object(text="Арктика"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Сейчас будет построен график!"


@pytest.mark.asyncio
async def test_handler_start_popular():
    requester = MockedBot(
        MessageHandler(
            start_popular, state=Form2.currently_in_popular, state_data={"info": "False"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Выберите дату в формате: YYYY-MM-DD"


@pytest.mark.asyncio
async def test_handler_cmd_popular_1():
    requester = MockedBot(
        MessageHandler(
            cmd_popular, state=Form2.currently_in_popular, state_data={"info": "True"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Ошибка: неправильный формат команды. Пример:\n YYYY-MM-DD"


@pytest.mark.asyncio
async def test_handler_cmd_popular_2():
    requester = MockedBot(
        MessageHandler(
            cmd_popular, state=Form2.currently_in_popular, state_data={"info": "True"}
        )
    )
    calls = await requester.query(MESSAGE.as_object(text="2010-10-10"))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text is not None
