from discord import embeds
from requests.exceptions import HTTPError
import requests
import discord
import json
import os

from embeds.link_embed import link_embed

# Links a discord name to a minecraft name.
def link(ctx, arg):

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/link", "")
    try:
        url = f"http://api.mojang.com/users/profiles/minecraft/{arg}"   # Checks if the player exists.
        res = requests.get(url)

        if res.status_code != 200:
            raise HTTPError

        embed = link_embed(ctx.message.author, arg)

    except HTTPError:   # The given username isn't valid.
        embed = discord.Embed(title="Error", description="Invalid username !")
        return embed

    with open(DIR_PATH+r"/ressources/linked.json", "r") as file:
        linked = json.load(file)

    linked.update({str(ctx.message.author) : arg})

    with open(DIR_PATH+r"/ressources/linked.json", "w+") as file:
        json.dump(linked, file, indent=4)

    return embed