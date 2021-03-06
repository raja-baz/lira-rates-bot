import json
import time

# Make sure time are rendered as if we're in Lebanon
import os
os.environ['TZ'] = 'Asia/Beirut'
time.tzset()

rates = json.loads(input())

last_buy = rates['buy'][-1]
last_sell = rates['sell'][-1]

ts, br = last_buy
_, sr = last_sell

ts = ts // 1000


result = {'buy': br, 'sell': sr, 'time': time.ctime(ts)}

prev_buy = rates['buy'][-2]
prev_sell = rates['sell'][-2]
result['db'] = br - prev_buy[1]
result['ds'] = sr - prev_sell[1]
result['dts'] = ts - prev_buy[0]//1000

print(json.dumps(result))

