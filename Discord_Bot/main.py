# bot.py
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

for file in os.listdir("Discord_Bot/cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)