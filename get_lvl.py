try:
    from math import round
except:
    pass

def get_skill_lvl(exp, cap=60):
    
    skills = {
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

    for i in skills.keys():
        level = skills[i]
        if exp >= i : 
            if level == cap:
                return {"level": level, "overflow" : exp - i}
            else:
                previous = i
        else:
            level = round(level - 1 + (exp-previous) / (i-previous), 2)
            return {"level": level, "overflow" : 0}


def get_slayer_lvl(exp):

    slayers = {
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

    for i in slayers.keys():
        if exp >= i : 
            if exp >= 1000000:
                return 9
            else:
                pass
        else:
            return slayers[i]-1 


def get_dungeon_lvl(exp):

    dungeons = {
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

    for i in dungeons.keys():
        level = dungeons[i]
        if exp >= i : 
            if exp >= 569809640:
                return {"level" : 50, "overflow" : exp - 569809640}
            else:
                previous = i
        else:
            level = level - 1 + (exp-previous) / (i-previous)
            return {"level" : level, "overflow" : 0}


def get_skills(res, current):

    caps = {"farming" : 60, "combat" : 60, "foraging" : 50, "enchanting" : 60, "alchemy" : 50, "taming" : 50, "fishing" : 50, "mining" : 60}

    skill_lvl = {
        "mining" : None,
        "foraging" : None,
        "enchanting" : None,
        "farming" : None,
        "combat" : None,
        "fishing" : None,
        "alchemy" : None,
        "taming" : None,
    }

    for skill in skill_lvl:

        try:
            cap = res["profiles"][current]["data"]["levels"][skill]["levelCap"]
        except KeyError:
            cap = caps[skill]
        
        xp = res["profiles"][current]["data"]["levels"][skill]["xp"]
        lvl = get_skill_lvl(xp, cap)
        skill_lvl.update({skill : lvl})

    return skill_lvl


def get_slayers(res, current):

    slayer_lvl = {
        "zombie" : None,
        "spider" : None,
        "wolf" : None,
        "enderman" : None
    }

    for slayer in slayer_lvl:
        
        try:
            exp = res['profiles'][current]["data"]["slayers"][slayer]["xp"]
        except KeyError:
            exp = 0

        lvl = get_slayer_lvl(exp)
        slayer_lvl.update({slayer : lvl})
    
    return slayer_lvl


def get_dungeons(res, current):

    dungeon_lvl = {
        "healer" : None,
        "mage" : None,
        "berserk" : None,
        "archer" : None,
        "tank" : None
    }

    for class_ in dungeon_lvl:
        try:
            class_xp = res["profiles"][current]["data"]["dungeons"]["classes"][class_]["experience"]["xp"]
        except KeyError:
            class_xp = 0
        
        class_lvl = get_dungeon_lvl(class_xp)
        dungeon_lvl.update({class_ : class_lvl})

    try:
        cata_exp = res["profiles"][current]["data"]["dungeons"]["catacombs"]["level"]["xp"]
    except KeyError:
        cata_exp = 0

    dungeon_lvl.update({"catacomb" : get_dungeon_lvl(cata_exp)})
    return dungeon_lvl
