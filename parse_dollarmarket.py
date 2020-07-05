import json
import dateparser

def parse_record(record):
    return (record['buy'], record['sell'], record['updated_at'], dateparser.parse(record['updated_at']))

data = json.loads(input())

sr, br, t, ts = parse_record(data[-1])
psr, pbr, pt, pts = parse_record(data[-2])

print(json.dumps({'buy': br, 'sell': sr, 'time': t,
                  'db': br - pbr, 'ds': sr - psr, 'dts': int((ts - pts).total_seconds())}))

