import inspect
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes

from .logger import create_logger


def send_telegram_error_message(message: str, *, _: Update = None):
    log = create_logger(inspect.currentframe().f_code.co_name)

    log.error(message)


# should we implement the actual ISO8601:3.1.1.23
# see https://www.iso.org/obp/ui/#iso:std:iso:8601:-1:ed-1:v1:en:term:3.1.1.23
# spec? nah, we're doing a binary search and compare against the strftime("%W") format modifier
def find_end_date_for_kw(week_number: int, now: datetime) -> datetime:
    start_of_year = datetime(now.year, 1, 1, tzinfo=ZoneInfo("Europe/Berlin"))
    naive_end_of_week_date = start_of_year + timedelta(weeks=week_number)

    end_of_week_date = naive_end_of_week_date
    attempts = 0
    # whatever
    max_attempts = 100

    while int(end_of_week_date.strftime("%W")) != week_number and attempts <= max_attempts:
        if int(end_of_week_date.strftime("%w")) > week_number:
            end_of_week_date += timedelta(days=1)
        else:
            end_of_week_date -= timedelta(days=1)

        attempts += 1

    # sunday is always the final day of the week for our purposes (iso standard, sunday=7, same as `isoweekday()`)
    end_of_week_date.replace(day=7)
    return end_of_week_date


async def month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log = create_logger(inspect.currentframe().f_code.co_name)
    log.debug("start")
    now = datetime.now()
    message = f"{now.strftime('%B')} ({now.month})"

    if context.args:
        try:
            float(context.args[0])
            message = "no"
        except ValueError:
            pass

    log.debug("end")
    return await update.effective_message.reply_text(text=message)


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log = create_logger(inspect.currentframe().f_code.co_name)
    log.debug("start")
    now = datetime.now()
    message = f"of the year: {now.strftime('%j')}\nof the month: {now.strftime('%d')}"

    if context.args:
        try:
            float(context.args[0])
            message = "no"
        except ValueError:
            pass

    log.debug("end")
    return await update.effective_message.reply_text(text=message)


async def kw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log = create_logger(inspect.currentframe().f_code.co_name)
    log.debug("start")

    now = datetime.now(tz=ZoneInfo("Europe/Berlin"))
    if context.args:
        week_number = int(context.args[0])
        end_of_given_week_number = find_end_date_for_kw(week_number, now)
        start_of_given_week_number = end_of_given_week_number - timedelta(days=6)

        date_format = '%d.%m.%Y'
        message = f"{start_of_given_week_number.strftime(date_format)} - {end_of_given_week_number.strftime(date_format)}"
    else:
        message = now.strftime("%W")

    log.debug("end")
    return await update.effective_message.reply_text(message)
