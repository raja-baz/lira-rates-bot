import sys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token, read_channels, get_config, meta

import telegram

bot = telegram.Bot(get_token())

if len(sys.argv) >= 2:
    changed = sys.argv[1].split(",")
else:
    sys.exit(1)

for channel_id in read_channels():
    c = get_config(channel_id)
    found = False
    for u in changed:
        notify = meta[u]['default_notify']
        if u in c:
            notify = c[u]['sub'] and c[u]['notify']
        if notify:
            found = True
            break
    if not found:
        continue
    text = "*Rates updated*:\n\n" + render_rates(channel_id, changed)
    try:
        bot.send_message(channel_id, text, disable_web_page_preview=True, parse_mode=telegram.ParseMode.MARKDOWN_V2)
    except:
        pass
