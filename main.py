import random

from aiogram import executor, types
from aiogram.utils.callback_data import CallbackData

from initialization import bot, dp

change_sum = CallbackData("sum", "action", "value")
b = 0
a = 70


def main_game_keyboard():
    return types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(
            "1", callback_data=change_sum.new(action="make", value="1")
        ),
        types.InlineKeyboardButton(
            "10", callback_data=change_sum.new(action="make", value="10")
        ),
        types.InlineKeyboardButton(
            "100", callback_data=change_sum.new(action="make", value="100")
        ),
        types.InlineKeyboardButton(
            "1000", callback_data=change_sum.new(action="make", value="1000")
        ),
        types.InlineKeyboardButton(
            "+ 1", callback_data=change_sum.new(action="plus", value="1")
        ),
        types.InlineKeyboardButton(
            f"{b}", callback_data=change_sum.new(action="show_current_sum", value="-")
        ),
        types.InlineKeyboardButton(
            "- 1", callback_data=change_sum.new(action="minus", value="1")
        ),
        types.InlineKeyboardButton(
            "play", callback_data=change_sum.new(action="play", value="-")
        ),
        types.InlineKeyboardButton(
            "rules", callback_data=change_sum.new(action="show_rules", value="-")
        ),
    )


def get_menu_button():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "menu", callback_data=change_sum.new(action="menu", value="-")
        )
    )


def bitcoin():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "grow", callback_data=change_sum.new(action="up", value="-")
        ),
        types.InlineKeyboardButton(
            "fall", callback_data=change_sum.new(action="down", value="-")
        ),
    )


def play_again():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "play again!", callback_data=change_sum.new(action="play_again", value="-")
        )
    )


async def bitcoin_change(message: types.Message, callback_data: dict, a, b):
    number = random.randint(0, 10)
    await bot.send_message(
        message.chat.id, "Bitcoin will fall or grow?", reply_markup=bitcoin()
    )

    if callback_data["action"] == "grow" and number > 5:

        await bot.send_message(
            message.chat.id, f"You win {b} money!", reply_markup=play_again()
        )

        a += b

    elif callback_data["action"] == "fall" and number < 5:

        await bot.send_message(
            message.chat.id, f"You win {b} money!", reply_markup=play_again()
        )

        a += b

    elif callback_data["action"] == "fall" and number > 5:

        await bot.send_message(
            message.chat.id, f"You lose {b} money!", reply_markup=play_again()
        )

        a -= b

    elif callback_data["action"] == "grow" and number < 5:

        await bot.send_message(
            message.chat.id, f"You lose {b} money!", reply_markup=play_again()
        )

        a -= b

    if callback_data["action"] == "play_again":
        await bot.send_message(
            message.chat.id,
            f"Сейчас у вас есть {a} монет!",
            reply_markup=main_game_keyboard(),
        )


@dp.message_handler(commands="start")
async def main_game_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f"Сейчас у вас есть {a} монет!",
        reply_markup=main_game_keyboard(),
    )


@dp.callback_query_handler(
    change_sum.filter(
        action=[
            "make",
            "plus",
            "show_current_sum",
            "minus",
            "play",
            "show_rules",
            "menu",
        ]
    )
)
async def callback_results(query: types.CallbackQuery, callback_data: dict):
    global b

    if callback_data["action"] in ["make", "plus", "minus", "show_current_sum"]:

        if callback_data["action"] == "make" and callback_data["value"] == "1":
            b = 1

        if callback_data["action"] == "make" and callback_data["value"] == "10":
            b = 10

        if callback_data["action"] == "make" and callback_data["value"] == "100":
            b = 100

        if callback_data["action"] == "make" and callback_data["value"] == "1000":
            b = 1000

        if callback_data["action"] == "plus" and callback_data["value"] == "1":
            b += 1

        if callback_data["action"] == "minus" and callback_data["value"] == "1":
            b -= 1

        if (
            callback_data["action"] == "show_current_sum"
            and callback_data["value"] == "-"
        ):
            b = b * 2
        await bot.edit_message_text(
            "some text",
            query.message.chat.id,
            query.message.message_id,
            reply_markup=main_game_keyboard(),
        )

    if callback_data["action"] == "show_rules":

        await bot.send_message(
            query.message.chat.id,
            "Bitcoin rate is changing every second!\nSolve how it will change and win coins!",
            reply_markup=get_menu_button(),
        )

    if callback_data["action"] == "menu":
        await bot.send_message(
            query.message.chat.id,
            f"Сейчас у вас есть {a} монет!",
            reply_markup=main_game_keyboard(),
        )

    if callback_data["action"] == "play" and callback_data["value"] == "-":
        await bitcoin_change(query.message, callback_data, a, b)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
