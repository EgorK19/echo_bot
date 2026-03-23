from aiogram import Bot, Dispatcher, F  # взаимодействие с api, маршрутизация апдейтов
from aiogram.filters import Command  # фильтрация команд
from aiogram.types import Message  # фиксация апдейтов в виде сообщений
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# обработчик команды /start
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("echo bot\nsend smth")


# обработчик команды /help
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("echo bot\nsend smth to see answer")


# данный обработчик не дает работать обработчиками ниже
# он отлавливает все типы сообщений
@dp.message()
async def echo(message: Message):

    # красивое отображение сообщения (объект сообщения преобразовали в json)
    print(message.model_dump_json(indent=4, exclude_none=True))

    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.reply("it`s nothing i can do")


# обработка фотографий (НЕ УЧАСТВУЕТ)
@dp.message(F.photo)
async def send_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)


# обработчик сообщений (НЕ УЧАСТВУЕТ)
@dp.message()
async def send_echo(message: Message):
    text = message.text

    # message.reply содержит ссылку на сообщение
    # answer просто отвечает но сообщение
    await message.reply(f"echo says: {text}")

    # ИЛИ await bot.send_message(message.chat.id, message.text)
    # можно передать id любого чата


if __name__ == "__main__":
    dp.run_polling(bot)
