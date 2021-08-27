import discord
from discord.ext import commands
import requests
from math import ceil
import os

TOKEN = "ODgwNTcxNjkzOTg1MzIwOTkw.YSgOTA.JJBa0YzLSFex_CK0vsqnNBUk5jg"
DIR_PATH = os.path.dirname(__file__)

client = commands.Bot(command_prefix="d.")


def get_current(arg):

    url = f"https://sky.shiiyu.moe/api/v2/profile/{arg}"
    res = requests.get(url).json()
    profiles = res["profiles"]

    for profile in profiles:
        current = profiles[profile]["current"]
        if current is True:
            return profile

@client.event
async def on_ready():
    print("I am ready")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong\n {round(client.latency*1000)} ms.")


@client.command()
async def weight(ctx, arg):

    print(ctx.message.author.id)

    url = f"https://sky.shiiyu.moe/api/v2/profile/{arg}"
    res = requests.get(url).json()

    if "error" in res.keys():
        await ctx.send(f"Couldn't find {arg}")
        return
    else:
        current = get_current(arg)
        weight = ceil(res["profiles"][current]["data"]["weight"])
        await ctx.send(f"{arg}'s weight on {res['profiles'][current]['cute_name']} is {weight} weight.")


client.run(TOKEN)