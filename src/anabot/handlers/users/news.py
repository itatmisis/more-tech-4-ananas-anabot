from aiogram import types
from aiogram.dispatcher.filters import Text
from anabot.keyboards.inline.callback_datas import continue_callback, reaction_callback
from anabot.keyboards.inline.reaction_buttons import create_reaction_keyboard
from anabot.loader import dp, bot
from anabot.loader import api
from anabot.utils.db_api.models import News


@dp.message_handler(Text(equals=["Дневной дайджест"]), state=None)
async def send_news(message: types.Message):
    news = api.digest(message.from_user.id, 1)
    await message.answer(text=news[0].short_text,
                         reply_markup=create_reaction_keyboard(news[0].url, 1, str(news[0].id)[:5]))
    await message.answer(text=news[1].short_text,
                         reply_markup=create_reaction_keyboard(news[1].url, 2, str(news[1].id)[:5]))
    await message.answer(text=news[2].short_text,
                         reply_markup=create_reaction_keyboard(news[2].url, 3, str(news[2].id)[:5], continue_button=True))
    print("Запрос дневного дайджеста")


@dp.callback_query_handler(reaction_callback.filter(reaction=["like", "dislike"]))
async def save_reaction(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=15)
    answer_reaction = 1 if callback_data["reaction"] == "like" else 2
    # api.add_reaction(callback_data["news_id"], call.from_user.id, answer_reaction)
    reaction_bool = True if callback_data["reaction"] == "like" else False
    await call.message.edit_reply_markup(
        create_reaction_keyboard(
            callback_data["link"],
            int(callback_data["article_number"]),
            callback_data["news_id"],
            reaction=reaction_bool,
            continue_button=bool(int(callback_data["continue_button"])),
        )
    )
    print(callback_data)
    # save like/dislike


@dp.callback_query_handler(continue_callback.filter(article_number=["1", "2", "3"]))
async def continue_news(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=15)
    if callback_data["reaction"] == "None":
        reaction = None
    elif callback_data["reaction"] == "True":
        reaction = True
    else:
        reaction = False
    await call.message.edit_reply_markup(
        create_reaction_keyboard(
            callback_data["link"],
            int(callback_data["article_number"]),
            int(callback_data["news_id"]),
            reaction=reaction,
        )
    )
    news = api.digest(call.from_user.id, 1)
    await bot.send_message(call.from_user.id, text=news[0].short_text,
                           reply_markup=create_reaction_keyboard(news[0].url, 1, str(news[0].id)[:5]))
    await bot.send_message(call.from_user.id, text=news[1].short_text,
                           reply_markup=create_reaction_keyboard(news[1].url, 2, str(news[1].id)[:5]))
    await bot.send_message(call.from_user.id, text=news[2].short_text,
                           reply_markup=create_reaction_keyboard(news[2].url, 3, str(news[2].id)[:5], continue_button=True))
    print(callback_data)
