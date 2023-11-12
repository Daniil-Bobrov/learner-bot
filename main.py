import asyncio
import os
import random

import telebot.types
from telebot.async_telebot import AsyncTeleBot
import database
import dotenv

dotenv.load_dotenv()

bot = AsyncTeleBot(token=os.environ.get("TOKEN"))
db = database.DataBase()


def read_words():
    with open("words.txt", 'r', encoding="utf-8") as words_txt:
        words = words_txt.read().rstrip().split()
    return words


def get_user(message: telebot.types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if user is False or user is None:
        words = read_words()
        random.shuffle(words)
        user = db.create_user(user_id, words)
    return user


def check_answer(answer, right_answer):
    # print(right_answer[0].islower(), answer[1:] == right_answer[1:], answer == right_answer, answer, right_answer)
    if right_answer[0].islower() and answer[1:] == right_answer[1:] or answer == right_answer:
        return True
    return False


async def print_stats(message, user):
    await bot.send_message(message.chat.id, f"""Тренировка закончена!
Правильных ответов: {user.right_answers}
Неправильных ответов: {user.wrong_answers}
Попыток назвать одно слово: {(user.wrong_answers + user.right_answers) / user.right_answers}
Используйте /start, чтобы начать новую тренировку!""")
    user.right_answers = 0
    user.wrong_answers = 0
    user.testing = 0


@bot.message_handler(commands=['start'])
async def start_training(message: telebot.types.Message):
    user = get_user(message)
    user = database.User(user)
    user.testing = 1
    words = read_words()
    user.words = words
    user.update(db)
    await bot.send_message(message.chat.id, words[0].lower())


@bot.message_handler(commands=['stop'])
async def stop_training(message: telebot.types.Message):
    user = get_user(message)
    user = database.User(user)
    await print_stats(message, user)
    user.update(db)


@bot.message_handler()
async def get_message(message):
    if message.text.lower() == "остановка сука":
        await bot.send_message(message.chat.id, "Остановка \"твое очко\". Снимай штаны, сейчас будем тебя ебать")
        return
    user = get_user(message)
    user = database.User(user)
    testing = user.testing
    if not testing:
        await start_training(message)
        return Exception
    answer = message.text
    words = user.words
    right_answer: str = words[0]
    if check_answer(answer, right_answer):
        await bot.send_message(message.chat.id, "Верно")
        if len(words) == 0:
            await print_stats(message, user)
            return
        else:
            words = words[1:]
            user.right_answers += 1
    else:
        await bot.send_message(message.chat.id, f"Неверно. {right_answer}")
        user.wrong_answers += 1
    random.shuffle(words)
    user.words = words
    user.update(db)
    await bot.send_message(message.chat.id, words[0].lower())


async def main():
    read_words()
    await bot.infinity_polling(timeout=1000)


if __name__ == "__main__":
    asyncio.run(main())
