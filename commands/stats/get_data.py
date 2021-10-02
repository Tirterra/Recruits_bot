import requests
import json
import os

# Returns a bunch of data for the stats command.
def get_data(uuid, profile, **kwargs):

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/stats", "")
    with open(DIR_PATH+r"/ressources/credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]

    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"   # I get the data from hypixel's API.
    res = requests.get(url).json()["profile"]
    res2 = res['community_upgrades']['upgrade_states']   # The crafted minions and community upgrades are profile related, not player.

    minions = []
    for member in res["members"]:   # Get all the crafted minions crafted by every profile member.
        for minion in res["members"][member]["crafted_generators"]:
            minions.append(minion)

    res = res["members"][uuid]
    data = {}
    data.update({"upgrades" : res2})
    data.update({"minions" : minions})

    for arg in kwargs:   # Returns anything as long as the given arg is a valid path to data.
        data.update({arg : res[kwargs[arg]]})

    return data

