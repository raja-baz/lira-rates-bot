#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json

html = BeautifulSoup(requests.get("https://www.omt.com.lb/en").content, features="lxml")
container = html.find('div', attrs={'class': 'exchange-rate-container'})
rate_string = container.find('span', attrs={'class':'exchange-rate'}).text
date_string = container('span')[-1].text

rate = rate_string.split()[-2].replace(",", "")

result = {'buy': rate, 'sell': None, 'time': date_string}
print(json.dumps(result))
