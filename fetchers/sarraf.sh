#!/bin/bash

curl https://dollebweb.firebaseapp.com  2>/dev/null | grep /co/ | tail -n2 | python3 "$ROOT"/parse_sarraf.py
