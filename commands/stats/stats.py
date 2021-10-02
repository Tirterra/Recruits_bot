import os
import discord
import json

from player_info.get__uuid import get_uuid
from player_info.get_played_profile import get_current
from player_info.get_skin import get_avatar
from commands.stats.get_data import get_data
from commands.weight.get_weight import get_weight
from embeds.stats_embed import stats_embed

# Returns an embed with a bunch of stats.
def stats(ctx, arg):

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/stats", "")
    with open(DIR_PATH+r"/ressources/constants.json", "r") as file :   # Access a dict with minions slots and unique minions.
        unique_minions = json.load(file)["minions"]

    if arg is None:   # If the user didn't give an argument, try to see if he's linked.
        with open(DIR_PATH+r"/ressources/linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:
                embed = discord.Embed(title="Error", description="Invalid argument: pls insert a valid username or try linking !")
                return embed

    uuid = get_uuid(arg)   # Get all the data I need to put in the embed.
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
    collections = len(data["collection"])
    previous = 0

    for i in unique_minions:   # Get the minions slots from the community upgrades and unique minions.
        if uniques <= int(i) :
            minions = unique_minions[previous]
        else:
            previous = i

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
    return embed