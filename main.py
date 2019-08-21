import random

from aiogram import executor, types
from aiogram.utils.callback_data import CallbackData

from initialization import bot, dp

change_sum = CallbackData("sum", "action", "value")
b = 0
a = 70


def main_game_keyboard():
    return types.InlineKeyboardMarkup(row_width=4).add(
        types.InlineKeyboardButton(
            "1", callback_data=change_sum.new(action="make", value="1")
        ),
        types.InlineKeyboardButton(
            "10", callback_data=change_sum.new(action="make", value="10")
        ),
        types.InlineKeyboardButton(
            "50", callback_data=change_sum.new(action="make", value="50")
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
            "+ 5", callback_data=change_sum.new(action="plus", value="5")
        ),
        types.InlineKeyboardButton(
            "- 1", callback_data=change_sum.new(action="minus", value="1")
        ),
        types.InlineKeyboardButton(
            "- 5", callback_data=change_sum.new(action="minus", value="5")
        ),
        types.InlineKeyboardButton(
            "\U0001F3B2 play \U0001F3B2",
            callback_data=change_sum.new(action="play", value="-"),
        ),
        types.InlineKeyboardButton(
            "\U0001F4DC rules \U0001F4DC",
            callback_data=change_sum.new(action="show_rules", value="-"),
        ),
    )


def get_menu_button():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "\U0001F519 menu \U0001F519",
            callback_data=change_sum.new(action="menu", value="-"),
        )
    )


def bitcoin():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "\U00002B06 grow \U00002B06",
            callback_data=change_sum.new(action="up", value="-"),
        ),
        types.InlineKeyboardButton(
            "\U00002B07 fall \U00002B07",
            callback_data=change_sum.new(action="down", value="-"),
        ),
    )


def play_again():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "\U0001F3B0 play again! \U0001F3B0",
            callback_data=change_sum.new(action="play_again", value="-"),
        )
    )


@dp.message_handler(commands="start")
async def main_game_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f"\U0001F4B8 You have {a} money now! \U0001F4B8",
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
            "menu",
            "up",
            "down",
            "play_again",
            "show_rules",
        ]
    )
)
async def callback_results(query: types.CallbackQuery, callback_data: dict):
    global b, a
    await query.answer()

    if callback_data["action"] in ["make", "plus", "minus", "show_current_sum"]:

        if callback_data["action"] == "make" and callback_data["value"] == "1":
            b = 1

        if callback_data["action"] == "make" and callback_data["value"] == "10":
            b = 10

        if callback_data["action"] == "make" and callback_data["value"] == "50":
            b = 50

        if callback_data["action"] == "make" and callback_data["value"] == "100":
            b = 100

        if callback_data["action"] == "make" and callback_data["value"] == "1000":
            b = 1000

        if callback_data["action"] == "plus" and callback_data["value"] == "1":
            b += 1

        if callback_data["action"] == "plus" and callback_data["value"] == "5":
            b += 5

        if callback_data["action"] == "minus" and callback_data["value"] == "1":
            if b >= 1:
                b -= 1

        if callback_data["action"] == "minus" and callback_data["value"] == "5":
            if b >= 5:
                b -= 5
            else:
                b = 0

        await bot.edit_message_text(
            f"\U0001F4B8 you have {a} money and your bet is {b} money \U0001F4B8",
            query.message.chat.id,
            query.message.message_id,
            reply_markup=main_game_keyboard(),
        )
    if callback_data["action"] == "show_rules":

        await bot.send_message(
            query.message.chat.id,
            "Bitcoin rate is changing every second!\nSolve how it will change and win coins!\nYou can't bet more money than yot have.",
            reply_markup=get_menu_button(),
        )

    if callback_data["action"] == "menu":
        await bot.send_message(
            query.message.chat.id,
            f"\U0001F4B8 You have {a} money now! \U0001F4B8",
            reply_markup=main_game_keyboard(),
        )

    if callback_data["action"] in ["play", "up", "down", "play_again"]:
        if a >= b:
            number = random.randint(0, 20)
            if callback_data["action"] not in ["up", "down", "play_again"]:
                await bot.edit_message_text(
                    "Bitcoin will fall or grow?",
                    query.message.chat.id,
                    query.message.message_id,
                    reply_markup=bitcoin(),
                )
            if callback_data["action"] == "up" and number > 5:

                await bot.edit_message_text(
                    f"\U0001F601 You win {b} money! \U0001F601",
                    query.message.chat.id,
                    query.message.message_id,
                    reply_markup=play_again(),
                )

                a += b

            elif callback_data["action"] == "down" and number < 5:

                await bot.edit_message_text(
                    f"\U0001F601 You win {b} money! \U0001F601",
                    query.message.chat.id,
                    query.message.message_id,
                    reply_markup=play_again(),
                )

                a += b

            elif callback_data["action"] == "down" and number > 5:

                await bot.edit_message_text(
                    f"\U0001F614 You lose {b} money! \U0001F614",
                    query.message.chat.id,
                    query.message.message_id,
                    reply_markup=play_again(),
                )

                a -= b

            elif callback_data["action"] == "up" and number < 5:

                await bot.edit_message_text(
                    f"\U0001F614 You lose {b} money! \U0001F614",
                    query.message.chat.id,
                    query.message.message_id,
                    reply_markup=play_again(),
                )

                a -= b

            if callback_data["action"] == "play_again":
                if a < 1:
                    await bot.edit_message_text(
                        "\U0001F915 Sorry! You have now money \U0001F915",
                        query.message.chat.id,
                        query.message.message_id,
                    )
                else:
                    await bot.edit_message_text(
                        f"\U0001F4B8 You have {a} money now! \U0001F4B8",
                        query.message.chat.id,
                        query.message.message_id,
                        reply_markup=main_game_keyboard(),
                    )
        else:
            await bot.edit_message_text(
                "\U000026D4	your bet is too big! \U000026D4",
                query.message.chat.id,
                query.message.message_id,
                reply_markup=main_game_keyboard(),
            )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
