from discord.user import Profile
from requests.models import HTTPError
from get_leaderboard import get_booked_leaderboard, get_leaderboard
from update_leaderboard import get_uuid, update_data
import asyncio
from get_data import get_data
from discord import embeds, player
from get_lvl import get_secrets, get_skill_lvl, get_slayer_lvl, get_dungeon_lvl, get_skills, get_slayers, get_dungeons
from get_weight import get_dungeons_weight, get_skills_weight, get_slayers_weight, get_weight
from get_played_profile import get_current
from discord.ext import commands
from bot_embeds import dungeons_embed, get_guild_average, get_rank, leaderboard_embed, link_embed, stats_embed, weight_embed
from math import ceil, floor    
import requests
import discord
import time
import math
import json
from get_skin import get_avatar
import os

DIR_PATH = os.path.dirname(__file__)
with open(DIR_PATH+r"\credentials.json", "r+") as file : TOKEN = json.load(file)["TOKEN"]

client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
    print("I am ready")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong\n {round(client.latency*1000)} ms.")


@client.command()
async def calcskills(ctx, *, arg):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : levels = json.load(file)["skill_levels_to_xp"]

    args = arg.split(" ")
    start = str(args[0])
    end = str(args[1])
    xp = '{:,}'.format(levels[end] - levels[start])
    embed = discord.Embed(title="**Skill Calculation**", description=f"You need **{xp}** to go from level **{start}** to **{end}**!")

    await ctx.send(embed=embed)

@client.command()
async def stats(ctx, arg=None):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : unique_minions = json.load(file)["minions"]

    if arg is None:
        with open(DIR_PATH+r"\linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:
                await ctx.send("Invalid argument: pls insert a valid username or try linking !")
                return

    uuid = get_uuid(arg)
    profile, cute_name = get_current(uuid)

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)
    average_skill = skills["skill_average"]["normal"]
    true_average_skill = skills["skill_average"]["overflow"]
    catacombs_level = dungeons["catacombs"]["level"]
    slayers_xp = slayers["total"]
    normal_weight = weight["total"]["normal"]
    overflow_weight = weight["total"]["overflow"]
    data = get_data(uuid, profile, pets="pets", coins="coin_purse", collection="unlocked_coll_tiers")
    pets = len(data["pets"])
    coins = data["coins"]
    uniques= len(data["minions"])
    previous = 0

    for i in unique_minions:
        if uniques <= i :
            minions = unique_minions[previous]
        else:
            previous = i
    collections = len(data["collection"])

    for value in data["upgrades"]:
        if value["upgrade"] == "minion_slots":
            minions += 1

    stats = {
        "average_skill" : average_skill,
        "true_average_skill" : true_average_skill,
        "catacombs_level" : catacombs_level,
        "slayers_xp" : '{:,}'.format(slayers_xp),
        "normal_weight" : normal_weight,
        "overflow_weight" : overflow_weight,
        "pets" : pets,  
        "coins" : coins,
        "minions" : minions,
        "collections" : collections
        }

    embed = stats_embed(stats, arg)
    await ctx.send(embed=embed)


@client.command(aliases=["calccatacombs"])
async def calccata(ctx, *, arg):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : levels = json.load(file)["cata_levels_to_xp"]

    args = arg.split(" ")
    start = str(args[0])
    end = str(args[1])
    xp = '{:,}'.format(levels[end] - levels[start])
    embed = discord.Embed(title="**Catacombs Calculation**", description=f"You need **{xp}** to go from level **{start}** to **{end}**!")

    await ctx.send(embed=embed)


@client.command(aliases=["cata"])
async def catacombs(ctx, arg=None):

    DIR_PATH = os.path.dirname(__file__)

    if arg is None:
        with open(DIR_PATH+r"\linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:
                await ctx.send("Invalid argument: pls insert a valid username or try linking !")
                return

    with open(DIR_PATH+r"\credentials.json", "r+") as file : API_KEY = json.load(file)["API_KEY"]
    uuid = get_uuid(arg)
    (profile, cute_name) = get_current(uuid)

    secrets = get_secrets(url=f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}", player=arg)    

    if profile is None:
        await ctx.send(f"{arg} doesn't have a skyblock profile")
        return

    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
    res = requests.get(url).json()["profile"]["members"][uuid]

    clears = {}

    try:
        clears.update({"entrance" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["0"])})
        clears.update({"f1" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["1"])})
        clears.update({"f2" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["2"])})
        clears.update({"f3" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["3"])})
        clears.update({"f4" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["4"])})
        clears.update({"f5" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["5"])})
        clears.update({"f6" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["6"])})
        clears.update({"f7" : int(res["dungeons"]["dungeon_types"]["catacombs"]['tier_completions']["7"])})
    except KeyError:
        pass

    fastest = res["dungeons"]["dungeon_types"]["catacombs"]["fastest_time"]

    fastest_times = {}

    try:
        fastest_times.update({
            "entrance" : {
                "minutes" : int((fastest["0"] / 1000 - fastest["0"] / 1000 % 60) / 60),
                "seconds" : round(fastest["0"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f1" : {
                "minutes" : int((fastest["1"] / 1000 - fastest["1"] / 1000 % 60) / 60),
                "seconds" : round(fastest["1"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f2" : {
                "minutes" : int((fastest["2"] / 1000 - fastest["2"] / 1000 % 60) / 60),
                "seconds" : round(fastest["2"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f3" : {
                "minutes" : int((fastest["3"] / 1000 - fastest["3"] / 1000 % 60) / 60),
                "seconds" : round(fastest["3"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f4" : {
                "minutes" : int((fastest["4"] / 1000 - fastest["4"] / 1000 % 60) / 60),
                "seconds" : round(fastest["4"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f5" : {
                "minutes" : int((fastest["5"] / 1000 - fastest["5"] / 1000 % 60) / 60),
                "seconds" : round(fastest["5"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f6" : {
                "minutes" : int((fastest["6"] / 1000 - fastest["6"] / 1000 % 60) / 60),
                "seconds" : round(fastest["6"] / 1000 % 60),
            }
        })
        fastest_times.update({
            "f7" : {
                "minutes" : int((fastest["7"] / 1000 - fastest["7"] / 1000 % 60) / 60),
                "seconds" : round(fastest["7"] / 1000 % 60),
            }
        })
    except:
        pass

    dungeons = get_dungeons(res)
    dungeons.update({"clears": clears})
    dungeons.update({"fastest_times" : fastest_times})

    embed = dungeons_embed(dungeons, secrets, arg)
    await ctx.send(embed=embed)


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


@client.command()
@commands.has_permissions(administrator=True)
async def update(ctx):

    start = time.time()
    await ctx.send("Started update")
    task = update_data()
    await task

    end = time.time()
    await ctx.send(f"data updated in {end - start}")


@client.command(aliases=["lb"])
async def leaderboard(ctx, *, arg="weight"):

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
async def weight(ctx, arg=None):

    DIR_PATH = os.path.dirname(__file__)

    if arg is None:
        with open(DIR_PATH+r"\linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:
                await ctx.send("Invalid argument: pls insert a valid username or try linking !")
                return

    uuid = get_uuid(arg)
    (profile, cute_name) = get_current(uuid)

    if profile is None:
        await ctx.send(f"{arg} doesn't have a skyblock profile")

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)
    
    embed = weight_embed(arg, weight, skills, dungeons, slayers, cute_name)
    await ctx.send(embed=embed)

client.run(TOKEN)   
