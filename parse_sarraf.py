import json
import re

rates_line = input()
time_line = input()

capture_number = "([0-9]+\s*,\s*[0-9]+)"
regexp = re.compile(f"/co/\s*{capture_number}\s+{capture_number}")

def captured_to_num(s):
    return int(s.replace(" ", "").replace(",", ""))

rates = [captured_to_num(s) for s in regexp.match(rates_line).groups()]
time = time_line[4:].strip().split()[0]
result = {'buy': rates[1], 'sell':rates[0], 'time': time}
print(json.dumps(result))
