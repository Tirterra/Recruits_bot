#modules import
from discord.ext import commands
import discord
import time
import json
import os

#commands import
import commands.calcskills.calcskills as calcskills_
import commands.stats.stats as stats_
import commands.leaderboard.leaderboard as leaderboard_
import commands.calccata.calccata as calccata_
import commands.catacombs.catacombs as catacombs_
import commands.link.link as link_
import commands.weight.weight as weight_

#data import
from update_data.update_leaderboard import update_data


DIR_PATH = os.path.dirname(__file__)
with open(DIR_PATH+r"\ressources\credentials.json", "r+") as file :
    TOKEN = json.load(file)["TOKEN"]

client = commands.Bot(command_prefix="-")


@client.event
async def on_ready():

    print("I am ready")


@client.command()
async def ping(ctx):

    embed = discord.Embed(title="**Pong**", description=f"You have {round(client.latency*1000)} ms latency.")
    await ctx.send(embed=embed)


@client.command()
async def calcskills(ctx, *, arg):

    embed = calcskills_.calcskills(arg)
    await ctx.send(embed=embed)


@client.command()
async def stats(ctx, arg=None):

    embed = stats_.stats(ctx, arg)
    await ctx.send(embed=embed)


@client.command(aliases=["calccatacombs"])
async def calccata(ctx, *, arg):

    embed = calccata_.calccata(arg)
    await ctx.send(embed=embed)


@client.command(aliases=["cata"])
async def catacombs(ctx, arg=None):

    embed = catacombs_.catacombs(ctx, arg)
    await ctx.send(embed=embed)


@client.command()
async def link(ctx, arg):

    embed = link_.link(ctx, arg)
    await ctx.send(embed=embed)


@client.command(aliases=["lb"])
async def leaderboard(ctx, *, arg="weight"):

    embed = leaderboard_.leaderboard(ctx, arg)
    await ctx.send(embed=embed)


@client.command(aliases=["we"])
async def weight(ctx, arg=None):

    embed = weight_.weight(ctx, arg)
    await ctx.send(embed=embed)


def update():

    start = time.time()
    print("Started Update")
    update_data()
    end = time.time()
    print(f"data updated in {end - start}")

# Update the leaderboard on start of program then run the bot. (The server where the bot is hosted restarts every 24h.)
update()
client.run(TOKEN)   
