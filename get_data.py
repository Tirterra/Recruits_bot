import requests
import json
import os

def get_data(uuid, profile, **kwargs):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\credentials.json", "r+") as file : API_KEY = json.load(file)["API_KEY"]
    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
    res = requests.get(url).json()["profile"]
    res2 = res['community_upgrades']['upgrade_states']

    minions = []
    for member in res["members"]:
        for minion in res["members"][member]["crafted_generators"]:
            minions.append(minion)

    res = res["members"][uuid]
    data = {}
    data.update({"upgrades" : res2})
    data.update({"minions" : minions})

    for arg in kwargs:
        data.update({arg : res[kwargs[arg]]})

    return data

