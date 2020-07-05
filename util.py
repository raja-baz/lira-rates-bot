# -*- coding: utf-8 -*-

import json
import datetime
import os

meta = {
    "lirarate": {
        "name": "Lira Rate",
        "site": "https://lirarate.com",
        'desc': 'Updates one or two times a day',
        'default_enabled': True,
        'default_notify': True
    },
    'lelai': {
        "name": "LELAI Abdellatif",
        "site": "https://lelai-abdellatif.online/",
        'desc': "Run by a dictator, updates whenever said dictator likes the rates. Stops updating when he doesn't",
        'default_enabled': False,
        'default_notify': False
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

_config = None
def get_global_config():
    global _config
    if _config is None:
        try:
            _config = json.load(open('config'))
        except FileNotFoundError:
            _config = {}
    return _config

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
    return escape(s, "().-+")

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

def render_rates(chat_id, changed=[]):
    text = ""
    c = get_config(chat_id)
    for source in sorted(os.listdir('rates_out')):
        show = c[source]['sub'] if source in c else meta[source]['default_enabled']
        if not show:
            continue
        if len(text) > 0:
            text += "\n"
        text += render_single(source, source in changed)

    return text

def read_channels():
    try:
        return [int(x.strip()) for x in open('channels').readlines()]
    except FileNotFoundError:
        return []
        
