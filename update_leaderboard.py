from requests.models import HTTPError
from get_weight import get_dungeons_weight, get_skills_weight, get_slayers_weight, get_weight
from get_lvl import get_dungeons, get_secrets, get_skills, get_slayers
import time
from get_played_profile import get_current
import requests
import time
import asyncio
import os
import json

async def get_guild_list(GUILD_ID):
    
    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\credentials.json", "r+") as file : API_KEY = json.load(file)["API_KEY"]
    url = f"https://api.hypixel.net/guild?key={API_KEY}&id={GUILD_ID}"
    res = requests.get(url).json()
    guild_list = res["guild"]["members"]
    return guild_list


def get_uuid(name):

    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    res = requests.get(url).json()
    uuid = res["id"]
    return uuid

async def update_player(member):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\credentials.json", "r+") as file : API_KEY = json.load(file)["API_KEY"]
    uuid = member["uuid"]
    name = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
    name = name[len(name)-1]["name"]
    (profile, cute_name) = get_current(uuid)

    if profile is None:
        return

    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        res = res.json()
        res = res['profile']['members'][uuid]
    except HTTPError:
        return

    (weight, dungeons, slayers, skills) = get_weight(profile, uuid)

    total_weight = weight["total"]["normal"] + weight["total"]["overflow"]
    total_slayer_xp = slayers["total"]
    catacombs = dungeons["catacombs"]["level"]
    secrets = get_secrets(url=f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}", player=name)
    revenants = slayers["zombie"]["exp"]
    svens = slayers["wolf"]["exp"]
    tarantula = slayers["spider"]["exp"]
    enderman = slayers["enderman"]["exp"]
    skill_average = skills["skill_average"]["normal"]

    player_data = {
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


async def update_data():

    print("Started update")

    DIR_PATH = os.path.dirname(__file__)
    task = asyncio.create_task(get_guild_list(GUILD_ID="5ec14e148ea8c93479da0f4b"))
    guild_list = await task
    start = time.time()
    data = {}

    for count, member in enumerate(guild_list):

        task = asyncio.create_task(update_player(member))
        player_data = await task

        if player_data is None:
            continue

        data.update(player_data)

    with open(DIR_PATH+r"\guild_data.json", "w+") as file:
        json.dump(data, file, indent=4)

