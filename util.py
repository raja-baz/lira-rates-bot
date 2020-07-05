# -*- coding: utf-8 -*-

import json
import datetime
import os

meta = {
    "lirarate": {
        "name": "Lira Rate",
        "site": "https://lirarate.com"
    },
    'lelai': {
        "name": "LELAI",
        "site": "https://lebaneselira.org"
    },
    'businessnews': {
        'name': "Business News",
        'site': "http://www.businessnews.com.lb/"
    },
    'dollarmarket': {
        'name': 'Dollar Market',
        'site': 'https://play.google.com/store/apps/details?id=com.usdmarketapp&hl=ar',
        'site_text': 'سوق الدولار mobile app',
    }
}

ignored = ["lelai"]

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
    
    print(text)
    return text

def render_rates(changed=[]):
    text = ""
    for source in sorted(os.listdir('rates_out')):
        if source in ignored:
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
        
