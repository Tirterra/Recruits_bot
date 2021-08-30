import requests
from requests.models import HTTPError

def get_current(uuid):

    API_KEY = "YOUR API KEY"

    for _ in range(0, 2):

        try:
            url = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
            res = requests.get(url)
            res.raise_for_status()
            res = res.json()
            profiles = res["player"]["stats"]["SkyBlock"]["profiles"].keys()
            last_save = 0
            break
        except HTTPError:
            profiles = None

    if profiles is None:
        return (None, None)

    for profile in profiles:
        
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

    if "current" not in locals():
        current = None
        cute_name = None
    
    return (current, cute_name)