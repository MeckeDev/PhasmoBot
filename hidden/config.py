import json

with open("settings/join.json", "r+") as f:
    to_join = json.load(f)

CHANNEL = to_join.keys()
ALL_CHANNELS = to_join
print(CHANNEL)
