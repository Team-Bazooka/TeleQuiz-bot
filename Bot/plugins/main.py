import datetime
import json
import random
import time
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from Bot import bot, dp
from Bot.helper.button import main_menu, category_btn, start_btn, select_language
from Bot.helper.methods import process_quiz


@dp.message_handler(commands="start")
async def start_handler(message: types.Message, state: FSMContext):
    await state.update_data(lang=0)
    ref_id = message.get_args()
    user_id = message.from_user.id
    url = "http://196.189.124.159/api/user/register"

    payload = json.dumps({
        "telegram_id": user_id+1,
        "username": message.from_user.username,
        "ref_id": ref_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    await message.answer("Hey", reply_markup=main_menu(0))


quiz_state = {}
poll_id = {}


@dp.message_handler(Text(equals=["Start Quiz", "ማጣቀሻዎች"]))
async def withdraw_handler(message: types.Message, state: FSMContext):
    text = "Please select quiz category"
    btn = category_btn()
    await message.answer(text, reply_markup=btn)
    await state.update_data(me=message.from_user.id)


@dp.callback_query_handler(Text(startswith='category_'))
async def category_handler(query: types.CallbackQuery, state: FSMContext):
    tag = query.data.split("_")[-1]
    url = "http://196.189.124.159/api/quiz/get"

    payload = json.dumps({
        "telegram_id": query.from_user.id,
        "tag": tag
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    await state.update_data(api_data=response.json())
    questions = (response.json())['data']['number_of_questions']
    message = query.message
    text = f"🎲 Get ready for `General` Quiz\n\n🖊 {questions} questions" \
           f"\n\n🏁 Press the button below when you are ready."
    btn = start_btn()
    await message.edit_text(text)
    await message.edit_reply_markup(btn)
    await state.update_data(tag=tag)


@dp.callback_query_handler(Text(startswith='quiz_'))
async def start_quiz_handler(query: types.CallbackQuery, state: FSMContext):
    data = query.data.split("_")[-1]
    message = query.message
    if data == "start":
        msg = await bot.send_message(query.from_user.id, "ready")
        tag = await state.get_data("tag")
        response = (await state.get_data())['api_data']
        for i in range(1, 4):
            await msg.edit_text(f"{i}")
            time.sleep(1)
        await msg.edit_text("Started")

        data = response
        datas = data['data']['questions']
        original_data = datas.copy()
        random.shuffle(datas)
        poll = await process_quiz(
            datas[0]['content'],
            datas[0]['choices'],
            datas[0]['answer'],
            bot,
            query.from_user.id
        )

        poll_id.update({poll.poll.id: query.from_user.id})
        start_time = datetime.datetime.now()
        quiz_state.update({
            message.chat.id: {
                "start_time": start_time,
                "questions": datas,
                "next_index": 1,
                "correct": 0,
                "quiz_id": data['data']['id'],
                "wrong": 0,
                "q_stats": [],
                "q_start_time": start_time,
                "original_data": original_data
            }
        })
    elif data == 'cancel':
        await message.delete()
        await message.answer("Quiz Canceled")
        print(await state.get_data())


@dp.poll_handler()
async def some_poll_handler(poll: types.Poll):
    correct_answer = poll.options[poll.correct_option_id]['voter_count'] == 1
    user_id = poll_id[poll.id]
    quiz = quiz_state[user_id]
    question = quiz['questions']
    next_index = quiz['next_index']
    current_time = (datetime.datetime.now() - quiz['q_start_time']).total_seconds()
    index = [i for i, d in enumerate(quiz['original_data']) if d == question[next_index-1]][0]
    quiz['q_stats'].append([round(current_time), int(correct_answer), index])
    if correct_answer:
        quiz['correct'] += 1
    else:
        quiz['wrong'] += 1
    if next_index < len(question):
        new_poll = await process_quiz(
            question[next_index]['content'],
            question[next_index]['choices'],
            question[next_index]['answer'],
            bot,
            user_id
        )
        quiz['next_index'] = next_index + 1
        poll_id.update({new_poll.poll.id: user_id})
        quiz['q_start_time'] = datetime.datetime.now()
    else:
        end_time = datetime.datetime.now() - quiz['start_time']
        text = f"""🏁 The quiz has Ended!


*✅ Correct* – {quiz['correct']}
*❌ Wrong* – {quiz['wrong']}
*⏱ {round(end_time.total_seconds(), 2)} sec *

__You have taken {next_index} question(s)__"""
        await bot.send_message(
            user_id,
            text,
            parse_mode="MARKDOWN"
        )
        url = "http://196.189.124.159/api/quiz/submit"

        payload = json.dumps({
            "telegram_id": user_id,
            "points": quiz_state[user_id]['q_stats'],
            "quiz_id": quiz_state[user_id]['quiz_id']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.json())
        quiz_state.pop(user_id)


@dp.message_handler(Text(equals=["Referrals", "ማጣቀሻዎች"]))
async def withdraw_handler(message: types.Message):
    text = f"""Hey this is your part of referral"""
    await message.answer(text)


@dp.message_handler(Text(equals=["Language", "ቋንቋ"]))
async def withdraw_handler(message: types.Message, state: FSMContext):
    try:
        lang = select_language((await state.get_data())['lang'])
    except KeyError:
        lang = select_language(0)
    await message.answer(lang[0], reply_markup=lang[1])


@dp.callback_query_handler(Text(startswith="lang_"))
async def setLang(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    user_id = query.from_user.id
    if query.data == "lang_english":
        await state.update_data(lang=0)
        await query.message.answer("Language settled to english",
                                   reply_markup=main_menu(0))
    if query.data == "lang_amharic":
        await state.update_data(lang=1)
        await query.message.answer("ቋንቋ ወደ አማርኛ ተለውጧል",
                                   reply_markup=main_menu(1))


@dp.message_handler(Text(equals=["My Points", "ቋንቋ"]))
async def withdraw_handler(message: types.Message, state: FSMContext):
    point = 9
    if point == 0:
        text = f"Oh you have no points, play some quizzes and incite friends to earn more"
    else:
        text = f"You have earned {point} Points using the bot"
    await message.answer(text)


@dp.message_handler(Text(equals=["Invite", "ቋንቋ"]))
async def withdraw_handler(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    invites = 0
    if invites == 0:
        text = f"oops you haven't invited anyone, use the below link to invite your friends" \
               f"\n\n🔗 Share your unique referral link: https://t.me/{(await bot.get_me())['username']}?start={user_id}"
    else:
        text = f"You have invited {invites} to the bot, use your link to invite more." \
               f"\n\n🔗 Share your unique referral link: https://t.me/{(await bot.get_me())['username']}?start={user_id}"
    await message.answer(text)
