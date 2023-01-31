#!/usr/bin/env python3


import json
import dateparser
import requests
import pytz

def parse_record(record):
    t = dateparser.parse(record['createdAt']).astimezone(pytz.timezone('EET'))
    return (int(record['marketBuy']), int(record['marketSell']), t.ctime(), t)

host="www.lbpprice.info"

headers = {
    "user-agent": "okhttp/5.0.0-alpha.1",
    "host": host,
    "authorization": "JSXIUQFFnkfZ0Wdsa2332ESWjrebvVYeapjGU"
}

token = requests.post("https://" + host + "/api/v1/auth/login", headers = headers).json()["successResult"]["session"]

headers["mtoken"] = "8"
headers["authorization"] = token

current = parse_record(requests.get("https://" + host + "/api/v1/lebanese_lira/latest", timeout=10, headers=headers).json()["successResult"])
spread = current[1] - current[0]
history = requests.get("https://" + host + "/api/v1/lebanese_lira/chart", params={"from": "2022-12-31", "to": "2023-12-31"}, timeout=10, headers=headers)
data = history.json()["successResult"]

lrecord = parse_record(data[0])
precord = parse_record(data[1])

history_record = lrecord
if abs((current[3] - lrecord[3]).total_seconds()) < 10:
    history_record = precord

sr, br, t, ts = current
psr, pbr, pt, pts = history_record

print(json.dumps({'buy': br, 'sell': sr, 'time': t,
                  'db': br - pbr, 'ds': sr - psr, 'dts': int((ts - pts).total_seconds())}))




