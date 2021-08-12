import json

rates_line = input()
time_line = input()

rates = [int(x.replace(",", "")) for x in rates_line[4:].strip().split()]
time = time_line[4:].strip().split()[0]
result = {'buy': rates[1], 'sell':rates[0], 'time': time}
print(json.dumps(result))
