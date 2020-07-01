import sys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token

from telegram.ext import Updater, CommandHandler
import datetime

last_rates_times = {}

def rate_limit(chat):
    if chat.type == 'private':
        return False
    
    last_rates_time = last_rates_times[chat.id] if chat.id in last_rates_times else None
    now = datetime.datetime.now()
    if last_rates_time is not None and (now - last_rates_time).total_seconds() <= 3600:
        return True

    last_rates_times[chat.id] = now
    return False

def print_rates(update, context):
    if rate_limit(update.effective_chat):
        return
    update.message.reply_text("Latest rates:\n\n" + render_rates())

TOKEN = get_token()

if TOKEN is None or len(TOKEN) == 0:
    print("Please put a auth token for the bot in the token file")
    sys.exit(1)


updater = Updater(token=TOKEN, use_context = True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('rates', print_rates))

updater.start_polling()
updater.idle()

