import sys

import tempfile
import os

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token, read_channels

from telegram.ext import Updater, CommandHandler
import datetime

last_rates_times = {}

def get_chat_info(bot, chat_id):
    chat = bot.getChat(chat_id)
    if chat.type == 'private':
        return str(chat.get_member(chat_id))
    return str(chat)

def list_subscribers(update, context):
    if update.effective_chat.id != 907198901:
        return

    text = ""
    for channel_id in read_channels():
        if len(text) > 0:
            text += "\n\n"
        text += get_chat_info(context.bot, channel_id)
        if len(text) > 3000:
            update.message.reply_text(text)
            text = ""

    if len(text) > 0:
        update.message.reply_text(text)

def write_channels(channels):
    _, tmpFile = tempfile.mkstemp()
    f = open(tmpFile, 'w')
    f.write("\n".join(map(str, channels)))
    f.flush()
    os.fsync(f.fileno())
    f.close()
    os.rename(tmpFile, 'channels')

def mod_protect(update):
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == "private":
        return False
    
    uid = user.id
    mod_ids = [m.user.id for m in chat.get_administrators()]
    if uid not in mod_ids:
        update.message.reply_text("Only mods can do this")
        return True
    return False
    

def subscribe(update, context):
    if mod_protect(update):
        return
    
    to_add = update.effective_chat.id
    channels = read_channels()
    if to_add in channels:
        update.message.reply_text("Already subscribed")
        return
    channels.append(to_add)
    write_channels(channels)
    update.message.reply_text("Subscribed")

def unsubscribe(update, context):
    if mod_protect(update):
        return
    
    to_remove = update.effective_chat.id
    channels = read_channels()
    try:
        channels.remove(to_remove)
        write_channels(channels)
        update.message.reply_text("Goodbye")
    except ValueError:
        update.message.reply_text("Wasn't subscribed to begin with >_>")

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
    update.message.reply_text("Latest rates:\n\n" + render_rates(), disable_web_page_preview=True)

TOKEN = get_token()

if TOKEN is None or len(TOKEN) == 0:
    print("Please put a auth token for the bot in the token file")
    sys.exit(1)


updater = Updater(token=TOKEN, use_context = True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('rates', print_rates))
dp.add_handler(CommandHandler('sub', subscribe))
dp.add_handler(CommandHandler('unsub', unsubscribe))
dp.add_handler(CommandHandler('subscribers', list_subscribers))

updater.start_polling()
updater.idle()

