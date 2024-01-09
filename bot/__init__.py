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
    while int(end_of_week_date.strftime("%W")) != week_number:
        if int(end_of_week_date.strftime("%w")) < week_number:
            end_of_week_date += timedelta(days=1)
        else:
            end_of_week_date -= timedelta(days=1)

    if end_of_week_date.weekday() != 0:
        # since we want the end of the week we want to go to the next sunday
        end_of_week_date += timedelta(days=(7 - end_of_week_date.weekday()))

    return end_of_week_date


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
