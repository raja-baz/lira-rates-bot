import sys
import json
import os

name = sys.argv[1]
f1 = "rates_next/%s" % name
f2 = "rates_out/%s" % name

from util import ignored

if name in ignored:
    sys.exit(1)

if not os.path.exists(f2):
    sys.exit(0)

d1 = json.load(open(f1))
d2 = json.load(open(f2))
for field in ('ts', 'buy', 'sell'):
    if d1[field] != d2[field]:
        sys.exit(0)
        
sys.exit(1)
