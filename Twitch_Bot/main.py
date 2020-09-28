from twitchio.ext import commands
from NewChannel import *
from play import *
from games.csgo import *
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
                "blacklist": [
                        "streamlabs",
                        "anotherttvviewer",
                        "aten",
                        "lurxx",
                        "1fps",
                        "communityshowcase",
                        "nightbot",
                        "thiccur",
                        "commanderroot",
                        "bloodlustr",
                        "thecommandergroot"
                ],
                "language": "en",
                "discord": "",
                "prefix": "$",
                "points": "Punkte",
                "point_amount": 10,
                "point_period": 10,
                "point_get_period": 0,
                "evidence" : [],
                "commands_link": ""
        }

with open("Twitch_Bot/settings/channels.json", "w+") as f:
    json.dump(channels, f)

with open("Twitch_Bot/points/points.json", "r") as f:
    
    points = json.load(f)
    for ch in CHANNEL:
        try:
            x = points[ch]
        except KeyError:

            points[ch.lower()] = {}

with open("Twitch_Bot/points/points.json", "w+") as f:
    json.dump(points, f)

# Dieses Event wird getriggert wenn der Bot bereit ist
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

    # Hier starten wir das Punktesystem
    # um den Zuschauern im festgelegten Intervall
    # die festgelegte Anzahl an Punkten zu geben
    # kann in der channels.json unter:
    #                 "point_amount": 10,
    #                 "point_period": 10,
    # editiert werden, wenn der Bot nicht läuft

    # Oder im Chat direkt mit   $set point_amount ZAHL
    #                oder mit   $set point_period ZAHL
    # festgelegt werden

    await give_points()


# Das ist das eigene Punktesystem des Bots welches
# jeden der sich aktuell im Channel befindet mit Punkten belohnt
@bot.event
async def give_points():

    # Hier sorgen wir dafür, dass das System durchgehend läuft solange der Bot gestartet ist
    while True:

        # Hier generieren wir aus dem Channel von channels.json eine Klasse
        for chan in CHANNEL:
            channel = chan
            ch = NewChannel(channel)

            # Sucht die Namen aller aktiven User im Channel
            try:
                chatters = await bot.get_chatters(channel)

                # Überprüft jede Sekunde ob die User Punkte bekommen oder nicht
                if ch.points_get_period < ch.points_period:
                    ch.set("point_get_period", ch.points_get_period + 1)

                # setzt den Counter für die Punkteverteilung auf 0 zurück
                # und verteilt die Punkte an die User
                else:
                    ch.add_points(chatters[1], ch.points_amount)
                    ch.set("point_get_period", 0)

            # fängt Fehler ab und überspringt eine Sekunde sollte etwas schieflaufen
            except:
                print("ERROR")
                pass

        # Das System wartet eine Sekunde
        # und startet einen neuen Durchlauf zum Punkte verteilen
        time.sleep(1)


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
    print(message.raw_data)

    # Überprüft ob eine Nachricht mit dem Symbol für Commands beginnt
    # und ersetzt das Symbol mit einem !
    # das gewünschte Symbol welches den Bot triggern soll kann auch festgelegt werden

    # Option 1: im Chat → $set prefix SYMBOL

    # Option 2:
    # "prefix": "$",
    # ↑ in der channels.json abändern, wenn der Bot nicht läuft

    if message.content.startswith(ch.prefix):
        message.content.replace(ch.prefix, "!")

    # Schreibt den Usernamen und die Nachricht in die Konsole
    print(f"{message.author.name.rjust(30, ' ')}: \t{message.content}")

    # Überprüft ob sich der User in der Blacklist befindet
    # User in der Blacklist bekommen keine Punkte und können keine Commands nutzen
    if message.author.name not in ch.blacklist:

        # Hier überprüft der Bot ob das Command exisistiert und führt es aus
        await bot.handle_commands(message)


# Mit diesem Command kann man sich das Scoreboard im Chat anzeigen lassen 
# z.B.: $top 3
# ↑ zeigt die 3 Leute mit den meisten Punkten

@bot.command(name='top', aliases=["bestenliste", "scoreboard"])
async def score(ctx, count=3):

    # Klasse erstellen und so weiter
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # Hier werden die User aus points/points.json sortiert um die Top 10 in eine Liste zu schreiben 
    sort_orders = sorted(ch.channel_points.items(), key=lambda b: b[1], reverse=True)

    # Überprüft ob der User bei dem Command eine Zahl zwischen 1 und 10 eingegeben hat
    if count in range(0, 11):

        # Sollte der User $top 10 eingeben, aber es existieren erst 5 User die Punkte haben 
        # wandelt der Bot das Command automatisch auf $top 5 um
        if count > len(sort_orders):
            count = len(sort_orders)

        # Hier generiert der Bot den Text den er am Ende im Chat posted 
        # nach dem Muster:
        # Mecke_Dev : 150, Chris_Live : 120, Mecke_Dev : 100
        top = ""
        for x in range(0, count):
            top += f"{sort_orders[x][0]} : {sort_orders[x][1]}, "

        # Hier wird die generierte Bestenliste im Chat gepostet
        await ctx.send(top[:-2])

    # Sollte der User eine Zahl über 10 eingeben postet der Bot eine Fehlermeldung
    else:
        await ctx.send(f"{ctx.author.name} bitte nur zahlen zwischen 1 - 10 eingeben")


# Mit dem Command kann man sich diverse Einstellungen im Chat posten lassen
@bot.command(name='show')
async def commands(ctx, setting):

    # Channel zu Klasse
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # $show admin ← spuckt eine Liste der im Bot eingestellten Admins aus
    # Admins können mit $add admins USERNAME ← hinzugefügt werden
    # oder bei ausgeschaltetem Bot in der channels.json unter:

    # "admins": [
    #            "Mecke_Dev"
    #  ],

    # angepasst werden

    if setting.lower() in ["admin", "admins"]:

        admins = ", ".join(ch.admins)

        # Postet die Liste der Admins im Chat nach dem Muster:
        # Admins: Mecke_Dev

        await ctx.send(f"Admins: {admins}")

    # Das selbe Prinzip wie bei $show admins, nur eben für Moderatoren
    if setting.lower() in ["mods", "moderator", "moderators"]:

        mods = ", ".join(ch.moderators)

        await ctx.send(f"Mods: {mods}")

    # $show points ← zeigt die aktuellen Einstellungen des Punktesystems im Chat
    # wie bereits unter "event_ready()" erklärt kann die Anzahl der Punkte und der Intervall angepasst werden
    # auch der Name der Punkte lässt sich ändern in der channels.json oder mit:
    # $set points Dollar

    if setting.lower() in ["points"]:
        await ctx.send(f"Viewer getting {ch.points_amount} {ch.points} every {ch.points_period} seconds.")


# mit $commands ← kann man einen festgelegten Link zu den Commands im Chat ausgeben lassen
# Der Link lässt sich in der channels.json unter:
#           "commands_link": "Kein Link festgelegt"
# festlegen

@bot.command(name='commands')
async def commands(ctx):

    # Channel zu Klasse
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # postet den festgelegten Link-text im Chat
    await ctx.send(f"{ch.commands_link}")


# Dieses Command ist zur Moderation des Punktesystems
# Hier kann man Usern Punkte geben oder nehmen
@bot.command(name='punkte', aliases=["points"])
async def set_points(ctx, com="me", name="", amount=0):

    # Channel zu Klasse
    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    # $punkte
    # ↑ zeigt deine aktuellen Punkte im Chat
    if com == "me":
        await ctx.send(f"{ctx.author.name} besitzt {ch.channel_points[ctx.author.name.lower()]} {ch.points}")

    # Diese Commands können nur von Admins oder Mods genutzt werden
    if ch.is_mod(ctx.author.name) or ch.is_admin(ctx.author.name):

        # $punkte add Mecke_Dev 1000
        # ↑ würde Mecke_Dev 1000 Punkte geben
        if com == "add":
            ch.channel_points[name.lower()] += int(amount)
            ch.save_points()
            await ctx.send(f"{ctx.author.name} gibt {name} {amount} {ch.points}")

        # $punkte rm Mecke_Dev 1000
        # ↑ entfernt 1000 Punkte von Mecke_Dev
        elif com in ["remove", "rm"]:
            ch.channel_points[name.lower()] -= int(amount)
            ch.save_points()
            await ctx.send(f"{ctx.author.name} entfernt {amount} {ch.points} von {name}")

        # $punkte set Mecke_Dev 1000
        # ↑ setzt die Punkte von Mecke_Dev auf genau 1000
        elif com == "set":
            ch.channel_points[name.lower()] = int(amount)
            ch.save_points()
            await ctx.send(f"{ctx.author.name} setzt die {ch.points} von {name} auf {amount}")

    # Dieses Command kann nur von eingetragenen Admins genutzt werden
    if ch.is_admin(ctx.author.name):

        # $punkte reset
        # ↑ setzt alle Pukte des Channels wieder zurück auf 50
        if com == "reset":

            for user in ch.channel_points:

                # setzt die Punkte für jeden auf 50 zurück
                # und User auf der Blacklist werden auf -1 gesetzt
                if user not in ch.blacklist:
                    ch.channel_points[user.lower()] = 50
                else:
                    ch.channel_points[user.lower()] = -1

            ch.save_points()

            # Postet im Chat dass das Punktesystem resettet wurde
            await ctx.send(f"{ch.points} wurden zurückgesetzt")


@bot.command(name='set')
async def setting_set(ctx, setting, *, value):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    setting = setting.lower()

    if ch.is_mod(ctx.author.name) or ch.is_admin(ctx.author.name):

        if setting in ["prefix", "points", "game", "title", "discord", "commands_link", "point_amount", "point_period"]:
            ch.set(setting, value)

        if setting in ["language"] and value in ["de", "en"]:
            ch.set(setting, value)


@bot.command(name='add')
async def add(ctx, setting, value):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    setting = setting.lower()

    if setting in ["admins", "moderators"] and ch.is_admin(ctx.author.name):

        ch.save_settings(setting, value)

    elif setting in ["blacklist"] and (ch.is_mod(ctx.author.name) or ch.is_admin(ctx.author.name)):

        ch.save_settings(setting, value)


@bot.command(name='remove', aliases=["rm"])
async def remove(ctx, setting, value):

    channel = ctx.channel.name.lower()
    ch = NewChannel(channel)

    setting = setting.lower()

    if (ch.is_mod(ctx.author.name) or ch.is_admin(ctx.author.name)) and setting == "blacklist":
        ch.remove_setting(setting, value)

    elif ch.is_admin(ctx.author.name):

        if setting in ["admins", "moderators", "blacklist"]:
            value = value.lower()
            ch.remove_setting(setting, value)

@bot.command(name='evidence', aliases=["evi"])
async def ghost(ctx, ghostname=None, detail=None):
    if ghostname == "Beta":
        pass
    else:
        pass

@bot.command(name='ghost', aliases=["g"])
async def ghost(ctx, ghostname=None, detail=None):

    if not detail:
        with open("Discord_Bot/infos/ghosts.json", mode="r", encoding="utf-8") as f:
            ghosts = json.load(f)
        
        try:
            ghost = ghosts["Ghosts"][ghostname.title()]
        
            await ctx.send(f'{ghost["Description"]}')
            time.sleep(1)
        except:

            await ctx.send(f'{ghostname} is not known at the Moment')

    else:
        with open("Discord_Bot/infos/ghosts.json", mode="r", encoding="utf-8") as f:
            ghosts = json.load(f)
        
        try:
            
            if detail.lower() in ["evidence", "evidences", "evi"]:

                ghost = ghosts["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Evidence"][0]}, {ghost["Evidence"][1]}, {ghost["Evidence"][2]}')

            if detail.lower() in ["strength", "power"]:

                ghost = ghosts["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Strength"]}')
            
            if detail.lower() in ["weak", "weakness", "weaknesses"]:

                ghost = ghosts["Ghosts"][ghostname.title()]
                await ctx.send(f'{ghost["Weaknesses"]}')


        except:

            await ctx.send(f'{ghostname} is not known at the Moment')



def check_word(text):

    with open("Twitch_Bot/hidden/bad_words.txt", "r") as f:
        bad_words = f.readlines()

    for word in text.lower.split():
        if word in bad_words:
            return False

    else:
        return True

    

b1 = threading.Thread(target=bot.run, args=[])
b1.start()