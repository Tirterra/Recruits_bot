try:
    from math import ceil
    from get_lvl import get_skill_lvl, get_slayer_lvl, get_dungeon_lvl
except:
    pass

def get_skills_weight(data, current):

    total_skill_weight = 0
    total_skill_weight_overflow = 0

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
            cap = data["profiles"][current]["data"]["levels"][skill]["levelCap"]
        except KeyError:
            cap = caps[skill]

        xp = data["profiles"][current]["data"]["levels"][skill]["xp"]
        lvl = get_skill_lvl(xp, cap)
        skill_lvl.update({skill : lvl})

    skill_weight = {
        "mining" : {
            "normal" : (skill_lvl["mining"]["level"]*10)**(0.5+1.18207448+skill_lvl["mining"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["mining"]["overflow"]/259634)**0.968,
            },
        "foraging" : {
            "normal" : (skill_lvl["foraging"]["level"]*10)**(0.5+1.232826+skill_lvl["foraging"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["foraging"]["overflow"]/259634)**0.968,
            },
        "enchanting" : {
            "normal" : (skill_lvl["enchanting"]["level"]*10)**(0.5+0.96976583+skill_lvl["enchanting"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["enchanting"]["overflow"]/882758)**0.968,
            },
        "farming" : {
            "normal" : (skill_lvl["farming"]["level"]*10)**(0.5+1.217848139+skill_lvl["farming"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["farming"]["overflow"]/220689)**0.968,
            },
        "combat" : {
            "normal" : (skill_lvl["combat"]["level"]*10)**(0.5+1.15797687265+skill_lvl["combat"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["combat"]["overflow"]/275862)**0.968,
            },
        "fishing" : {
            "normal" : (skill_lvl["fishing"]["level"]*10)**(0.5+1.406418+skill_lvl["fishing"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["fishing"]["overflow"]/88274)**0.968,
            },
        "alchemy" : {
            "normal" : (skill_lvl["alchemy"]["level"]*10)**(0.5+1.0+skill_lvl["alchemy"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["alchemy"]["overflow"]/1103448)**0.968,
            },
        "taming" : {
            "normal" : (skill_lvl["taming"]["level"]*10)**(0.5+1.14744+skill_lvl["taming"]["level"]/100) / 1250,
            "overflow" : (skill_lvl["taming"]["overflow"]/441379)**0.968,
            },
    }

    for skill in skill_weight:
        skill_weight[skill]["normal"] = ceil(skill_weight[skill]["normal"])
        skill_weight[skill]["overflow"] = ceil(skill_weight[skill]["overflow"])
        total_skill_weight += skill_weight[skill]["normal"]
        total_skill_weight_overflow += skill_weight[skill]["overflow"]

    skill_weight.update({
        "total" : {
            "normal" : ceil(total_skill_weight),
            "overflow" : ceil(total_skill_weight_overflow),
        },
    })
    return skill_weight


def get_slayers_weight(data, current):

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


    try:
        rev_xp = data['profiles'][current]["data"]["slayers"]["zombie"]["xp"]
    except KeyError:
        rev_xp = 0  
    try:
        tara_xp = data['profiles'][current]["data"]["slayers"]["spider"]["xp"]
    except KeyError:
        tara_xp = 0
    try:
        sven_xp = data['profiles'][current]["data"]["slayers"]["wolf"]["xp"]
    except KeyError:
        sven_xp = 0
    try:
        enderman_xp = data['profiles'][current]["data"]["slayers"]["enderman"]["xp"]
    except KeyError:
        enderman_xp = 0

    total_slayer_weight = 0
    total_overflow_slayer_weight = 0


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


def get_dungeon_weight(data, current):

    dungeons_weight = {
        "catacomb" : None,
        "healer" : None,
        "mage" : None,
        "berserk" : None,
        "archer" : None,
        "tank" : None
    }

    total = 0
    total_overflow = 0

    try:
        cata_exp = data["profiles"][current]["data"]["dungeons"]["catacombs"]["level"]["xp"]
    except:
        cata_exp = 0

    cata_lvl = get_dungeon_lvl(cata_exp)
    
    catacomb_weight = cata_lvl["level"]**4.5 * 0.0002149604615
    overflow_dungeon_weight = (cata_lvl["overflow"]/251288.2695)**0.968
    dungeons_weight.update({"catacomb" : {"normal" : catacomb_weight, "overflow" : overflow_dungeon_weight }}) 

    for class_ in dungeons_weight:

        if class_.startswith("cata") :
            pass
        else:

            try:
                class_xp = data["profiles"][current]["data"]["dungeons"]["classes"][class_]["experience"]["xp"]
            except KeyError:
                class_xp = 0

            class_lvl = get_dungeon_lvl(class_xp)

            class_weight = class_lvl["level"]**4.5 * 0.0000045254834
            overflow_class_weight = (class_lvl["overflow"]/11936192.8)**0.968

            dungeons_weight.update({class_ : {"normal" : class_weight, "overflow" : overflow_class_weight}})

    for i in dungeons_weight:
        total += dungeons_weight[i]["normal"]
        total_overflow += dungeons_weight[i]["overflow"]

    dungeons_weight.update({
        "total" : {
            "normal" : ceil(total),
            "overflow" : ceil(total_overflow)
        },
    })

    return dungeons_weight