import sys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token, read_channels

import telegram

bot = telegram.Bot(get_token())

changed = []
if len(sys.argv) >= 2:
    changed = sys.argv[1].split(",")

text = "*Rates updated*:\n\n" + render_rates(changed)

for channel_id in read_channels():
    bot.send_message(channel_id, text, disable_web_page_preview=True, parse_mode=telegram.ParseMode.MARKDOWN_V2)
