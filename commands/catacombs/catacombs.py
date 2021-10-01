import requests
import discord
import json
import os

from player_info.get__uuid import get_uuid
from player_info.get_played_profile import get_current
from player_info.get_skin import get_avatar
from commands.weight.get_lvl import get_dungeons
from embeds.dungeons_embed import dungeons_embed

# Returns an embed with a bunch of dungeons stats.
def catacombs(ctx, arg=None):

    DIR_PATH = os.path.dirname(__file__).replace(r"\commands\catacombs", "")

    if arg is None:   # If the user gives no argument, I try to see if he's linked.
        with open(DIR_PATH+r"\ressources\linked.json", "r") as file:
            linked = json.load(file)
            if str(ctx.message.author) in linked.keys():
                arg = linked[str(ctx.message.author)]
            else:   # Returns an erro if not linked and no argument was given.
                embed = discord.Embed(titel="Error", description="Invalid argument: pls insert a valid username or try linking !")
                return embed

    with open(DIR_PATH+r"\ressources\credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]

    uuid = get_uuid(arg)
    (profile, cute_name) = get_current(uuid)

    if profile is None:   # If the player has no profile but has an hypixel account, returns an error.
        embed = discord.Embed(title="Error", description=f"{arg} doesn't have a skyblock profile")
        return embed

    with open(DIR_PATH+r"\ressources\guild_data.json", "r") as file:
        secrets = json.load(file)[arg]["secrets"]  

    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
    res = requests.get(url).json()["profile"]["members"][uuid]

    clears = {}   # I create a dictionary with all the floor completions.

    try:   # This try and except is here because if someone hasn't completed a floor yet it would break.
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

    fastest_times = {}   # I create a dictionary with all the fastest times.

    try:   # Same reason here.
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
    return embed