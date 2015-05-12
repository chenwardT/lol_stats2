import json
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'seed/matches10.json'), 'r') as f:
    json_data = json.dumps(f.read())

results = re.findall(r'\\"summonerId\\":\d+', json_data)

ids = []

for pair in results:
    _k, v = pair.split(':')
    ids.append(v)

with open(os.path.join(BASE_DIR, 'seed/summonerIds10.txt'), 'w') as f:
    for id in set(ids):
        f.write(id + '\n')