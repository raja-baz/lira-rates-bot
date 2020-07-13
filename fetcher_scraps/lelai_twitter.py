import sys
import json

# Make sure time are rendered as if we're in Lebanon
import time
import os
os.environ['TZ'] = 'Asia/Beirut'
time.tzset()

from twitter_scraper import get_tweets

def get_number(line):
    pass

def parse_tweet(tweet):
    text = tweet['text'].lower()
    buy = None
    sell = None
    for line in text.split("\n"):
        if "lelai min" in line:
            sell = get_number(line)
        elif "lelai max" in line:
            buy = get_number(line)
    if buy is None or sell is None:
        return None
    return buy,sell,tweet['time']

tweets = get_tweets("lirawatch", pages=10)
latest = None
previous = None
for t in tweets:
    result = parse_tweet(t)
    if result is None:
        continue
    if latest is None:
        latest = result
    else:
        previous = result
        break

if latest is None:
    sys.exit(1)

br, sr, t = latest
result = {'buy': br, 'sell': sr, 'time': t.strftime("%m/%d/%Y, %H:%M:%S")}

if previous is not None:
    

