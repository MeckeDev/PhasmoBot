from hidden.config import *
import json


class NewChannel:

    def __init__(self, channel_name):

        self.name = channel_name

        self.settings = ""
        self.texts = ""
        self.user_points = ""

        with open("Twitch_Bot/settings/channels.json", "r") as set_f:
            self.settings = json.load(set_f)[self.name]

        try:
            with open("Twitch_Bot/points/points.json", "r") as point_f:
                self.user_points = json.load(point_f)

        except json.JSONDecodeError:
            print("points.json konnte nicht gelesen werden.")
            self.user_points = {}

        with open("Twitch_Bot/settings/text.json", "r") as text_f:
            self.texts = json.load(text_f)[self.settings["language"]]

        self.command_texts = self.texts["commands"]
        self.bot_texts = self.texts["bot_info"]

        self.save_points()

        self.admins = self.settings["admins"]
        self.moderators = self.settings["moderators"]
        self.blacklist = self.settings["blacklist"]
        self.language = self.settings["language"]
        self.discord = self.settings["discord"]
        self.points = self.settings["points"]
        self.points_amount = self.settings["point_amount"]
        self.points_period = self.settings["point_period"]
        self.points_get_period = self.settings["point_get_period"]
        self.commands_link = self.settings["commands_link"]
        self.prefix = self.settings["prefix"]
        self.channel_points = self.user_points[self.name]
        self.evidence = self.settings["evidence"]

        self.ghosts = self.check_evidences()


    def check_evidences(self):

        possible_ghosts = []

        with open("Discord_Bot/infos/ghosts.json", "r") as f:
            all_ghosts = json.load(f)

        for ghost in all_ghosts["Ghosts"]:
            evi = all_ghosts["Ghosts"][ghost]["Evidence"]
            if all(elem in evi  for elem in self.evidence):
                possible_ghosts.append(ghost)

        return possible_ghosts


    def get_point_list(self):

        with open("Twitch_Bot/points/points.json", "r") as point_f:
            self.user_points = json.load(point_f)

        self.channel_points = self.user_points[self.name]

    def pay_points(self, name, cost):

        if name not in self.admins:

            if self.channel_points[name] > cost:

                self.channel_points[name] = self.channel_points[name] - cost
                self.save_points()

                return True

            else:

                return False

        else:
            return True

    def save_points(self):

        with open("Twitch_Bot/points/points.json", "w") as point_f:
            text = json.dumps(self.user_points, indent=8)
            point_f.write(text)

    def set_values(self, text, val1, val2, val3):

        text = text.replace("NAME1", val1)
        text = text.replace("DISCORD", val1)
        text = text.replace("WORD", val1)
        text = text.replace("NAME2", val2)

        try:
            text = text.replace("AMOUNT", str(val3))
        except ValueError:
            pass

        text = text.replace("POINTS", self.settings["points"])
        text = text.replace("GAME", str(val3))

        return text

    def add_points(self, users, amount):

        for user in users:
            if user not in self.channel_points:
                self.channel_points[user] = 50
            else:
                if user not in self.blacklist:
                    self.channel_points[user] = self.channel_points[user] + amount

        for x in self.blacklist:
            self.channel_points[x] = -1

        self.save_points()

    def is_admin(self, user):

        if user in self.admins:
            return True
        else:
            return False

    def is_mod(self, user):

        if user in self.moderators:
            return True
        else:
            return False

    def set(self, setting, text):

        with open("Twitch_Bot/settings/channels.json", "r") as set_f:
            settings = json.load(set_f)

        try:
            text = int(text)
        except:
            pass

        settings[self.name][setting] = text

        with open("Twitch_Bot/settings/channels.json", "w+") as chann_f:
            json.dump(settings, chann_f, indent=8)

    def save_settings(self, setting, value):

        if value == "make_empty":

            with open("Twitch_Bot/settings/channels.json", "r") as set_f:
                settings = json.load(set_f)

            settings[self.name][setting] = []

            with open("Twitch_Bot/settings/channels.json", "w+") as chann_f:
                json.dump(settings, chann_f, indent=8)

        else:
            with open("Twitch_Bot/settings/channels.json", "r") as set_f:
                settings = json.load(set_f)

            settings[self.name][setting].append(value)

            with open("Twitch_Bot/settings/channels.json", "w+") as chann_f:
                json.dump(settings, chann_f, indent=8)

    def remove_setting(self, setting, value):

        with open("Twitch_Bot/settings/channels.json", "r") as chann_f:
            settings = json.load(chann_f)

        settings[self.name][setting].remove(value)

        with open("Twitch_Bot/settings/channels.json", "w+") as chann_f:
            json.dump(settings, chann_f, indent=8)


def is_int(num):
    try:
        num = int(num)
        return True
    except (ValueError, TypeError):
        return False
