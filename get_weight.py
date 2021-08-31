from get_lvl import get_dungeons, get_skills, get_slayers
import requests
import json
import os


try:
    from math import ceil, floor
    from get_lvl import get_skill_lvl, get_slayer_lvl, get_dungeon_lvl
except:
    pass

def get_skills_weight(skills):

    total_skill_weight = 0
    total_skill_weight_overflow = 0

    skills_weight = {
        "mining" : {
            "normal" : (skills["mining"]["level"]*10)**(0.5+1.18207448+skills["mining"]["level"]/100) / 1250,
            "overflow" : (skills["mining"]["overflow"]/259634)**0.968,
            },
        "foraging" : {
            "normal" : (skills["foraging"]["level"]*10)**(0.5+1.232826+skills["foraging"]["level"]/100) / 1250,
            "overflow" : (skills["foraging"]["overflow"]/259634)**0.968,
            },
        "enchanting" : {
            "normal" : (skills["enchanting"]["level"]*10)**(0.5+0.96976583+skills["enchanting"]["level"]/100) / 1250,
            "overflow" : (skills["enchanting"]["overflow"]/882758)**0.968,
            },
        "farming" : {
            "normal" : (skills["farming"]["level"]*10)**(0.5+1.217848139+skills["farming"]["level"]/100) / 1250,
            "overflow" : (skills["farming"]["overflow"]/220689)**0.968,
            },
        "combat" : {
            "normal" : (skills["combat"]["level"]*10)**(0.5+1.15797687265+skills["combat"]["level"]/100) / 1250,
            "overflow" : (skills["combat"]["overflow"]/275862)**0.968,
            },
        "fishing" : {
            "normal" : (skills["fishing"]["level"]*10)**(0.5+1.406418+skills["fishing"]["level"]/100) / 1250,
            "overflow" : (skills["fishing"]["overflow"]/88274)**0.968,
            },
        "alchemy" : {
            "normal" : (skills["alchemy"]["level"]*10)**(0.5+1.0+skills["alchemy"]["level"]/100) / 1250,
            "overflow" : (skills["alchemy"]["overflow"]/1103448)**0.968,
            },
        "taming" : {
            "normal" : (skills["taming"]["level"]*10)**(0.5+1.14744+skills["taming"]["level"]/100) / 1250,
            "overflow" : (skills["taming"]["overflow"]/441379)**0.968,
            },
    }

    for skill in skills_weight:
        skills_weight[skill]["normal"] = ceil(skills_weight[skill]["normal"])
        skills_weight[skill]["overflow"] = ceil(skills_weight[skill]["overflow"])
        total_skill_weight += skills_weight[skill]["normal"]
        total_skill_weight_overflow += skills_weight[skill]["overflow"]

    skills_weight.update({
        "total" : {
            "normal" : ceil(total_skill_weight),
            "overflow" : ceil(total_skill_weight_overflow),
        },
    })
    return skills_weight


def get_slayers_weight(slayers):

    def slayer_function(exp, divider, modifier):

        if exp == 0:
            return {"normal" : 0, "overflow" : 0}
        elif exp <= 1000000:
            return {"normal" : exp / divider, "overflow" : 0}
        else:
            normal_weight = 1000000 / divider
            remaining = exp - 1000000
            modifier_ = modifier
            overflow = 0

            while remaining > 0:
                left = min(remaining, 1000000)

                overflow += pow(left / (divider * (1.5 + modifier_)), 0.942)
                remaining -= left
                modifier_ += modifier
            
            return {"normal" : normal_weight, "overflow" : overflow}

    total_slayer_weight = 0
    total_overflow_slayer_weight = 0

    rev_xp = slayers["zombie"]["exp"]
    tara_xp = slayers["spider"]["exp"]
    sven_xp = slayers["wolf"]["exp"]
    enderman_xp = slayers["enderman"]["exp"]


    slayers_weight = {
        "zombie" : slayer_function(rev_xp, divider=2208, modifier=0.15),
        "spider" : slayer_function(tara_xp, divider=2118, modifier=0.08),
        "wolf" : slayer_function(sven_xp, divider=1962, modifier=0.015),
        "enderman" : slayer_function(enderman_xp, divider=1430, modifier=0.017),
    }

    for slayer in slayers_weight:
        slayers_weight[slayer]["normal"] = ceil(slayers_weight[slayer]["normal"])
        slayers_weight[slayer]["overflow"] = ceil(slayers_weight[slayer]["overflow"])
        total_slayer_weight += slayers_weight[slayer]["normal"]
        total_overflow_slayer_weight += slayers_weight[slayer]["overflow"]

    slayers_weight.update({
        "total" : {
            "normal" : ceil(total_slayer_weight),
            "overflow" : ceil(total_overflow_slayer_weight),
        },
    })

    return slayers_weight


def get_dungeons_weight(dungeons):

    dungeons_weight = {
        "catacombs" : None,
        "healer" : None,
        "mage" : None,
        "berserk" : None,
        "archer" : None,
        "tank" : None
    }

    total = 0
    total_overflow = 0
    cata_lvl = dungeons["catacombs"]["level"]
    catacombs_weight = cata_lvl**4.5 * 0.0002149604615
    overflow_dungeons_weight = (dungeons["catacombs"]["overflow"] / 251288.2695)**0.968
    dungeons_weight.update({"catacombs" : {"normal" : catacombs_weight, "overflow" : overflow_dungeons_weight }}) 

    for class_ in dungeons_weight:

        if class_.startswith("cata") :
            pass
        else:

            class_lvl = dungeons[class_]["level"]
            class_weight = class_lvl**4.5 * 0.0000045254834
            overflow_class_weight = (dungeons[class_]["overflow"] / 11936192.8)**0.968
            dungeons_weight.update({class_ : {"normal" : class_weight, "overflow" : overflow_class_weight}})

    for i in dungeons_weight:
        dungeons_weight[i]["normal"] = ceil(dungeons_weight[i]["normal"])
        dungeons_weight[i]["overflow"] = ceil(dungeons_weight[i]["overflow"])
        total += dungeons_weight[i]["normal"]
        total_overflow += dungeons_weight[i]["overflow"]

    dungeons_weight.update({
        "total" : {
            "normal" : ceil(total),
            "overflow" : ceil(total_overflow)
        },
    })

    return dungeons_weight

def get_weight(profile, uuid):

    DIR_PATH = os.path.dirname(__file__)
    with open(DIR_PATH+r"\credentials.json", "r+") as file : API_KEY = json.load(file)["API_KEY"]
    url = f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={profile}"
    res = requests.get(url).json()["profile"]["members"][uuid]

    dungeons = get_dungeons(res)
    slayers = get_slayers(res)
    skills = get_skills(res)

    dungeons_weight = get_dungeons_weight(dungeons)
    slayers_weight = get_slayers_weight(slayers)
    skills_weight = get_skills_weight(skills)
    
    weight = {
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