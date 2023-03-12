import re
import random
from aiogram import Bot
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def validate_phone_number(phone_number):
    pattern = "^(09|\+2519|2519|9)\d{8,}$"
    return re.match(pattern, phone_number)


async def process_quiz(question: str, options: list, correct_option: int, bot: Bot, chat_id: int):
    correct = options[int(correct_option)]
    random.shuffle(options)
    return await bot.send_poll(
        chat_id,
        question=question,
        options=options,
        correct_option_id=options.index(correct),
        type="quiz"
    )

