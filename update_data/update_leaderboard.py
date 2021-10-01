from discord import player
from requests.exceptions import HTTPError, ConnectionError
import requests
import time
import json
import os

from commands.weight.get_weight import get_weight
from commands.weight.skills_weight import get_skills_weight
from commands.weight.slayers_weight import get_slayers_weight
from commands.weight.dungeons_weight import get_dungeons_weight
from commands.weight.get_lvl import get_dungeons, get_skills, get_slayers

from player_info.get_played_profile import get_current
from update_data.get_guild_list import get_guild_list
from update_data.secrets import get_secrets


def update_player(member):

    DIR_PATH = os.path.dirname(__file__).replace(r"\update_data", "")
    with open(DIR_PATH+r"\ressources\credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]
        
    uuid = member["uuid"]   # Gets the username from the uuid.
    try:
        name = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
    except ConnectionError:
        return

    name = name[len(name)-1]["name"]
    (profile, cute_name) = get_current(uuid)   # Gets the current profile.

    if profile is None:
        return

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)   # Gets all the main stats of a player.

    total_weight = weight["total"]["normal"] + weight["total"]["overflow"]
    total_slayer_xp = slayers["total"]
    catacombs = dungeons["catacombs"]["level"]
    secrets = get_secrets(url=f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}", player=name)
    revenants = slayers["zombie"]["exp"]
    svens = slayers["wolf"]["exp"]
    tarantula = slayers["spider"]["exp"]
    enderman = slayers["enderman"]["exp"]
    skill_average = skills["skill_average"]["normal"]

    player_data = {   # Puts everything in a dict.
        "weight" : total_weight,
        "slayers" : total_slayer_xp,
        "catacombs" : catacombs,
        "secrets" : secrets,
        "revenants" : revenants,
        "svens" : svens,
        "tarantula" : tarantula,
        "enderman" : enderman,
        "skill_average" : skill_average
    }

    return {name : player_data}

# Updates all the data I need to create the leaderboards.
def update_data():

    DIR_PATH = os.path.dirname(__file__).replace(r"\update_data", "")
    with open(DIR_PATH+r"\ressources\credentials.json", "r") as file:
        GUILD_ID = json.load(file)["GUILD_ID"]

    guild_list = get_guild_list(GUILD_ID)
    data = {}

    for count, member in enumerate(guild_list):   # Append all the player data in a dict.

        player_data = update_player(member)

        if player_data is None:
            continue

        data.update(player_data)

    with open(DIR_PATH+r"\ressources\guild_data.json", "w+") as file:
        json.dump(data, file, indent=4)

