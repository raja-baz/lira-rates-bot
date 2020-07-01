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

def render_single(source):
    info = json.load(open('rates_out/' + source))

    text = "%s (Last update: %s):\n" % (meta[source]['name'], info['time'])
    
    text +=  "Buy: " + str(info['buy'])
    if 'db' in info:
        text += " (%s%d change over a period of: %s)" % ("+" if info['db'] > 0 else "", info['db'], time_ago(info['dts']))
    text += "\n"
    
    text +=  "Sell: " + str(info['sell'])
    if 'ds' in info:
        text += " (%s%d change over a period of: %s)" % ("+" if info['ds'] > 0 else "", info['ds'], time_ago(info['dts']))

    text += "\nSource: %s\n" % meta[source]['site']
    
    return text

def render_rates():
    text = ""
    for source in sorted(os.listdir('rates_out')):
        if source in ignored:
            continue
        if len(text) > 0:
            text += "\n"
        text += render_single(source)

    return text
