import random
import asyncio
import json
import discord
from discord.ext import commands

class Ghosts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Ghosts loaded.")

    @commands.command(name='ghost', help='Shows information about a specific Ghost.')
    async def ghost(self, ctx, ghostname=None):
        if ghostname:
            async with ctx.typing():

                try:
                    
                    with open("infos/ghosts.json", mode="r", encoding="utf-8") as f:
                        ghosts = json.load(f)

                    ghost = ghosts["Ghosts"][ghostname.title()]
                    evi = 0

                    embed=discord.Embed(
                        title=ghostname.title(), 
                        description=ghost["Description"], 
                        color=0xc80e0e
                    )

                    embed.set_author(
                        name="Phasmophobia", 
                        url="https://store.steampowered.com/app/739630/Phasmophobia/", 
                        icon_url="https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/73/73974d6799d163b296b79422270213abcc68a6d5_full.jpg"
                    )

                    embed.add_field(
                        name="Unique Strengths:", 
                        value=ghost["Strength"], 
                        inline=False
                    )

                    embed.add_field(
                        name="Weaknesses:", 
                        value=ghost["Weaknesses"], 
                        inline=False
                    )

                    for evidence in ghost["Evidence"]:

                        embed.add_field(
                            name=f"{evi+1}", 
                            value=ghost["Evidence"][evi], 
                            inline=True
                        )
                        
                        evi += 1

                    embed.set_footer(text="powered by MeckeDev")

                    await asyncio.sleep(0.5)

                except:

                    embed=discord.Embed(title=ghostname.title(), description="Does not exist!", color=0xc80e0e)
                    embed.set_footer(text="powered by MeckeDev")

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ghosts(bot))