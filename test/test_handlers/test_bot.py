from unittest.mock import AsyncMock
import pytest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.handlers import get_news
from handlers.questions import command_start_handler, display_head, display_random
from main import df


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await command_start_handler(message)
    message.answer.assert_called_with('Welcome! I am your news bot. Use /news to see the news(TBD), /popular YYYY-MM-DD to get top tags of the chosen day, /random to get random news story, /guessadategame to play a game, /plot to plot some data.',
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


# @pytest.mark.asyncio
# async def test_plot_handler():
#     text_mock = '/plot'
#     message = AsyncMock(text=text_mock)
#     state = FSMContext(
#         storage=BaseStorage(),
#         key=StorageKey(bot_id=123456789, user_id=123456789, chat_id=123456789),
#     )
#     await start_plot(message, state=state)
#
#     # assert await state.get_state() == "currently_in_plot"
#     message.answer.assert_called_with("Напишите тег для построения графика:")


# @pytest.mark.asyncio
# async def test_start_plot():
#
#     state = AsyncMock(spec=FSMContext)
#     chat = types.Chat(id=123, type="private")
#     message = types.Message(message_id=456, date=1234567890, chat=chat)
#     await start_plot(message, state)
#     state.set_state.assert_called_once_with(Form.currently_in_plot())
#     message.answer.assert_called_with("Напишите тег для построения графика:")
