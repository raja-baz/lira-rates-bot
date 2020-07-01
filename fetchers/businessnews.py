#!/usr/bin/env python3

from lxml import html
import requests
import json

def parse_range(r):
    r = r.replace(",", "")
    if "-" in r:
        r = r[r.index("-")+1:]
    return r

page=requests.get('http://www.businessnews.com.lb/asp/MarketUSDLL740.asp')
tree = html.fromstring(page.content)

date_spans = [x.text for x in tree.xpath('//table')[1].xpath('//span')]

date_string = date_spans[1] + " " + date_spans[2]

prices = [x.text for x in tree.xpath('//font')]
sell = parse_range(prices[2])
buy = parse_range(prices[3])

print(json.dumps({'time': date_string, 'buy': buy, 'sell': sell}))
