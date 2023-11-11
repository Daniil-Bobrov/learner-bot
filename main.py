import asyncio
import random

import telebot.types
from telebot.async_telebot import AsyncTeleBot
import database

bot = AsyncTeleBot(token="6872689037:AAEP1jFJKnwcqi2MnScWCofLy9wNRKJ9plo")

words = list()
db = database.DataBase()


def get_user(message: telebot.types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if user is False or user is None:
        random.shuffle(words)
        user = db.create_user(user_id, words)
    return user


def read_words():
    global words
    with open("words.txt", 'r', encoding="utf-8") as words_txt:
        words = words_txt.read().rstrip().split()
    return words


def check_answer(answer, right_answer):
    # print(right_answer[0].islower(), answer[1:] == right_answer[1:], answer == right_answer, answer, right_answer)
    if right_answer[0].islower() and answer[1:] == right_answer[1:] or answer == right_answer:
        return True
    return False


@bot.message_handler(commands=['start'])
async def start_training(message: telebot.types.Message):
    user = get_user(message)
    words = user["words"].split(",")
    await bot.send_message(message.chat.id, words[0].lower())


@bot.message_handler()
async def get_message(message):
    user = get_user(message)
    testing = int(user["testing"])
    if not testing:
        await bot.send_message(message.chat.id, "Error. Fuck yourself please.")
        return Exception
    answer = message.text
    words = user["words"].split(",")
    right_answer: str = words[0]
    if check_answer(answer, right_answer):
        db.remove_word(user["telegram_id"])
        await bot.send_message(message.chat.id, "Верно")
    else:
        await bot.send_message(message.chat.id, "Неверно")
        db.shuffle_words(user["telegram_id"])
    user = get_user(message)
    words = user["words"].split(",")
    await bot.send_message(message.chat.id, words[0].lower())


async def main():
    read_words()
    await bot.infinity_polling(timeout=1000)


if __name__ == "__main__":
    asyncio.run(main())
