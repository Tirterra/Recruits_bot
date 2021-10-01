from math import ceil

# Returns a dict with the skills weights.
def get_skills_weight(skills):

    total_skill_weight = 0
    total_skill_weight_overflow = 0

    skills_weight = {   # I transform the xp into weight directly in the dict because the formula is simple.
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

    for skill in skills_weight:   # Calculates the total skill weight and overflow weight.
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