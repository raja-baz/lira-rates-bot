import sys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token

from telegram.ext import Updater, CommandHandler
import datetime

last_rates_time = None
def print_rates(update, context):
    global last_rates_time

    now = datetime.datetime.now()
    if last_rates_time is None or (now - last_rates_time).total_seconds() > 3600:
        update.message.reply_text(render_rates())
        last_rates_time = now

TOKEN = get_token()

if TOKEN is None or len(TOKEN) == 0:
    print("Please put a auth token for the bot in the token file")
    sys.exit(1)


updater = Updater(token=TOKEN, use_context = True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('rates', print_rates))

updater.start_polling()
updater.idle()

