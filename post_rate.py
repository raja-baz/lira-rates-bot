import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token, read_channels

from telegram import Bot

bot = Bot(get_token())

text = "Rates updated:\n\n" + render_rates()

for channel_id in read_channels():
    bot.send_message(channel_id, text, disable_web_page_preview=True)
