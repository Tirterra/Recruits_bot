from requests.models import HTTPError
import requests
import json
import os

# Returns the ID of a player's played profile.
def get_current(uuid):

    DIR_PATH = os.path.dirname(__file__).replace(r"\player_info", "")
    with open(DIR_PATH+r"\ressources\credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]


    try:   # I try to get all the profiles of a player.
        url = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
        res = requests.get(url)
        res.raise_for_status()   # If there is a connection error, raise an HTTPError.
        res = res.json()
        profiles = res["player"]["stats"]["SkyBlock"]["profiles"].keys()
        last_save = 0
    except HTTPError:   # If there was an error, set the profiles to None.
        profiles = None

    if profiles is None:
        return (None, None)

    for profile in profiles:   # I set the current profile to the most recently saved profile.
        
        cute_name = res["player"]["stats"]["SkyBlock"]["profiles"][profile]["cute_name"]
        url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
        res2 = requests.get(url).json()

        if res2["profile"] is None:
            continue

        try:
            if res2["profile"]["members"][uuid]["last_save"] > last_save:
                last_save = res2["profile"]["members"][uuid]["last_save"]
                current = profile
        except KeyError:
            continue

    if "current" not in locals():   # If there was an error, set the values to None.
        current = None
        cute_name = None
    
    return (current, cute_name)