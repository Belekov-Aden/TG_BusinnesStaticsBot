import asyncio
import os
import logging
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types

load_dotenv()

TOKEN = os.getenv("SECRET_KEY")

dp = Dispatcher()


# TODO: Придумать куда хранить сообщение, у каждого пользователя свое хранение там есть: MESSAGE, EDITED, DELETED,
# После придумать у бота возможность введение статистики в чатах

@dp.business_message()
async def message_business_handler(message: types.Message) -> None:
    print(f'MESSAGE: {message.from_user.username}\nText: {message.text}')


@dp.edited_business_message()
async def edited_business_handler(message: types.Message) -> None:
    print(f'EDITED: {message.from_user.username}\nText: {message.text}')


@dp.deleted_business_messages()
async def deleted_business_handler(message: types.BusinessMessagesDeleted) -> None:
    # Удаленные сообщение, удаляются полностью, тут возращает ID сообщение
    ...


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
