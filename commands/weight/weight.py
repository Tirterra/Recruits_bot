import discord
import json
import os

from player_info.get__uuid import get_uuid
from player_info.get_played_profile import get_current
from commands.weight.get_weight import get_weight
from embeds.weight_embed import weight_embed

# Returns an embed with all the weight stats.
def weight(ctx, arg=None):

    DIR_PATH = os.path.dirname(__file__).replace(r"\commands\weight", "")

    if arg is None:   # Check if the user is linked if he didn't specify a username.
        with open(DIR_PATH+r"\ressources\linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:
                embed = discord.Embed(title="Error", description="Invalid argument: pls insert a valid username or try linking !")
                return embed

    uuid = get_uuid(arg)
    (profile, cute_name) = get_current(uuid)

    if profile is None:   # If the player doesn't have a skyblock profile, returns an error embed.
        embed = discord.Embed(title="Error", description=f"{arg} doesn't have a skyblock profile")
        return embed

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)   # Get all the data, do the math and put everything in an embed.
    embed = weight_embed(arg, weight, skills, dungeons, slayers, cute_name)
    return embed