import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token

from telegram import Bot

bot = Bot(get_token())

text = "Rates updated:\n\n" + render_rates()

for l in open('channels').readlines():
    bot.send_message("@" + l, text)
