import sys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import get_token, read_channels

import telegram

bot = telegram.Bot(get_token())

if len(sys.argv) >= 2:
    message = sys.argv[1]
else:
    sys.exit(1)

for channel_id in read_channels():
    bot.send_message(channel_id, message)
