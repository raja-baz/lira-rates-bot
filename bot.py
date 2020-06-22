import sys
import json
import datetime

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater, CommandHandler

def time_ago(ms):
    seconds = ms // 1000
    if seconds < 3600:
        return str(seconds // 60) + " min"
    return str(seconds // 3600) + " hr"

def render_rates():
    text = "Latest rates: \n\n"
    info = json.load(open('last_rates.json'))
    
    text +=  "Buy: " + str(info['buy'])
    if 'db' in info:
        text += " (%s%d change over a period of: %s)" % ("+" if info['db'] > 0 else "", info['db'], time_ago(info['dts']))
    text += "\n"
    
    text +=  "Sell: " + str(info['sell'])
    if 'ds' in info:
        text += " (%s%d change over a period of: %s)" % ("+" if info['ds'] > 0 else "", info['ds'], time_ago(info['dts']))
    text += "\n\n"

    text += "Source: https://lirarate.com\n"
    dt = datetime.datetime.now() - datetime.datetime.fromtimestamp(info['ts']/1000)
    text += "Last update: %s ago" % time_ago(dt.seconds * 1000)

    return text

def print_rates(update, context):
    update.message.reply_text(render_rates())

try:
    TOKEN = open('token').read().strip()
except:
    TOKEN = None

if TOKEN is None or len(TOKEN) == 0:
    print("Please put a auth token for the bot in the token file")
    sys.exit(1)


updater = Updater(token=TOKEN, use_context = True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('rates', print_rates))

updater.start_polling()
updater.idle()

# print(render_rates())
