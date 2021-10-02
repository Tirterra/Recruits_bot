import discord
import json
import os

from commands.leaderboard.get_leaderboard import get_leaderboard, get_booked_leaderboard
from embeds.leaderboard_embed import leaderboard_embed

# Returns the guild average for a given type of leaderboard.
def get_guild_average(leaderboard):

    total = 0   # This is a simple average algorithm, I bet you can figure it out.

    for player in leaderboard:
        total += leaderboard[player]

    average = total / (len(leaderboard) + 1)
    return average

# Returns the rank of a player in a given type of leaderboard.
def get_rank(leaderboard, target):

    for rank, player in enumerate(leaderboard):
        if player.lower() == target.lower():
            return rank

# Returns an embed with the guild leaderboard.
def leaderboard(ctx, arg):    

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/leaderboard", "")
    with open(DIR_PATH+r"/ressources/linked.json", "r") as file:
        linked = json.load(file)

    page = arg[-2:].replace(" ", "")   # Gets the page that the user asked for, if he didn't, sets it to 1.
    
    try: 
        page = int(page)
        arg = arg.replace(f" {page}", "")
    except ValueError:
        page = 1

    leaderboard, arg = get_leaderboard(arg)

    if isinstance(leaderboard, discord.embeds.Embed):   # If get_leaderboard returned an error embed, return it.
        return leaderboard

    try:   # Check if the user is linked, he has to be linked because it's a guild command.
        target = linked[str(ctx.message.author)]
    except KeyError:
        embed = discord.Embed(title="Error", description="Link yourself first !")
        return embed

    book = get_booked_leaderboard(leaderboard)   # Do the magic and create the embed.
    average = get_guild_average(leaderboard)
    rank = get_rank(leaderboard, target)
    embed = leaderboard_embed(book, page, arg, average, rank, target)

    return embed