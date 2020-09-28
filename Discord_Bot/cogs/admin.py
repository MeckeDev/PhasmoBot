import discord
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("AdminCommands loaded.")

    @commands.command(name='create', help="Create a new Channel")
    @commands.has_role('Admin')
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

def setup(bot):
    bot.add_cog(AdminCommands(bot))