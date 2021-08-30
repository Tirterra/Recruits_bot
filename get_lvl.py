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
    
    required_xp = {
        50 : 1,	
        175	: 2,
        375	: 3,
        675	: 4,
        1175 : 5,	
        1925 : 6,
        2925 : 7,	
        4425 : 8,
        6425 : 9,
        9925 : 10,	
        14925 :	11,
        22425 :	12,
        32425 :	13,
        47425 :	14,
        67425 :	15,
        97425 :	16,
        147425 : 17,	
        222425 : 18,
        322425 : 19,
        522425 : 20,	
        822425 : 21,
        1222425 : 22,	
        1722425 : 23,
        2322425 : 24,	
        3022425	: 25,
        3822425	: 26,
        4722425	: 27,
        5722425	: 28,
        6822425	: 29,
        8022425	: 30,
        9322425	: 31,
        10722425 : 32,	
        12222425 : 33,	
        13822425 : 34,	
        15522425 : 35,	
        17322425 : 36,
        19222425 : 37,	
        21222425 : 38,	
        23322425 : 39,	
        25522425 : 40,	
        27822425 : 41,	
        30222425 : 42,	
        32722425 : 43,	
        35322425 : 44,	
        38072425 : 45,	
        40972425 : 46,	
        44072425 : 47,	
        47472425 : 48,	
        51172425 : 49,	
        55172425 : 50,	
        59472425 : 51,	
        64072425 : 52,	
        68972425 : 53,	
        74172425 : 54,	
        79672425 : 55,	
        85472425 : 56,	
        91572425 : 57,	
        97972425 : 58,	
        104672425 : 59,	
        111672425 :	60,
    }

    previous = 0

    for xp in required_xp.keys():

        level = required_xp[xp]

        if player_xp >= xp : 
            if level == cap:
                return {"level": level, "overflow" : player_xp - xp}
            else:
                previous = xp
        else:
            level = level - 1 + (player_xp-previous) / (xp-previous)
            return {"level": round(level, 2), "overflow" : 0}


def get_slayer_lvl(player_xp):

    required_xp = {
        5 : 1,	
        15 : 2,
        200 : 3,	
        1000 : 4,	
        5000 : 5,	
        20000 : 6,	
        100000 : 7,	
        400000 : 8,	
        1000000 : 9,
    }

    previous = 0

    for xp in required_xp.keys():
        level = required_xp[xp]
        if player_xp >= xp : 
            if player_xp >= 1000000:
                return {"level" : 9, "overflow" : player_xp - 1000000, "exp" : player_xp}
            else:
                previous = xp
        else:
            level = level - 1 + (player_xp-previous) / (xp-previous)
            return {"level" : round(level, 2), "overflow" : 0, "exp" : player_xp} 


def get_dungeon_lvl(player_xp):

    required_xp = {
        50 : 1,	
        125	: 2,
        235	: 3,
        395	: 4,
        625	: 5,
        955	: 6,
        1425 : 7,	
        2095 : 8,
        3045 : 9,	
        4385 : 10,	
        6275 : 11,	
        8940 : 12,	
        12700 : 13,	
        17960 : 14,	
        25340 : 15,	
        35640 :	16,
        50040 :	17,
        70040 :	18,
        97640 :	19,
        135640 : 20,	
        188140 : 21,
        259640 : 22,
        356640 : 23,
        488640 : 24,	
        668640 : 25,	
        911640 : 26,	
        1239640 : 27,	
        1684640	: 28,
        2284640	: 29,
        3084640	: 30,
        4149640	: 31,
        5559640	: 32,
        7459640	: 33,
        9959640	: 34,
        13259640 : 35,	
        17559640 : 36,	
        23159640 : 37,	
        30359640 : 38,	
        39559640 : 39,	
        51559640 : 40,
        66559640 : 41,	
        85559640 : 42,	
        109559640 :	43,
        139559640 :	44,
        177559640 : 45,
        225559640 :	46,
        285559640 :	47,
        360559640 :	48,
        453559640 :	49,
        569809640 :	50,
    }

    previous = 0

    for xp in required_xp.keys():

        level = required_xp[xp]

        if player_xp >= xp : 

            if player_xp >= 569809640:
                return {"level" : 50, "overflow" : player_xp - 569809640}
            else:
                previous = xp

        else:
            level = level - 1 + (player_xp-previous) / (xp-previous)
            return {"level" : round(level, 2), "overflow" : 0}


def get_skills(res):

    caps = {
        "farming" : 60,
        "combat" : 60,
        "foraging" : 50,
        "enchanting" : 60,
        "alchemy" : 50,
        "taming" : 50,
        "fishing" : 50,
        "mining" : 60,
        }

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