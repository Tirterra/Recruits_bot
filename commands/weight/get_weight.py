from commands.weight.get_lvl import get_dungeons, get_skills, get_slayers
import requests
import json
import os

from commands.weight.skills_weight import get_skills_weight
from commands.weight.slayers_weight import get_slayers_weight
from commands.weight.dungeons_weight import get_dungeons_weight

# Returns a tuple with four dicts. Total weight, skills, slayers, dungeons weight.
def get_weight(profile, uuid):

    DIR_PATH = os.path.dirname(__file__).replace(r"/commands/weight", "")
    with open(DIR_PATH+r"/ressources/credentials.json", "r+") as file :
        API_KEY = json.load(file)["API_KEY"]
        
    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
    try:
        res = requests.get(url).json()["profile"]["members"][uuid]    # Get all the data from hypixel's API.
    except KeyError:
        return (None, None, None, None)

    dungeons = get_dungeons(res)   # extract and process the data to get the different weights.
    slayers = get_slayers(res)
    skills = get_skills(res)

    dungeons_weight = get_dungeons_weight(dungeons)
    slayers_weight = get_slayers_weight(slayers)
    skills_weight = get_skills_weight(skills)
    
    weight = {   # Jumbles everything into a dict.
        "total" : {
            "normal" : dungeons_weight["total"]["normal"] +\
                       slayers_weight["total"]["normal"] +\
                       skills_weight["total"]["normal"],
            "overflow" : dungeons_weight["total"]["overflow"] +\
                         slayers_weight["total"]["overflow"] +\
                         skills_weight["total"]["overflow"],
        },
        "skills" : skills_weight,
        "slayers" : slayers_weight,
        "catacombs" : dungeons_weight,
    }

    return (weight, dungeons, slayers, skills)