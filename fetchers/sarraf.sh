#!/bin/bash

curl https://dola-62d9a.firebaseapp.com  2>/dev/null | grep /co/ | tail -n2 | python3 "$ROOT"/parse_sarraf.py
