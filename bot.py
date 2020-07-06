import sys

import tempfile
import os
import copy
import json
import base64

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from util import render_rates, get_token, read_channels, get_global_config, meta, set_config

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import datetime

last_rates_times = {}
global_config = get_global_config()

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

def atomic_write(file_name, data):
    _, tmpFile = tempfile.mkstemp()
    f = open(tmpFile, 'w')
    f.write(data)
    f.flush()
    os.fsync(f.fileno())
    f.close()
    os.rename(tmpFile, file_name)
    

def write_channels(channels):
    atomic_write('channels', "\n".join(map(str, channels)))

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

def _subscribe(to_add):
    channels = read_channels()
    if to_add in channels:
        return False
    channels.append(to_add)
    write_channels(channels)
    return True
    
    

def subscribe(update, context):
    if mod_protect(update):
        return
    
    to_add = update.effective_chat.id
    if _subscribe(to_add):
        update.message.reply_text("Subscribed")
    else:
        update.message.reply_text("Already subscribed")


def _unsubscribe(to_remove):
    channels = read_channels()
    try:
        channels.remove(to_remove)
        write_channels(channels)
        return True
    except ValueError:
        return False
    

def unsubscribe(update, context):
    if mod_protect(update):
        return
    
    to_remove = update.effective_chat.id
    if _unsubscribe(to_remove):
        update.message.reply_text("Goodbye")
    else:
        update.message.reply_text("Wasn't subscribed to begin with >_>")

def configure_next_source(chat_id, text_func, so_far):
    for key, m in meta.items():
        if key in so_far:
            continue

        options = [
            ("Yes", {"question": "show", "answer": "yes", "so_far": so_far, "subject": key}),
            ("No", {"question": "show", "answer": "no", "so_far": so_far, "subject": key}),
        ]
        markup = create_keyboard(options)
        text_func("%s: %s\n\nWould you like to see rates from %s? Default: %s" % (m['name'], m['desc'], m['name'], str(m['default_enabled'])),
                  reply_markup = markup)
        return

    print(so_far)
    
    summary = ""
    for k, config in so_far.items():
        if len(summary) > 0:
            summary += "\n"
        summary += "%s: show: %s" % (meta[k]['name'], str(config['sub']))
        if config['sub']:
            summary += " notify: %s" % str(config['notify'])
    
    text_func("Done! Summary:\n\n%s" % summary)
    set_config(chat_id, so_far)
    atomic_write('config', json.dumps(global_config))
    _subscribe(chat_id)
    

def process_next_configuration(chat_id, text_func, data):
    so_far = data['so_far'] if 'so_far' in data else {}
    question, answer = data['question'], data['answer']
    if question == 'show':
        subject = data['subject']
        m = meta[subject]
        if answer == "no":
            so_far[subject] = {'sub': False}
            configure_next_source(chat_id, text_func, so_far)
        else:
            so_far[subject] = {'sub': True}
            options = [("Yes", {"question": "notify", "answer": "yes", "so_far": so_far, "subject": subject}),
                       ("No", {"question": "notify", "answer": "no", "so_far": so_far, "subject": subject})]
            markup = create_keyboard(options)
            text_func("Would you like to receive a message whenever %s updates? Default: %s" % (m['name'], str(m['default_notify'])),
                      reply_markup = markup)
    elif question == "notify":
        subject = data['subject']
        so_far[subject]['notify'] = answer == "yes"
        configure_next_source(chat_id, text_func, so_far)

cached_button_data = {}
button_data_lookup = []

def configure_options(update, context):
    if mod_protect(update):
        return
    query = update.callback_query
    query.answer()

    data = copy.deepcopy(button_data_lookup[int(query.data)])
    
    question, answer = data['question'], data['answer']
    if question == 'sub':
        if answer == 'no':
            query.edit_message_text(text="Okay, bye")
            _unsubscribe(update.effective_chat.id)
            return
        if answer == 'yes':
            configure_next_source(query.message.chat.id, query.message.edit_text, {})
    else:
        process_next_configuration(query.message.chat.id, query.message.edit_text, data)


def create_keyboard(options):
    keyboard = []
    a = 1
    for text,data in options:
        cbdata = base64.b64encode(json.dumps(data, ensure_ascii=False).encode('utf-8')).decode('utf-8')
        try:
            key = cached_button_data[cbdata]
        except KeyError:
            key = str(len(button_data_lookup))
            button_data_lookup.append(data)
            cached_button_data[cbdata] = key
            
        keyboard.append(InlineKeyboardButton(text, callback_data = key))
        
    return InlineKeyboardMarkup([keyboard])

def configure(update, context):
    if mod_protect(update):
        return

    channels = read_channels()
    chat = update.effective_chat
    if chat.id not in channels:
        options = [
            ("Yes", {'question': 'sub', 'answer': 'yes'}),
            ("No", {'question': 'sub', 'answer': 'no'})
        ]
        update.message.reply_text('Do you want to subscribe for rate updates?', reply_markup=create_keyboard(options))
    else:
        configure_next_source(chat.id, update.message.reply_text, {})
        

def rate_limit(chat):
    if chat.type == 'private':
        return False
    
    last_rates_time = last_rates_times[chat.id] if chat.id in last_rates_times else None
    now = datetime.datetime.now()
    if last_rates_time is not None and (now - last_rates_time).total_seconds() <= 3600:
        return True

    last_rates_times[chat.id] = now
    return False

def start(update, context):
    update.message.reply_text("Welcome. This bot monitors multiple sources for lira rate updates. Send /config to configure which sources you want to see. Send /sub or /unsub to subscribe or unsubscribe from getting notified when rates changed. Send /rates for latest rates on record")

def print_rates(update, context):
    if rate_limit(update.effective_chat):
        return
    update.message.reply_text("*Latest rates*:\n\n" + render_rates(update.effective_chat.id), disable_web_page_preview=True, parse_mode=telegram.ParseMode.MARKDOWN_V2)

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
dp.add_handler(CommandHandler('config', configure))
dp.add_handler(CallbackQueryHandler(configure_options))
dp.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()

