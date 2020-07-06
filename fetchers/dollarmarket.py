#!/usr/bin/env python3


import json
import dateparser
import requests

def parse_record(record):
    return (int(record['buy']), int(record['sell']), record['updated_at'], dateparser.parse(record['updated_at']))

history = requests.get("https://lebanese-pound-to-usd-price.com/dollar/api/history-1-today")
data = history.json()

lrecord = parse_record(data[-1])
precord = parse_record(data[-2])

current = requests.get("https://lebanese-pound-to-usd-price.com/dollar/api/dollar-lebanon").json()

latest = None
for record in current['data']:
    if record['id'] == 1:
        latest = record
        break

if latest is not None:
    current = parse_record(latest)
    if current != lrecord:
        precord = lrecord
        lrecord = current


sr, br, t, ts = lrecord
psr, pbr, pt, pts = precord

print(json.dumps({'buy': br, 'sell': sr, 'time': t,
                  'db': br - pbr, 'ds': sr - psr, 'dts': int((ts - pts).total_seconds())}))




