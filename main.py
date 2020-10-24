from twitchio.ext import commands 
from NewChannel import * 
import time 
import os
import threading
from datetime import datetime
import requests as r
from dotenv import load_dotenv
load_dotenv()


# The Bot is getting created with the Tokens and IDs
bot = commands.Bot(
    irc_token=os.getenv('TMI_TOKEN'),
    api_token=os.getenv('CLIENT_ID'),
    nick=os.getenv('BOT_NICK'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=CHANNEL
)


# If a Channel was added and is not in the Settings-File atm, he will get added with Default-Parameters and his selected Language
with open("settings/channels.json", "r") as f:
    channels = json.load(f)
    
    # Checks ever Channel in the Joining-Queue
    for ch in CHANNEL:
        try:
            x = channels[ch]
        
        # Adding the Channel if it doesn't exist
        except KeyError:

            channels[ch.lower()] = {
                "language": ALL_CHANNELS[ch],
                "evidence" : [],
                "ghost_name" : "",
                "responds" : "",
                "whitelist" : False,
                "allowed" : [],
                "ignore" : [],
                "death_message": "COUNT",
                "death_count" : 0,
                "used" : 0
        }

# Saving the new Settings-File with all new Channels
with open("settings/channels.json", "w+") as f:
    json.dump(channels, f, indent=8)


# Just lets me know that the Bot is Ready
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

# Gets triggered every time someone sends a Message in a active Channel
@bot.event
async def event_message(message):

    # checks if i am the Person who wrote the Message
    channel = message.channel.name.lower()
    if message.author.name.lower() in ["mecke_dev"]:
        time.sleep(1)

    ch = NewChannel(channel)

    # Prints the Message in my Console if the Message contains my Name or is a Command
    if message.content.startswith("$") or " mecke " in message.content.lower() or " mecke_" in message.content.lower():
        print(f"{message.author.name} @ {message.channel.name} \n{message.content}\n")

    # starts checking if the Message was a valid Command
    await bot.handle_commands(message)


# sets the Name of the Ghost, because you will forget it for sure
@bot.command(name='channels')
async def channels(ctx):
    if ctx.author.name.lower() == "mecke_dev":

        all = "Bot-Users: "

        for x in CHANNEL:
            all += f"{x}, "

        await ctx.send(f"{all[:-2]}")


# sets the Name of the Ghost, because you will forget it for sure
@bot.command(name='name')
async def name_ghost(ctx, first_name=None, last_name=None, *, responds=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the User is allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        # if the Command was $name reset it will reset the Name
        if first_name == "reset":

            # opens the settings for the Channel
            with open("settings/channels.json", "r") as f:
                settings = json.load(f)
            
            # sets the Name and the Response to an empty String
            settings[channel]["ghost_name"] = ""
            settings[channel]["responds"] = ""
                
            # saves the settings
            with open("settings/channels.json", "w+") as f:
                json.dump(settings, f, indent=8)

            await ctx.send("Name cleared")

        # if somebody enters a name save the name
        elif first_name and last_name:

            # if the user dont enters a Value for the Response, just set a default Value depending on the channels Language
            if not responds:

                responds = ch.bot_text["name"]["not_responding"]

            # open the settings
            with open("settings/channels.json", "r") as f:
                settings = json.load(f)
            
            # set the name and the response
            settings[channel]["ghost_name"] = f"{first_name} {last_name}"
            settings[channel]["responds"] = f"{responds}"
                
            # save the settings
            with open("settings/channels.json", "w+") as f:
                json.dump(settings, f, indent=8)

            # let the user know that the name was set
            await ctx.send(f'{first_name} {last_name} {ch.bot_text["name"]["responds_to"]} {responds}')

        # if the user only enters $name just respond the saved Name and Response
        elif not first_name and not last_name and not responds:
            await ctx.send(f'{ch.ghost_name} {ch.bot_text["name"]["responds_to"]} {ch.responds}')


# if a user enters $join and his prefered Language, mark the Channel to join on next restart
@bot.command(name='join', aliases=["enter"])
async def join_me(ctx, language=None, name=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # if i am the User i am also allowed to add users by myself
    if ctx.author.name.lower() == "mecke_dev" and name:
        name = name.lower()
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        name = ctx.message.author.name.lower()

    # open the join-file
    with open("settings/join.json", "r") as f:
        joinable = json.load(f)

    # check if the Channel isn't there by now
    try: 
        x = joinable["Channels"][name]
        await ctx.send(f'{name} {ch.bot_text["join"]["already_joined"]}')

    # if the Channel is new, let the user know that the Bot will join the Channel
    except KeyError:

        if language:

            # check if the user want to set the Bot to english
            if language in ["en", "eng", "english", "uk", "us"]:
                joinable["Channels"][name] = "en"
                await ctx.send(f'{name} i\'m joining your Channel with english Settings')

            # or if he wants german
            elif language in ["de", "ger", "deutsch", "german"]:
                joinable["Channels"][name] = "de"                
                await ctx.send(f'{name} ich joine deinem Channel mit deutschen Einstellungen')

            # or if he wants spanish
            elif language in ["sp", "es", "espanol", "spanish"]:
                joinable["Channels"][name] = "es"                
                await ctx.send(f'{name} Me uniré a tu canal con la configuración español')

            # save the File again
            with open("settings/join.json", "w+") as f:
                json.dump(joinable, f, indent=8)

        # if the user didnt enter a Language or it wasn't recognized, give him a hint on how to use the Command
        else:
            await ctx.send(f'{name} {ch.bot_text["join"]["help"]}')


# If someone want the bot to leave his channel he can just enter $leave
@bot.command(name='leave', aliases=["part", "exit", "quit"])
async def leave_me(ctx, name=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # i can let the Bot leave channels whenever i want
    if ctx.author.name.lower() == "mecke_dev" and name:
        name = name.lower()
    else:
        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        name = ctx.message.author.name.lower()

    # open the join-file
    with open("settings/join.json", "r") as f:
        joinable = json.load(f)

    # check if the Bot is active on the channel and leave if it is the Case
    try: 
        x = joinable["Channels"][name]
        joinable["Channels"].pop(name)
        await ctx.send(f'{name}{ch.bot_text["leave"]["left"]}')

        with open("settings/join.json", "w+") as f:
            json.dump(joinable, f, indent=8)
        
    # if the Bot isn't active on the Channel, let the user know
    except KeyError:
        await ctx.send(f'{name}{ch.bot_text["leave"]["not_active"]}')


# Prints a list or a Link for the Commands
@bot.command(name='commands', aliases=["befehle", "cmd"])
async def commands(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # check if the user is allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:
        # Dev, please fix ####################################################################################
        await ctx.send(f"")


# responds a quick explenation for the Game
@bot.command(name='game', aliases=["phasmophobia"])
async def whats_game(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the user is allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        await ctx.send(ch.bot_text["game"]["description"])


# gives a quick introducion to the user
@bot.command(name='intro', aliases=["phasmobot"])
async def introduce(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if a user is allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        # responds depending on the Channel-Language
        await ctx.send(ch.bot_text["bot"]["intro"])


# Command to change the Language
# only Channel-owners can use this Command
@bot.command(name='language', aliases=["lang", "sprache", "idioma", "lingua"])
async def language(ctx, lang=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the owner of the channel is using the command
    if can_use(ch, ctx.author.name.lower()) and lang:

        language = ""
        
        # check if the user want to set the Bot to english
        if language in ["en", "eng", "english", "uk", "us"]:
            lang = "en"
            language = "English"

        # or if he wants german
        elif language in ["de", "ger", "deutsch", "german"]:
            lang = "de"
            language = "Deutsch"

        # or if he wants spanish
        elif language in ["sp", "es", "espanol", "spanish"]:
            lang = "es"
            language = "Espanol"

        # opens the channel-settings
        with open("settings/channels.json", "r") as f:
            settings = json.load(f)
        
        # sets everything back to the default-values
        settings[channel]["language"] = lang
            
        # saves the new settings
        with open("settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

        await ctx.send(f"set Language: {language}")

    else:

        # opens the channel-settings
        with open("settings/channels.json", "r") as f:
            settings = json.load(f)

        if settings[channel]["language"] == "en":
            language = "English"

        if settings[channel]["language"] == "de":
            language = "Deutsch"

        if settings[channel]["language"] == "es":
            language = "Espanol"

        await ctx.send(f"Channel-Language: {language}")


# Command to enable or disable the Whitelist
# only Channel-owners can use this Command
@bot.command(name='whitelist', aliases=["wl", "white", "black", "blacklist"])
async def whitelist(ctx, val):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the owner of the channel is using the command
    if ctx.author.name.lower() == ctx.channel.name.lower() or ctx.author.is_mod:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)

        if val in ["on", "start", "+", "1", "y", "yes", "j", "ja"]:

            # opens the channel-settings
            with open("settings/channels.json", "r") as f:
                settings = json.load(f)
            
            # sets everything back to the default-values
            settings[channel]["whitelist"] = True
                
            # saves the new settings
            with open("settings/channels.json", "w+") as f:
                json.dump(settings, f, indent=8)
                
            await ctx.send(ch.bot_text["whitelist"]["on"])

        elif val in ["off", "stop", "-", "0", "n", "no", "nein"]:

            # opens the channel-settings
            with open("settings/channels.json", "r") as f:
                settings = json.load(f)
            
            # sets everything back to the default-values
            settings[channel]["whitelist"] = False
                
            # saves the new settings
            with open("settings/channels.json", "w+") as f:
                json.dump(settings, f, indent=8)

            await ctx.send(ch.bot_text["whitelist"]["off"])
            
        elif val in ["show"]:
            await ctx.send(f"Whitlisted: {ch.allowed}")


        else:
            await ctx.send(f'{ctx.author.name} {ch.bot_text["whitelist"]["help"]}')


# Command to add People to the Allow-List, users on this list are allowed to use commands on the channel 
# if the whitelist is active and they are not on the Allow-list 
# only Channel-owners can use this Command
@bot.command(name='allow', aliases=["permit", "erlaube"])
async def allow(ctx, val, *, names=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the owner of the channel is using the command
    if ctx.author.name.lower() == ctx.channel.name.lower() or ctx.author.is_mod:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        failed = []

        # opens the channel-settings
        with open("settings/channels.json", "r") as f:
            settings = json.load(f)

        # if the command starts with $allow +
        # users get added to the allow-list
        if val == "+":

            if names:

                # adds every given user to the allow list
                names = names.split(" ")

                for name in names:
                    # adds a user to the allow list
                    try:
                        ch.allowed.append(name.lower())
                        time.sleep(1)
                        await ctx.send(f'{name} {ch.bot_text["allow"]["add"]}')

                    # collects usernames where errors occured
                    except:
                        failed.append(name.lower())

        # if the command starts with $allow -
        # users get removed from the allow-list
        elif val == "-":

            names = names.split(" ")

            for name in names:
                # removes every given user from the allow list
                try:
                    ch.allowed.remove(name.lower())
                    time.sleep(1)
                    await ctx.send(f'{name} {ch.bot_text["allow"]["remove"]}')
                except:
                    # collects usernames where errors occured
                    failed.append(name.lower())

        # sets the new allow-list to the active allow-list
        settings[channel]["allowed"] = ch.allowed

        # if an error happened
        if len(failed) > 0:
            # it will post a list of names where it failed
            await ctx.send(f'{ch.bot_text["allow"]["failed"]} {failed}')

        # saves the new list to the settings
        with open("settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

    # if someone is not allowed to allow someone, it will let him know
    else:
        await ctx.send(f'{ctx.author.name} {ch.bot_text["allow"]["forbidden"]}')


# Command to add People to the Ignore-List, users on this list are not able to use commands on the channel 
# only Channel-owners can use this Command
@bot.command(name='ignore', aliases=["ban", "verbiete"])
async def ignore(ctx, val, *, names=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the owner of the channel is using the command
    if ctx.author.name.lower() == ctx.channel.name.lower() or ctx.author.is_mod:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        failed = []

        # opens the channel-settings
        with open("settings/channels.json", "r") as f:
            settings = json.load(f)

        # if the command starts with $ignore +
        # users get added to the ignore-list
        if val == "+":

            if names:

                # adds every given user to the ignore list
                names = names.split(" ")

                for name in names:
                    # adds a user to the ignore list
                    try:
                        ch.ignore.append(name.lower())
                        await ctx.send(f'{name} {ch.bot_text["ignore"]["add"]}')


                    # collects usernames where errors occured
                    except:
                        failed.append(name.lower())

        # if the command starts with $ignore -
        # users get removed from the ignore-list
        elif val == "-":

            names = names.split(" ")

            for name in names:
                # removes every given user from the ignore list
                try:
                    ch.ignore.remove(name.lower())
                    await ctx.send(f'{name} {ch.bot_text["ignore"]["remove"]}')

                except:
                    # collects usernames where errors occured
                    failed.append(name.lower())

        # sets the new ignore-list to the active ignore-list
        settings[channel]["ignore"] = ch.ignore

        # if an error happened
        if len(failed) > 0:
            # it will post a list of names where it failed
            await ctx.send(f'{ch.bot_text["ignore"]["failed"]} {failed}')

        # saves the new list to the settings
        with open("settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

    # if someone is not allowed to ban/ignore someone, it will let him know
    else:
        await ctx.send(f'{ctx.author.name} {ch.bot_text["ignore"]["forbidden"]}')

# This Command is used to check or add evidences to the active ghost
@bot.command(name='evidence', aliases=["evi", "e", "beweis", "bew", "hinweis", "hinweise"])
async def evidence(ctx, *, detail=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # ignores the input if the user is not allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass

    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)

        # if the user only enters $evi it will respond the currently collected evidences and the possible Ghosts
        if not detail:
            await ctx.send(f'{ch.bot_text["evidence"]["evi"]} {ch.evidence}{ch.bot_text["evidence"]["possible"]} {ch.ghosts}')
            
        # if an evidence was given behind the $evi
        if detail:

            # if the user enters $evi reset the evidences and the Ghostname will get reset
            if detail.lower() in ["reset", "clear", "remove", "erase", "empty"]:
            
                # opens the channel-settings
                with open("settings/channels.json", "r") as f:
                    settings = json.load(f)
                
                # sets everything back to the default-values
                settings[channel]["evidence"] = []
                settings[channel]["ghost_name"] = ""
                settings[channel]["responds"] = ""
                    
                # saves the new settings
                with open("settings/channels.json", "w+") as f:
                    json.dump(settings, f, indent=8)

                # lets the user know that everything worked
                await ctx.send(ch.bot_text["evidence"]["reset"])
                
            else:
                # at this point the Bot tries to recognize the given evidence
                try:

                    # sets the evidences to the german names
                    if ch.language == "de":

                        evidences = {

                            "EMF Level 5"           : ["emf", "emf level 5", "level 5"],
                            "Geisterbox"            : ["spirit box", "spirit", "box", "talk", "spiritbox", "geisterbox"],
                            "Fingerabdrücke"        : ["fingerprints", "finger", "footprints", "prints", "abdruck", "abdrücke", "fingerabdrücke"],
                            "Geisterbuch"           : ["ghost writing", "ghostwriting","writing", "book", "write", "wrote", "written", "writer", "ghostwriter", "ghost writer", "buch", "geisterbuch"],
                            "Gefriertemperaturen"   : ["frost", "eis", "gefrier", "freezing", "freezing temperatures", "frozen", "cold", "ice", "temps", "temperature", "freeze", "temperatur", "kalt", "kälte", "gefriertemperatur", "temperaturas bajo cero", "temperaturas"],
                            "Geisterorb"            : ["orb", "ghost orb", "ghostorb", "orbs", "ghostorbs", "ghost orbs", "kugel", "geisterkugel", "geister kugel"]

                        }

                    elif ch.language == "en":

                        evidences = {

                            "EMF Level 5"           : ["emf", "emf level 5", "level 5"],
                            "Spirit Box"            : ["spirit box", "spirit", "box", "talk", "spiritbox", "geisterbox"],
                            "Fingerprints"          : ["fingerprints", "finger", "footprints", "prints", "abdruck", "abdrücke", "fingerabdrücke"],
                            "Ghost Writing"         : ["ghost writing", "ghostwriting","writing", "book", "write", "wrote", "written", "writer", "ghostwriter", "ghost writer", "buch", "geisterbuch"],
                            "Freezing Temperatures" : ["frost", "eis", "gefrier", "freezing", "freezing temperatures", "frozen", "cold", "ice", "temps", "temperature", "freeze", "temperatur", "kalt", "kälte", "gefriertemperatur", "temperaturas bajo cero", "temperaturas"],
                            "Ghost Orb"             : ["orb", "ghost orb", "ghostorb", "orbs", "ghostorbs", "ghost orbs", "kugel", "geisterkugel", "geister kugel"]

                        }

                    elif ch.language == "es":

                        evidences = {

                            "EMF Nivel 5"           : ["emf", "emf level 5", "level 5", "emf nivel 5", "emf 5", "emf5"],
                            "Spirit Box"            : ["spirit box", "spirit", "box", "talk", "spiritbox", "geisterbox"],
                            "Huellas Dactilares"    : ["fingerprints", "finger", "footprints", "prints", "abdruck", "abdrücke", "fingerabdrücke", "huellas dactilares", "huellas", "dactilares"],
                            "Escritura Fantasma"    : ["ghost writing", "ghostwriting","writing", "book", "write", "wrote", "written", "writer", "ghostwriter", "ghost writer", "buch", "geisterbuch", "escritura fantasma", "escritura", "fantasma"],
                            "Temperaturas bajo cero": ["frost", "eis", "gefrier", "freezing", "freezing temperatures", "frozen", "cold", "ice", "temps", "temperature", "freeze", "temperatur", "kalt", "kälte", "gefriertemperatur", "temperaturas bajo cero", "temperaturas"],
                            "Orbes"                 : ["orb", "ghost orb", "ghostorb", "orbs", "ghostorbs", "ghost orbs", "kugel", "geisterkugel", "geister kugel", "orbes"]

                        }

                    # sets some default Variables
                    found = False
                    real = False
                    evid = False

                    # the bot tries to understand which evidence should be added
                    for evi in evidences:
                        # if the given evidence is found
                        if detail.lower() in evidences[evi]:
                            # the bot checks if the evidence is already added to the current ghost
                            if evi not in ch.evidence:
                                
                                # opens the settings
                                with open("settings/channels.json", "r") as f:
                                    settings = json.load(f)
                    
                                # adds the evidence to the Ghost
                                settings[channel]["evidence"].append(evi)
                        
                                # saves the settings
                                with open("settings/channels.json", "w+") as f:
                                    json.dump(settings, f, indent=8)

                                # sets the real name of the evidence like "Freezing Temperatures" if the evidence was not already set
                                real = evi
                                found = True
                            else:
                                
                                # sets the real name of the evidence like "Freezing Temperatures" if the Evidence was already added
                                evid = evi
                                found = True


                    channel = ctx.channel.name.lower()
                    ch = NewChannel(channel)
                        
                    # lets the user know if the evidence was added or not
                    if found and real:
                        await ctx.send(f'{real} {ch.bot_text["evidence"]["added"]} {ch.ghosts}')
                    elif found and evid:
                        await ctx.send(f'{evid} {ch.bot_text["evidence"]["already_added"]} {ch.ghosts}')

                    # gets triggerd if the bot didn't understand the given evidence like: $evi fdfbdsg
                    else:
                        raise NameError("not found")

                # lets the user know that the evidence didnt got recognized
                except NameError:
                    await ctx.send(f'{detail} {ch.bot_text["evidence"]["not_known"]}')


# prints a short information about me
@bot.command(name='creator', aliases=["dev", "author", "entwickler", "developer"])
async def developer(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # checks if the user is allowed to use the Command
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:
        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        await ctx.send(ch.bot_text["dev"])


# prints a link to my Steam-Group for the Bot
@bot.command(name='steam')
async def steam_link(ctx):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:
        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        await ctx.send(ch.bot_text["steam"])


# This is our own Death-Counter
@bot.command(name='death', aliases=["dead", "down", "tot", "died"])
async def death(ctx, val=None, *, value=None):
    
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # opens the settings
    with open("settings/channels.json", "r") as f:
        settings = json.load(f)

    try:
        value = int(value)
        is_int = True
    except:
        is_int = False

    if val:

        if val == "+" and not value:
            
            # increases the Counter by 1 
            settings[channel]["death_count"] += 1

        elif val == "-" and not value:
            
            # decreases the Counter by 1
            settings[channel]["death_count"] -= 1

        elif val == "set" and "COUNT" in str(value) and is_owner(ctx):

            # sets the Death-Message to the given String and replacing the COUNT with the Number everytim e it gets called
            settings[channel]["death_message"] = value

        elif val == "set" and is_int and is_owner(ctx):

            # sets the Counter to the given Number
            settings[channel]["death_count"] = value

        # saves the settings
        with open("settings/channels.json", "w+") as f:
            json.dump(settings, f, indent=8)

    #  opens the settings
    with open("settings/channels.json", "r") as f:
        settings = json.load(f)

    await ctx.send(settings[channel]["death_message"].replace("COUNT", str(settings[channel]["death_count"])))


# This Command is user to post a specific information about a specific Ghost
@bot.command(name='item', aliases=["tool"])
async def item(ctx, *, item):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    tool = ""

    # ignores the Command if the user isn't allowed to use it
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)
        
        # the bot tries to understand what ghost was meant
        try:
            tool = ch.texts["Items"][item.title()]
        
            await ctx.send(f'{tool["Description"][:-1]}: {str(tool["Price"])}$')
            time.sleep(1)

        # if the bot doesn't find the specific ghost, he will let the user know
        except:
            await ctx.send(f'{tool} {ch.bot_text["tool"]["unknown"]}')


# This Command is user to post a specific information about a specific Ghost
@bot.command(name='ghost', aliases=["g", "geist", "ghosts", "geister"])
async def ghost(ctx, ghostname=None, detail=None):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # ignores the Command if the user isn't allowed to use it
    if not can_use(ch, ctx.author.name.lower()):
        pass
    else:

        add_point(ctx.author.name.lower(),ctx.message.content, channel)


        if ghostname:

            if ch.language == "de":

                ghosts = {

                    "Spirit" : ["spirit", "sprit", "spirt"],
                    "Gespenst" : ["gespenst", "geist", "wraith", "ghost"],
                    "Phantom" : ["phantom", "fantom", "fanthom", "phanthom"],
                    "Poltergeist" : ["poltergeist"],
                    "Banshee" : ["banshee", "banshe", "banschi", "bansche"],
                    "Dschinn" : ["dschin", "dschinn", "djinn", "jinn", "jin", "dshin", "dshinn"],
                    "Mare" : ["mare", "nightmare", "mär"],
                    "Revenant" : ["revenant", "rev", "ravenant", "ravenent"],
                    "Shade" : ["shade", "schade", "shadow", "schatten", "shede"],
                    "Dämon" : ["demon", "dämon", "dimon"],
                    "Yurei" : ["yurei", "jurei", "jurai", "yurai"],
                    "Oni" : ["oni"]

                }

            elif ch.language == "en":

                ghosts = {

                    "Spirit" : ["spirit", "sprit", "spirt"],
                    "Wraith" : ["gespenst", "geist", "wraith", "ghost"],
                    "Phantom" : ["phantom", "fantom", "fanthom", "phanthom"],
                    "Poltergeist" : ["poltergeist"],
                    "Banshee" : ["banshee", "banshe", "banschi", "bansche"],
                    "Jinn" : ["dschin", "dschinn", "djinn", "jinn", "jin", "dshin", "dshinn"],
                    "Mare" : ["mare", "nightmare", "mär"],
                    "Revenant" : ["revenant", "rev", "ravenant", "ravenent"],
                    "Shade" : ["shade", "schade", "shadow", "schatten", "shede"],
                    "Demon" : ["demon", "dämon", "dimon"],
                    "Yurei" : ["yurei", "jurei", "jurai", "yurai"],
                    "Oni" : ["oni"]

                }

            elif ch.language == "es":

                ghosts = {

                    "Espíritu" : ["spirit", "sprit", "spirt", "espíritu"],
                    "Espectro" : ["gespenst", "geist", "wraith", "ghost", "espectro"],
                    "Ente" : ["phantom", "fantom", "fanthom", "phanthom", "ente"],
                    "Poltergeist" : ["poltergeist"],
                    "Banshee" : ["banshee", "banshe", "banschi", "bansche"],
                    "Jinn" : ["dschin", "dschinn", "djinn", "jinn", "jin", "dshin", "dshinn"],
                    "Pesadilla" : ["mare", "nightmare", "mär", "pesadilla"],
                    "Revenant" : ["revenant", "rev", "ravenant", "ravenent"],
                    "Sombra" : ["shade", "schade", "shadow", "schatten", "shede", "sombra"],
                    "Demonio" : ["demon", "dämon", "dimon", "demonio"],
                    "Yurei" : ["yurei", "jurei", "jurai", "yurai"],
                    "Oni" : ["oni"]

                }

            for ghost in ghosts:
                if ghostname.lower() in ghosts[ghost]:
                    ghostname = ghost


        # if the user only enters $g ghostname the bot responds with the description of the Ghost
        if not detail:
            
            # the bot tries to understand what ghost was meant
            try:
                ghost = ch.texts["Ghosts"][ghostname.title()]
            
                await ctx.send(f'{ghost["Description"]}')
                time.sleep(1)

            # if the bot doesn't find the specific ghost, he will let the user know
            except:
                await ctx.send(f'{ghostname} {ch.bot_text["ghost"]["unknown_ghost"]}')

        # if the user enters a specific detail about the Ghost
        else:
            
            # the bot checks if he can find the given detail
            try:
                
                # tries to recognize the given detail
                if detail.lower() in ["evidence", "evidences", "evi", "e", "beweise", "hinweis", "beweis", "hinweise"]:

                    ghost = ch.texts["Ghosts"][ghostname.title()]
                    await ctx.send(f'{ghost["Evidence"][0]}, {ghost["Evidence"][1]}, {ghost["Evidence"][2]}')

                if detail.lower() in ["strength", "power", "stärke", "macht", "ability"]:

                    ghost = ch.texts["Ghosts"][ghostname.title()]
                    await ctx.send(f'{ghost["Strength"]}')
                
                if detail.lower() in ["weak", "weakness", "weaknesses", "schwäche", "schwach"]:

                    ghost = ch.texts["Ghosts"][ghostname.title()]
                    await ctx.send(f'{ghost["Weaknesses"]}')

            # if the bot doesn't understand the given detail, he will let the user know
            except:
                await ctx.send(f'{detail} {ch.bot_text["ghost"]["unknown_detail"]}')


# Function to check for the Channelowner
def is_owner(ctx):

    if ctx.author.name.lower() == ctx.channel.name.lower() or ctx.author.name.lower() == "mecke_dev":
        return True
    else:
        return False


# this is a check if a given user is allowed to use a command on the specific channel
def can_use(ch, name):

    # checks if the user is on the ignore-list
    if name in ch.ignore:
        return False

    # checks if the whitelist is active and if so, checks if the user is allowed to use the Command
    if ch.whitelist and name in ch.allowed:
        return True
    
    # checks if the whitlist isn't active and if the user is not on the ignore-list
    if not ch.whitelist and name not in ch.ignore:
        return True


# not implemented, but to check if a user is using a bad word
def check_word(text):

    # opens the badwords-list
    with open("hidden/bad_words.txt", "r") as f:
        bad_words = f.readlines()

# checks every word in the meesage if it is on the badword-list
    for word in text.lower.split():
        if word in bad_words:
            return False

    else:
        return True

def add_point(user, message, channel):

    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")

    # opens the point-list
    with open("settings/points.json", "r") as f:
        points = json.load(f)
            
    try:
        # adds a point to the user
        points[user] += 1
    except KeyError:
        points[user] = 1
        
    # saves the new point-list
    with open("settings/points.json", "w+") as f:
        json.dump(points, f, indent=8)

    # opens the userfile
    filename = f"users/{user}.txt"

    if os.path.exists(filename):
        userlines = open(filename, "a+")
        userlines.write(f"{message} ||| {time} ||| {channel}\n")
        userlines.close()
    else:
        f = open(filename, "w")
        f.write(f"{message} ||| {time} ||| {channel}\n")
        f.close()
        

# this starts the bot
bot.run()
