import json
import re

with open('../seed/matches2.json', 'r') as f:
    json_data = json.dumps(f.read())

results = re.findall(r'\\"summonerId\\":\d+', json_data)

ids = []

for pair in results:
    _k, v = pair.split(':')
    ids.append(v)

with open('../seed/summonerIds.txt', 'w') as f:
    for id in set(ids):
        f.write(id + '\n')