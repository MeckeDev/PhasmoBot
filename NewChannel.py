from hidden.config import *
import json
import requests as r

# the Class for every Channel
class NewChannel:

    def __init__(self, channel_name):

        # sets the name of the Channel
        self.name = channel_name

        # placeholder for the settings
        self.settings = ""

        # opens the Settings-File
        with open("settings/channels.json", "r") as set_f:
            self.settings = json.load(set_f)[self.name]

        # sets all settings from the File to the specific Variable
        self.language = self.settings["language"]
        self.evidence = self.settings["evidence"]
        self.used = self.settings["used"]
        self.responds = self.settings["responds"]
        self.ghost_name = self.settings["ghost_name"]
        self.allowed = self.settings["allowed"]
        self.ignore = self.settings["ignore"]
        self.whitelist = self.settings["whitelist"]
        self.d_count = self.settings["death_count"]
        self.d_message = self.settings["death_message"]
        
        
        # opens the Text-File
        with open("../texts.json", "r") as text_f:
            self.texts = json.load(text_f)[self.language]
            
        self.bot_text = self.texts["Bot_text"]

        # generates the list of possible ghosts depending on the given evidences
        self.ghosts = self.check_evidences()


    # This Function is testing what Ghosts are possible depending on given evidences
    def check_evidences(self):

        # placeholder for the possible ghosts
        possible_ghosts = []

        # gets every ghost from my selfwritten API
        # all_ghosts = json.loads(r.get("https://meckedev.com/PhasmoBot/api.json").text)

        # checks every Ghost if it is still possible
        for ghost in self.texts["Ghosts"]:

            # gets a list of all evidences of the specific Ghost
            evi = self.texts["Ghosts"][ghost]["Evidence"]

            # adds the Ghost to the possible Ghosts if every collected evidence matches the needed evidence for the specific Ghost
            if all(elem in evi  for elem in self.evidence):
                possible_ghosts.append(ghost)

        # returns a list of the possible Ghosts
        return possible_ghosts
