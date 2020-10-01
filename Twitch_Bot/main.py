from twitchio.ext import commands
from NewChannel import *
import time
import threading

# Hier wird der Bot erstellt und mit den Keys/Tokens gefüttert
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    api_token=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNEL
)

with open("Twitch_Bot/settings/channels.json", "r") as f:
    channels = json.load(f)
    
    for ch in CHANNEL:
        try:
            x = channels[ch]
        except KeyError:

            channels[ch.lower()] = {
                "admins": [
                        ch.lower(),
                        "mecke_dev"
                ],
                "moderators": [],
                "blacklist": [],
                "language": ALL_CHANNELS[ch],
                "evidence" : [],
                "commands_link" : "",
                "ghost_name" : "",
                "responds" : "",
                "used" : 0
        }

with open("Twitch_Bot/settings/channels.json", "w+") as f:
    json.dump(channels, f, indent=8)

# Dieses Event wird getriggert wenn der Bot bereit ist
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


# Das Event wird jedes mal getriggert wenn eine Nachricht im Channel geschrieben wird
@bot.event
async def event_message(message):

    channel = message.channel.name.lower()
    if message.author.name.lower() in ["chris_live", "mecke_dev"]:
        time.sleep(1)

    # Hier wird wieder die channels.json zu einer Klasse gemacht
    # ↑ Wird in Zukunft nicht weiter kommentiert
    ch = NewChannel(channel)

    # ↓ Zum Debuggen und um Informationen zur Nachricht zu bekommen
    # ↓ In der raw_data stehen auch die IDs von Kanalpunkt-Belohnungen
    # print(message.raw_data)

    # Schreibt den Usernamen und die Nachricht in die Konsole
    print(f"{message.author.name} @ {message.channel.name} \n{message.content}\n")
    
    await bot.handle_commands(message)

@bot.command(name='name')
async def name_ghost(ctx, first_name=None, last_name=None, *, responds=None):

    # Channel zu Klasse
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    if first_name == "reset":

        with open("Twitch_Bot/settings/channels.json", "r") as f:
            settings = json.load(f)
        
        settings[channel]["ghost_name"] = ""
        settings[channel]["responds"] = ""
            
        with open("Twitch_Bot/settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

    elif first_name and last_name:

        if not responds:

            if ch.language == "de":
                responds = "nicht angegeben"
            elif ch.language == "en":
                responds = "no set"

        with open("Twitch_Bot/settings/channels.json", "r") as f:
            settings = json.load(f)
        
        settings[channel]["ghost_name"] = f"{first_name} {last_name}"
        settings[channel]["responds"] = f"{responds}"
            
        with open("Twitch_Bot/settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

        if ch.language == "de":
            await ctx.send(f"{first_name} {last_name} reagiert auf: {responds}")
        elif ch.language == "en":
            await ctx.send(f"{first_name} {last_name} responds to: {responds}")

    elif not first_name and not last_name and not responds:

        if ch.language == "de":
            await ctx.send(f"{ch.ghost_name} antwortet: {ch.responds}")
        elif ch.language == "en":
            await ctx.send(f"{ch.ghost_name} responds to: {ch.responds}")


@bot.command(name='join', aliases=["enter"])
async def join_me(ctx, language=None, name=None):

    if ctx.author.name.lower() == "mecke_dev" and name:
        name = name.lower()
    else:
        name = ctx.message.author.name.lower()

    with open("Twitch_Bot/settings/join.json", "r") as f:
        joinable = json.load(f)

    try: 
        x = joinable["Channels"][name]
        if x == "de":
            await ctx.send(f'{name} ich bin bereits in deinem Channel')
        elif x == "en":
            await ctx.send(f'{name} i\'m already in your Channel')

        
    except KeyError:

        if language:

            if language in ["en", "eng", "english", "uk", "us"]:
                joinable["Channels"][name] = "en"
                await ctx.send(f'{name} i\'m joining your Channel with english Settings')

            elif language in ["de", "ger", "deutsch", "german"]:
                joinable["Channels"][name] = "de"                
                await ctx.send(f'{name} ich joine deinem Channel mit deutschen Einstellungen')

            with open("Twitch_Bot/settings/join.json", "w+") as f:
                json.dump(joinable, f, indent=8)

        else:
            await ctx.send(f'{name} please enter "$join eng" or "$join de"')


@bot.command(name='leave', aliases=["part", "exit", "quit"])
async def leave_me(ctx, name=None):

    if ctx.author.name.lower() == "mecke_dev" and name:
        name = name.lower()
    else:
        name = ctx.message.author.name.lower()

    with open("Twitch_Bot/settings/join.json", "r") as f:
        joinable = json.load(f)

    try: 
        x = joinable["Channels"][name]
        joinable["Channels"].pop(name)
        await ctx.send(f'{name}, Bye. FeelBadMan')
        
    except KeyError:
        await ctx.send(f'I\'m not active at {name}\'s Channel.')


@bot.command(name='commands', aliases=["befehle", "cmd"])
async def commands(ctx):

    # Channel zu Klasse
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # postet den festgelegten Link-text im Chat
    await ctx.send(f"{ch.commands_link}")


@bot.command(name='game', aliases=["phasmophobia"])
async def whats_game(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    await ctx.send(f"Phasmophobia is a 4 player online co-op psychological horror where you and your team members of paranormal investigators will enter haunted locations filled with paranormal activity and gather as much evidence of the paranormal as you can. You will use your ghost hunting equipment to search for and record evidence of whatever ghost is haunting the location.")


@bot.command(name='intro', aliases=["phasmobot"])
async def introduce(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    if ch.language == "de":
        await ctx.send(f"Ich bin ein Bot, welcher speziell für Phasmophobia entwickelt wurde, mein Entwickler ist nicht der Entwickler des Spiels.")
    else:
        await ctx.send(f"Hey, I'm a Bot especially created for the Game Phasmophobia, my Dev is not the Dev of the Game.")


@bot.command(name='evidence', aliases=["evi", "e"])
async def ghost(ctx, *, detail=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    if not detail:
        if ch.language == "de":
            await ctx.send(f"Beweise: {ch.evidence}. Mögliche Geister: {ch.ghosts}")
        else:
            await ctx.send(f"Evidences: {ch.evidence}. Possible Ghosts: {ch.ghosts}")

    # if ch.is_mod(ctx.author.name) or ch.is_admin(ctx.author.name) and detail:

    if detail.lower() == "reset":
        
        with open("Twitch_Bot/settings/channels.json", "r") as f:
            settings = json.load(f)
        
        settings[channel]["evidence"] = []
        settings[channel]["ghost_name"] = ""
        settings[channel]["responds"] = ""
            
        with open("Twitch_Bot/settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

        if ch.language == "de":
            await ctx.send(f"Beweise zurückgesetzt.")
        else: 
            await ctx.send(f"Evidences are reset.")

    else:

        if ch.language == "de":

            evidences = {

                "EMF Level 5"           : ["emf", "emf level 5", "level 5"],
                "Geisterbox"            : ["spirit box", "spirit", "box", "talk", "spiritbox", "geisterbox"],
                "Fingerabdrücke"        : ["fingerprints", "finger", "footprints", "prints", "abdruck", "abdrücke", "fingerabdrücke"],
                "Geisterbuch"           : ["ghost writing", "ghostwriting","writing", "book", "write", "wrote", "written", "writer", "ghostwriter", "ghost writer", "buch", "geisterbuch"],
                "Gefriertemperaturen"   : ["freezing", "freezing temperatures", "frozen", "cold", "ice", "temps", "temperature", "freeze", "temperatur", "kalt", "kälte", "gefriertemperatur"],
                "Geisterorb"            : ["orb", "ghost orb", "ghostorb", "orbs", "ghostorbs", "ghost orbs"]

            }

        else:

            evidences = {

                "EMF Level 5"           : ["emf", "emf level 5", "level 5"],
                "Spirit Box"            : ["spirit box", "spirit", "box", "talk", "spiritbox", "geisterbox"],
                "Fingerprints"          : ["fingerprints", "finger", "footprints", "prints", "abdruck", "abdrücke", "fingerabdrücke"],
                "Ghost Writing"         : ["ghost writing", "ghostwriting","writing", "book", "write", "wrote", "written", "writer", "ghostwriter", "ghost writer", "buch", "geisterbuch"],
                "Freezing Temperatures" : ["freezing", "freezing temperatures", "frozen", "cold", "ice", "temps", "temperature", "freeze", "temperatur", "kalt", "kälte", "gefriertemperatur"],
                "Ghost Orb"             : ["orb", "ghost orb", "ghostorb", "orbs", "ghostorbs", "ghost orbs"]

            }

        found = False
        real = None

        for evi in evidences:
            if detail.lower() in evidences[evi]:
                if evi not in ch.evidence:
                    
                    with open("Twitch_Bot/settings/channels.json", "r") as f:
                        settings = json.load(f)
        
                    settings[channel]["evidence"].append(evi)
            
                    with open("Twitch_Bot/settings/channels.json", "w+") as f:
                        json.dump(settings, f, indent=8)

                    real = evi
                    found = True
                else:
                    found = True


        channel = ctx.channel.name.lower()
        ch = NewChannel(channel)
            
        if found and real:
            if ch.language == "de":
                await ctx.send(f"{real} als Beweis eingetragen. Mögliche Geister: {ch.ghosts}")
            else:
                await ctx.send(f"{real} added to evidences. Possible Ghosts: {ch.ghosts}")
        elif found and not real:
            if ch.language == "de":
                await ctx.send(f"{real} ist bereits eingetragen. Mögliche Geister: {ch.ghosts}")
            else:
                await ctx.send(f"{real} is already an evidence. Possible Ghosts: {ch.ghosts}")
        else:
            if ch.language == "de":
                await ctx.send(f"{detail} ist nicht als Beweis erkannt worden.")
            else:
                await ctx.send(f"{detail} is not known as an evidence.")


@bot.command(name='ghost', aliases=["g"])
async def ghost(ctx, ghostname=None, detail=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    if not detail:
        with open("Discord_Bot/infos/ghosts.json", mode="r", encoding="utf-8") as f:
            ghosts = json.load(f)
        
        try:
            ghost = ghosts[ch.language]["Ghosts"][ghostname.title()]
        
            await ctx.send(f'{ghost["Description"]}')
            time.sleep(1)
        except:
                if ch.language == "de":
                    await ctx.send(f"{ghostname} ist kein bekannter Geist.")
                else:
                    await ctx.send(f'{ghostname} is not known at the Moment.')

    else:
        with open("Discord_Bot/infos/ghosts.json", mode="r", encoding="utf-8") as f:
            ghosts = json.load(f)
        
        try:
            
            if detail.lower() in ["evidence", "evidences", "evi"]:

                ghost = ghosts[ch.language]["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Evidence"][0]}, {ghost["Evidence"][1]}, {ghost["Evidence"][2]}')

            if detail.lower() in ["strength", "power"]:

                ghost = ghosts[ch.language]["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Strength"]}')
            
            if detail.lower() in ["weak", "weakness", "weaknesses"]:

                ghost = ghosts[ch.language]["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Weaknesses"]}')

        except:

                if ch.language == "de":
                    await ctx.send(f"{ghostname} ist kein bekannter Geist.")
                else:
                    await ctx.send(f'{ghostname} is not known at the Moment.')

def check_word(text):

    with open("Twitch_Bot/hidden/bad_words.txt", "r") as f:
        bad_words = f.readlines()

    for word in text.lower.split():
        if word in bad_words:
            return False

    else:
        return True

bot.run()
