#!/bin/bash

auth=$(curl -s 'https://lirarate.org/wp-content/themes/lirarate/assets/js/main.js?ver=1.0.34'\
            -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5'\
            --compressed -H 'Connection: keep-alive' -H 'Referer: https://lirarate.org/'  -H 'Sec-GPC: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'\
      | grep "'Authorization'" | sed 's/.*Authorization'"'"'*: *//' | sed "s/'//g")

ver=t$(date '+%Y%-m%-d%-H')
curl -s "https://lirarate.org/wp-json/lirarate/v2/rates?currency=LBP&_ver=$ver" -H "Authorization: $auth" -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5'\
             --compressed -H 'Connection: keep-alive' -H 'Referer: https://lirarate.org/'  -H 'Sec-GPC: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'\
      | python3 "$ROOT"/parse_lira_rate.py

