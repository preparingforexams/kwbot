import inspect
import os
import sys

import telegram.ext
from telegram.ext import ApplicationBuilder

import kw
from kw import create_logger


def get_bot_token_or_die(env_variable: str = "BOT_TOKEN"):
    logger = create_logger(inspect.currentframe().f_code.co_name)  # type: ignore
    if token := os.getenv(env_variable):
        return token

    logger.error(f"failed to retrieve token from environment (`{env_variable}`)")
    sys.exit(1)


def main():
    bot_token = get_bot_token_or_die()
    application = ApplicationBuilder().token(bot_token).build()

    kw_handler = telegram.ext.CommandHandler("kw", kw.kw)
    application.add_handler(kw_handler)
    month_handler = telegram.ext.CommandHandler("month", kw.month)
    application.add_handler(month_handler)
    gibmonth_handler = telegram.ext.CommandHandler("gibMonat", kw.month)
    application.add_handler(gibmonth_handler)
    gibtag_handler = telegram.ext.CommandHandler("gibTag", kw.day)
    application.add_handler(gibtag_handler)
    day_handler = telegram.ext.CommandHandler("day", kw.day)
    application.add_handler(day_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
