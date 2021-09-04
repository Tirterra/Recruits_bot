import requests
from math import floor
import os
import json
from requests.models import HTTPError

try:
    from math import round
except:
    pass

def get_skill_lvl(player_xp, cap):
    
    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : required_xp = json.load(file)["skill_xp_to_level"]
    previous = 0

    for xp in required_xp.keys():

        level = required_xp[xp]

        if player_xp >= int(xp) : 
            if level == cap:
                return {"level": level, "overflow" : player_xp - int(xp)}
            else:
                previous = int(xp)
        else:
            level = level - 1 + (player_xp-previous) / (int(xp)-previous)
            return {"level": round(level, 2), "overflow" : 0}


def get_slayer_lvl(player_xp):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : required_xp = json.load(file)["slayer_xp_to_level"]

    previous = 0

    for xp in required_xp.keys():
        level = required_xp[xp]
        if player_xp >= int(xp) : 
            if player_xp >= 1000000:
                return {"level" : 9, "overflow" : player_xp - 1000000, "exp" : player_xp}
            else:
                previous = int(xp)
        else:
            level = level - 1 + (player_xp-previous) / (int(xp)-previous)
            return {"level" : round(level, 2), "overflow" : 0, "exp" : player_xp} 


def get_dungeon_lvl(player_xp):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : required_xp = json.load(file)["catacombs_xp_to_level"]
    previous = 0

    for xp in required_xp.keys():

        level = required_xp[xp]

        if player_xp >= int(xp) : 

            if player_xp >= 569809640:
                return {"level" : 50, "overflow" : player_xp - 569809640}
            else:
                previous = int(xp)

        else:
            level = level - 1 + (player_xp-previous) / (int(xp)-previous)
            return {"level" : round(level, 2), "overflow" : 0}


def get_skills(res):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\constants.json", "r") as file : caps = json.load(file)["caps"]

    skills = {
        "mining" : None,
        "foraging" : None,
        "enchanting" : None,
        "farming" : None,
        "combat" : None,
        "fishing" : None,
        "alchemy" : None,
        "taming" : None,
    }

    sa = 0
    true_sa = 0

    for skill in skills:

        try:
            xp = eval(f"res['experience_skill_{skill}']")
        except KeyError:
            xp = 0

        cap = caps[skill]
        lvl = get_skill_lvl(xp, cap)
        skills.update({skill : lvl})
        true_sa += floor(lvl["level"])
        sa += lvl["level"]
        
    sa = round(sa / 8, 2)
    true_sa = true_sa / 8
    skills.update({"skill_average" : {"normal" : true_sa, "overflow" : sa}})

    return skills


def get_slayers(res):

    slayers = {
        "zombie" : None,
        "spider" : None,
        "wolf" : None,
        "enderman" : None
    }

    total_xp = 0

    for slayer in slayers:
        
        try:
            exp = res["slayer_bosses"][slayer]["xp"]
        except KeyError:
            exp = 0

        total_xp += exp
        lvl = get_slayer_lvl(exp)
        slayers.update({slayer : lvl})

    slayers.update({"total" : total_xp})
    return slayers


def get_dungeons(res):

    dungeons = {
        "healer" : None,
        "mage" : None,
        "berserk" : None,
        "archer" : None,
        "tank" : None
    }

    for class_ in dungeons:
        try:
            class_xp = res["dungeons"]["player_classes"][class_]["experience"]
        except KeyError:
            class_xp = 0
        
        class_lvl = get_dungeon_lvl(class_xp)
        dungeons.update({class_ : class_lvl})

        try:
            cata_exp = res["dungeons"]["dungeon_types"]["catacombs"]["experience"]
        except KeyError:
            cata_exp = 0

    dungeons.update({"catacombs" : get_dungeon_lvl(cata_exp)})

    return dungeons

def get_secrets(url, player):

    DIR_PATH = os.path.dirname(__file__)

    for i in range(0, 2):

        try:
            res = requests.get(url)
            res.raise_for_status() 
            res = res.json()
            secrets = res["player"]["achievements"]["skyblock_treasure_hunter"]
            break
        except HTTPError:
            with open(DIR_PATH+r"\guild_data.json", "r") as file:
                secrets = json.load(file)
                try:
                    secrets = secrets[player]["secrets"]
                except KeyError:
                    secrets = 0
        except KeyError:
            secrets = 0
            break
        else:
            secrets = 0

        
    return secrets