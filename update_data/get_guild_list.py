import requests
import json
import os

# Returns the guild list.
def get_guild_list(GUILD_ID):
    
    DIR_PATH = os.path.dirname(__file__).replace(r"\update_data", "")
    with open(DIR_PATH+r"\ressources\credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]
        
    url = f"https://api.hypixel.net/guild?key={API_KEY}&id={GUILD_ID}"
    res = requests.get(url).json()
    guild_list = res["guild"]["members"]
    return guild_list