from requests.models import HTTPError
from get_leaderboard import get_booked_leaderboard, get_leaderboard
from update_leaderboard import get_uuid
from discord import embeds, player
from get_lvl import get_skill_lvl, get_slayer_lvl, get_dungeon_lvl, get_skills, get_slayers, get_dungeons
from get_weight import get_dungeons_weight, get_skills_weight, get_slayers_weight, get_weight
from get_played_profile import get_current
from discord.ext import commands
from bot_embeds import get_guild_average, get_rank, leaderboard_embed, link_embed, weight_embed
from math import ceil, floor
import requests
import discord
import math
import json
from get_skin import get_avatar
import os

TOKEN = "YOUR TOKEN"

client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
    print("I am ready")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong\n {round(client.latency*1000)} ms.")

@client.command()
async def link(ctx, arg):

    DIR_PATH = os.path.dirname(__file__)

    try:

        url = f"http://api.mojang.com/users/profiles/minecraft/{arg}"
        res = requests.get(url)

        if res.status_code != 200:
            raise HTTPError

        embed = link_embed(ctx.message.author, arg)

    except :
        await ctx.send("Invalid username !")
        return

    with open(DIR_PATH+r"\linked.json", "r") as file:
        linked = json.load(file)

    linked.update({str(ctx.message.author) : arg})

    with open(DIR_PATH+r"\linked.json", "w+") as file:
        json.dump(linked, file, indent=4)
        await ctx.send(embed=embed)


@client.command(aliases=["lb"])
async def leaderboard(ctx, *, arg):

    DIR_PATH = os.path.dirname(__file__)

    page = arg[-2:].replace(" ", "")
    with open(DIR_PATH+r"\linked.json", "r") as file:
        linked = json.load(file)
    
    try:
        page = int(page)
        arg = arg.replace(f" {page}", "")
    except:
        page = 1

    leaderboard, arg = get_leaderboard(arg)

    if isinstance(leaderboard, discord.embeds.Embed):
        await ctx.send(embed=leaderboard)
        return

    try:
        target = linked[str(ctx.message.author)]
    except KeyError:
        await ctx.send("Link yourself first !")
        return

    book = get_booked_leaderboard(leaderboard)
    average = get_guild_average(leaderboard)
    rank = get_rank(leaderboard, target)
    embed = leaderboard_embed(book, page, arg, average, rank)

    await ctx.send(embed=embed)


@client.command(aliases=["we"])
async def weight(ctx, arg):

    uuid = get_uuid(arg)
    (profile, cute_name) = get_current(uuid)

    if profile is None:
        await ctx.send(f"{arg} doesn't have a skyblock profile")

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)
    
    embed = weight_embed(arg, weight, skills, dungeons, slayers, cute_name)
    await ctx.send(embed=embed)

client.run(TOKEN)   