import calendar
import inspect
from datetime import datetime, timedelta

import telegram.constants
from telegram import Update
from telegram.ext import ContextTypes

from .logger import create_logger


def send_telegram_error_message(message: str, *, _: Update = None):
    log = create_logger(inspect.currentframe().f_code.co_name)

    log.error(message)


async def kw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    if context.args:
        week_number = int(context.args[0])
        start_of_year = datetime(now.year, 1, 1)
        end_of_given_week_number = start_of_year + timedelta(weeks=week_number)
        start_of_given_week_number = end_of_given_week_number - timedelta(days=6)

        date_format = '%d.%m.%Y'
        message = f"{start_of_given_week_number.strftime(date_format)} - {end_of_given_week_number.strftime(date_format)}"
    else:
        message = str(now.strftime("%W"))

    return await update.effective_message.reply_text(message)
