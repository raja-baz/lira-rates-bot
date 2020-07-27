# -*- coding: utf-8 -*-

import json
import datetime
import os
import random

meta = {
    "lirarate": {
        "name": "Lira Rate",
        "site": "https://lirarate.com",
        'desc': 'Updates one or two times a day',
        'default_enabled': True,
        'default_notify': True
    },
    'businessnews': {
        'name': "Business News",
        'site': "http://www.businessnews.com.lb/",
        'desc': 'Updates once daily, around midday',
        'default_enabled': True,
        'default_notify': True
    },
    'dollarmarket': {
        'name': 'Dollar Market',
        'site': 'https://play.google.com/store/apps/details?id=com.usdmarketapp&hl=ar',
        'site_text': 'سوق الدولار mobile app',
        'desc': 'Updates frequently. Sometimes 5+ times daily',
        'default_enabled': True,
        'default_notify': False
    }
}

lelai_troll_data = [
    "Everyone else +500",
    "Filtering out manipulation...",
    'Trying to "Just show results" to everyone...',
    "Waiting for the dictator to pull rates out of his ass...",
    "!warn stop making fun of me",
    "!warn I don't like your face",
    "!ban no questioning authority, we're revolutionaries who like dictatorships here!",
    "Banning doubters from the internets...",
    "Inflating my creator's ego...",
    "Exploring the blockchain for rates data...",
    "Sacrificing virgins at the altar of the dark Gods of rates...",
    "Not reporting a rate... On Purpose! Take that manipulators, LELAI has detected your silly games!",
    "!warn no speculation unless it's speculation I like",
    "Beware the politically involved administrator of the money laundering, fraud and other illegal activities Telegram group that keeps force-adding CORE members against their will. #staysafe #beware #caution #lebaneselira #marketmanipulation #currencycrisis #devaluation #speculation #lebanon #lebanese #beirut #lbp #usd #usdollar #dollar #lebanesepound",
    "World War Three has just started. This might have a negative impact on sentiment."
]

_config = None
def get_global_config():
    global _config
    if _config is None:
        try:
            _config = json.load(open('config'))
        except FileNotFoundError:
            _config = {}
    return _config

def set_config(chat_id, config):
    get_global_config()[str(chat_id)] = config

def get_config(chat_id):
    config = get_global_config()
    return config[str(chat_id)] if str(chat_id) in config else {}

def get_token():
    try:
        return open('token').read().strip()
    except:
        pass
    return None

def time_ago(seconds):
    if seconds < 3600:
        return str(seconds // 60) + " min"
    return str(seconds // 3600) + " hr"


def escape(s, chars):
    for c in chars:
        s = s.replace(c, "\\" + c)
    return s

def escape_markdown(s):
    return escape(s, "#!().-+")

def render_single(source, highlight=False):
    info = json.load(open('rates_out/' + source))

    m = meta[source]

    text = "%s%s%s _(Last update: %s)_:\n" % ("*" if highlight else "", m['name'], "*" if highlight else "", info['time'])
    
    text +=  "Buy: " + str(info['buy'])
    if 'db' in info:
        text += " _(%s%d change over a period of: %s)_" % ("+" if info['db'] > 0 else "", info['db'], time_ago(info['dts']))
    text += "\n"
    
    text +=  "Sell: " + str(info['sell'])
    if 'ds' in info:
        text += " _(%s%d change over a period of: %s)_" % ("+" if info['ds'] > 0 else "", info['ds'], time_ago(info['dts']))

    text = escape_markdown(text)

    site_link = m['site']
    site_text = escape_markdown(m['site_text'] if 'site_text' in m else site_link)

    text += "\nSource: [%s](%s)\n" % (site_text, site_link)
    
    return text

def render_lelai():
    text = "LELAI: _%s_\n"  % lelai_troll_data[random.randint(0, len(lelai_troll_data)-1)]
    text += "Source: https://lelai-abdellatif.online/"

    return escape_markdown(text)

def render_rates(chat_id, changed=[]):
    text = ""
    c = get_config(chat_id)
    for source in sorted(os.listdir('rates_out')):
        if source not in meta:
            continue
        show = c[source]['sub'] if source in c else meta[source]['default_enabled']
        if not show:
            continue
        if len(text) > 0:
            text += "\n"
        text += render_single(source, source in changed)


    text += "\n%s" % render_lelai()
    return text

def read_channels():
    try:
        return [int(x.strip()) for x in open('channels').readlines()]
    except FileNotFoundError:
        return []
        
