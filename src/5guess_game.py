from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN
import random

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = {}


def get_random_number() -> int:
    return random.randint(1, 100)


ATTEMPTS = 7


@dp.message(Command(commands=["start"]))
async def process_cmd_start(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    user_id = message.from_user.id
    if users.get(user_id, None) is None:
        users[user_id] = {
            "in_game": False,
            "secret_number": None,
            "attempts": ATTEMPTS,
            "total_games": 0,
            "wins": 0,
        }
    await message.answer(
        "Ваша цель - отгадать загаданное мною число\n\nЧтобы получить больше подробностей, отправьте команду /help "
    )
    await message.answer("Желаете сыграть?")


@dp.message(Command(commands=["help"]))
async def process_cmd_help(message: Message):
    await message.answer(
        "Данный бот предназначен для игры-угадайки, ваша цель - отгадать загаданное мною число\n\n"
        "Желаете сыграть?"
    )


@dp.message(Command(commands=["stats"]))
async def process_cmd_stats(message: Message):
    user_id = message.from_user.id
    if users.get(user_id, None) is None:
        await message.answer("Запустите бота кнопкой /start")
    else:
        user = users[user_id]
        await message.answer(
            f"Всего игр сыграно {user['total_games']}\n"
            f"Победных игр {user['wins']}\n"
            f"Частота побед {round(user['wins'] / user['total_games'], 2) if user['total_games'] != 0 else 0}\n\n"
            'Введите "игра" чтобы вернуться к игре'
        )


@dp.message(
    F.text.lower().in_(["да", "давай", "сыграем", "игра", "играть", "хочу играть"])
)
async def process_pos(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await process_cmd_start(message)
        return

    user = users[user_id]
    if user["in_game"]:
        await message.answer("Игра в процессе\n\nОтправьте число от 1 до 100")
    else:
        user["in_game"] = True
        user["secret_number"] = get_random_number()
        user["attempts"] = ATTEMPTS
        await message.answer("Я задумал число, можете угадывать")


@dp.message(F.text.lower().in_(["нет", "не", "не хочу", "не буду"]))
async def process_neg(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await process_cmd_start(message)
        return

    user = users[user_id]
    if user["in_game"]:
        await message.answer("Игра в процессе\n\nОтправьте число от 1 до 100")
    else:
        await message.answer("Готовы сыграть?")


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_guess(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await process_cmd_start(message)
        return

    user = users[user_id]
    if user["in_game"]:
        guess = int(message.text)
        if guess == user["secret_number"]:
            user["in_game"] = False
            user["secret_number"] = None
            user["total_games"] += 1
            user["wins"] += 1
            await message.answer("Вы победили, угадав мое число! Сыграем еще раз?")
        elif guess < user["secret_number"]:
            user["attempts"] -= 1
            if user["attempts"] > 0:
                await message.answer(
                    f"Загаданное число больше. Осталось {user['attempts']} попыток"
                )
        else:
            user["attempts"] -= 1
            if user["attempts"] > 0:
                await message.answer(
                    f"Загаданное число меньше. Осталось {user['attempts']} попыток"
                )

        if user["in_game"] and user["attempts"] == 0:
            secret = user["secret_number"]
            user["in_game"] = False
            user["secret_number"] = None
            user["total_games"] += 1
            await message.answer(
                f"Увы, попытки кончились, а Вы проиграли. Я загадал число {secret}\n\n"
                "Готовы сыграть еще раз?"
            )

    else:
        await message.answer("Желаете начать игру?")


@dp.message()
async def process_else(message: Message):
    user_id = message.from_user.id
    if user_id in users and users[user_id]["in_game"]:
        await message.answer(
            "Мы же сейчас играем. Пришлите, пожалуйста, число от 1 до 100"
        )
    else:
        await message.answer(
            "Я довольно ограниченный бот, давайте просто сыграем в игру?"
        )


if __name__ == "__main__":
    dp.run_polling(bot)
