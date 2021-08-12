import sys
import json
import os

name = sys.argv[1]
f1 = "rates_next/%s" % name
f2 = "rates_out/%s" % name

if not os.path.exists(f2):
    sys.exit(0)

d1 = json.load(open(f1))
d2 = json.load(open(f2))
fields = ['buy', 'sell']
for field in fields:
    if field not in d1 or field not in d2:
        if field in d1 or field in d2:
            sys.exit(0)
    if d1[field] != d2[field]:
        sys.exit(0)
        
sys.exit(1)
