import json

with open("Twitch_Bot/settings/join.json", "r+") as f:
    to_join = json.load(f)

CHANNEL = to_join["Channels"].keys()
ALL_CHANNELS = to_join["Channels"]
print(CHANNEL)

TMI_TOKEN = 'oauth:ax9kgxruhg4lea8oqso20cbbsbfhwo'
CLIENT_ID = '5rlr0r8pg4vnh9hl4kc8wvqhv4idkz'
BOT_NICK = 'PhasmoBot'
BOT_PREFIX = "$"
NEVER_VISIT_AGAIN = ["kanyetwittee"]
CHANNEL_ID = "55898523"
