import asyncio
import json
import os
import logging
import sys

from aiogram.filters import Command
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import types
from openai import OpenAI

load_dotenv()

TOKEN = os.getenv("SECRET_KEY")
KEY = os.getenv("OPENAI_KEY")
JSON_FILE = "data.json"

dp = Dispatcher(storage=MemoryStorage())

client = OpenAI(api_key=KEY)


class ChatGPTStates(StatesGroup):
    waiting_for_query = State()


# TODO: Придумать куда хранить сообщение, у каждого пользователя свое хранение там есть: MESSAGE, EDITED, DELETED,
# После придумать у бота возможность введение статистики в чатах

async def save_message_to_json(message: types.Message):
    """Записывает сообщение в JSON, сохраняя историю переписки."""
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # TODO: Реализовать возможность т.к пользователь один, в json нужно сделать функцию получение имени бота
    chat_username = message.chat.username
    sender_username = message.from_user.username
    text = message.text

    # If symbol_ "+" is admin bot gets message
    if sender_username == 'adenchikio':
        symbol_ = "-"
    else:
        symbol_ = "+"
        # Если пишет другой человек, то получатель – ты

    message_entry = {
        "symbol": symbol_,
        "text": text
    }

    for chat in data["chats"]:
        if chat["chat"] == chat_username:
            chat.setdefault("messages", []).append(message_entry)
            break
    else:
        data["chats"].append({"chat": chat_username, "messages": [message_entry]})

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@dp.business_message()
async def message_business_handler(message: types.Message) -> None:
    await save_message_to_json(message)


@dp.edited_business_message()
async def edited_business_handler(message: types.Message) -> None:
    print(f'EDITED: {message.from_user.username}\nText: {message.text}')


@dp.deleted_business_messages()
async def deleted_business_handler(message: types.BusinessMessagesDeleted) -> None:
    # Удаленные сообщение, удаляются полностью, тут возращает ID сообщение
    ...


# TODO: После реализации сохранении переписок с каждого чата за опр срок, сделать возможным анализ переписок с помощью ИИ
# @dp.message(Command("query"))
# async def query_chat_gpt(message: types.Message, state: FSMContext):
#     await message.answer('Введите запрос: ', reply_markup=types.ReplyKeyboardRemove())
#     await state.set_state(ChatGPTStates.waiting_for_query)
#
#
# @dp.message(ChatGPTStates.waiting_for_query)
# async def response_chat_gpt_for_command(message: types.Message, state: FSMContext):
#     user_query = message.text
#
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "Личный ассистент, помогай по всему вопросу, правда и честно!"
#             },
#             {
#                 "role": "user",
#                 "content": user_query
#             }
#         ]
#     )
#
#     response = completion.choices[0].message.content
#
#     await message.answer(response)
#     await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
