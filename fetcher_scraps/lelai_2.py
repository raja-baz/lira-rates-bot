import requests
import json

def from_weird_format(s):
    result = ""
    escaped = False
    i = -1
    while i < len(s)-1:
        i += 1
        c = s[i]
        if escaped:
            if c == "x":
                num=s[i+1:i+3]
                result += chr(int(num, 16))
                i += 2
            elif c == "\\":
                result += c
            elif c == "n":
                result += "\n"
            else:
                result += "\\" + c
            
            escaped = False
            continue
        if c == "\\":
            escaped = True
            continue
        result += c
    return result

data=requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vQKxp7P4c5bbgJf403C4r51yQDeDljC6-ETLLBPYEXX9q64iGSRo0PpPEtY4W68qOYEmFTiEfVKDkz3/pubhtml/sheet?headers\x3dfalse&gid=540565156").content.decode('utf-8')
search="serializedChartProperties'"
idx = data.index(search) + len(search)
start = data.index("'", idx) + 1
end = data.index("'", start)

stage_1 = json.loads(from_weird_format(data[start:end]))
stage_2 = json.loads(stage_1[7][1])

latest = int(stage_2['rows'][0]['c'][0]['v'])
prev = int(stage_2['rows'][1]['c'][0]['v'])

print(json.dumps({'buy': latest, 'time': 




