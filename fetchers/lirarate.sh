#!/bin/bash

auth=$(curl -s https://lirarate.com/wp-content/themes/lirarate/assets/js/main.js | grep "'Authorization'" | sed 's/.*Authorization'"'"'*: *//' | sed "s/'//g")
ver=$(date '+%Y%-m%-d%-H')
curl -s "https://lirarate.com/wp-json/lirarate/v2/rates?currency=LBP&_ver=$ver" -H "Authorization: $auth" | python3 "$ROOT"/parse_lira_rate.py

