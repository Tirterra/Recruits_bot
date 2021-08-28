try:
    import requests
    import json
except:
    pass

def get_avatar(arg):

    url = f"https://api.mojang.com/users/profiles/minecraft/{arg}"
    res = requests.get(url).json()
    uuid = res["id"]

    avatar_url = f"https://crafatar.com/avatars/{uuid}"
    return avatar_url
