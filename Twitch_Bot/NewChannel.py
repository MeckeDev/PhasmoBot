from hidden.config import *
import json


class NewChannel:

    def __init__(self, channel_name):

        self.name = channel_name

        self.settings = ""
        self.texts = ""

        with open("Twitch_Bot/settings/channels.json", "r") as set_f:
            self.settings = json.load(set_f)[self.name]

        with open("Twitch_Bot/settings/text.json", "r") as text_f:
            self.texts = json.load(text_f)[self.settings["language"]]

        self.command_texts = self.texts["commands"]
        self.bot_texts = self.texts["bot_info"]

        self.admins = self.settings["admins"]
        self.moderators = self.settings["moderators"]
        self.language = self.settings["language"]
        self.evidence = self.settings["evidence"]
        self.used = self.settings["used"]
        self.responds = self.settings["responds"]
        self.ghost_name = self.settings["ghost_name"]

        self.ghosts = self.check_evidences()


    def check_evidences(self):

        possible_ghosts = []

        with open("Discord_Bot/infos/ghosts.json", "r", encoding="utf-8") as f:
            all_ghosts = json.load(f)

        for ghost in all_ghosts[self.language]["Ghosts"]:
            evi = all_ghosts[self.language]["Ghosts"][ghost]["Evidence"]
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
