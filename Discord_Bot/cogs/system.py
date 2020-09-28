import os
import asyncio
import discord
from discord.ext import commands

class SystemCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("SystemCommands loaded.")

    @commands.command(name='status', help="changes the Status of the Bot")
    @commands.has_role('Admin')
    async def status(self, ctx, status="online"):
        
        if status == "online":
            await self.bot.change_presence(status=discord.Status.online)

        if status == "offline":
            await self.bot.change_presence(status=discord.Status.offline)

        if status == "dnd":
            await self.bot.change_presence(status=discord.Status.do_not_disturb)

        if status == "idle":
            await self.bot.change_presence(status=discord.Status.idle)

    @commands.command(name='reload', help="reload all/specific Cogs")
    @commands.has_role('Admin')
    async def reload_cogs(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():

                embed = discord.Embed(
                    title="Reloading all Cogs!",
                    color = 0x808080,
                    timestamp = ctx.message.created_at
                )

                for ext in os.listdir("./cogs/"):

                    if ext.endswith(".py") and not ext.startswith("_"):

                        try:
                            
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")

                            embed.add_field(
                                name = f"Reloaded: {ext}",
                                value = '\uFEFF',
                                inline=True
                            )

                        except Exception as e:
                            embed.add_field(
                                name = f"Failed to reload: `{ext}`",
                                value=e,
                                inline=True
                            )

                        await asyncio.sleep(0.5)
                
                await ctx.send(embed=embed)

        else:

            async with ctx.typing():

                embed = discord.Embed(
                    title="Reloading all Cogs!",
                    color = 0x808080,
                    timestamp = ctx.message.created_at
                )

                try:

                    self.bot.unload_extension(f"cogs.{cog}")
                    self.bot.load_extension(f"cogs.{cog}")

                    embed.add_field(
                        name = f"Reloaded: {cog}.py",
                        value = '\uFEFF',
                        inline=True
                    )

                except Exception as e:
                    embed.add_field(
                        name = f"Failed to reload: `{cog}.py`",
                        value=e,
                        inline=True
                    )

                await asyncio.sleep(0.5)

            await ctx.send(embed=embed)


    @commands.command(name='unload', help="unload a specific Cog")
    @commands.has_role('Admin')
    async def unload_cogs(self, ctx, cog=None):
        if cog:
            async with ctx.typing():

                embed = discord.Embed(
                    title=f"Unloading {cog}!",
                    color = 0x808080,
                    timestamp = ctx.message.created_at
                )

                try:

                    self.bot.unload_extension(f"cogs.{cog}")

                    embed.add_field(
                        name = f"Unloaded: {cog}.py",
                        value = '\uFEFF',
                        inline=True
                    )

                except Exception as e:
                    embed.add_field(
                        name = f"Failed to unload: `{cog}.py`",
                        value=e,
                        inline=True
                    )

                await asyncio.sleep(0.5)

            await ctx.send(embed=embed)

    @commands.command(name='load', help="load a Cog")
    @commands.has_role('Admin')
    async def load_cogs(self, ctx, cog=None):
        if cog:
            async with ctx.typing():

                embed = discord.Embed(
                    title=f"Loading {cog}!",
                    color = 0x808080,
                    timestamp = ctx.message.created_at
                )

                try:

                    self.bot.load_extension(f"cogs.{cog}")

                    embed.add_field(
                        name = f"Loaded: {cog}.py",
                        value = '\uFEFF',
                        inline=True
                    )

                except Exception as e:
                    embed.add_field(
                        name = f"Failed to load: `{cog}.py`",
                        value=e,
                        inline=True
                    )

                await asyncio.sleep(0.5)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SystemCommands(bot))