#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
import os

html = BeautifulSoup(requests.get("https://www.omt.com.lb/en").content, features="lxml")
container = html.find('div', attrs={'class': 'exchange-rate-container'})
image_name=container.find('span', attrs={'class':'exchange-rate'}).find('img').get('src')
path=os.getenv("ROOT") + "/omt_ocr.sh"
os.system(path + " '" + image_name + "'")

rate_string = open('/tmp/bla.txt').readlines()[0]
date_string = container('span')[-1].text

rate = rate_string.split()[-2].replace(",", "")

result = {'buy': None, 'sell': rate, 'time': date_string}
print(json.dumps(result))
