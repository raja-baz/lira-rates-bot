import json
import os
import tempfile

rates = json.loads(input())

last_buy = rates['buy'][-1]
last_sell = rates['sell'][-1]

ts, br = last_buy
_, sr = last_sell

result = {'buy': br, 'sell': sr, 'ts': ts}

prev_buy = rates['buy'][-2]
prev_sell = rates['sell'][-2]
result['db'] = br - prev_buy[1]
result['ds'] = sr - prev_sell[1]
result['dts'] = ts - prev_buy[0]

_, tmpFile = tempfile.mkstemp()
f = open(tmpFile, 'w')
f.write(json.dumps(result))
f.flush()
os.fsync(f.fileno()) 
f.close()
os.rename(tmpFile, 'last_rates.json')

