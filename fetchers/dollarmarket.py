#!/usr/bin/env python3


import json
import dateparser
import requests
import pytz

def parse_record(record):
    t = dateparser.parse(record['createdAt']).astimezone(pytz.timezone('EET'))
    return (int(record['marketBuy']), int(record['marketSell']), t.ctime(), t)

def parse_history(record, spread):
    v = int(record['value'])
    t = dateparser.parse(record['createdAt']).astimezone(pytz.timezone('EET'))
    return (v - spread, v, t.ctime(), t)

headers = {
    "user-agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; HTC Desire HD A9191 Build/GRJ90)",
    "host": "cur-now.herokuapp.com",
}

token = requests.post("https://cur-now.herokuapp.com/api/auth/user/login", json={"secret": "Zhy6nzsmUOydMzHWKrayRGlRyV_333"}).json()["token"]

headers["mtoken"] = "mtoken@690acdbhkdj65h"
headers["authorization"] = "Bearer " + token

current = parse_record(requests.get("https://cur-now.herokuapp.com/api/LBP/latest", timeout=10, headers=headers).json())
spread = current[1] - current[0]
history = requests.get("https://cur-now.herokuapp.com/api/currencies/historical/LBP", timeout=10, headers=headers)
data = history.json()

lrecord = parse_history(data['rates'][-1], spread)
precord = parse_history(data['rates'][-2], spread)

history_record = lrecord
if abs((current[3] - lrecord[3]).total_seconds()) < 10:
    history_record = precord

sr, br, t, ts = current
psr, pbr, pt, pts = history_record

print(json.dumps({'buy': br, 'sell': sr, 'time': t,
                  'db': br - pbr, 'ds': sr - psr, 'dts': int((ts - pts).total_seconds())}))




