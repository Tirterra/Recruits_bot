import requests

# Returns the uuid of a player.
def get_uuid(name):

    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    res = requests.get(url).json()
    uuid = res["id"]
    return uuid