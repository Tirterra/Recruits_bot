import discord
import json
import os

# Returns an embed with the xp you need to go from a start cata level to another level.
def calccata(arg):

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/calccata", "")
    with open(DIR_PATH+r"/ressources/constants.json", "r") as file :   # I get a dictionary with the exp per level. 
        levels = json.load(file)["cata_levels_to_xp"]

    args = arg.split(" ")
    start = str(args[0])
    end = str(args[1])
    xp = '{:,}'.format(levels[end] - levels[start])   # I get the total xp from the dict.

    embed = discord.Embed(title="**Catacombs Calculation**", description=f"You need **{xp}** to go from level **{start}** to **{end}**!")
    return embed