from discord import embeds
from get_lvl import get_skill_lvl, get_slayer_lvl, get_dungeon_lvl, get_skills, get_slayers, get_dungeons
from get_weight import get_dungeon_weight, get_skills_weight, get_slayers_weight
from get_played_profile import get_current
from discord.ext import commands
from weight_embed import create_weight_embed
from math import ceil, floor
import requests
import discord
import math
import json
from get_skin import get_avatar
import os

TOKEN = "ODgwNTcxNjkzOTg1MzIwOTkw.YSgOTA.zpGPIr-HF-ZTZesC8rvh0XzVELo"
DIR_PATH = os.path.dirname(__file__)

client = commands.Bot(command_prefix="d.")

@client.event
async def on_ready():
    print("I am ready")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong\n {round(client.latency*1000)} ms.")


@client.command()
async def weight(ctx, arg):

    url = f"https://sky.shiiyu.moe/api/v2/profile/{arg}"
    res = requests.get(url).json()

    with open(DIR_PATH+r"\data.json", "w+") as file:
        json.dump(res, file, indent=4)

    if "error" in res.keys():
        await ctx.send(f"Couldn't find {arg}")
        return
    else:
        current = get_current(res)
    
    embed = create_weight_embed(arg, res, current)

    await ctx.send(embed=embed)

client.run(TOKEN)